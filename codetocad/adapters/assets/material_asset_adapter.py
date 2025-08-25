"""
Material asset adapter for downloading materials from online sources.

This module provides adapters for downloading material assets from various online
sources like ambientCG, Poliigon, and other material libraries.
"""

import os
import json
import time
import requests
from typing import Dict, Any, List
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
    tags: list[str]
    preview_url: str | None = None
    download_urls: dict[str, str] | None = None  # map_type -> url
    resolution: str = "1K"
    file_format: str = "jpg"
    license: str = "CC0"
    description: str = ""

    def __post_init__(self):
        if self.download_urls is None:
            self.download_urls = {}


class MaterialAssetAdapter:
    """Base class for material asset adapters."""

    def __init__(self, api_key: str | None = None, cache_dir: str | None = None):
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
        self, query: str, category: str | None = None, limit: int = 10
    ) -> list[MaterialAsset]:
        """Search for materials by name/category."""
        raise NotImplementedError("Subclasses must implement search method")

    def download(
        self, asset: MaterialAsset, cache_dir: str | None = None
    ) -> dict[str, str]:
        """Download material textures to temporary directory."""
        raise NotImplementedError("Subclasses must implement download method")

    def save(self, downloaded_files: dict[str, str], target_dir: str) -> dict[str, str]:
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


class MaterialAssetManager:
    """Manager for multiple material asset adapters."""

    def __init__(self):
        self.adapters: dict[str, MaterialAssetAdapter] = {}

    def add_adapter(self, name: str, adapter: MaterialAssetAdapter):
        """Add a material asset adapter."""
        self.adapters[name] = adapter

    def search_all(
        self, query: str, category: str | None = None, limit: int = 10
    ) -> dict[str, list[MaterialAsset]]:
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
        self, adapter_name: str, asset: MaterialAsset, temp_dir: str | None = None
    ) -> dict[str, str]:
        """Download material using specific adapter."""
        if adapter_name not in self.adapters:
            print(f"Adapter {adapter_name} not found")
            return {}

        return self.adapters[adapter_name].download(asset, temp_dir)
