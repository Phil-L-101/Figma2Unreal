import requests
import json
import unreal
import os

# Helper function to check if an Unreal directory exists and make it if not
def createDirSafe(DirectoryPath):
    if not unreal.EditorAssetLibrary.does_directory_exist(DirectoryPath):
        unreal.EditorAssetLibrary.make_directory(DirectoryPath)

# Helper function to sanitise name to use with unreal paths
def sanitiseName(Name):
        SanitisedName = (Name.replace(" ", "_").
                     replace("-", "_").
                     replace("(", "").
                     replace(")", "").
                     replace(".", "_").
                     replace("\"", "").
                     replace(",", "").
                     replace("\'", "").
                     replace("“", "").
                     replace("”", "").
                     replace("[","").
                     replace("]","").
                     replace("=", "").
                     replace("#", "").
                     splitlines(False)[0][:50])
        return SanitisedName

# Gets full path to bluerint class
def getAssetPath(Directory, AssetName):
    Path = Directory + AssetName + "." + AssetName + "_C"
    return Path

# Create unique instance name to avoid conflicts
def createInsatanceName(Name, id):
    return Name + "_" + id

# Convert Fills into a single colour
def getColorFromFills(Fills, DefaultColor):
        try: # May not have a background colour
            Color = {
                                "r" : Fills[0]["color"]["r"],
                                "g" : Fills[0]["color"]["g"],
                                "b" : Fills[0]["color"]["b"],
                             }
            try: # Only has opacity attribute if opacity not 1
                Color["a"] = Fills[0]["opacity"]
            except:
                Color["a"] = 1
        except:
            Color = DefaultColor
        return Color

# Helper function to save assets
def saveAsset(Asset):
    unreal.EditorAssetLibrary.save_loaded_asset(Asset, only_if_is_dirty=False)

# Figma API uses absolute positions, we want relative positions
def createRelativePosition(ParentPosition, ChildPosition):
    RelativePosition = [ChildPosition[0]-ParentPosition[0],ChildPosition[1]-ParentPosition[1]]
    return RelativePosition

# Function to create a new frame asset from the template file
def createFigmaFrameAsset(AssetPath):
        if unreal.EditorAssetLibrary.does_asset_exist(AssetPath):
            return unreal.EditorAssetLibrary.load_asset(AssetPath)
        else:
            FrameAsset = unreal.EditorAssetLibrary.duplicate_asset("/FigmaImporter/WBP_FigmaFrame",AssetPath)
            unreal.EditorAssetLibrary.save_loaded_asset(FrameAsset)
            return FrameAsset

