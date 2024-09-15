import cv2
import curses

import misc
import time

file = "New folder/dQw4w9WgXcQ.mp4"
video = cv2.VideoCapture(file)
# frame = cv2.imread(file)

height = 32
fps = video.get(cv2.CAP_PROP_FPS)
total_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
total_frames = fps * 20       # 20 seconds
total_frames = 20

misc.windows_font(height)

def main(window):
    curses.initscr()
    curses.curs_set(0)

    max_y, max_x = window.getmaxyx()
    curses.use_default_colors()

    pad = curses.newpad(height * 2, height * 4)
    pad_size = (0, 0, 0, 0, max_y - 1, max_x - 1)

    for i in range(1, curses.COLOR_PAIRS - 1):
        curses.init_pair(i, i, -1)

    status, img = video.read()
    width = int(img.shape[1] * (height / img.shape[0])) * 2
    dim = width, height

    def render_frames():
        current_frame = total_frames
        frames = []

        while current_frame:
            current_frame -= 1

            status, img = video.read()
            if status:
                img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
                frame = []

                for y in range(height):
                    for x in range(width):
                        r = int(img[y, x, 2] / 51)
                        g = int(img[y, x, 1] / 51)
                        b = int(img[y, x, 0] / 51)
                        frame.append((r * 36) + (g * 6) + (b + 16))

                frames.append(frame)
            else:
                break

        return frames

    pad.addstr(max_y - 1, 0, "Rendering frames")
    pad.refresh(*pad_size)
    frames = render_frames()
    pad.clear()

    def play(frames):
        def draw(pad, frame, width, height):
            for y in range(height):
                pad.move(y, 0)
                for i in range(width * y, width * (y + 1)):
                    pad.addstr("|", curses.color_pair(frame[i]))

        for frame in frames:
            draw(pad, frame, width, height)
            pad.refresh(*pad_size)
            time.sleep(1 / fps)

    play(frames)

curses.wrapper(main)