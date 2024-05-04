__providers = {}


def register(provider, interface):
    global __providers
    __providers[interface] = provider


def get_provider(interface):
    global __providers
    return __providers[interface]
