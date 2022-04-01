import sys
from pathlib import Path
scriptDir = Path(__file__).parent.parent.absolute()
if scriptDir not in sys.path:
    sys.path.insert(0, str(scriptDir))


import bpy
from textToBlender import shape, scene, BlenderLength, joint

def createFeature(name, feature):
  source = feature["source"]  
  dimensions = feature["dimensions"]
  initialRotation = feature["initialRotation"]

  shape(name).primitive(source, dimensions)
  
  if initialRotation:
    shape(name).rotate(initialRotation)

  landmarks = feature["landmarks"]
  landmarks_split = [landmark.split(",") for landmark in landmarks]

  for landmark in landmarks_split:
    shape(name).landmark(landmark[0], landmark[1:])
    
scene().setDefaultUnit(BlenderLength.INCHES)

axleRodParts = {
  "cap": {
    "source": "cylinder",
    "dimensions": "3/8/2,1,in",
    "initialRotation": "0,90d,0",
    "landmarks": ["left,min,center,center", "right,max,center,center"]
  },
  "hubTeeth": {
    # "source": "teeth",
    "source": "cylinder",
    "dimensions": "1/2,1.5,in",
    "initialRotation": "0,90d,0",
    "landmarks": ["left,min,center,center", "right,max,center,center"]
  },
  "bearing": {
    "source": "cylinder",
    "dimensions": "1.15/2,4.5,in",
    "initialRotation": "0,90d,0",
    "landmarks": ["left,min,center,center", "right,max,center,center"]
  },
  "breakdisc": {
    "source": "cylinder",
    "dimensions": "1.35/2,12,in",
    "initialRotation": "0,90d,0",
    "landmarks": ["left,min,center,center", "right,max,center,center"]
  }
}

def createAxleParts():
  scene().deleteGroup("Axle Parts", removeNestedShapes=True)
  scene().createGroup("Axle Parts")

  previousPart = None
  for axleRodPart in axleRodParts:
    
    createFeature(axleRodPart, axleRodParts[axleRodPart])

    scene().assignShapeToGroup(axleRodPart, "Axle Parts")
    
    if previousPart != None:
      joint(previousPart, axleRodPart, "right", "left").transformLandmarkOntoAnother()
      shape("axleRod").union(axleRodPart)

    if previousPart == None:
      shape("axleRod").cloneShape(axleRodPart)
    
    previousPart = axleRodPart

# createAxleParts()
# shape("axleRod").landmark("left", "min,center,center")
# shape("axleRod").landmark("right", "max,center,center")
# shape("axleRod").mirror("axleRod_right", (True, False, False))


engineFrameParts = {
  "horizontalPole": {
    "source": "cylinder",
    "dimensions": "1.25/2,21.5,in",
    "initialRotation": "0d,90d,0",
    "landmarks": ["left,min,center,center", "right,max,center,center", "minirod_left,min+12.5,center,center,in",  "minirod_right,min-2.5,center,center,in"]
  },
  "verticalPole": {
    "source": "cube",
    "dimensions": "1.5,22.5,1.25,in",
    "initialRotation": "0,90d,0",
    "landmarks": ["hook,min,min+1,max,in", "horizontalPole,max,min + 19,center, in"]
  },
  # "miniPoleLeft": {
  #   "source": "cylinder",
  #   "dimensions": "3/16,12,in",
  #   "initialRotation": "90d,0,0",
  #   "landmarks": ["top,center,max,center", "bottom,center,min,center"]
  # },
  # "miniPoleRight": {
  #   "source": "cylinder",
  #   "dimensions": "3/16,12,in",
  #   "initialRotation": "90d,0,0",
  #   "landmarks": ["top,center,max,center", "bottom,center,min,center"]
  # },
  # "miniPoleHorizontal": {
  #   "source": "cylinder",
  #   "dimensions": "3/16,12,in",
  #   "initialRotation": "0,90d,0",
  #   "landmarks": ["left,min,center,center", "right,max,center,center"]
  # },
  "verticalPoleHook": {
    "source": "cube",
    "dimensions": "1/4,4.35,5,in",
    "initialRotation": "0,0d,0",
    "landmarks": ["bearing,max,min+2.2,max-3.1,in", "top, max, min, max"]
  }
}
def createEngineFrameParts():
  scene().deleteGroup("Engine Frame Parts", removeNestedShapes=True)
  scene().createGroup("Engine Frame Parts")

  for engineFramePart in engineFrameParts:
    
    createFeature(engineFramePart, engineFrameParts[engineFramePart])

    scene().assignShapeToGroup(engineFramePart, "Engine Frame Parts")

createEngineFrameParts()

joint("bearing", "verticalPoleHook", "right", "bearing").transformLandmarkOntoAnother()
joint("verticalPoleHook", "verticalPole", "top", "hook").transformLandmarkOntoAnother()
joint("verticalPole", "horizontalPole", "horizontalPole", "left").transformLandmarkOntoAnother()

shape("verticalPoleHook").mirror("axleRod_right", (True, False, False))
shape("verticalPole").mirror("axleRod_right", (True, False, False))


  # "breakdisc core": {
  #   "source": "cylinder",
  #   "dimensions": "29/32,1,in",
  #   "landmarks": ["breakHolesBegin, 0.5in,center,center"],
  # },
  # "breakdisc mount core": {
  #   "source": "cylinder",
  #   "dimensions": "2.9/32,0.5,in",
  #   "landmarks": ["top,center,max,center"],
  # },
  # "breakdisc mount hole": {
  #   "source": "cube",
  #   "dimensions": "0.9,0.5,0.5,in",
  #   "landmarks": ["bottomcenter,min,center,center",
  #   "screwHole,center,11mm,center"],
  # },



  # "breakdisc mount holes": {
  #   "source": "circle pattern (breakdisc mount hole, radius: 2.9/32, instances:4)",
  # },
  # "breakdisc mount": {
  #   "source": "union(breakdisc mount holes, breakdisc mount core)",
  # },
  # "breakdisc left": {
  #   "source": "union(breakdisc core, breakdisc mount)"
  # },
  # "breakdisc right": {
  #   "source": "mirror (breakdisc left)",
  # }
# }

# for feature in features:
#   createFeature(feature, features[feature])

# sprocket = {
#   "source": str(Path(__file__).parent.absolute()) + "/testFiles/6280K267_Roller Chain Sprocket.stl"
#   }
# shape("sprocket").fromFile(sprocket["source"]).scale(",3in,")