# Function to run through all the children of a frame and create assets for them recursively
def createChildren(ChildrenDict, Document, Parent):
        Children = []
        # Create a progress bar
        TotalFrames = len(ChildrenDict)
        DialogLabel = "Creating Children for: " + Parent.Name
        with unreal.ScopedSlowTask(TotalFrames, DialogLabel) as slow_task:
            slow_task.make_dialog(True) #Show Progress bar             
            
            # Loop through all children and check the asset type        
            for child in ChildrenDict:
                if child["type"] == "FRAME":
                    ChildNode = FigmaFrame(Document,child, Parent)
                    ChildNode.writeToUnreal()
                    Children.append(ChildNode )
                elif child["type"] == "GROUP":
                    ChildNode = FigmaFrame(Document,child, Parent)
                    ChildNode.writeToUnreal()
                    Children.append(ChildNode )
                elif child["type"] == "COMPONENT_SET":
                    ChildNode = FigmaComponent(Document,child, Parent)
                    ChildNode.writeToUnreal()
                    Children.append(ChildNode )
                elif child["type"] == "COMPONENT":
                    ChildNode = FigmaComponent(Document,child, Parent)
                    ChildNode.writeToUnreal()
                    Children.append(ChildNode )
                elif child["type"] == "INSTANCE":
                    ChildNode = FigmaInstance(Document,child, Parent)
                    Document.ComponentInstances.append(ChildNode)
                    Children.append(ChildNode )
                elif child["type"] == "VECTOR":
                    ChildNode = FigmaVector(Document,child, Parent)
                    ChildNode.writeToUnreal()
                    Children.append(ChildNode )
                elif child["type"] == "LINE":
                    ChildNode = FigmaVector(Document,child, Parent)
                    ChildNode.writeToUnreal()
                    Children.append(ChildNode )
                elif child["type"] == "BOOLEAN_OPERATION":
                    ChildNode = FigmaVector(Document,child, Parent)
                    ChildNode.writeToUnreal()
                    Children.append(ChildNode )
                elif child["type"] == "ELLIPSE":
                    ChildNode = FigmaVector(Document,child, Parent)
                    ChildNode.writeToUnreal()
                    Children.append(ChildNode )
                elif child["type"] == "REGULAR_POLYGON":
                    ChildNode = FigmaVector(Document,child, Parent)
                    ChildNode.writeToUnreal()
                    Children.append(ChildNode )
                elif child["type"] == "STAR":
                    ChildNode = FigmaVector(Document,child, Parent)
                    ChildNode.writeToUnreal()
                    Children.append(ChildNode )
                elif child["type"] == "RECTANGLE":
                    ChildNode = FigmaVector(Document,child, Parent)
                    ChildNode.writeToUnreal()
                    Children.append(ChildNode )
                elif child["type"] == "TEXT": 
                    ChildNode = FigmaText(Document,child, Parent)
                    ChildNode.writeToUnreal()
                    Children.append(ChildNode ) 
                if slow_task.should_cancel():         # True if the user has pressed Cancel in the UI
                            break
                slow_task.enter_progress_frame(1)     # Advance progress by one frame.
        return Children

# Top level parent for a Figma document
class FigmaDocument():
    def __init__(self, FileID, BaseDirectory, AccessToken, Pages = [-1]):
        self.FileID = FileID
        self.BaseDirectory = BaseDirectory
        self.AccessToken = AccessToken
        self.Components = {}
        self.ComponentInstances = []
        self.Pages= Pages
        self.readFile()

    # Read in file from API    
    def readFile(self):
        FileResponse=requests.get("https://api.figma.com/v1/files/" + self.FileID, headers={"X-Figma-Token": self.AccessToken})
        self.File = json.loads(FileResponse.text)
        self.Name = sanitiseName(self.File["name"])
        self.Directory = self.BaseDirectory + self.Name +"/"
        self.Canvases = []
        for i, CanvasContent in enumerate(self.File["document"]["children"]):
            if i in self.Pages or self.Pages[0] == -1: 
                self.Canvases.append(FigmaCanvas(CanvasContent, self)) 
        
        

    # Produce assets from file in Unreal
    def writeToUnreal(self):
        createDirSafe(self.Directory)
        for Canvas in self.Canvases:
            createDirSafe(Canvas.Directory)
            AssetName = "WBP_" + Canvas.Name
            Canvas.FrameAsset = createFigmaFrameAsset(Canvas.Directory+AssetName) # Create new frame asset to use

            unreal.FigmaImporterBPLibrary.clear_content(Canvas.FrameAsset) # Clear any existing content from content tree (does not delete blueprint code but may break references)
            unreal.FigmaImporterBPLibrary.set_background(Canvas.FrameAsset, [10000,10000], [Canvas.BackgroundColor["r"],Canvas.BackgroundColor["g"],Canvas.BackgroundColor["b"],Canvas.BackgroundColor["a"]]) # Canvas Background set to arbitrary size of 10000x10000px
            Canvas.Children = createChildren(Canvas.ChildrenDict, self, Canvas) # Recursively creates child assets
            for Instance in self.ComponentInstances:
                Instance.writeToUnreal()
            saveAsset(Canvas.FrameAsset)

    # Add a component to the document that can be instanced
    def addComponent(self,Component):
        self.Components[Component.id] = Component


