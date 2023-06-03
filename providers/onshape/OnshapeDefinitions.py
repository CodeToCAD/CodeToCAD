class OnshapeUrl:
    # Onshape Url's have three components:
    # https://cad.onshape.com/documents/b5c68587473845a7c3313c68/w/df7e37f0d4d9aa712d9eb3db/e/80cf7ac7b27188a730391d61
    # documentId, workspaceId and tabId respectively.
    def __init__(self, documentId: str, workspaceId: str, tabId: str, baseUrl: str = "https://cad.onshape.com") -> None:
        self.documentId = documentId
        self.workspaceId = workspaceId
        self.tabId = tabId
        self.baseUrl = baseUrl

    def __repr__(self) -> str:
        return "{}/documents/{}/w/{}/e/{}".format(self.baseUrl, self.documentId, self.workspaceId, self.tabId)

    def __str__(self) -> str:
        return self.__repr__()
