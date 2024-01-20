from dataclasses import dataclass
from onshape_client import Client

from providers.onshape.onshape_provider import onshape_definitions


@dataclass
class OnshapeContext:
    active_client: Client
    active_tab_url: onshape_definitions.OnshapeUrl

    @classmethod
    def get_active(cls):
        return cls._active_context

    @classmethod
    def set_active(cls, context: "OnshapeContext"):
        cls._active_context = context
