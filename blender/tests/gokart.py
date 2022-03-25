import sys
from pathlib import Path
scriptDir = Path(__file__).parent.parent.absolute()
if scriptDir not in sys.path:
    sys.path.insert(0, str(scriptDir))


import bpy
from textToBlender import shape, scene, BlenderLength, joint

# scene().setDefaultUnit(BlenderLength.INCHES)

sprocket = {
  "source": str(Path(__file__).parent.absolute()) + "/testFiles/6280K267_Roller Chain Sprocket.stl"
  }
features = {
  "Half Axle rod": {
    "Source": "cylinder",
    "dimensions": "3/8,21, in",
    "landmarks": [
        "teethBegin,1,center,center,in",
        "teethEnd,2.5,center,center,in",
        "bearingEnd, 7,center,center,in",
        "breakDiscStart,11,center,center,in",
        "breakDiscEnd,15,center,center,in"
    ]
  },
  "Axle teeth": {
    "Source": "teeth",
    "dimensions": "1.5,1,1,in",
    "landmarks": ["left,min,center,center,in"],
  },
  "bearing rod": {
    "Source": "cylinder",
    "dimensions": "4.5,1.15,1.15,in",
    "landmarks": ["left,min,center,center,in"]
  },
  "breakdisc rod": {
    "Source": "cylinder",
    "dimensions": "14,1.35,1.35,in",
    "landmarks": ["left,min,center,center,in"],
  },
  "Half Axle rod with teeth": {
    "Source": "union (half axle rod, axle teeth)",
    "dimensions": "21,3/8,3/8, in",
  },
  "Half Axle rod with teeth and bearing rod": {
    "Source": "union (Half Axle rod with teeth, bearing rod)",
    "dimensions": "21,3/8,3/8, in",
  },
  "Half Axle rod with teeth and bearing rod and breakdisc rod": {
    "Source": "union (Half Axle rod with teeth and bearing rod, breakdisc rod)",
    "dimensions": "21,3/8,3/8, in",
    "landmarks": ["teethBegin,1,center,center,in",
    "teethEnd,2.5,center,center,in",
    "bearingEnd, 7,center,center,in",
    "breakDiscStart,11,center,center,in",
    "breakDiscEnd,15,center,center,in"
    ]
  },
  "Axle rod": {
    "Source": "mirror (Half Axle rod with teeth and bearing rod and breakdisc rod)",
    "landmarks": ["mirrored",
    "mirrored",
    "mirrored",
    "mirrored",
    "mirrored"]
  },
  "breakdisc core": {
    "Source": "cylinder",
    "dimensions": "1,29/32,29/32, in",
    "landmarks": ["breakHolesBegin, 0.5,center,center"],
  },
  "breakdisc mount core": {
    "Source": "cylinder",
    "dimensions": "0.5,2.9/32,2.9/32,",
    "landmarks": ["top,center,max,center"],
  },
  "breakdisc mount hole": {
    "Source": "cube",
    "dimensions": "0.5,0.9,0.9",
    "landmarks": ["bottomcenter,min,center",
    "screwHole,center,11mm,center"],
  },
  "breakdisc mount holes": {
    "Source": "circle pattern (breakdisc mount hole, radius: 2.9/32, instances:4)",
  },
  "breakdisc mount": {
    "Source": "union(breakdisc mount holes, breakdisc mount core)",
  },
  "breakdisc left": {
    "Source": "union(breakdisc core, breakdisc mount)"
  },
  "breakdisc right": {
    "Source": "mirror (breakdisc left)",
  }
}

# shape("sprocket").fromFile(sprocket["source"]).scale(",3in,")

shape("Half Axle rod").primitive("cylinder", features["Half Axle rod"]["dimensions"]).landmark("top", "center,center,max").rotate(["10d","20d",0])
shape("Half Axle rod2").primitive("cylinder", features["Half Axle rod"]["dimensions"]).landmark("bottom", "center,center,min").translate([0,0,30])

joint("Half Axle rod2", "Half Axle rod", "bottom", "top").transformLandmarkOntoAnother()
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