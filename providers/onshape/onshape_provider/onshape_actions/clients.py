from onshape_client import Client

import codetocad.utilities as Utilities


def get_onshape_client(config: dict) -> Client:
    return Client(configuration=config).get_client()


def get_onshape_client_with_config_file(config_filepath: str) -> Client:
    configAbsolutePath = Utilities.get_absolute_filepath(config_filepath)
    return Client(keys_file=configAbsolutePath).get_client()
