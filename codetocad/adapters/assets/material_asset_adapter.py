"""
Material asset adapter for downloading materials from online sources.

This module provides adapters for downloading material assets from various online
sources like ambientCG, Poliigon, and other material libraries.
"""

import os
import json
import time
import requests
from typing import Optional, Dict, Any, List
from pathlib import Path
from urllib.parse import urljoin, urlparse
from dataclasses import dataclass

from codetocad.core.material import Material
from codetocad.interfaces.cad.material_interface import TextureMaps


@dataclass
class MaterialAsset:
    """Container for material asset information."""

    id: str
    name: str
    category: str
    tags: List[str]
    preview_url: Optional[str] = None
    download_urls: Dict[str, str] = None  # map_type -> url
    resolution: str = "1K"
    file_format: str = "jpg"
    license: str = "CC0"
    description: str = ""

    def __post_init__(self):
        if self.download_urls is None:
            self.download_urls = {}


class MaterialAssetAdapter:
    """Base class for material asset adapters."""

    def __init__(self, api_key: Optional[str] = None, cache_dir: Optional[str] = None):
        self.api_key = api_key
        self.cache_dir = (
            Path(cache_dir)
            if cache_dir
            else Path.home() / ".codetocad" / "material_cache"
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
    ) -> List[MaterialAsset]:
        """Search for materials by name/category."""
        raise NotImplementedError("Subclasses must implement search method")

    def download(
        self, asset: MaterialAsset, temp_dir: Optional[str] = None
    ) -> Dict[str, str]:
        """Download material textures to temporary directory."""
        raise NotImplementedError("Subclasses must implement download method")

    def save(self, downloaded_files: Dict[str, str], target_dir: str) -> Dict[str, str]:
        """Move downloaded files to permanent location."""
        target_path = Path(target_dir)
        target_path.mkdir(parents=True, exist_ok=True)

        saved_files = {}
        for map_type, temp_path in downloaded_files.items():
            if os.path.exists(temp_path):
                filename = Path(temp_path).name
                target_file = target_path / filename

                # Copy file to target location
                import shutil

                shutil.copy2(temp_path, target_file)
                saved_files[map_type] = str(target_file)

        return saved_files


