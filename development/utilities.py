import re

pattern1 = re.compile(r'(.)([A-Z][a-z]+)')
pattern2 = re.compile(r'__([A-Z])')
pattern3 = re.compile(r'([a-z0-9])([A-Z])')


def to_snake_case(name):
    # references https://stackoverflow.com/a/1176023/9824103
    name = pattern1.sub(r'\1_\2', name)
    name = pattern2.sub(r'_\1', name)
    name = pattern3.sub(r'\1_\2', name)
    return name.lower()