class FigmaCanvas():
    def __init__(self,CanvasContent, Document):
        self.Document = Document
        self.CanvasContent = CanvasContent
        self.Name = sanitiseName(self.CanvasContent["name"])
        try: # May not have a background colour
                    self.BackgroundColor = {
                                    "r" : self.CanvasContent["backgroundColor"]["r"],
                                    "g" : self.CanvasContent["backgroundColor"]["g"],
                                    "b" : self.CanvasContent["backgroundColor"]["b"],
                                    "a" : self.CanvasContent["backgroundColor"]["a"]
                                    }
        except KeyError:
                    self.BackgroundColor = {
                                    "r" : 0.5,
                                    "g" : 0.5,
                                    "b" : 0.5,
                                    "a" : 1
                                    }
        self.ChildrenDict = self.CanvasContent["children"]
        self.xPosition = 0
        self.yPosition = 0
        self.Directory = self.Document.Directory+self.Name+"/"

# Standard Figma frame holds children
class FigmaFrame():
    def __init__(self, Document, FrameDict, Parent):
        self.Document = Document
        self.Parent = Parent
        self.Name = sanitiseName(FrameDict["name"])
        self.Directory = self.Parent.Directory +  self.Name + "/"
        self.Height = FrameDict["absoluteBoundingBox"]["height"]
        self.Width = FrameDict["absoluteBoundingBox"]["width"]
        self.xPosition = FrameDict["absoluteBoundingBox"]["x"]
        self.yPosition = FrameDict["absoluteBoundingBox"]["y"]
        self.id = FrameDict["id"]
        if type(self.Parent) == FigmaCanvas: # Check if parent is the canvas and set anchors accordingly
            self.MinAnchors = [0.5,0.5]
            self.MaxAnchors = [0.5,0.5]
            self.Alignment = [0,0]
        else:
            self.MinAnchors = [0,0]
            self.MaxAnchors = [0,0]
            self.Alignment = [0,0] 

        self.ChildrenDict = FrameDict["children"]
        
        self.BackgroundColor = getColorFromFills(FrameDict["fills"],{
                                    "r" : 0,
                                    "g" : 0,
                                    "b" : 0,
                                    "a" : 0
                                    })
            
        
    # Produce assets from frame in Unreal and add to parent frame
    def writeToUnreal(self):
        
        createDirSafe(self.Directory)
        
        self.AssetName = "WBP_" + self.Name
        
        self.FrameAsset = createFigmaFrameAsset(self.Directory+"/"+ self.AssetName)

        unreal.FigmaImporterBPLibrary.clear_content(self.FrameAsset)
        unreal.FigmaImporterBPLibrary.set_background(self.FrameAsset, [self.Width,self.Height], [self.BackgroundColor["r"],self.BackgroundColor["g"],self.BackgroundColor["b"],self.BackgroundColor["a"]])
        self.Children = createChildren(self.ChildrenDict, self.Document, self)
        saveAsset(self.FrameAsset)
        unreal.FigmaImporterBPLibrary.add_child_widget(self.Parent.FrameAsset,getAssetPath(self.Directory, self.AssetName) , createInsatanceName(self.Name, self.id), [self.Width,self.Height], createRelativePosition([self.Parent.xPosition, self.Parent.yPosition], [self.xPosition, self.yPosition]), self.Alignment, self.MinAnchors, self.MaxAnchors)
        saveAsset(self.Parent.FrameAsset)

# Special frame class that can be instanced
class FigmaComponent(FigmaFrame):
    # Produce assets from frame in Unreal and add to parent frame
    def writeToUnreal(self):
        
        createDirSafe(self.Directory)
        
        self.AssetName = "WBP_" + self.Name
        
        self.FrameAsset = createFigmaFrameAsset(self.Directory+"/"+ self.AssetName)

        unreal.FigmaImporterBPLibrary.clear_content(self.FrameAsset)
        unreal.FigmaImporterBPLibrary.set_background(self.FrameAsset, [self.Width,self.Height], [self.BackgroundColor["r"],self.BackgroundColor["g"],self.BackgroundColor["b"],self.BackgroundColor["a"]])
        self.Children = createChildren(self.ChildrenDict, self.Document, self)
        saveAsset(self.FrameAsset)
        unreal.FigmaImporterBPLibrary.add_child_widget(self.Parent.FrameAsset,getAssetPath(self.Directory, self.AssetName) , createInsatanceName(self.Name, self.id), [self.Width,self.Height], createRelativePosition([self.Parent.xPosition, self.Parent.yPosition], [self.xPosition, self.yPosition]), self.Alignment, self.MinAnchors, self.MaxAnchors)
        saveAsset(self.Parent.FrameAsset)
        self.Document.addComponent(self)

