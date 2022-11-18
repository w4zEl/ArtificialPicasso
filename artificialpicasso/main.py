import tkinter as tk
from PIL import Image, ImageTk
import cv2
import ImageTracer
from datetime import datetime
from mathutils import between

isCameraOn = False


def lights_camera_action():
    global cam, isCameraOn
    cam = cv2.VideoCapture(0)
    isCameraOn = True
    webcam_stream()


def webcam_stream():
    global frame, isCameraOn
    if isCameraOn:
        _, frame = cam.read()
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        webcam.imgtk = imgtk
        webcam.configure(image=imgtk)
        webcam.after(1, webcam_stream)


def stopWebcamStream():
    global isCameraOn, root
    isCameraOn = False
    cam.release()

def takePicture():
    global frame
    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    cv2.imwrite(f"../output_images/image_{now}.jpg", frame)
    stopWebcamStream()
    cropLabel = tk.Label(window, text='Crop image by mouse selection')
    cropLabel.grid(row=0)
    canvas = tk.Canvas(window, width=frame.shape[1], height=frame.shape[0])
    canvas.create_image(0, 0, anchor=tk.NW, image=webcam.imgtk)
    canvas.grid(row=1)
    p1: tuple
    p2: tuple
    crop_box_id = None
    has_rect = False
    move_start: tuple

    def mouse_down(event):
        nonlocal p1, has_rect, move_start
        if has_rect and between(p1[0], p2[0], event.x) and between(p1[1], p2[1], event.y):
            move_start = event.x, event.y
        else:
            has_rect = False
            reset_rect()
            p1 = event.x, event.y

    def update_rect():
        nonlocal p1, p2, crop_box_id
        if p1 and p2:
            if crop_box_id:
                canvas.coords(crop_box_id, *p1, *p2)
            else:
                crop_box_id = canvas.create_rectangle(*p1, *p2, width=1)

    def mouse_move(event):
        nonlocal p1, p2, has_rect, move_start
        if has_rect:
            dx, dy = event.x - move_start[0], event.y - move_start[1]
            p1 = p1[0] + dx, p1[1] + dy
            p2 = p2[0] + dx, p2[1] + dy
            move_start = event.x, event.y
        else:
            p2 = event.x, event.y
        update_rect()

    def mouse_up(event):
        nonlocal p2, has_rect
        if not has_rect:
            p2 = event.x, event.y
            has_rect = True

    def reset_rect(event=None):
        nonlocal p1, p2, has_rect, crop_box_id
        p1 = p2 = None
        has_rect = False
        canvas.delete(crop_box_id)
        crop_box_id = None

    canvas.bind("<Button-1>", mouse_down)
    canvas.bind("<B1-Motion>", mouse_move)
    canvas.bind("<ButtonRelease-1>", mouse_up)
    root.bind('<Escape>', reset_rect)
    webcam.destroy()

    def doTrace():
        global frame
        window.destroy()
        root.unbind('<Escape>')
        if p1 and p2:
            frame = frame[min(p1[1], p2[1]):max(p1[1], p2[1]), min(p1[0], p2[0]):max(p1[0], p2[0])]
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.geometry(f'300x300+{int(screen_width / 2 - 150)}+{int(screen_height / 2 - 150)}')

        titleLabel = tk.Label(root, text="Image Tracer")
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
        tk.Button(root, text='Run', command=lambda: cv2.imwrite(f'../output_images/trace_{now}.jpg',
                                                                ImageTracer.run(frame, minStrokeLengthSlider.get(),
                                                                                speedSlider.get())),
                  width=10).pack(pady=(20, 20))
        tk.Label(root, text="Press Q to stop animation").pack()

    btnPicture.configure(text='Trace!', command=doTrace)
    btnPicture.grid(row=2)


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Artificial Picasso")
    window = tk.Frame(root)
    window.grid()
    webcam = tk.Label(window)
    webcam.grid()
    btnPicture = tk.Button(window, width=20, text="Take Picture", font="none 12", command=takePicture)
    btnPicture.grid()
    lights_camera_action()
    root.mainloop()
