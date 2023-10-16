from typing import Optional
from mock.modeling.mock_blender import inject_mock_bpy, reset_mock_bpy


def inject_mock_modeling_provider(global_context: Optional[dict]):

    # We don't have a mock provider yet, so we'll use the blender_provider temporarily.

    inject_mock_bpy()


def reset_mock_modeling_provider():
    reset_mock_bpy()
