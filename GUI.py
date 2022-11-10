import tkinter as tk
from PIL import Image, ImageTk
import cv2
import os

isCameraOn = False

def lightsCameraAction():
    global cam, isCameraOn
    cam = cv2.VideoCapture(0)
    isCameraOn = True
    webcamStream()

def webcamStream():
    global frame, isCameraOn
    if isCameraOn:
        _, frame = cam.read()
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        webcam.imgtk = imgtk
        webcam.configure(image=imgtk)
        webcam.after(1, webcamStream) 

def stopWebcamStream():
    global isCameraOn, root
    isCameraOn = False
    cam.release()
    root.destroy()

def takePicture():
    global frame
    cv2.imwrite(str(os.getcwd()) + '\\testimage.jpg', frame)
    stopWebcamStream()


root = tk.Tk()
window = tk.Frame(root)
window.grid()
webcam = tk.Label(window)
webcam.grid()
btnPicture = tk.Button(window, width=20, text="take picture", font="none 12", command=takePicture)
btnPicture.grid()
lightsCameraAction()
root.mainloop()
