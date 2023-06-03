class OnshapeUrl:
    # Onshape Url's have three components:
    # https://cad.onshape.com/documents/b5c68587473845a7c3313c68/w/df7e37f0d4d9aa712d9eb3db/e/80cf7ac7b27188a730391d61
    # documentId, workspaceId and tabId respectively.
    # This class helps keep track and format this url.
    def __init__(self, documentId: str, workspaceId: str, tabId: str, baseUrl: str = "https://cad.onshape.com") -> None:
        self.documentId = documentId
        self.workspaceId = workspaceId
        self.tabId = tabId
        self.baseUrl = baseUrl

    def __repr__(self) -> str:
        return "{}/documents/{}/w/{}/e/{}".format(self.baseUrl, self.documentId, self.workspaceId, self.tabId)

    def __str__(self) -> str:
        return self.__repr__()

    # Mark: formatters for Onshape-Client dict

    @property
    def dictDocument(self) -> dict[str, str]:
        '''
        returns a dictionary with ["did"] as keys
        '''
        return {
            "did": self.documentId
        }

    @property
    def dictDocumentAndWorkspace(self) -> dict[str, str]:
        '''
        returns a dictionary with ["did", "wid"] as keys
        '''
        return {
            "did": self.documentId,
            "wid": self.workspaceId
        }

    @property
    def dictDocumentAndWorkspaceAndModel(self) -> dict[str, str]:
        '''
        returns a dictionary with ["did", "wvmid", "wvm"] as keys
        '''
        return {
            "did": self.documentId,
            "wvmid": self.workspaceId,
            "wvm": "w"
        }

    @property
    def dictDocumentAndWorkspaceAndTab(self) -> dict[str, str]:
        '''
        returns a dictionary with ["did", "wid", "eid"] as keys
        '''
        return {
            "did": self.documentId,
            "wid": self.workspaceId,
            "eid": self.tabId
        }

    @property
    def dictDocumentAndWorkspaceAndModelAndTab(self) -> dict[str, str]:
        '''
        returns a dictionary with ["did", "wvmid", "wvm", "eid"] as keys
        '''
        return {
            "did": self.documentId,
            "wvmid": self.workspaceId,
            "wvm": "w",
            "eid": self.tabId
        }
