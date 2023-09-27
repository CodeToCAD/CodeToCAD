
# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilitiesJsonToPython/capabilitiesToPy.sh to generate this file.

from abc import ABCMeta, abstractmethod
from CodeToCAD.CodeToCADTypes import *


class JointInterface(metaclass=ABCMeta):
    '''Joints define the relationships and constraints between entities.'''

    
    entity1:EntityOrItsNameOrLandmark
    entity2:EntityOrItsNameOrLandmark

    @abstractmethod
    def __init__(self, entity1:EntityOrItsNameOrLandmark, entity2:EntityOrItsNameOrLandmark):
        self.entity1 = entity1
        self.entity2 = entity2

    @abstractmethod
    def translateLandmarkOntoAnother(self):
        '''
        Transforms one landmark onto another
        '''
        
        print("translateLandmarkOntoAnother is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def pivot(self):
        '''
        Constraint the rotation origin of entity B to entity A's landmark.
        '''
        
        print("pivot is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def gearRatio(self, ratio:float):
        '''
        Constraint the rotation of entity B to be a percentage of entity A's
        '''
        
        print("gearRatio is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def limitLocationXYZ(self, x:Optional[DimensionOrItsFloatOrStringValue]=None, y:Optional[DimensionOrItsFloatOrStringValue]=None, z:Optional[DimensionOrItsFloatOrStringValue]=None):
        '''
        Constraint the translation of entity B, relative to entity A's landmark.
        '''
        
        print("limitLocationXYZ is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def limitLocationX(self, min:Optional[DimensionOrItsFloatOrStringValue]=None, max:Optional[DimensionOrItsFloatOrStringValue]=None):
        '''
        Constraint the translation of entity B, relative to entity A's landmark.
        '''
        
        print("limitLocationX is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def limitLocationY(self, min:Optional[DimensionOrItsFloatOrStringValue]=None, max:Optional[DimensionOrItsFloatOrStringValue]=None):
        '''
        Constraint the translation of entity B, relative to entity A's landmark.
        '''
        
        print("limitLocationY is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def limitLocationZ(self, min:Optional[DimensionOrItsFloatOrStringValue]=None, max:Optional[DimensionOrItsFloatOrStringValue]=None):
        '''
        Constraint the translation of entity B, relative to entity A's landmark.
        '''
        
        print("limitLocationZ is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def limitRotationXYZ(self, x:Optional[AngleOrItsFloatOrStringValue]=None, y:Optional[AngleOrItsFloatOrStringValue]=None, z:Optional[AngleOrItsFloatOrStringValue]=None):
        '''
        Constraint the rotation of entity B, relative to entity A's landmark.
        '''
        
        print("limitRotationXYZ is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def limitRotationX(self, min:Optional[AngleOrItsFloatOrStringValue]=None, max:Optional[AngleOrItsFloatOrStringValue]=None):
        '''
        Constraint the rotation of entity B, relative to entity A's landmark.
        '''
        
        print("limitRotationX is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def limitRotationY(self, min:Optional[AngleOrItsFloatOrStringValue]=None, max:Optional[AngleOrItsFloatOrStringValue]=None):
        '''
        Constraint the rotation of entity B, relative to entity A's landmark.
        '''
        
        print("limitRotationY is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def limitRotationZ(self, min:Optional[AngleOrItsFloatOrStringValue]=None, max:Optional[AngleOrItsFloatOrStringValue]=None):
        '''
        Constraint the rotation of entity B, relative to entity A's landmark.
        '''
        
        print("limitRotationZ is called in an abstract method. Please override this method.")
        return self
        