# An instance that references an existing component
class FigmaInstance():
    def __init__(self, Document, FrameDict, Parent):
        self.Document = Document
        self.Parent = Parent
        self.Name = sanitiseName(FrameDict["name"])
        self.Directory = self.Parent.Directory +  self.Name + "/"
        self.Height = FrameDict["absoluteBoundingBox"]["height"]
        self.Width = FrameDict["absoluteBoundingBox"]["width"]
        self.xPosition = FrameDict["absoluteBoundingBox"]["x"]
        self.yPosition = FrameDict["absoluteBoundingBox"]["y"]
        self.id = FrameDict["id"]
        self.ComponentID = FrameDict["componentId"]
        if type(self.Parent) == FigmaCanvas: # Check if parent is the canvas and set anchors accordingly
            self.MinAnchors = [0.5,0.5]
            self.MaxAnchors = [0.5,0.5]
            self.Alignment = [0,0]
        else:
            self.MinAnchors = [0,0]
            self.MaxAnchors = [0,0]
            self.Alignment = [0,0] 

        self.ChildrenDict = FrameDict["children"]
        
        self.BackgroundColor = getColorFromFills(FrameDict["fills"],{
                                    "r" : 0,
                                    "g" : 0,
                                    "b" : 0,
                                    "a" : 0
                                    })
            
        
    # Produce assets from frame in Unreal and add to parent frame
    def writeToUnreal(self):
        try: # Try finding source component in document
            InstanceSource = self.Document.Components[self.ComponentID]
            InstanceSourceDirectory = InstanceSource.Directory
            InstanceSourceAssetName = InstanceSource.AssetName
            unreal.FigmaImporterBPLibrary.add_child_widget(self.Parent.FrameAsset,getAssetPath(InstanceSourceDirectory, InstanceSourceAssetName) , createInsatanceName(self.Name, self.id), [self.Width,self.Height], createRelativePosition([self.Parent.xPosition, self.Parent.yPosition], [self.xPosition, self.yPosition]), self.Alignment, self.MinAnchors, self.MaxAnchors)
            saveAsset(self.Parent.FrameAsset)
        except KeyError:
            print("Unable to find source component")