class AmbientCGAdapter(MaterialAssetAdapter):
    """Adapter for ambientCG (free CC0 materials)."""

    BASE_URL = "https://ambientcg.com/api/v2/"

    def __init__(self, cache_dir: Optional[str] = None):
        super().__init__(
            api_key=None, cache_dir=cache_dir
        )  # ambientCG is free, no API key needed
        self.rate_limit_delay = 2.0  # Be respectful to free service

    def search(
        self, query: str, category: Optional[str] = None, limit: int = 10
    ) -> List[MaterialAsset]:
        """Search ambientCG for materials."""
        self._rate_limit()

        try:
            # Build search parameters
            params = {
                "limit": min(limit, 100),  # API limit
                "include": "tagData,previewImage,downloadData",
                "sort": "Popular",
            }

            if query:
                params["q"] = query
            if category:
                params["category"] = category

            response = self.session.get(
                urljoin(self.BASE_URL, "full_json"), params=params, timeout=30
            )
            response.raise_for_status()

            data = response.json()
            assets = []

            for item in data.get("foundAssets", []):
                # Extract download URLs for different map types
                download_urls = {}
                downloads = item.get("downloadFolders", {})

                # Look for 1K resolution first, then fallback to others
                for res in ["1K", "2K", "512", "4K"]:
                    if res in downloads:
                        download_data = downloads[res]
                        # Try different download categories
                        for category in ["zip", "jpg", "png"]:
                            category_data = download_data.get(
                                "downloadFiletypeCategories", {}
                            ).get(category, {})
                            for file_info in category_data.get("downloads", []):
                                file_name = file_info.get("fileName", "")
                                download_link = file_info.get("downloadLink", "")
                                if download_link:
                                    if category == "zip":
                                        download_urls["zip"] = download_link
                                    else:
                                        # For individual files, try to determine type
                                        if (
                                            "color" in file_name.lower()
                                            or "diffuse" in file_name.lower()
                                        ):
                                            download_urls["diffuse"] = download_link
                                        elif "normal" in file_name.lower():
                                            download_urls["normal"] = download_link
                                        elif "rough" in file_name.lower():
                                            download_urls["roughness"] = download_link
                                    break
                            if download_urls:
                                break
                        if download_urls:
                            break

                asset = MaterialAsset(
                    id=item.get("assetId", ""),
                    name=item.get("displayName", ""),
                    category=item.get("category", ""),
                    tags=item.get("tags", []),
                    preview_url=item.get("previewImage", {}).get("1K-JPG", ""),
                    download_urls=download_urls,
                    resolution="1K",
                    file_format="jpg",
                    license="CC0",
                    description=item.get("description", ""),
                )
                assets.append(asset)

                if len(assets) >= limit:
                    break

            return assets

        except requests.RequestException as e:
            print(f"Error searching ambientCG: {e}")
            # Return some example materials as fallback
            return self._get_fallback_materials(query, limit)
        except Exception as e:
            print(f"Unexpected error: {e}")
            return self._get_fallback_materials(query, limit)

    def _get_fallback_materials(self, query: str, limit: int) -> List[MaterialAsset]:
        """Provide fallback materials when API is unavailable."""
        fallback_materials = [
            MaterialAsset(
                id="fallback_steel",
                name="Industrial Steel",
                category="metal",
                tags=["steel", "metal", "industrial"],
                description="High-strength industrial steel material",
                license="CC0",
            ),
            MaterialAsset(
                id="fallback_aluminum",
                name="Brushed Aluminum",
                category="metal",
                tags=["aluminum", "metal", "brushed"],
                description="Brushed aluminum with metallic finish",
                license="CC0",
            ),
            MaterialAsset(
                id="fallback_wood",
                name="Oak Wood",
                category="wood",
                tags=["wood", "oak", "natural"],
                description="Natural oak wood texture",
                license="CC0",
            ),
            MaterialAsset(
                id="fallback_concrete",
                name="Rough Concrete",
                category="concrete",
                tags=["concrete", "rough", "construction"],
                description="Rough concrete surface texture",
                license="CC0",
            ),
        ]

        # Filter by query
        query_lower = query.lower()
        filtered = []
        for material in fallback_materials:
            if (
                query_lower in material.name.lower()
                or query_lower in material.category.lower()
                or any(query_lower in tag.lower() for tag in material.tags)
            ):
                filtered.append(material)

        return filtered[:limit]

    def download(
        self, asset: MaterialAsset, cache_dir: Optional[str] = None
    ) -> Dict[str, str]:
        """Download material textures from ambientCG."""
        if not cache_dir:
            from codetocad.cli.config import get_material_cache_dir

            cache_dir = str(get_material_cache_dir())

        # Create subdirectory for this specific material
        material_dir = Path(cache_dir) / "ambientcg" / asset.id
        material_dir.mkdir(parents=True, exist_ok=True)

        downloaded_files = {}

        # Check if material is already cached
        cached_files = self._check_cached_material(material_dir, asset)
        if cached_files:
            print(f"Using cached material: {asset.name}")
            return cached_files

        try:
            # Download ZIP file if available
            zip_url = asset.download_urls.get("zip")
            if not zip_url:
                print(f"No download URL found for asset {asset.name}")
                return downloaded_files

            self._rate_limit()

            # Download ZIP file
            response = self.session.get(zip_url, timeout=60)
            response.raise_for_status()

            zip_path = material_dir / f"{asset.id}.zip"
            with open(zip_path, "wb") as f:
                f.write(response.content)

            # Extract ZIP file
            import zipfile

            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(material_dir)

            # Find extracted texture files
            for file_path in material_dir.rglob("*.jpg"):
                filename = file_path.name.lower()

                # Map filenames to texture types
                if "color" in filename or "diffuse" in filename or "albedo" in filename:
                    downloaded_files["diffuse"] = str(file_path)
                elif "normal" in filename or "nrm" in filename:
                    downloaded_files["normal"] = str(file_path)
                elif "rough" in filename:
                    downloaded_files["roughness"] = str(file_path)
                elif "metal" in filename:
                    downloaded_files["metallic"] = str(file_path)
                elif "spec" in filename:
                    downloaded_files["specular"] = str(file_path)
                elif "ao" in filename or "ambient" in filename:
                    downloaded_files["ambient_occlusion"] = str(file_path)
                elif "disp" in filename or "height" in filename:
                    downloaded_files["displacement"] = str(file_path)

            # Clean up ZIP file
            zip_path.unlink()

            # Save metadata for caching
            if downloaded_files:
                self._save_material_metadata(material_dir, asset, downloaded_files)

            return downloaded_files

        except Exception as e:
            print(f"Error downloading material {asset.name}: {e}")
            return {}

    def _check_cached_material(
        self, material_dir: Path, asset: MaterialAsset
    ) -> Dict[str, str]:
        """Check if material is already cached and return file paths."""
        metadata_file = material_dir / "metadata.json"
        if not metadata_file.exists():
            return {}

        try:
            with open(metadata_file, "r") as f:
                metadata = json.load(f)

            # Verify all files still exist
            cached_files = {}
            for texture_type, file_path in metadata.get("files", {}).items():
                if Path(file_path).exists():
                    cached_files[texture_type] = file_path

            if cached_files:
                return cached_files
        except Exception:
            pass

        return {}

    def _save_material_metadata(
        self, material_dir: Path, asset: MaterialAsset, downloaded_files: Dict[str, str]
    ):
        """Save material metadata for caching."""
        metadata = {
            "asset_id": asset.id,
            "asset_name": asset.name,
            "category": asset.category,
            "tags": asset.tags,
            "description": asset.description,
            "files": downloaded_files,
            "download_date": time.time(),
        }

        metadata_file = material_dir / "metadata.json"
        with open(metadata_file, "w") as f:
            json.dump(metadata, f, indent=2)

    def create_material_from_asset(
        self, asset: MaterialAsset, downloaded_files: Dict[str, str]
    ) -> Material:
        """Create a Material object from downloaded asset."""
        material = Material()
        material.set_name(asset.name)
        material.set_description(asset.description)
        material.set_category(asset.category)

        # Add tags
        for tag in asset.tags:
            material.add_tag(tag)

        # Set texture paths
        material.set_textures(
            diffuse=downloaded_files.get("diffuse"),
            normal=downloaded_files.get("normal"),
            roughness=downloaded_files.get("roughness"),
            metallic=downloaded_files.get("metallic"),
            specular=downloaded_files.get("specular"),
            ambient_occlusion=downloaded_files.get("ambient_occlusion"),
            displacement=downloaded_files.get("displacement"),
        )

        # Try to infer material properties from category and tags
        self._infer_material_properties(material, asset)

        return material

    def _infer_material_properties(self, material: Material, asset: MaterialAsset):
        """Infer physical properties from asset metadata."""
        category = asset.category.lower()
        tags = [tag.lower() for tag in asset.tags]

        # Set properties based on category and tags
        if "metal" in category or any(
            tag in tags for tag in ["metal", "steel", "iron", "aluminum"]
        ):
            material.set_physical_properties(
                density=7850.0, friction=0.7, restitution=0.1
            )
            material.set_visual_properties(metallic=1.0, roughness=0.3)
        elif "wood" in category or "wood" in tags:
            material.set_physical_properties(
                density=600.0, friction=0.8, restitution=0.3
            )
            material.set_visual_properties(metallic=0.0, roughness=0.8)
        elif "concrete" in category or "concrete" in tags:
            material.set_physical_properties(
                density=2400.0, friction=0.9, restitution=0.05
            )
            material.set_visual_properties(metallic=0.0, roughness=0.95)
        elif "plastic" in category or "plastic" in tags:
            material.set_physical_properties(
                density=1050.0, friction=0.4, restitution=0.5
            )
            material.set_visual_properties(metallic=0.0, roughness=0.6)
        elif "fabric" in category or "fabric" in tags:
            material.set_physical_properties(
                density=300.0, friction=1.0, restitution=0.2
            )
            material.set_visual_properties(metallic=0.0, roughness=0.9)


