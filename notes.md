# notes.md

# feature TODOs
- [x] sending keys to itgmania
- [x] making sure itgmania is always the active window
- [x] reliable button positioning
- [x] both P1 and P2 buttons
- [x] button holding
- [x] dedicated keys just like ITG wheel remote (menu, close folder, profile switch, favorite, etc)
- [x] upload to github
- [x] hide during gameplay (use the simply-love module)
  - [ ] maybe also add a restart button for during gameplay?
- [ ] favorite button
- [ ] maybe hide mouse cursor?
- [x] add to ITG machine and make it auto start
- [x] make it properly quit on Ctrl-C
- [ ] change the button layout to vertical on the sides instead (more ergonomic)


# itgmania Simply-Love ScreenSwitcher.lua module
https://github.com/Simply-Love/Simply-Love-Modules/blob/main/ScreenSwitcher.lua


# sizes of UI elements in itgmania
at 1080p
top/bottom bar: 71 pixels tall I think
top-left corner of itgmania window vs top-left corner of desktop monitor: 93 pixels down, 6 pixels right



# tkinter
https://docs.python.org/3/library/tkinter.html#tkinter.Tk
https://github.com/lecrowpus/overlay
https://cs111.wellesley.edu/archive/cs111_fall14/public_html/labs/lab12/tkintercolor.html


# xdotool
https://github.com/jordansissel/xdotool
https://www.cl.cam.ac.uk/~mgk25/ucs/keysymdef.h
```bash
xdotool search --name 'Simply Love'
xdotool search --name 'Simply Love' windowactivate
xdotool search --name 'Simply Love' key --window '%1' Return
xdotool search --name 'Simply Love' getwindowgeometry

xdotool search --name 'Simply Love' keydown Left
xdotool search --name 'Simply Love' keyup Left
xdotool search --name 'Simply Love' keydown Left Right
xdotool search --name 'Simply Love' keyup Left Right

```

note that the version of xdotool installed here does not have as many features as the latest upstream version
```log
> xdotool help 
Available commands:
  getactivewindow
  getwindowfocus
  getwindowname
  getwindowpid
  getwindowgeometry
  getdisplaygeometry
  search
  selectwindow
  help
  version
  behave
  behave_screen_edge
  click
  getmouselocation
  key
  keydown
  keyup
  mousedown
  mousemove
  mousemove_relative
  mouseup
  set_window
  type
  windowactivate
  windowfocus
  windowkill
  windowclose
  windowmap
  windowminimize
  windowmove
  windowraise
  windowreparent
  windowsize
  windowunmap
  set_num_desktops
  get_num_desktops
  set_desktop
  get_desktop
  set_desktop_for_window
  get_desktop_for_window
  get_desktop_viewport
  set_desktop_viewport
  exec
  sleep
```

