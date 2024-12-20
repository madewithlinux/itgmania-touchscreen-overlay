# notes.md


# tkinter
https://github.com/lecrowpus/overlay



# xdotool
https://github.com/jordansissel/xdotool
```bash
xdotool search --name 'Simply Love'
xdotool search --name 'Simply Love' windowactivate
xdotool search --name 'Simply Love' key --window '%1' Return
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

