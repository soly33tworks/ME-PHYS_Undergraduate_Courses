import cv2
import numpy as np
import Plot_results as plt
from matplotlib.path import Path


def custom_filter(image, x_range, y_range, threshold, noise_thresh, kernel_x=3):
    proto1 = (image[:] > noise_thresh)*image
    proto = proto1[:]
    for row in range(y_range[0], y_range[1]):
        for col in range(x_range[0], x_range[1]):
            total = np.sum(proto1[row-kernel_x:row+kernel_x+1, col-1:col+2])
            if (total < threshold):
                proto[row, col] = 0
    
    return proto                

def summer(image, x_range, y_range, kernel_x=3):
    proto = np.zeros_like(image, dtype=np.int64)
    for row in range(y_range[0], y_range[1]):
        for col in range(x_range[0], x_range[1]):
            total = np.sum(image[row-kernel_x:row+kernel_x+1, col-1:col+2])
            #grad = abs(int(image[row+1, col]) - int(image[row, col]))
            if total > 0:
                proto[row, col] = total
            else:
                proto[row, col] = 0
    return proto

def filter_debug(gray, image2, roi, thresh=70):
    print(gray[roi[0][0]:roi[0][1], roi[1][0]:roi[1][1]])
    im3 = gray[:]
    mask = (im3 > thresh)*im3
    print(mask[roi[0][0]:roi[0][1], roi[1][0]:roi[1][1]])
    print(np.var(mask[roi[0][0]:roi[0][1], roi[1][0]:roi[1][1]], axis=0))
    proto = summer(mask, [roi[1][0], roi[1][1]], [roi[0][0], roi[0][1]], kernel_x=4)
    print(proto[roi[0][0]:roi[0][1], roi[1][0]:roi[1][1]])
    print(image2[roi[0][0]:roi[0][1], roi[1][0]:roi[1][1]])

def track(figure, filtrd_img, y, x_range, center_width, outline_width): # Tracks the bottom connection
        trck = max(range(len(filtrd_img[y, x_range[0]:x_range[1]])), key=filtrd_img[y, x_range[0]:x_range[1]].__getitem__) + x_range[0]
        rx_center = [trck-center_width, trck+center_width]
        rx_outline = [trck-outline_width, trck+outline_width]
        figure = cv2.circle(figure, (trck, y), 4, (0, 255, 255), -1)
        figure = cv2.rectangle(figure,(x_range[0], y),(x_range[1], y-15),(0,255,0),1)
        return figure, rx_center, rx_outline

def orthogonal_dist(x, y, top, bottom, rangey_outline): # Finds orth distance to line ax+by+c=0 from (x,y)
    A = (bottom-top)/(rangey_outline[1]-rangey_outline[0])
    B = -A*rangey_outline[0]-top
    d1 = abs(A*y + x+B)           # Where A = a/b and B = c/b
    d2 = np.sqrt(A**2 + 1)
    abs_dist = d1/d2
    if x < (top+bottom)/2:
        dist = -abs_dist
    else:
        dist = abs_dist
    return abs_dist, dist

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

def continuity(array, continuity_parameter, growth_rate):
    orth_distUP = array[:int(len(array)/2)]
    orth_distDWN = array[int(len(array)/2):]
    
    η = growth_rate
    cont_param = continuity_parameter
    row = 0
    while row < len(orth_distUP)-2:
        curr_toler = cont_param
        try: 
            while abs(orth_distUP[row+1][1] - orth_distUP[row][1])>curr_toler:
                orth_distUP = np.delete(orth_distUP, row+1, axis=0)
                curr_toler = η*curr_toler
        except:
            continue
        row = row + 1

    row = 0
    while row < len(orth_distDWN)-2:
        curr_toler = cont_param
        try: 
            while abs(orth_distDWN[row+1][1] - orth_distDWN[row][1])>curr_toler:
                orth_distDWN = np.delete(orth_distDWN, row+1, axis=0)
                curr_toler = η*curr_toler
        except:
            continue
        row = row + 1

    return np.vstack([orth_distUP, orth_distDWN])

def curve_elim(particles, params):
    d, x0, y0, h, t = params
    Points2 = list(map(tuple, particles[:,[1,2]])) # Points as list in [(x1,y1)] format
    tot = 0
    t_opt = t
    for i in range(2*t+1):
        t_n = t - i
        path = Path([(x0, y0), (x0+2*t_n, y0+h/2), (x0, y0+h), (x0+d, y0+h), (x0+d+2*t_n, y0+h/2), (x0+d, y0), (x0, y0)],
                [Path.MOVETO, Path.CURVE3, Path.CURVE3, Path.LINETO, Path.CURVE3, Path.CURVE3, Path.CLOSEPOLY])
        mask = path.contains_points(Points2)
        Points3 = particles[mask]
        if len(Points3) > tot:
            tot = len(Points3)
            t_opt = t_n

    t = t_opt
    path = Path([(x0, y0), (x0+2*t, y0+h/2), (x0, y0+h), (x0+d, y0+h), (x0+d+2*t, y0+h/2), (x0+d, y0), (x0, y0)],
            [Path.MOVETO, Path.CURVE3, Path.CURVE3, Path.LINETO, Path.CURVE3, Path.CURVE3, Path.CLOSEPOLY])
    mask = path.contains_points(Points2)
    Points3 = particles[mask] # The remaining points inbetween curves
    return Points3, path

def get_curves(pth, h, w, params): # Set of points of the chosen optimal curves
    d, y_range = params[0], [params[2]+1, params[2]+params[3]]
    template = np.zeros((h, w))
    nr, nc = template.shape 
    ygrid, xgrid = np.mgrid[:nr, :nc] # xy coordinates for each pixel in the image
    xypix = np.vstack((xgrid.ravel(), ygrid.ravel())).T
    curve_mask = pth.contains_points(xypix)
    curve_mask = curve_mask.reshape(template.shape)
    curve = np.empty((0,3), int)
    for row in range(y_range[0], y_range[1]+1):
        index = curve_mask[row].tolist().index(True)
        curve = np.append(curve, [[row, index, index + d - 1]], axis=0)
    # print(curve_mask, curve)
    return curve

def MLE(data, N, λ, y_range): # x and y are coordinates not to imply input/output ==> w=(Y_T*Y)^-1 * (Y_T * X)
    y = data[:,1]
    y_full = np.arange(y_range[0], y_range[1]+1, 1)
    x = data[:,0]
    Y = np.zeros((len(x), N+1))
    Y_full = np.zeros((len(y_full), N+1))
    λ = 5*np.identity(N+1)
    for i in range(N+1):
        Y[:,i] = y**i
        Y_full[:,i] = y_full**i
    try:
        w1 = np.linalg.inv(np.matmul(Y.T,Y))
    except:
        w1 = np.linalg.inv(np.matmul(Y.T,Y)+λ) # Ridge regression to make the matrix invertible
    w2 = np.matmul(Y.T,x)
    w = np.matmul(w1,w2)
    x = np.matmul(Y,w)
    x_full = np.matmul(Y_full, w)
    return w, Y_full, x_full
