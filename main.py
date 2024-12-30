from pathlib import Path
from typing import *
import dataclasses
from time import sleep
import re
import signal
import subprocess
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *

# for use with itgmania Simply-Love ScreenSwitcher.lua module
# https://github.com/Simply-Love/Simply-Love-Modules/blob/main/ScreenSwitcher.lua


def get_current_screen():
    current_screen_paths = [
        "~/.itgmania/Save/CurrentScreen.txt",
        "~/Apps/itgmania/Save/CurrentScreen.txt",
    ]
    for sp in current_screen_paths:
        p = Path(sp).expanduser()
        if p.exists():
            break
    return p.read_text().strip()


use_game_buttons = False
# use_game_buttons = True
window_position_x = 0
window_position_y = 0
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


# fmt: off
if use_game_buttons:
    p1_left   = "Left"
    p1_right  = "Right"
    p1_up     = "Up"
    p1_down   = "Down"
    p1_start  = "Return"
    p1_select = "slash"
    p1_back   = "Escape"

    p2_left   = "KP_4"
    p2_right  = "KP_6"
    p2_up     = "KP_8"
    p2_down   = "KP_2"
    p2_start  = "KP_Enter"
    p2_select = "KP_0"
    p2_back   = "backslash"
else:
    p1_left   = "Delete"
    p1_right  = "Page_Down"
    p1_up     = "Home"
    p1_down   = "End"
    p1_start  = "Return"
    p1_select = "slash"
    p1_back   = "Escape"

    p2_left   = "KP_Divide"
    p2_right  = "KP_Multiply"
    p2_up     = "KP_Minus"
    p2_down   = "KP_Add"
    p2_start  = "KP_Enter"
    p2_select = "KP_0"
    p2_back   = "backslash"
# fmt: on

# menu buttons
nav_buttons_p1 = [
    # fmt: off
    UiButton(text="",       style=right_btn_style,  key=p1_right,  ),
    UiButton(text="",       style=left_btn_style,   key=p1_left,   ),
    UiButton(text="",       style=up_btn_style,     key=p1_up,     ),
    UiButton(text="",       style=down_btn_style,   key=p1_down,   ),
    UiButton(text="Start",  style=start_btn_style,  key=p1_start,  ),
    UiButton(text="Select", style=select_btn_style, key=p1_select, ),
    UiButton(text="Back",   style=back_btn_style,   key=p1_back,   ),
    # fmt: on
]
nav_buttons_p2 = [
    # fmt: off
    UiButton(text="",       style=right_btn_style,  key=p2_right,  ),
    UiButton(text="",       style=left_btn_style,   key=p2_left,   ),
    UiButton(text="",       style=up_btn_style,     key=p2_up,     ),
    UiButton(text="",       style=down_btn_style,   key=p2_down,   ),
    UiButton(text="Start",  style=start_btn_style,  key=p2_start,  ),
    UiButton(text="Select", style=select_btn_style, key=p2_select, ),
    UiButton(text="Back",   style=back_btn_style,   key=p2_back,   ),
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
    child_x: int,
    child_y: int,
    *,
    # x_midpoint=window_width / 4,
    direction: Literal["v", "h"] = "h",
    unit=itgmania_status_bar_height,
):
    child = tk.Toplevel(root)
    child.transient(root)
    child.title("child")
    # make window always on top
    child.wm_attributes("-topmost", 1)
    if direction == "h":
        width = unit * len(nav_buttons)
        height = unit
    else:
        height = unit * len(nav_buttons)
        width = unit

    # make sure they are integers (in case division was uneven)
    x = window_position_x + int(child_x)
    y = window_position_y + int(child_y)
    child.geometry(f"={width}x{height}+{x}+{y}")
    child.overrideredirect(True)

    for i, btn in enumerate(nav_buttons):
        if not btn:
            continue
        b = ttk.Button(child, text=btn.text, style=btn.style)
        b.bind("<ButtonPress>", btn.on_press)
        b.bind("<ButtonRelease>", btn.on_release)
        if direction == "h":
            b.place(x=i * unit, y=0, width=unit, height=unit)
        else:
            b.place(x=0, y=i * unit, width=unit, height=unit)

    return child


def create_nav_windows() -> List[tk.Toplevel]:
    unit = itgmania_status_bar_height
    player_nav_buttons_width = len(nav_buttons_p1) * unit
    p1 = create_child_window(
        root,
        nav_buttons=nav_buttons_p1,
        child_x=0,
        child_y=window_height / 2 - player_nav_buttons_width / 2,
        direction="v",
        unit=unit,
    )
    p2 = create_child_window(
        root,
        nav_buttons=nav_buttons_p2,
        child_x=window_width - unit,
        child_y=window_height / 2 - player_nav_buttons_width / 2,
        direction="v",
        unit=unit,
    )
    middle_nav_buttons_width = len(nav_buttons_middle) * unit
    middle = create_child_window(
        root,
        nav_buttons=nav_buttons_middle,
        child_x=window_width / 2 - middle_nav_buttons_width / 2,
        child_y=window_height - unit,
        unit=unit,
    )
    ensure_itgmania_active(fail_ok=True)
    return [p1, p2, middle]


nav_windows: List[tk.Toplevel] = create_nav_windows()
nav_window_check_interval_ms = 500
last_screen = ""


def show_or_hide_nav_windows():
    global nav_windows
    global last_screen
    current_screen = get_current_screen()
    # print(f"{current_screen=}")
    if last_screen != current_screen:
        # print("screen changed")
        last_screen = current_screen
        if get_current_screen() == "ScreenGameplay":
            for w in nav_windows:
                w.withdraw()
        else:
            for w in nav_windows:
                w.deiconify()
        ensure_itgmania_active()
    root.after(nav_window_check_interval_ms, show_or_hide_nav_windows)


# quit on control-C
def ctrl_c_handler(*_unused):
    root.destroy()
    print("caught ^C")


def check():
    root.after(500, check)  #  time in ms.


root.after(500, check)
signal.signal(signal.SIGINT, ctrl_c_handler)
# root.bind("<Control-c>", ctrl_c_handler)

root.after(250, ensure_itgmania_active)
root.after(nav_window_check_interval_ms, show_or_hide_nav_windows)
root.mainloop()
