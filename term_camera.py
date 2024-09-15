import cv2
import curses
import misc

cap = cv2.VideoCapture(0)
width = 64
height = 32
misc.windows_font(height)

def main(window):
    curses.initscr()
    curses.curs_set(0)

    max_y, max_x = window.getmaxyx()
    curses.use_default_colors()

    pad = curses.newpad(height * 2, height * 4)
    pad_size = (0, 0, 0, 0, max_y-1, max_x-1)

    for i in range(1, curses.COLOR_PAIRS - 1):
        curses.init_pair(i, i, -1)

    pad.clear()

    def draw(pad, frame, width, height):
        for y in range(height):
            pad.move(y, 0)
            for x in range(width):
                r = int(frame[y][x][2] / 51)
                g = int(frame[y][x][1] / 51)
                b = int(frame[y][x][0] / 51)
                pixel = (r * 36) + (g * 6) + (b + 16)

                pad.addstr("|", curses.color_pair(pixel))

    while True:
        ret, frame = cap.read()

        if ret:
            frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)
            draw(pad, frame, width, height)

        pad.refresh(*pad_size)

curses.wrapper(main)