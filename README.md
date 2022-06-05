# Figma2Unreal

Figma2Unreal uses the [Figma API](https://www.figma.com/developers/api) and python scripts to take assets created in Figma and create nested UMG widgets suitable for making more advanced prototypes.

It is rudimentary at the moment so complex Figma functionality is not maintained, but it should still speed up the process with some manual cleanup required.

## Installation and Usage
*Install the plugin to your Unreal Project and make sure you have Python scripting enabled.
*Use pip install requests to install the requests module to your Unreal Python environment {IMPORTANT: Must be your Unreal python envinronment found in "Engine/Binaries/ThirdParty/Python3" folder
*Edit "Content/Python/runImportFigmaDoc.py" to use your [Personal Access Token](https://www.figma.com/developers/api#access-tokens), [FileID](https://www.figma.com/developers/api#files-endpoints), and desired import directory.
*Run "runImportFigmaDoc.py" from inside Unreal and you should get sub-folders with all of your newly created widgets and asssets
*Restart Unreal to have all of your referenced widgets update in their parents (seems to be a new-ish bug with Unreal that editing User Widgets isn't reflected in parents until restart)


## Known Issues
*Only supports a single canvas
*Reimporting overrides assets and brings up dialogue boxes for each overrides
*Doesn't seem to release access to some widgets so deleting/editing widgets immedietly after running can cause issues
*Requires restart to update widgets in their parents (think this is an Unreal bug)
*Doesn't support gradient fills
*Doesn't support outlines
*Doesn't support advanced layouts
*Doesn't use text justification
*Text doesn't wrap or set up spacing correctly
*Would like to support multiple fonts (could download google fonts with separate API)
*Would idealy like to use native unreal materials for rectangles and lines to allow more flexible editibility
*Would like to use native Unreal layouts for grids, horizontal, vertical boxes etx
