import adsk.core, adsk.fusion, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        design = app.activeProduct

        # Get the root component of the active design.
        rootComp = design.rootComponent

        # Create a new sketch on the xy plane.
        sketches = rootComp.sketches
        xyPlane = rootComp.xYConstructionPlane
        sketch = sketches.add(xyPlane)

        # Draw two point rectangle.
        lines = sketch.sketchCurves.sketchLines
        lineList = lines.addTwoPointRectangle(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(5, 5, 0))

        # Add a distance distance chamfer.
        line = sketch.sketchCurves.sketchLines.addDistanceChamfer(lineList[0], lineList[0].endSketchPoint.geometry, lineList[1], lineList[1].startSketchPoint.geometry, 1,1)

        # Add a distance angle chamfer.
        line = sketch.sketchCurves.sketchLines.addAngleChamfer(lineList[1], lineList[1].endSketchPoint.geometry, lineList[2], lineList[2].startSketchPoint.geometry, 1,1)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def stop(context):
    ...
