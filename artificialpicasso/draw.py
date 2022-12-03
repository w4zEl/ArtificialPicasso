from arm import ArmController, Paper
from servo_utils import make_servo, make_adjusted_servo
import StrokeExtractor
import tkinter as tk
from tkinter.filedialog import askopenfilename
import cv2
from PIL import ImageTk, Image
from tkinter.messagebox import showwarning
from logsetup import logger
import os.path
from imgutils import cv2_image_to_image_tk
import tkutils
from threading import Thread


def supplementary_angle(angle):
    return 180 - angle


def draw(img, blur):
    draw_frame = tk.Frame(root)
    top_label = tk.Label(draw_frame, text='Drawing in progress...')
    top_label.pack()
    imgtk = cv2_image_to_image_tk(img)
    img_label = tk.Label(draw_frame, image=imgtk)
    img_label.imgtk = imgtk  # hold that reference
    img_label.pack()
    draw_frame.pack()
    controller = ArmController(arm1len=20.2, arm2len=22.1,
                               arm1servo=make_adjusted_servo(3, convert_angle=supplementary_angle, max_pulse=2500),
                               arm2servo=make_adjusted_servo(1, convert_angle=supplementary_angle, max_pulse=2500),
                               tip_servo=make_servo(0), paper=Paper(3.5, 3.5, 27.6, 21.3))
    strokes = StrokeExtractor.getStrokes(img, blur)
    strokeMinLength = 50
    img_height, img_width, *_ = img.shape

    def scale_to_paper(x, y):
        return (1 - x / img_width) * controller.paper.width, (1 - y / img_height) * controller.paper.height

    def update_img():
        img_label.imgtk = cv2_image_to_image_tk(img)
        img_label.configure(image=img_label.imgtk)

    def do_draw():
        for stroke in strokes:
            perimeter = cv2.arcLength(stroke, True)

            if perimeter >= strokeMinLength:
                controller.lift_tip()
                first: bool = True
                for (x, y), in stroke:
                    controller.move_to(*scale_to_paper(x, y), 0.1 if first else 0.03)
                    if first:
                        controller.drop_tip()
                        first = False
                    cv2.circle(img, (x, y), 2, (255, 0, 0), 1)
                    img_label.after(1, update_img)
        top_label.configure(text='Beautiful abstract art complete!')
        tk.Button(draw_frame, text='Reset controller', command=controller.reset_positions).pack(after=img_label, pady=5)
    Thread(target=do_draw).start()


def open_file():
    filename = askopenfilename(filetypes=[('Image File', '.jpg .jpeg .png')])
    if filename and os.path.isfile(filename):
        img = cv2.imread(filename)
        main_frame.destroy()
        draw(img, False)
    else:
        showwarning("ArtificialPicasso", "No image selected")


def show_cam_stream():
    import tkinter.ttk
    cam = cv2.VideoCapture(0)
    main_frame.destroy()
    cam_frame = tk.Frame(root)
    cam_label = tk.Label(cam_frame)
    frame = None

    def do_stream():
        nonlocal frame
        ret, frame = cam.read()
        if not ret:
            logger.warning("Could not read frame from camera!")
            exit(1)
        imgtk = cv2_image_to_image_tk(frame)
        cam_label.imgtk = imgtk
        cam_label.configure(image=imgtk)
        cam_label.after(1, do_stream)

    def allow_crop():
        nonlocal frame
        tk.Label(text='Crop image by mouse selection').pack(before=cam_label)
        canvas = tk.Canvas(cam_frame, width=frame.shape[1], height=frame.shape[0])
        canvas.create_image(0, 0, anchor=tk.NW, image=cam_label.imgtk)
        canvas.pack(before=cam_label)
        cam_label.destroy()

        def start_draw():
            cam_frame.destroy()
            cleanup_cropping()
            draw(tkutils.crop(frame, crop_region), True)
        picture_btn.configure(text='Start drawing!', command=start_draw)
        crop_region = tkutils.CropRegion()
        cleanup_cropping = tkutils.setup_cropping(canvas, root, crop_region)

    cam_label.pack()
    picture_btn = tkinter.ttk.Button(text='Take picture!', command=allow_crop)
    picture_btn.pack(after=cam_label, pady=5)
    cam_frame.pack()
    do_stream()


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Artificial Picasso")
    main_frame = tk.Frame(root)
    tk.Label(main_frame, text='Draw an abstract image with the Artificial Picasso!', font='Arial 12 bold')\
        .grid(row=0, pady=5, columnspan=2)
    photo_image = ImageTk.PhotoImage(Image.open("../docs/media/RobotArmTopView1.jpg").resize((600, 400)))
    tk.Label(main_frame, image=photo_image).grid(row=1, columnspan=2, pady=10, padx=10, )
    file_btn = tk.Button(main_frame, text='Open file', command=open_file)
    file_btn.grid(column=0, row=2, pady=7)
    camera_btn = tk.Button(main_frame, text='Take picture with camera', command=show_cam_stream)
    camera_btn.grid(column=1, row=2)
    main_frame.pack()
    root.eval('tk::PlaceWindow . center')
    root.mainloop()
