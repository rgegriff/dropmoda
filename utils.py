import xpybutil
import xpybutil.event as event
import xpybutil.ewmh as ewmh
import xpybutil.motif as motif
import xpybutil.util as util
import xpybutil.window as window
import xpybutil.ewmh as ewmh

def try_get_wid_by_pid(pid):
    wids = ewmh.get_client_list().reply()
    found = []
    for wid in wids:
        window_pid = ewmh.get_wm_pid(wid).reply()
        if window_pid == pid:
            found.append(wid)
    return found

def get_active_window():
    wid = ewmh.get_active_window().reply()
    if wid not in [0, None]:
        win = Window(wid)
    else:
        win = None
    return win

class Window():
    def __init__(self, wid):
        if type(wid) == int:
            self.id = wid
        elif type(wid) == str:
            self.id = int(wid, 16)
        self.refresh()

    def refresh(self):
        properties = {
            "name": ("_NET_WM_NAME", "str"),
            "pid": ("_NET_WM_PID", "int[]"),
            "type": ("_NET_WM_WINDOW_TYPE", "atoms[]"),
            "wm_class": ("WM_CLASS", "str[]"),
            "desktop": ("_NET_WM_DESKTOP", "int")
        }
        for k, v in properties.items():
            try:
                response = util.PropertyCookie(util.get_property(self.id, v[0])).reply()
                if v[1] == "atoms[]":
                    response = list(map(util.get_atom_name, response))
                setattr(self, k, response)
            except Exception as e: 
                print(k,v,e)

    @property
    def id_hex(self):
        return hex(self.id)

    def __str__(self):
        return f"{'.'.join(self.wm_class):<20} {self.name}"
