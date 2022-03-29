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

  shape(name).primitive(source, dimensions) \
    .rotate("0,90d,0")

  landmarks = feature["landmarks"]
  landmarks_split = [landmark.split(",") for landmark in landmarks]

  for landmark in landmarks_split:
    shape(name).landmark(landmark[0], landmark[1:])
# scene().setDefaultUnit(BlenderLength.INCHES)

# sprocket = {
#   "source": str(Path(__file__).parent.absolute()) + "/testFiles/6280K267_Roller Chain Sprocket.stl"
#   }
features = {
  "Half Axle rod": {
    "source": "cylinder",
    "dimensions": "3/8,21, in",
    "landmarks": [
        "teethBegin,min+1,center,center,in",
        "teethEnd,min+2.5,center,center,in",
        "bearingEnd, min+7,center,center,in",
        "breakDiscStart,min+11,center,center,in",
        "breakDiscEnd,min+15,center,center,in"
    ]
  },
  # "Axle teeth": {
  #   # "source": "teeth",
  #   "source": "cylinder",
  #   "dimensions": "1,1.5,in",
  #   "landmarks": ["left,min,center,center,in"],
  # },
  # "bearing rod": {
  #   "source": "cylinder",
  #   "dimensions": "1.15,4.5,in",
  #   "landmarks": ["left,min,center,center,in"]
  # },
  # "breakdisc rod": {
  #   "source": "cylinder",
  #   "dimensions": "1.35,14,in",
  #   "landmarks": ["left,min,center,center,in"],
  # },
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
}

for feature in features:
  createFeature(feature, features[feature])

joints = {
  
  "Half Axle rod with teeth": {
    "source": "union (half axle rod, axle teeth)",
    "dimensions": "21,3/8,3/8, in",
  },
  "Half Axle rod with teeth and bearing rod": {
    "source": "union (Half Axle rod with teeth, bearing rod)",
    "dimensions": "21,3/8,3/8, in",
  },
  "Half Axle rod with teeth and bearing rod and breakdisc rod": {
    "source": "union (Half Axle rod with teeth and bearing rod, breakdisc rod)",
    "dimensions": "21,3/8,3/8, in",
    "landmarks": ["teethBegin,1,center,center,in",
    "teethEnd,2.5,center,center,in",
    "bearingEnd, 7,center,center,in",
    "breakDiscStart,11,center,center,in",
    "breakDiscEnd,15,center,center,in"
    ]
  },
  "Axle rod": {
    "source": "mirror (Half Axle rod with teeth and bearing rod and breakdisc rod)",
    "landmarks": ["mirrored",
    "mirrored",
    "mirrored",
    "mirrored",
    "mirrored"]
  },

}

# shape("sprocket").fromFile(sprocket["source"]).scale(",3in,")

# shape("Half Axle rod").primitive("cylinder", features["Half Axle rod"]["dimensions"]).landmark("top", "center,center,max").rotate(["10d","20d",0])
# shape("Half Axle rod2").primitive("cylinder", features["Half Axle rod"]["dimensions"]).landmark("bottom", "center,center,min").translate([0,0,30])

# joint("Half Axle rod2", "Half Axle rod", "bottom", "top").transformLandmarkOntoAnother()
# shape("Axle teeth").primitive("cube", features["Axle teeth"]["dimensions"])
# shape("bearing rod").primitive("cube", features["bearing rod"]["dimensions"])
# shape("breakdisc rod").primitive("cube", features["breakdisc rod"]["dimensions"])
# shape("Half Axle rod with teeth").primitive("cube", features["Half Axle rod with teeth"]["dimensions"])
# shape("Half Axle rod with teeth and bearing rod").primitive("cube", features["Half Axle rod with teeth and bearing rod"]["dimensions"])
# shape("Half Axle rod with teeth and bearing rod and breakdisc rod").primitive("cube", features["Half Axle rod with teeth and bearing rod and breakdisc rod"]["dimensions"])
# shape("Axle rod")
# shape("breakdisc core").primitive("cube", features["breakdisc core"]["dimensions"])
# shape("breakdisc mount core").primitive("cube", features["breakdisc mount core"]["dimensions"])
# shape("breakdisc mount hole").primitive("cube", features["breakdisc mount hole"]["dimensions"])
# shape("breakdisc mount holes")
# shape("breakdisc mount")
# shape("breakdisc left")
# shape("breakdisc right")