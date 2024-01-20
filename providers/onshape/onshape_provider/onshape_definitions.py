class OnshapeUrl:
    # Onshape Url's have three components:
    # https://cad.onshape.com/documents/b5c68587473845a7c3313c68/w/df7e37f0d4d9aa712d9eb3db/e/80cf7ac7b27188a730391d61
    # document_id, workspace_id and tab_id respectively.
    # This class helps keep track and format this url.
    def __init__(
        self,
        document_id: str,
        workspace_id: str,
        tab_id: str | None = None,
        base_url: str = "https://cad.onshape.com",
    ) -> None:
        self.document_id = document_id
        self.workspace_id = workspace_id
        self.tab_id = tab_id
        self.base_url = base_url

    def __repr__(self) -> str:
        return "{}/documents/{}/w/{}/e/{}".format(
            self.base_url, self.document_id, self.workspace_id, self.tab_id
        )

    def __str__(self) -> str:
        return self.__repr__()

    # Mark: formatters for Onshape-Client dict

    @property
    def dict_document(self) -> dict[str, str]:
        """
        returns a dictionary with ["did"] as keys
        """
        return {"did": self.document_id}

    @property
    def dict_document_and_workspace(self) -> dict[str, str]:
        """
        returns a dictionary with ["did", "wid"] as keys
        """
        return {"did": self.document_id, "wid": self.workspace_id}

    @property
    def dict_document_and_workspace_and_model(self) -> dict[str, str]:
        """
        returns a dictionary with ["did", "wvmid", "wvm"] as keys
        """
        return {"did": self.document_id, "wvmid": self.workspace_id, "wvm": "w"}

    @property
    def dict_document_and_workspace_and_tab(self) -> dict[str, str]:
        """
        returns a dictionary with ["did", "wid", "eid"] as keys
        """
        if self.tab_id is None:
            raise Exception("Tab ID is None.")
        return {"did": self.document_id, "wid": self.workspace_id, "eid": self.tab_id}

    @property
    def dict_document_and_workspace_and_model_and_tab(self) -> dict[str, str]:
        """
        returns a dictionary with ["did", "wvmid", "wvm", "eid"] as keys
        """
        if self.tab_id is None:
            raise Exception("Tab ID is None.")
        return {
            "did": self.document_id,
            "wvmid": self.workspace_id,
            "wvm": "w",
            "eid": self.tab_id,
        }
