# CodeToCAD - Onshape Provider

This is the Onshape Provider that allows CodeToCAD to talk with the Onshape client.

Onshape uses a REST API: [https://cad.onshape.com/glassworks/explorer](https://cad.onshape.com/glassworks/explorer) and OAuth tokens.

## Setup

1. Please copy and rename [.onshape_client_config.yaml.template](./.onshape_client_config.yaml.template) to [.onshape_client_config.yaml](./.onshape_client_config.yaml). [test_onshape_actions.py](../../tests/test_onshape_actions.py) will look for this yaml file when run.

    > Note: You can obtain the Access and Secret keys by visiting [the Dev Portal](https://dev-portal.onshape.com/keys) and creating a new API Key

## Resources

- [Glassworks](https://cad.onshape.com/glassworks/explorer?_gl=1*qvs0kd*_gcl_au*MTg4NTIyNDI0OS4xNjg1ODExMDM3#/PartStudio)
- [Python client test scripts](https://github.com/onshape-public/onshape-clients/tree/master/python/test)
- [API Snippets](https://github.com/PTC-Education/PTC-API-Playground)