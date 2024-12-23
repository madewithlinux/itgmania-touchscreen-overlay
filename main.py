from typing import *
import dataclasses
from time import sleep
import re
import subprocess
import tkinter as tk
import tkinter.ttk as ttk
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


def ensure_itgmania_active(fail_ok=True):
    try:
        subprocess.check_output(
            ["xdotool", "search", "--name", "Simply Love", "windowactivate"]
        )
    except subprocess.CalledProcessError as e:
        if not fail_ok:
            raise e


def send_key_to_itgmania(key: str):
    ensure_itgmania_active(fail_ok=False)
    subprocess.check_output(
        ["xdotool", "search", "--name", "Simply Love", "key", "--window", "%1", key]
    )


def send_keydown_to_itgmania(key: Union[str, Tuple[str]]):
    ensure_itgmania_active(fail_ok=False)
    if isinstance(key, str):
        key = (key,)
    subprocess.check_output(
        ["xdotool", "search", "--name", "Simply Love", "keydown", "--window", "%1"]
        + list(key)
    )


def send_keyup_to_itgmania(key: Union[str, Tuple[str]]):
    ensure_itgmania_active(fail_ok=False)
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

b = Button(
    root,
    text="quit",
    font=("Helvetica", "28"),
    command=lambda: exit(),
    width=12,
    height=4,
)
b.pack()


arrow_font = ("Courier", "48")
text_btn_font = ("Helvetica", "18")
label_arrows = Label(
    root,
    text="""_
    _ ⬅ ( ⮕ ➡ ) ⬆ ⬇
    _ ⇦ ⇨ ⇧ ⇩
    _ ⭅ ⭆ ⟰ ⟱
    _ 🠈 🠊 🠉 🠋
    _ 🠰 🠲 🠱 🠳
    _ 🡰 🡲 🡱 🡳
    _ 🡸 🡺 🡹 🡻
    _ ➤ , ⮜ ⮞ ⮝ ⮟

    _ 🠹 🠸 🠻 🠺
    _ 🡄 🡆 🡅 🡇
    _ 🠼 🠾 🠽 🠿
    _ 🡀 🡂 🡁 🡃

    _ ◀ ▶ ▲ ▼
    _ ⯇ ⯈ ⯅ ⯆
    _ ◂ ▸ ▴ ▾
    _ ◁ ▷ △ ▽
    _ ◃ ▹ ▵ ▿
    _ 🞀 🞂 🞁 🞃
                    |
""",
    font=arrow_font,
    fg="white",
    bg="black",
)
label_arrows.pack()

style = ttk.Style()
left_btn_style = "Left.TButton"
right_btn_style = "Right.TButton"
up_btn_style = "Up.TButton"
down_btn_style = "Down.TButton"
start_btn_style = "Start.TButton"
select_btn_style = "Select.TButton"
back_btn_style = "Back.TButton"
close_btn_style = "Close.TButton"
menu_btn_style = "Menu.TButton"
profile_btn_style = "Profile.TButton"


btn_style_params = [
    # fmt: off
(left_btn_style,    "Button.leftarrow",  arrow_font,    "#ff0000"       ),
(right_btn_style,   "Button.rightarrow", arrow_font,    "#ffff00"       ),
(up_btn_style,      "Button.uparrow",    arrow_font,    "#00ff00"       ),
(down_btn_style,    "Button.downarrow",  arrow_font,    "deep sky blue" ),
(start_btn_style,   None,                text_btn_font, "green3"        ),
(select_btn_style,  None,                text_btn_font, "red"           ),
(back_btn_style,    None,                text_btn_font, "gray80"        ),
(close_btn_style,   None,                text_btn_font, "gray69"        ),
(menu_btn_style,    None,                text_btn_font, "light salmon"  ),
(profile_btn_style, None,                text_btn_font, "MediumPurple1" ),
    # fmt: on
]
for btn_style, arrow, font, color in btn_style_params:
    if arrow:
        style.layout(btn_style, [("Button.focus", {"children": [(arrow, None)]})])
    style.configure(btn_style, font=font, arrowsize="40", background=color)
    style.map(btn_style, background=[("active", color)])

default_btn_style = "Default2.TButton"
style.configure(default_btn_style, font=text_btn_font, background="gray80")
style.map(default_btn_style, background=[("active", "gray80")])


