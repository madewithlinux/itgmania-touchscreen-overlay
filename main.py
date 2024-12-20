import subprocess
from tkinter import *


def send_key(key: str):
    subprocess.check_output(
        [
            "xdotool",
            "search",
            "--name",
            "Simply Love",
            "key",
            "--window",
            "%1",
            key,
        ]
    )


root = Tk()

root.title("overlay")

x = "0"
y = "0"

root.geometry(f"250x150+{x}+{y}")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
print(f"{screen_width=}")
print(f"{screen_height=}")

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

b = Button(root, text="P1 Start", command=lambda: send_key("Return"))
b.pack()

b = Button(root, text="quit", command=lambda: exit())
b.pack()


# make window to be always on top
root.wm_attributes("-topmost", 1)
root.mainloop()
