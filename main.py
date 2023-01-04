import cv2 as cv
import os
import time
import tkinter as tk
from windowcapture import WindowCapture
import win32api, win32con, win32gui
from PIL import Image, ImageTk
import windowName
import keyboard

def mainCapture():
    # Change the working directory to the folder this script is in.
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # initialize the WindowCapture class
    wincap = WindowCapture(window_title)

    # load the template images
    templates = [
        cv.imread('pictures\\fourH.png', cv.IMREAD_GRAYSCALE),
        cv.imread('pictures\\oneHeart.png', cv.IMREAD_GRAYSCALE),
        cv.imread('pictures\\twoHeart.png', cv.IMREAD_GRAYSCALE),
        cv.imread('pictures\\threeHeart.png', cv.IMREAD_GRAYSCALE),
    ]

    # set the threshold for a good match
    threshold = 0.8

    # initialize the timer variables
    timer_active = False
    start_time = 0
    elapsed_time = 0

    while capture_running:
        # get an updated image of the game
        screenshot = wincap.get_screenshot(x=1480, y=55, width=385, height=75)

        # convert the screenshot to grayscale
        screenshot_gray = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)

        # iterate over the templates and check for a match
        healthLow = False
        for template in templates:
            # perform template matching
            match_scores = cv.matchTemplate(screenshot_gray, template, cv.TM_CCOEFF_NORMED)

            # find the location of the best match
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(match_scores)

            # if the maximum value is above the threshold, consider the template to be detected
            if max_val > threshold:
                healthLow = True
                label2.config(text="Low Health Detected, Waiting for cooldown...")
                break

        if healthLow and not timer_active:
            label2.config(text="Low Health Detected, Drinking Potion")

            # press the "h" key
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.2)
            #win32api.keybd_event(0x48, 0, 0, 0)
            keyboard.press('h')
            time.sleep(0.2)
            #win32api.keybd_event(0x48, 0, win32con.KEYEVENTF_KEYUP, 0)
            keyboard.release('h')

            # start the timer
            time.sleep(0.5)
            timer_active = True
            start_time = time.time()
            elapsed_time = 0

        elif timer_active:
            elapsed_time = time.time() - start_time
            label.config(text=f"Timer running: {elapsed_time:.1f} seconds elapsed")

            # check if the timer has expired
            if elapsed_time >= 60:
                # stop the timer
                timer_active = False
                elapsed_time = 0
                label.config(text="Cooldown off")
        else:
            # if the health is not low and the timer is not active, do nothing
            label2.config(text="Health Full, No Cooldown, Waiting..")
            pass

        # Update the canvas with the screenshot
        screenshot_image = Image.fromarray(screenshot)
        screenshot_image = ImageTk.PhotoImage(screenshot_image)
        canvas.create_image(5, 0, anchor="nw", image=screenshot_image)
        canvas.image = screenshot_image

        window.update()

# Callback function for the start button
def start_callback():
    global capture_running
    capture_running = True
    mainCapture()

# Callback function for the stop button
def stop_callback():
    global capture_running
    capture_running = False
    label.config(text="Stopped.")
    label2.config(text=" ")
    print("Stopped.")

if __name__ == "__main__":

    hwnd, window_title = windowName.findTerraria()

    # Create the main window
    window = tk.Tk()

    # Set the window title and size
    window.wm_title("Terraria Health Monitor")
    window.geometry("400x200")

    # Create a frame to hold the buttons
    frame = tk.Frame(window)
    frame.pack(side=tk.BOTTOM)

    # Create a level widget to display the log
    label = tk.Label(window)
    label.pack(side=tk.BOTTOM)

    # Create second label widget to display key low health detected
    label2 = tk.Label(window)
    label2.pack(side=tk.BOTTOM)

    # Create the start and stop buttons
    start_button = tk.Button(frame, text="Start", command=start_callback)
    stop_button = tk.Button(frame, text="Stop", command=stop_callback)
    start_button.pack(side=tk.LEFT)
    stop_button.pack(side=tk.RIGHT)

    # Initialize the timer variables
    timer_active = False
    start_time = 0
    elapsed_time = 0

    # Flag to track whether the mainCapture loop is running
    capture_running = False

    # Create a canvas to display the image
    canvas = tk.Canvas(window, width=400, height=200)
    canvas.pack()

    window.mainloop()
