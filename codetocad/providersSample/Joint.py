# THIS IS AN AUTO-GENERATE FILE. 
# DO NOT EDIT MANUALLY.
# Please run development/capabilitiesJsonToPython/capabilitiesToPy.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from typing import Optional

from CodeToCAD.interfaces import JointInterface
from CodeToCAD.CodeToCADTypes import *
from CodeToCAD.utilities import *


class Joint(JointInterface): 
    
    
    entity1:EntityOrItsNameOrLandmark
    entity2:EntityOrItsNameOrLandmark

    def __init__(self, entity1:EntityOrItsNameOrLandmark, entity2:EntityOrItsNameOrLandmark):
        self.entity1 = entity1
        self.entity2 = entity2

    def translateLandmarkOntoAnother(self):
        
        return self
        

    def pivot(self):
        
        return self
        

    def gearRatio(self, ratio:float):
        
        return self
        

    def limitLocationXYZ(self, x:Optional[DimensionOrItsFloatOrStringValue]=None, y:Optional[DimensionOrItsFloatOrStringValue]=None, z:Optional[DimensionOrItsFloatOrStringValue]=None):
        
        return self
        

    def limitLocationX(self, min:Optional[DimensionOrItsFloatOrStringValue]=None, max:Optional[DimensionOrItsFloatOrStringValue]=None):
        
        return self
        

    def limitLocationY(self, min:Optional[DimensionOrItsFloatOrStringValue]=None, max:Optional[DimensionOrItsFloatOrStringValue]=None):
        
        return self
        

    def limitLocationZ(self, min:Optional[DimensionOrItsFloatOrStringValue]=None, max:Optional[DimensionOrItsFloatOrStringValue]=None):
        
        return self
        

    def limitRotationXYZ(self, x:Optional[AngleOrItsFloatOrStringValue]=None, y:Optional[AngleOrItsFloatOrStringValue]=None, z:Optional[AngleOrItsFloatOrStringValue]=None):
        
        return self
        

    def limitRotationX(self, min:Optional[AngleOrItsFloatOrStringValue]=None, max:Optional[AngleOrItsFloatOrStringValue]=None):
        
        return self
        

    def limitRotationY(self, min:Optional[AngleOrItsFloatOrStringValue]=None, max:Optional[AngleOrItsFloatOrStringValue]=None):
        
        return self
        

    def limitRotationZ(self, min:Optional[AngleOrItsFloatOrStringValue]=None, max:Optional[AngleOrItsFloatOrStringValue]=None):
        
        return self
        
    