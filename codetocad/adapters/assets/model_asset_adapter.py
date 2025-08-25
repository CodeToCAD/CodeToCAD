"""
3D model asset adapter for downloading models from online sources.

This module provides adapters for downloading 3D model assets from various online
sources like Thingiverse, free model repositories, and other 3D model libraries.
"""

import os
import json
import time
import requests
from typing import Dict, Any, Tuple
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
    tags: list[str]
    preview_url: str | None = None
    download_urls: dict[str, str] = None  # format -> url
    file_formats: list[str] = None  # Available formats (stl, obj, etc.)
    license: str = "Unknown"
    author: str = ""
    dimensions: tuple[float, float, float] | None = None  # x, y, z in mm
    file_size: int | None = None  # bytes

    def __post_init__(self):
        if self.download_urls is None:
            self.download_urls = {}
        if self.file_formats is None:
            self.file_formats = []


class ModelAssetAdapter:
    """Base class for 3D model asset adapters."""

    def __init__(self, api_key: str, cache_dir: str):
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
        self, query: str, category: str | None = None, limit: int = 10
    ) -> list[ModelAsset]:
        """Search for 3D models by keywords."""
        raise NotImplementedError("Subclasses must implement search method")

    def download(
        self, asset: ModelAsset, format: str = "stl", cache_dir: str | None = None
    ) -> str | None:
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


class ModelAssetManager:
    """Manager for multiple model asset adapters."""

    def __init__(self):
        self.adapters: dict[str, ModelAssetAdapter] = {}

    def add_adapter(self, name: str, adapter: ModelAssetAdapter):
        """Add a model asset adapter."""
        self.adapters[name] = adapter

    def search_all(
        self, query: str, category: str | None = None, limit: int = 10
    ) -> dict[str, list[ModelAsset]]:
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
        cache_dir: str | None = None,
    ) -> str | None:
        """Download model using specific adapter."""
        if adapter_name not in self.adapters:
            print(f"Adapter {adapter_name} not found")
            return None

        return self.adapters[adapter_name].download(asset, format, cache_dir)
