import inspect
import unittest
import json

capabilities_json = "codetocad/capabilities.json"

capabilies_class_names = []

with open(capabilities_json) as f:
    capabilities: dict = json.load(f)
    for capability_name, value in capabilities["capabilities"].items():
        if not value.get("is_interface_only", False):
            capabilies_class_names.append(capability_name)


class TestProviderCompliance(unittest.TestCase):
    def test_no_abstract_provider(self):
        print("capabilies_class_names", capabilies_class_names)
        all_providers_import = __import__("providers")
        all_providers_modules = inspect.getmembers(
            all_providers_import, predicate=inspect.ismodule
        )
        for module_name, provider_module in all_providers_modules:
            print(f"Testing module {module_name}")
            all_classes = inspect.getmembers(provider_module, predicate=inspect.isclass)
            for class_name, some_class in all_classes:
                if class_name not in capabilies_class_names:
                    continue
                abstract_methods = list(some_class.__abstractmethods__)
                assert (
                    len(abstract_methods) == 0
                ), f"{class_name} has abstract methods {abstract_methods} in the {module_name} provider."
