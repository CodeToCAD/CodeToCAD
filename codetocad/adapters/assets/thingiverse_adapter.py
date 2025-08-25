from pathlib import Path
from typing import Optional
from urllib.parse import urljoin

import requests

from codetocad.adapters.assets.model_asset_adapter import ModelAsset, ModelAssetAdapter
from codetocad.cli.config import read_config


class ThingiverseAdapter(ModelAssetAdapter):
    """Adapter for Thingiverse API."""

    BASE_URL = "https://api.thingiverse.com/"

    def __init__(self):
        api_key = read_config().assets.thingiverse_api_key
        cache_dir = read_config().assets.model_cache_dir
        super().__init__(api_key=api_key, cache_dir=cache_dir)
        self.session.headers.update({"Authorization": f"Bearer {api_key}"})
        self.rate_limit_delay = 2.0  # Thingiverse rate limiting

    def search(
        self, query: str, category: str | None = None, limit: int = 10
    ) -> list[ModelAsset]:
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

    def _get_thing_details(self, thing_id: str) -> ModelAsset | None:
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
        self, asset: ModelAsset, format: str = "stl", cache_dir: str | None = None
    ) -> str | None:
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