@dataclasses.dataclass
class UiButton:
    text: str
    key: Optional[Union[str, Tuple[str]]]
    bg: Optional[str] = None
    font: Optional[str] = None
    style: str = default_btn_style

    def on_press(self, event):
        print(f"button {self.text} {self.key} was pressed")
        send_keydown_to_itgmania(self.key)

    def on_release(self, event):
        print(f"button {self.text} {self.key} was released")
        send_keyup_to_itgmania(self.key)


if use_game_buttons:
    # game buttons
    nav_buttons_p1 = [
        # fmt: off
        UiButton(text="Left",   key="Left",      bg="#ff0000"),
        UiButton(text="Right",  key="Right",     bg="#ffff00"),
        UiButton(text="Up",     key="Up",        bg="#00ff00"),
        UiButton(text="Down",   key="Down",      bg="deep sky blue"),
        UiButton(text="Start",  key="Return",    bg="green3"),
        UiButton(text="Select", key="slash",     bg="red"),
        UiButton(text="Back",   key="Escape",    bg="gray69"),
        # fmt: on
    ]
    nav_buttons_p2 = [
        # fmt: off
        UiButton(text="Left",   key="KP_4",      bg="#ff0000"),
        UiButton(text="Right",  key="KP_6",      bg="#ffff00"),
        UiButton(text="Up",     key="KP_8",      bg="#00ff00"),
        UiButton(text="Down",   key="KP_2",      bg="deep sky blue"),
        UiButton(text="Start",  key="KP_Enter",  bg="green3"),
        UiButton(text="Select", key="KP_0",      bg="red"),
        UiButton(text="Back",   key="backslash", bg="gray69"),
        # fmt: on
    ]
else:
    # menu buttons
    nav_buttons_p1 = [
        # fmt: off
        UiButton(text="",       style=left_btn_style,   key="Delete",    ),
        UiButton(text="",       style=right_btn_style,  key="Page_Down", ),
        UiButton(text="",       style=up_btn_style,     key="Home",      ),
        UiButton(text="",       style=down_btn_style,   key="End",       ),
        UiButton(text="Start",  style=start_btn_style,  key="Return",    ),
        UiButton(text="Select", style=select_btn_style, key="slash",     ),
        UiButton(text="Back",   style=back_btn_style,   key="Escape",    ),
        # fmt: on
    ]
    nav_buttons_p2 = [
        # fmt: off
        UiButton(text="",       style=left_btn_style,   key="KP_Divide",   ),
        UiButton(text="",       style=right_btn_style,  key="KP_Multiply", ),
        UiButton(text="",       style=up_btn_style,     key="KP_Minus",    ),
        UiButton(text="",       style=down_btn_style,   key="KP_Add",      ),
        UiButton(text="Start",  style=start_btn_style,  key="KP_Enter",    ),
        UiButton(text="Select", style=select_btn_style, key="KP_0",        ),
        UiButton(text="Back",   style=back_btn_style,   key="backslash",   ),
        # fmt: on
    ]

nav_buttons_middle = [
    UiButton(
        text="Close\nFolder",
        key=(
            # fmt: off
            "Up", "Down",
            "Home", "End",
            "KP_Minus", "KP_Add",
            "KP_8", "KP_2",
            # fmt: on
        ),
        style=close_btn_style,
    ),
    UiButton(
        text="Menu",
        key=(
            # fmt: off
            "Left", "Right",
            "Delete", "Page_Down",
            "KP_Divide", "KP_Multiply",
            "KP_4", "KP_6",
            # fmt: on
        ),
        style=menu_btn_style,
    ),
    UiButton(text="Profile", key="p", style=profile_btn_style),
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
        b = ttk.Button(child, text=btn.text, style=btn.style)
        b.bind("<ButtonPress>", btn.on_press)
        b.bind("<ButtonRelease>", btn.on_release)
        b.place(x=i * unit, y=0, width=unit, height=unit)


create_child_window(root, nav_buttons=nav_buttons_p1, x_midpoint=window_width / 4)
create_child_window(root, nav_buttons=nav_buttons_p2, x_midpoint=3 * window_width / 4)
create_child_window(root, nav_buttons=nav_buttons_middle, x_midpoint=window_width / 2)
ensure_itgmania_active(fail_ok=True)


# quit on control-C
# TODO: this doesn't actually work?
root.bind("<Control-c>", exit)
root.after(250, ensure_itgmania_active)
root.mainloop()
