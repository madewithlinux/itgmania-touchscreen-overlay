from typing import *
import dataclasses
from time import sleep
import re
import subprocess
import tkinter as tk
from tkinter import *

use_game_buttons = False
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


def send_keydown_to_itgmania(key: Union[str, Tuple[str]]):
    ensure_itgmania_active()
    if isinstance(key, str):
        key = (key,)
    subprocess.check_output(
        ["xdotool", "search", "--name", "Simply Love", "keydown", "--window", "%1"]
        + list(key)
    )


def send_keyup_to_itgmania(key: Union[str, Tuple[str]]):
    ensure_itgmania_active()
    if isinstance(key, str):
        key = (key,)
    subprocess.check_output(
        ["xdotool", "search", "--name", "Simply Love", "keyup", "--window", "%1"]
        + list(key)
    )


root = Tk()
root.title("touchscreen overlay")
root.geometry(f"=250x150+{window_position_x}+{window_position_y}")
# root.geometry(f"=40x40+{window_position_x}+{window_position_y}")
# # to remove the titlebar
# root.overrideredirect(True)

l = Label(
    root, text="this is a touch input overlay for itgmania", font=("Helvetica", "18")
)
l.pack()

b = Button(root, text="quit", font=("Helvetica", "18"), command=lambda: exit())
b.pack()


@dataclasses.dataclass
class UiButton:
    text: str
    key_to_send: Optional[Union[str, Tuple[str]]]
    bg: Optional[str]

    def on_press(self, event):
        print(f"button {self.text} {self.key_to_send} was pressed")
        send_keydown_to_itgmania(self.key_to_send)

    def on_release(self, event):
        print(f"button {self.text} {self.key_to_send} was released")
        send_keyup_to_itgmania(self.key_to_send)


if use_game_buttons:
    # game buttons
    nav_buttons_p1 = [
        UiButton(text="Left", key_to_send="Left", bg="#ff0000"),
        UiButton(text="Right", key_to_send="Right", bg="#ffff00"),
        UiButton(text="Up", key_to_send="Up", bg="#00ff00"),
        UiButton(text="Down", key_to_send="Down", bg="deep sky blue"),
        UiButton(text="Start", key_to_send="Return", bg="green3"),
        UiButton(text="Select", key_to_send="slash", bg="red"),
        UiButton(text="Back", key_to_send="Escape", bg="gray69"),
    ]
    nav_buttons_p2 = [
        UiButton(text="Left", key_to_send="KP_4", bg="#ff0000"),
        UiButton(text="Right", key_to_send="KP_6", bg="#ffff00"),
        UiButton(text="Up", key_to_send="KP_8", bg="#00ff00"),
        UiButton(text="Down", key_to_send="KP_2", bg="deep sky blue"),
        UiButton(text="Start", key_to_send="KP_Enter", bg="green3"),
        UiButton(text="Select", key_to_send="KP_0", bg="red"),
        UiButton(text="Back", key_to_send="backslash", bg="gray69"),
    ]
else:
    # menu buttons
    nav_buttons_p1 = [
        UiButton(text="Left", key_to_send="Delete", bg="#ff0000"),
        UiButton(text="Right", key_to_send="Page_Down", bg="#ffff00"),
        UiButton(text="Up", key_to_send="Home", bg="#00ff00"),
        UiButton(text="Down", key_to_send="End", bg="deep sky blue"),
        UiButton(text="Start", key_to_send="Return", bg="green3"),
        UiButton(text="Select", key_to_send="slash", bg="red"),
        UiButton(text="Back", key_to_send="Escape", bg="gray69"),
    ]
    nav_buttons_p2 = [
        UiButton(text="Left", key_to_send="KP_Divide", bg="#ff0000"),
        UiButton(text="Right", key_to_send="KP_Multiply", bg="#ffff00"),
        UiButton(text="Up", key_to_send="KP_Minus", bg="#00ff00"),
        UiButton(text="Down", key_to_send="KP_Add", bg="deep sky blue"),
        UiButton(text="Start", key_to_send="KP_Enter", bg="green3"),
        UiButton(text="Select", key_to_send="KP_0", bg="red"),
        UiButton(text="Back", key_to_send="backslash", bg="gray69"),
    ]

nav_buttons_middle = [
    UiButton(
        text="Close",
        key_to_send=(
            "Up",
            "Down",
            "Home",
            "End",
            "KP_Minus",
            "KP_Add",
            "KP_8",
            "KP_2",
        ),
        bg="gray69",
    ),
    UiButton(
        text="Menu",
        key_to_send=(
            "Left",
            "Right",
            "Delete",
            "Page_Down",
            "KP_Divide",
            "KP_Multiply",
            "KP_4",
            "KP_6",
        ),
        bg="gray69",
    ),
    UiButton(text="Profile", key_to_send="p", bg="gray69"),
]


def create_child_window(
    root,
    nav_buttons: List[UiButton],
    *,
    x_midpoint=window_width / 4,
):
    child = tk.Toplevel(root)
    child.transient(root)
    child.title("child")
    # make window to be always on top
    child.wm_attributes("-topmost", 1)
    unit = itgmania_status_bar_height
    width = unit * len(nav_buttons)
    height = unit
    # x = window_position_x + x_offset
    x = window_position_x + int(x_midpoint - (unit * len(nav_buttons) / 2))
    y = window_position_y + window_height - unit
    child.geometry(f"={width}x{height}+{x}+{y}")
    child.overrideredirect(True)

    for i, btn in enumerate(nav_buttons):
        if not btn:
            continue
        b = tk.Button(
            child,
            font=("Helvetica", "18"),
            text=btn.text,
            # command=btn.command,
            bg=btn.bg,
        )
        b.bind("<ButtonPress>", btn.on_press)
        b.bind("<ButtonRelease>", btn.on_release)
        b.place(x=i * unit, y=0, width=unit, height=unit)


create_child_window(root, nav_buttons=nav_buttons_p1, x_midpoint=window_width / 4)
create_child_window(root, nav_buttons=nav_buttons_p2, x_midpoint=3 * window_width / 4)
create_child_window(root, nav_buttons=nav_buttons_middle, x_midpoint=window_width / 2)
ensure_itgmania_active()


# quit on control-C
# TODO: this doesn't actually work?
root.bind("<Control-c>", exit)
root.after(250, ensure_itgmania_active)
root.mainloop()
