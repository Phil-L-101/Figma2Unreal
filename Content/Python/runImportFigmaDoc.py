import figmaApi
from importlib import *
reload(figmaApi)

AccessToken = "<YourAccessTokenHere>"
ImportDirectory = "/Game/"
FileID = "<YourFileIDHere>"
Pages = [-1] #List of pages to import (zero indexed), -1 imports all pages in the document
FileDocument = figmaApi.FigmaDocument(FileID, ImportDirectory, AccessToken, Pages)
FileDocument.writeToUnreal()


