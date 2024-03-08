"""
Paths to folders and files used by JINJA template generation.
"""
import os


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

root_dir = f"{SCRIPT_DIR}/../.."
codetocad_dir = f"{root_dir}/codetocad/"
docs = f"{root_dir}/docs/"
templates_dir = f"{SCRIPT_DIR}/templates"

capabilities_json_path = f"{root_dir}/codetocad/capabilities.json"

capabilities_to_py_interface = "capabilities_to_py_interface.j2"
capabilities_to_py_interface_out = f"{codetocad_dir}/interfaces"

capabilities_to_py_facade = "capabilities_to_py_facade.j2"
capabilities_to_py_facade_out = f"{codetocad_dir}/facade/"


capabilities_to_py_provider = "capabilities_to_py_provider.j2"
capabilities_to_py_provider_out = f"{root_dir}/providers/sample"


capabilities_to_py_test_interface = "capabilities_to_py_test_interface.j2"
capabilities_to_py_test_interface_out = f"{codetocad_dir}/tests_interfaces"


capabilities_to_py_test = "capabilities_to_py_test.j2"
capabilities_to_py_test_out = f"{root_dir}/tests/test_providers/sample"


capabilities_to_python_documentation_html = (
    "capabilities_to_python_documentation_html.j2"
)
capabilities_to_python_documentation_html_out = f"{docs}/docs.html"
