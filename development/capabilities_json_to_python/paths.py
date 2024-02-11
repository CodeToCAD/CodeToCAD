"""
Paths to folders and files used by JINJA template generation.
"""
import os


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

output_dir = f"{SCRIPT_DIR}/../../codetocad/"
docs = f"{SCRIPT_DIR}/../../docs/"
templates_dir = f"{SCRIPT_DIR}/templates"

capabilities_json_path = f"{SCRIPT_DIR}/../../codetocad/capabilities.json"

capabilities_to_py_interface = "capabilities_to_py_interface.j2"
capabilities_to_py_interface_out = f"{output_dir}/interfaces"


capabilities_to_py_provider = "capabilities_to_py_provider.j2"
capabilities_to_py_provider_out = f"{output_dir}/providers_sample"


capabilities_to_py_test_interface = "capabilities_to_py_test_interface.j2"
capabilities_to_py_test_interface_out = f"{output_dir}/tests_interfaces"


capabilities_to_py_test = "capabilities_to_py_test.j2"
capabilities_to_py_test_out = f"{output_dir}/tests_sample"
