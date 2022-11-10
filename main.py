import tkinter as tk
from PIL import Image, ImageTk
import cv2
import ImageTracer
from datetime import datetime

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

def takePicture():
    global frame
    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    cv2.imwrite(f"image_{now}.jpg", frame)
    stopWebcamStream()
    window.destroy()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f'300x300+{int(screen_width / 2 - 150)}+{int(screen_height / 2 - 150)}')

    titleLabel = tk.Label(root, text="StrokeExtractor Main")
    titleLabel.config(font=("Arial", 15))
    titleLabel.pack(pady=(10, 0))

    tk.Label(root, text="Minimum stroke length").pack(pady=(10, 0))
    minStrokeLengthSlider = tk.Scale(root, from_=0, to=1000, length=250, orient='horizontal')
    minStrokeLengthSlider.set(50)
    minStrokeLengthSlider.pack()
    tk.Label(root, text="Animation speed").pack()
    speedSlider = tk.Scale(root, from_=0, to=100, length=250, orient='horizontal')
    speedSlider.set(100)
    speedSlider.pack()
    tk.Button(root, text='Run', command=lambda: cv2.imwrite(f'trace_{now}.jpg', ImageTracer.run(frame, minStrokeLengthSlider.get(), speedSlider.get())),
              width=10).pack(pady=(20, 20))
    tk.Label(root, text="Press Q to stop animation").pack()


root = tk.Tk()
root.title("Artificial Picasso")
window = tk.Frame(root)
window.grid()
webcam = tk.Label(window)
webcam.grid()
btnPicture = tk.Button(window, width=20, text="take picture", font="none 12", command=takePicture)
btnPicture.grid()
lightsCameraAction()
root.mainloop()