# A vector is the base class for all shapes and images in Figma
class FigmaVector():
    def __init__(self, Document, VectorDict, Parent):
        self.Document = Document
        self.Name = sanitiseName(VectorDict["name"])
        self.Height = VectorDict["absoluteBoundingBox"]["height"]
        self.Width = VectorDict["absoluteBoundingBox"]["width"]
        self.xPosition = VectorDict["absoluteBoundingBox"]["x"]
        self.yPosition = VectorDict["absoluteBoundingBox"]["y"]
        self.id = VectorDict["id"]
        self.MinAnchors = [0,0]
        self.MaxAnchors = [0,0]
        self.Alignment = [0,0]
        self.Parent = Parent

    # Uses Figma API to download a bitmap image representation of the vector (Special vectors like rectangles should use native Unreal assets where possible but not implemented yet)
    def downloadImage(self):
        FileResponse=requests.get("https://api.figma.com/v1/images/" + self.Document.FileID + "?ids=" + self.id, headers={"X-Figma-Token": self.Document.AccessToken})
        File = json.loads(FileResponse.text)
        ImageURL = File["images"][self.id]
        ImageData = requests.get(ImageURL).content
        
        self.RawImageDirectory = unreal.Paths.project_dir() + "RawAssets" + self.Parent.Directory
        if not os.path.exists(self.RawImageDirectory):
            os.makedirs(self.RawImageDirectory)
        self.ImageName = "T_" + self.Name
        self.RawImageName = self.ImageName + ".png"
        self.RawImagePath = self.RawImageDirectory + self.RawImageName
        self.ImageDirectory = self.Parent.Directory +"Images/"
        createDirSafe(self.ImageDirectory)
        self.ImagePath = os.path.splitext(self.ImageDirectory + self.RawImageName)[0]
        with open(self.RawImagePath, 'wb') as handler:
            handler.write(ImageData)

    # Produce assets and add to parent frame
    def writeToUnreal(self):
        self.downloadImage()
        AssetTools = unreal.AssetToolsHelpers.get_asset_tools()
        AssetImportTask = unreal.AssetImportTask()
        AssetImportTask.set_editor_property('filename', self.RawImagePath)
        AssetImportTask.set_editor_property('destination_path', self.ImageDirectory)
        AssetImportTask.set_editor_property('replace_existing', True)
        AssetImportTask.set_editor_property('replace_existing_settings', True)
        AssetImportTask.set_editor_property('save', True)
        AssetTools.import_asset_tasks([AssetImportTask])
        ImageTexture2D = unreal.EditorAssetLibrary.load_asset(self.ImagePath)
        self.Widget = unreal.FigmaImporterBPLibrary.add_image_widget(self.Parent.FrameAsset,
                                                                     createInsatanceName(self.Name, self.id),
                                                                     [ImageTexture2D.blueprint_get_size_x(),ImageTexture2D.blueprint_get_size_y()], # Use the image size rather than stated size to enable LINE to work which reports 0 width
                                                                     createRelativePosition([self.Parent.xPosition, self.Parent.yPosition],
                                                                     [self.xPosition, self.yPosition]),
                                                                    self.ImagePath, self.Alignment, self.MinAnchors, self.MaxAnchors)
        saveAsset(self.Parent.FrameAsset)

# Text class (need to add better font support, currently uses default Inter font)
class FigmaText():
    def __init__(self, Document, TextDict, Parent):
        self.Document = Document
        self.Name = sanitiseName(TextDict["name"])
        self.Height = TextDict["absoluteBoundingBox"]["height"]
        self.Width = TextDict["absoluteBoundingBox"]["width"]
        self.xPosition = TextDict["absoluteBoundingBox"]["x"]
        self.yPosition = TextDict["absoluteBoundingBox"]["y"]
        self.id = TextDict["id"]
        self.Parent = Parent
        self.Content = TextDict["characters"]
        self.FontSize = TextDict["style"]["fontSize"]
        self.FontColor = getColorFromFills(TextDict["fills"],{
                                "r" : 0,
                                "g" : 0,
                                "b" : 0,
                                "a" : 1,
                             })

        self.FontFamily = TextDict["style"]["fontFamily"]
        self.MinAnchors = [0,0]
        self.MaxAnchors = [0,0]
        self.Alignment = [0,0]


    # Adds text to parent frame
    def writeToUnreal(self):
        Font = unreal.SlateFontInfo()
        Font.set_editor_property('size', self.FontSize)
        Font.set_editor_property('FontObject',unreal.EditorAssetLibrary.load_asset("/FigmaImporter/Inter-VariableFont_slnt_wght_Font")) # Uses default Inter font from plugin
        Font.set_editor_property('TypefaceFontName', "Inter-VariableFont_slnt_wght")
        self.Widget = unreal.FigmaImporterBPLibrary.add_text_widget(self.Parent.FrameAsset, createInsatanceName(self.Name, self.id), self.Content, Font, [self.Width,self.Height], createRelativePosition([self.Parent.xPosition, self.Parent.yPosition], [self.xPosition, self.yPosition]), self.Alignment, self.MinAnchors, self.MaxAnchors)
        self.Widget.set_editor_property('color_and_opacity', unreal.SlateColor([self.FontColor["r"],self.FontColor["g"],self.FontColor["b"],self.FontColor["a"]]))
        saveAsset(self.Parent.FrameAsset)