class PoliigonAdapter(MaterialAssetAdapter):
    """Adapter for Poliigon (requires API key)."""

    BASE_URL = "https://www.poliigon.com/api/v1/"

    def __init__(self, api_key: str, cache_dir: Optional[str] = None):
        super().__init__(api_key=api_key, cache_dir=cache_dir)
        self.session.headers.update({"Authorization": f"Bearer {api_key}"})

    def search(
        self, query: str, category: Optional[str] = None, limit: int = 10
    ) -> List[MaterialAsset]:
        """Search Poliigon for materials (placeholder - would need actual API documentation)."""
        # This would need to be implemented based on Poliigon's actual API
        print("Poliigon adapter not fully implemented - requires API documentation")
        return []

    def download(
        self, asset: MaterialAsset, temp_dir: Optional[str] = None
    ) -> Dict[str, str]:
        """Download from Poliigon (placeholder)."""
        print("Poliigon download not implemented")
        return {}


class MaterialAssetManager:
    """Manager for multiple material asset adapters."""

    def __init__(self):
        self.adapters: Dict[str, MaterialAssetAdapter] = {}

    def add_adapter(self, name: str, adapter: MaterialAssetAdapter):
        """Add a material asset adapter."""
        self.adapters[name] = adapter

    def search_all(
        self, query: str, category: Optional[str] = None, limit: int = 10
    ) -> Dict[str, List[MaterialAsset]]:
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
        self, adapter_name: str, asset: MaterialAsset, temp_dir: Optional[str] = None
    ) -> Dict[str, str]:
        """Download material using specific adapter."""
        if adapter_name not in self.adapters:
            print(f"Adapter {adapter_name} not found")
            return {}

        return self.adapters[adapter_name].download(asset, temp_dir)
