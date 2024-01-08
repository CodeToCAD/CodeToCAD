import pcbnew
import ctypes
import itertools


# Place text
def place_text(board, text="CodeToCAD"):
    t = pcbnew.PCB_TEXT(board)
    t.SetText(text)
    t.SetPosition(pcbnew.VECTOR2I(pcbnew.wxPointMM(10.0, 10.0)))
    t.SetHorizJustify(pcbnew.GR_TEXT_H_ALIGN_CENTER)
    t.SetTextSize(pcbnew.VECTOR2I(pcbnew.wxSizeMM(10.0, 10.0)))
    t.SetLayer(pcbnew.F_SilkS)
    board.Add(t)
    pcbnew.Refresh()
    return t


def set_position(item, x=0.0, y=0.0):
    item.SetPosition(pcbnew.VECTOR2I(pcbnew.wxPointMM(x, y)))
    pcbnew.Refresh()


def rotate_footprint_90(item):
    # todo get footprint point
    item.Rotate(item.GetCenter(), pcbnew.ANGLE_90)
    pcbnew.Refresh()


def create_track(board, start, end, width=0.8, layer=pcbnew.F_Cu):
    track = pcbnew.PCB_TRACK(board)
    track.SetStart(pcbnew.VECTOR2I_MM(0.0, 0.0))
    track.SetEnd(pcbnew.VECTOR2I_MM(100.0, 100.0))
    track.SetWidth(int(width * pcbnew.EDA_UNITS_INCHES))
    track.SetLayer(layer)
    net = pcbnew.NETINFO_ITEM(board, "NET NAME")
    track.SetNetCode(net.GetNetCode())
    board.Add(track)
    pcbnew.Refresh()


def add_circle_edge_cut(board, item=item):
    centerpoint = item.GetCenter()
    circle = pcbnew.PCB_SHAPE(board)
    circle.SetShape(pcbnew.SHAPE_T_CIRCLE)
    circle.SetFilled(False)
    circle.SetStart(centerpoint)
    cx = centerpoint[0]
    cy = centerpoint[1]
    circle.SetEnd(pcbnew.VECTOR2I(pcbnew.wxPointMM(cx / 10e9 + 100, cy / 10e9)))
    circle.SetCenter(centerpoint)
    circle.SetLayer(pcbnew.Edge_Cuts)
    circle.SetWidth(int(0.1 * pcbnew.EDA_UNITS_INCHES))
    board.Add(circle)
    pcbnew.Refresh()


# Below here is just experimentation

# Place a footprint
# pcbnew.GetFootprintLibraries()
# footprint = pcbnew.FOOTPRINT(board)
# module = pcbnew.FootprintLoad("your_footprint.pretty", "your_footprint_name")
# module.SetPosition(pcbnew.wxPointMM(10.0, 10.0))  # Example position: (1mm, 1mm)
# board.Add(module)
# pcbnew.Refresh()

# libname = 'Connector_PinHeader_2.54mm'
# # Perform check
# pcbnew.FOOTPRINT_IsLibNameValid(libname)
# fps = pcbnew.GetFootprints(libname)
# sub = "1x05"
# [f for f in fps if sub in f][1]


# Utility function for printing meaningful stuff from C++ classes like Vector, etc
def swig_to_str(s):
    base = int(s)
    ty = ctypes.c_ubyte * 1

    def impl():
        for x in itertools.count():
            v = ty.from_address(base + x)[0]
            if not v:
                return
            yield chr(v)

    return "".join(impl())


if __name__ == "__main__":
    print(pcbnew.GetBuildVersion())
    board = pcbnew.GetBoard()
    # drawings = pcbnew.GetDrawings()
    libs = pcbnew.GetFootprintLibraries()
    dev_search_paths = pcbnew.GetWizardsSearchPaths().split("\n")
    pcb_text = place_text("COOL")
    set_position(pcb_text, 130.0, 130.0)
