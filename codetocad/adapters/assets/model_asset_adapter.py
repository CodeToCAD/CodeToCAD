"""
3D model asset adapter for downloading models from online sources.

This module provides adapters for downloading 3D model assets from various online
sources like Thingiverse, free model repositories, and other 3D model libraries.
"""

import os
import json
import time
import requests
from typing import Optional, Dict, Any, List, Tuple
from pathlib import Path
from urllib.parse import urljoin, urlparse
from dataclasses import dataclass


@dataclass
class ModelAsset:
    """Container for 3D model asset information."""

    id: str
    name: str
    description: str
    category: str
    tags: List[str]
    preview_url: Optional[str] = None
    download_urls: Dict[str, str] = None  # format -> url
    file_formats: List[str] = None  # Available formats (stl, obj, etc.)
    license: str = "Unknown"
    author: str = ""
    dimensions: Optional[Tuple[float, float, float]] = None  # x, y, z in mm
    file_size: Optional[int] = None  # bytes

    def __post_init__(self):
        if self.download_urls is None:
            self.download_urls = {}
        if self.file_formats is None:
            self.file_formats = []


class ModelAssetAdapter:
    """Base class for 3D model asset adapters."""

    def __init__(self, api_key: Optional[str] = None, cache_dir: Optional[str] = None):
        self.api_key = api_key
        self.cache_dir = (
            Path(cache_dir) if cache_dir else Path.home() / ".codetocad" / "model_cache"
        )
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.session = requests.Session()
        self.rate_limit_delay = 1.0  # seconds between requests
        self.last_request_time = 0.0

    def _rate_limit(self):
        """Implement rate limiting."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - time_since_last)
        self.last_request_time = time.time()

    def search(
        self, query: str, category: Optional[str] = None, limit: int = 10
    ) -> List[ModelAsset]:
        """Search for 3D models by keywords."""
        raise NotImplementedError("Subclasses must implement search method")

    def download(
        self, asset: ModelAsset, format: str = "stl", cache_dir: Optional[str] = None
    ) -> Optional[str]:
        """Download 3D model to cache directory."""
        raise NotImplementedError("Subclasses must implement download method")

    def save(self, temp_file: str, target_path: str) -> str:
        """Move downloaded file to permanent location."""
        target_file = Path(target_path)
        target_file.parent.mkdir(parents=True, exist_ok=True)

        # Copy file to target location
        import shutil

        shutil.copy2(temp_file, target_file)
        return str(target_file)


class ThingiverseAdapter(ModelAssetAdapter):
    """Adapter for Thingiverse API."""

    BASE_URL = "https://api.thingiverse.com/"

    def __init__(self, api_key: str, cache_dir: Optional[str] = None):
        super().__init__(api_key=api_key, cache_dir=cache_dir)
        self.session.headers.update({"Authorization": f"Bearer {api_key}"})
        self.rate_limit_delay = 2.0  # Thingiverse rate limiting

    def search(
        self, query: str, category: Optional[str] = None, limit: int = 10
    ) -> List[ModelAsset]:
        """Search Thingiverse for 3D models."""
        self._rate_limit()

        try:
            params = {
                "q": query,
                "per_page": min(limit, 20),  # API limit
                "sort": "popular",
            }

            if category:
                params["category"] = category

            response = self.session.get(
                urljoin(self.BASE_URL, "search/things"), params=params, timeout=30
            )
            response.raise_for_status()

            data = response.json()
            assets = []

            for item in data.get("hits", []):
                # Get detailed info for each thing
                thing_id = item.get("id")
                if thing_id:
                    thing_details = self._get_thing_details(thing_id)
                    if thing_details:
                        assets.append(thing_details)

                if len(assets) >= limit:
                    break

            return assets

        except requests.RequestException as e:
            print(f"Error searching Thingiverse: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error: {e}")
            return []

    def _get_thing_details(self, thing_id: str) -> Optional[ModelAsset]:
        """Get detailed information about a specific thing."""
        self._rate_limit()

        try:
            # Get thing details
            response = self.session.get(
                urljoin(self.BASE_URL, f"things/{thing_id}"), timeout=30
            )
            response.raise_for_status()
            thing_data = response.json()

            # Get files for this thing
            files_response = self.session.get(
                urljoin(self.BASE_URL, f"things/{thing_id}/files"), timeout=30
            )
            files_response.raise_for_status()
            files_data = files_response.json()

            # Extract download URLs and formats
            download_urls = {}
            file_formats = []

            for file_info in files_data:
                file_name = file_info.get("name", "").lower()
                download_url = file_info.get("download_url")

                if download_url:
                    if file_name.endswith(".stl"):
                        download_urls["stl"] = download_url
                        file_formats.append("stl")
                    elif file_name.endswith(".obj"):
                        download_urls["obj"] = download_url
                        file_formats.append("obj")
                    elif file_name.endswith(".3mf"):
                        download_urls["3mf"] = download_url
                        file_formats.append("3mf")

            asset = ModelAsset(
                id=str(thing_id),
                name=thing_data.get("name", ""),
                description=thing_data.get("description", ""),
                category=thing_data.get("category", ""),
                tags=thing_data.get("tags", []),
                preview_url=thing_data.get("thumbnail", ""),
                download_urls=download_urls,
                file_formats=file_formats,
                license=thing_data.get("license", "Unknown"),
                author=thing_data.get("creator", {}).get("name", ""),
                file_size=None,  # Would need to calculate from files
            )

            return asset

        except Exception as e:
            print(f"Error getting thing details for {thing_id}: {e}")
            return None

    def download(
        self, asset: ModelAsset, format: str = "stl", cache_dir: Optional[str] = None
    ) -> Optional[str]:
        """Download 3D model from Thingiverse."""
        if format not in asset.download_urls:
            print(f"Format {format} not available for {asset.name}")
            return None

        if not cache_dir:
            from codetocad.cli.config import get_model_cache_dir

            cache_dir = str(get_model_cache_dir())

        # Create subdirectory for this specific model
        model_dir = Path(cache_dir) / "thingiverse" / asset.id
        model_dir.mkdir(parents=True, exist_ok=True)

        try:
            self._rate_limit()

            download_url = asset.download_urls[format]
            response = self.session.get(download_url, timeout=60)
            response.raise_for_status()

            # Save file
            filename = f"{asset.id}_{asset.name.replace(' ', '_')}.{format}"
            file_path = model_dir / filename

            with open(file_path, "wb") as f:
                f.write(response.content)

            return str(file_path)

        except Exception as e:
            print(f"Error downloading model {asset.name}: {e}")
            return None


class FreeModelAdapter(ModelAssetAdapter):
    """Adapter for free 3D model repositories (placeholder for various free sources)."""

    def __init__(self, cache_dir: Optional[str] = None):
        super().__init__(api_key=None, cache_dir=cache_dir)
        self.rate_limit_delay = 3.0  # Be respectful to free services

    def search(
        self, query: str, category: Optional[str] = None, limit: int = 10
    ) -> List[ModelAsset]:
        """Search free model repositories."""
        # This would integrate with various free model sources
        # For now, return some example assets

        example_assets = [
            ModelAsset(
                id="example_car_chassis",
                name="Simple Car Chassis",
                description="Basic car chassis for robotics projects",
                category="automotive",
                tags=["car", "chassis", "robotics"],
                download_urls={"stl": "https://example.com/car_chassis.stl"},
                file_formats=["stl"],
                license="CC0",
                author="Example Author",
            ),
            ModelAsset(
                id="example_robotic_arm",
                name="6-DOF Robotic Arm",
                description="Six degree of freedom robotic arm",
                category="robotics",
                tags=["robot", "arm", "6dof"],
                download_urls={"stl": "https://example.com/robot_arm.stl"},
                file_formats=["stl"],
                license="CC BY",
                author="Robotics Community",
            ),
        ]

        # Filter by query
        filtered_assets = []
        query_lower = query.lower()

        for asset in example_assets:
            if (
                query_lower in asset.name.lower()
                or query_lower in asset.description.lower()
                or any(query_lower in tag.lower() for tag in asset.tags)
            ):
                filtered_assets.append(asset)

        return filtered_assets[:limit]

    def download(
        self, asset: ModelAsset, format: str = "stl", cache_dir: Optional[str] = None
    ) -> Optional[str]:
        """Download from free model repository."""
        # For example assets, create placeholder files
        if not cache_dir:
            from codetocad.cli.config import get_model_cache_dir

            cache_dir = str(get_model_cache_dir())

        # Create subdirectory for this specific model
        model_dir = Path(cache_dir) / "free_models" / asset.id
        model_dir.mkdir(parents=True, exist_ok=True)

        # Check if model is already cached
        filename = f"{asset.id}.{format}"
        file_path = model_dir / filename

        if file_path.exists():
            print(f"Using cached model: {asset.name}")
            return str(file_path)

        # Create a placeholder STL file (in real implementation, would download actual file)

        # Create a minimal STL file as placeholder
        if format == "stl":
            stl_content = """solid placeholder
