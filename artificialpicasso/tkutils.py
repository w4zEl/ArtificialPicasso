import tkinter
from typing import Optional
from dataclasses import dataclass
from mathutils import between


@dataclass
class CropRegion:
    p1: Optional[tuple] = None
    p2: Optional[tuple] = None


def setup_cropping(canvas: tkinter.Canvas, root: tkinter.Tk, crop_region: CropRegion):
    has_rect: bool = False
    move_start: Optional[tuple] = None
    crop_box_id: Optional[int] = None

    def mouse_down(event):
        nonlocal has_rect, move_start
        if has_rect and between(crop_region.p1[0], crop_region.p2[0], event.x) and \
                between(crop_region.p1[1], crop_region.p2[1], event.y):
            move_start = event.x, event.y
        else:
            has_rect = False
            reset_rect()
            crop_region.p1 = event.x, event.y

    def update_rect():
        nonlocal crop_box_id
        if crop_region.p1 and crop_region.p2:
            if crop_box_id:
                canvas.coords(crop_box_id, *crop_region.p1, *crop_region.p2)
            else:
                crop_box_id = canvas.create_rectangle(*crop_region.p1, *crop_region.p2, width=1)

    def mouse_move(event):
        nonlocal has_rect, move_start
        if has_rect:
            dx, dy = event.x - move_start[0], event.y - move_start[1]
            crop_region.p1 = crop_region.p1[0] + dx, crop_region.p1[1] + dy
            crop_region.p2 = crop_region.p2[0] + dx, crop_region.p2[1] + dy
            move_start = event.x, event.y
        else:
            crop_region.p2 = event.x, event.y
        update_rect()

    def mouse_up(event):
        nonlocal has_rect
        if not has_rect:
            crop_region.p2 = event.x, event.y
            has_rect = True

    def reset_rect(event=None):
        nonlocal has_rect, crop_box_id
        crop_region.p1 = crop_region.p2 = None
        has_rect = False
        canvas.delete(crop_box_id)
        crop_box_id = None

    canvas.bind("<Button-1>", mouse_down)
    canvas.bind("<B1-Motion>", mouse_move)
    canvas.bind("<ButtonRelease-1>", mouse_up)
    root.bind('<Escape>', reset_rect)

    def cleanup():
        root.unbind('<Escape>')
    return cleanup


def crop(img, crop_region: CropRegion):
    if crop_region.p1 and crop_region.p2:
        return img[min(crop_region.p1[1], crop_region.p2[1]):max(crop_region.p1[1], crop_region.p2[1]),
                   min(crop_region.p1[0], crop_region.p2[0]):max(crop_region.p1[0], crop_region.p2[0])]
    else:
        return img
