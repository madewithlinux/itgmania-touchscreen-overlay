import re
import subprocess
from tkinter import *


def get_itgmania_position():
    out = subprocess.check_output(
        ["xdotool", "search", "--name", "Simply Love", "getwindowgeometry"]
    ).decode("ascii", "ignore")
    m = re.search("\s*Position: (\d+),(\d+)", out)
    if not m:
        return (0,0) # default to top-left corner of screen
    return (
        int(m.group(1)),
        int(m.group(2))
    )


def ensure_itgmania_active():
    subprocess.check_output(
        ["xdotool", "search", "--name", "Simply Love", "windowactivate"]
    )


def send_key_to_itgmania(key: str):
    ensure_itgmania_active()
    subprocess.check_output(
        ["xdotool", "search", "--name", "Simply Love", "key", "--window", "%1", key]
    )

itgmania_status_bar_height = 71

root = Tk()
root.title("overlay")

# x = "0"
# y = "0"
print(f"{get_itgmania_position()=}")

# TODO: this doesn't work quite right due to the window decoration
# x, y = get_itgmania_position()

# hardcoded offset for desktop development
x = 6
y = 93

root.geometry(f"=250x150+{x}+{y}")
# screen_width = root.winfo_screenwidth()
# screen_height = root.winfo_screenheight()
# print(f"{screen_width=}")
# print(f"{screen_height=}")

# to remove the titlebar
root.overrideredirect(True)

# to make the window transparent
# root.attributes("-transparentcolor","red")

# set bg to red in order to make it transparent
root.config(bg="red")

l = Label(root, text="HI this is an overlay", fg="white", font=(60), bg="red")
l.pack()

b = Button(
    root, text="click me to print something", command=lambda: print("this is something")
)
b.pack()

b = Button(root, text="P1 Start", command=lambda: send_key_to_itgmania("Return"))
b.pack()

b = Button(root, text="P1 Back", command=lambda: send_key_to_itgmania("Escape"))
b.pack()

b = Button(root, text="quit", command=lambda: exit())
b.pack()

ensure_itgmania_active()
# make window to be always on top
root.wm_attributes("-topmost", 1)
# quit on control-C
root.bind('<Control-c>', exit)
root.mainloop()
