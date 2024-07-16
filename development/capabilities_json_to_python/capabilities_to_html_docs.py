"""
A script to generate the HTML docs from capabilities.json + jinja2 templates.
"""

from development.capabilities_json_to_python.capabilities_loader import (
    CapabilitiesLoader,
)
from development.capabilities_json_to_python.template_utils import get_jinja_environment
from development.capabilities_json_to_python.paths import (
    capabilities_to_python_documentation_html,
    capabilities_to_python_documentation_html_out,
)
from development.get_provider_supported_decorators import (
    get_provider_supported_decorators,
)

HTML_DOCS_PROVIDERS = ["Blender", "Fusion360", "Onshape"]


def _get_provider_supports():
    supported_providers = {}

    for provider_name in HTML_DOCS_PROVIDERS:
        supported_providers[provider_name] = get_provider_supported_decorators(
            provider_name
        )

    return supported_providers


if __name__ == "__main__":
    print("Generating", capabilities_to_python_documentation_html)

    supported_providers = _get_provider_supports()

    template = get_jinja_environment().get_template(
        capabilities_to_python_documentation_html
    )
    output_from_parsed_template = template.render(
        capabilities_loader=CapabilitiesLoader(),
        supported_providers=supported_providers,
    )
    with open(capabilities_to_python_documentation_html_out, "w") as fh:
        fh.write(output_from_parsed_template)

    print("Done")
