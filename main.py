from typing import *
import dataclasses
import re
import subprocess
import tkinter as tk
from tkinter import *

window_position_x = "0"
window_position_y = "0"
# hardcoded offset for desktop development
window_position_x = 6
window_position_y = 93

window_width = 1920
window_height = 1080

itgmania_status_bar_height = 71


def get_itgmania_position():
    out = subprocess.check_output(
        ["xdotool", "search", "--name", "Simply Love", "getwindowgeometry"]
    ).decode("ascii", "ignore")
    m = re.search("\s*Position: (\d+),(\d+)", out)
    if not m:
        return (0, 0)  # default to top-left corner of screen
    return (int(m.group(1)), int(m.group(2)))


def ensure_itgmania_active():
    subprocess.check_output(
        ["xdotool", "search", "--name", "Simply Love", "windowactivate"]
    )


def send_key_to_itgmania(key: str):
    ensure_itgmania_active()
    subprocess.check_output(
        ["xdotool", "search", "--name", "Simply Love", "key", "--window", "%1", key]
    )


root = Tk()
root.title("overlay")


# root.geometry(f"=250x150+{window_position_x}+{window_position_y}")
root.geometry(f"=40x40+{window_position_x}+{window_position_y}")

# to remove the titlebar
root.overrideredirect(True)


# l = Label(root, text="HI this is an overlay", fg="white", font=(60), bg="red")
# l.pack()

# b = Button(
#     root, text="click me to print something", command=lambda: print("this is something")
# )
# b.pack()

# b = Button(root, text="P1 Start", command=lambda: send_key_to_itgmania("Return"))
# b.pack()

# b = Button(root, text="P1 Back", command=lambda: send_key_to_itgmania("Escape"))
# b.pack()

b = Button(root, text="quit", command=lambda: exit())
b.pack()


@dataclasses.dataclass
class UiButton:
    text: str
    # key_to_send: Optional[str]
    command: Callable
    bg: Optional[str]


nav_buttons = [
    # P1
    UiButton(text="Left", command=lambda: send_key_to_itgmania("Left"), bg="#ff0000"),
    UiButton(text="Right", command=lambda: send_key_to_itgmania("Right"), bg="#ffff00"),
    UiButton(text="Up", command=lambda: send_key_to_itgmania("Up"), bg="#00ff00"),
    UiButton(text="Down", command=lambda: send_key_to_itgmania("Down"), bg="deep sky blue"),
    UiButton(text="Start", command=lambda: send_key_to_itgmania("Return"), bg="green3"),
    UiButton(text="Select", command=lambda: send_key_to_itgmania("slash"), bg="red"),
    UiButton(text="Back", command=lambda: send_key_to_itgmania("Escape"), bg="gray69"),

    # spacer
    None,
    None,
    None,

    # P2
    UiButton(text="Left", command=lambda: send_key_to_itgmania("KP_4"), bg="#ff0000"),
    UiButton(text="Right", command=lambda: send_key_to_itgmania("KP_6"), bg="#ffff00"),
    UiButton(text="Up", command=lambda: send_key_to_itgmania("KP_8"), bg="#00ff00"),
    UiButton(text="Down", command=lambda: send_key_to_itgmania("KP_2"), bg="deep sky blue"),
    UiButton(text="Start", command=lambda: send_key_to_itgmania("KP_Enter"), bg="green3"),
    UiButton(text="Select", command=lambda: send_key_to_itgmania("KP_0"), bg="red"),
    UiButton(text="Back", command=lambda: send_key_to_itgmania("backslash"), bg="gray69"),
]


def create_child_window(
    root,
    *,
    x_offset=100,
):
    child = tk.Toplevel(root)
    child.transient(root)
    child.title("child")
    unit = itgmania_status_bar_height
    width = unit * len(nav_buttons)
    height = unit
    # x = window_position_x + x_offset
    x = window_position_x + int(window_width/2 - (unit * len(nav_buttons) / 2))
    y = window_position_y + window_height - unit
    child.geometry(f"={width}x{height}+{x}+{y}")
    child.overrideredirect(True)

    for i, btn in enumerate(nav_buttons):
        if not btn:
            continue
        b = tk.Button(
            child,
            font=('Helvetica', '18'),
            text=btn.text,
            command=btn.command,
            bg=btn.bg,
        )
        b.place(x=i * unit, y=0, width=unit, height=unit)

create_child_window(root)


ensure_itgmania_active()
# make window to be always on top
root.wm_attributes("-topmost", 1)


# quit on control-C
# TODO: this doesn't actually work?
root.bind("<Control-c>", exit)

root.mainloop()