facet normal 0 0 1
  outer loop
    vertex 0 0 0
    vertex 1 0 0
    vertex 0 1 0
  endloop
endfacet
endsolid placeholder
"""
            with open(file_path, "w") as f:
                f.write(stl_content)

            return str(file_path)

        return None


class ModelAssetManager:
    """Manager for multiple model asset adapters."""

    def __init__(self):
        self.adapters: Dict[str, ModelAssetAdapter] = {}

    def add_adapter(self, name: str, adapter: ModelAssetAdapter):
        """Add a model asset adapter."""
        self.adapters[name] = adapter

    def search_all(
        self, query: str, category: Optional[str] = None, limit: int = 10
    ) -> Dict[str, List[ModelAsset]]:
        """Search all registered adapters."""
        results = {}

        for name, adapter in self.adapters.items():
            try:
                assets = adapter.search(query, category, limit)
                if assets:
                    results[name] = assets
            except Exception as e:
                print(f"Error searching {name}: {e}")

        return results

    def download_from_adapter(
        self,
        adapter_name: str,
        asset: ModelAsset,
        format: str = "stl",
        cache_dir: Optional[str] = None,
    ) -> Optional[str]:
        """Download model using specific adapter."""
        if adapter_name not in self.adapters:
            print(f"Adapter {adapter_name} not found")
            return None

        return self.adapters[adapter_name].download(asset, format, cache_dir)
