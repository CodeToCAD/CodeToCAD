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

if __name__ == "__main__":
    print("Generating", capabilities_to_python_documentation_html)

    template = get_jinja_environment().get_template(
        capabilities_to_python_documentation_html
    )
    output_from_parsed_template = template.render(
        capabilities_loader=CapabilitiesLoader(),
    )
    with open(capabilities_to_python_documentation_html_out, "w") as fh:
        fh.write(output_from_parsed_template)

    print("Done")
