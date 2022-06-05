import figmaApi
from importlib import *
reload(figmaApi)

AccessToken = "<YourAccessTokenHere>"
ImportDirectory = "/Game/"
FileID = "<YourFileIDHere>"
FileDocument = figmaApi.FigmaDocument(FileID, ImportDirectory, AccessToken)
FileDocument.writeToUnreal()


