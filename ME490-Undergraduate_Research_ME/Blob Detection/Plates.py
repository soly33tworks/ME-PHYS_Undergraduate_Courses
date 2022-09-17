import numpy as np
import cv2
from matplotlib.path import Path

def draw_plates(frame, plate_list):
    for plate in plate_list:
        pts = np.array(plate).reshape((-1,1,2))
        frame = cv2.polylines(frame, [pts], True, (0, 0, 255))
    return frame

def create_masks(plate_regs, h, w):
    masks = []
    template = np.zeros((h,w))
    # xy coordinates for each pixel in the image
    nr, nc = template.shape
    ygrid, xgrid = np.mgrid[:nr, :nc]
    xypix = np.vstack((xgrid.ravel(), ygrid.ravel())).T

    for plate_reg in plate_regs:
        plt = plate_reg.T
        xc, yc = plt[0], plt[1]
        xycrop = np.vstack((xc, yc)).T

        pth = Path(xycrop, closed=False)
        mask_local = pth.contains_points(xypix)
        mask_local = mask_local.reshape(template.shape)
        masks.append(mask_local)

    mask_plates = masks[0]
    for mask in masks[1:]:
        mask_plates = mask_plates | mask

    return mask_plates