import time
import sys

toolbar_width = 40

# setup toolbar
sys.stdout.write("[%s]" % (" " * toolbar_width))
sys.stdout.flush()
sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['

for i in range(toolbar_width):
    # update the bar
    percentage = i / toolbar_width * 100
    sys.stdout.write("%.2f %%" %percentage)
    sys.stdout.flush()
    time.sleep(0.1)  # do real work here
    if percentage >= 10:
        sys.stdout.write("\b" * 7)
    else:
        sys.stdout.write("\b" * 6)
    sys.stdout.flush()

sys.stdout.write("]\n") # this ends the progress bar