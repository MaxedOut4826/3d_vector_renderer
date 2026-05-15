TODO:
in render handler, to prevent doubling back on single line connections, can do something like:
  for index in ((lines[1:] + lines[:1]) if len(lines) > 2 else lines[1:]):

update variable name for "now" in draw_frame to be "start_time" or something