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
    "dimensions": "3/8,1,in",
    "initialRotation": "0,90d,0",
    "landmarks": ["left,min,center,center", "right,max,center,center"]
  },
  "hubTeeth": {
    # "source": "teeth",
    "source": "cylinder",
    "dimensions": "1,1.5,in",
    "initialRotation": "0,90d,0",
    "landmarks": ["left,min,center,center", "right,max,center,center"]
  },
  "bearing": {
    "source": "cylinder",
    "dimensions": "1.15,4.5,in",
    "initialRotation": "0,90d,0",
    "landmarks": ["left,min,center,center", "right,max,center,center"]
  },
  "breakdisc": {
    "source": "cylinder",
    "dimensions": "1.35,14,in",
    "initialRotation": "0,90d,0",
    "landmarks": ["left,min,center,center", "right,max,center,center"]
  }
}

scene().deleteGroup("Axle Parts", removeNestedShapes=True)
scene().createGroup("Axle Parts")

previousPart = None
for axleRodPart in axleRodParts:
  
  createFeature(axleRodPart, axleRodParts[axleRodPart])

  scene().assignShapeToGroup(axleRodPart, "Axle Parts")
  
  if previousPart != None:
    joint(previousPart, axleRodPart, "right", "left").transformLandmarkOntoAnother()
  
  previousPart = axleRodPart

shape("axleRod").cloneShape("")


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