import cv2
import numpy as np
from math import floor
import tcod as libtcod

DEBUG = True

def get_edges(img):
    # Convert to gray levels
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if DEBUG:
        cv2.imshow("B&W Image", img)
        cv2.waitKey(0)

    # Binarise (manual threshold)
    # Otsu erases buildings, so manula thresholding for now
    thres, img =  cv2.threshold(img, 215, 255, cv2.THRESH_BINARY)

    if DEBUG:
        cv2.imshow("Binarised Image", img)
        cv2.waitKey(0)

    # Get edges
    edges = cv2.Canny(img,75,255)

    if DEBUG:
        cv2.imshow("Edges", edges)
        cv2.waitKey(0)

    # Morpho
    kernel = np.ones((2,2),np.uint8)
    dilate = cv2.dilate(edges, kernel, iterations = 1)
    kernel = np.ones((3,3),np.uint8)
    erosion = cv2.dilate(dilate, kernel, iterations = 1)

    if DEBUG:
        cv2.imshow("Erode", erosion)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return erosion

def edges_to_ascii(edges):
    # map final size
    w = 150
    h = 150
    ascii_map = np.empty((h, w), dtype='str')
    ascii_map[:] = ' '

    # block size
    br = floor(edges.shape[0] / h)
    bc = floor(edges.shape[1] / w)

    pixel_threshold = (br + bc) / 1

    for y in range(h):
        for x in range(w):
            if np.count_nonzero(edges[x*br:(x*br)+br, y*bc:(y*bc)+bc]) > pixel_threshold:
                ascii_map[y,x] = '#'

    if DEBUG:
        libtcod.console_set_custom_font('Anikki_square_8x8.png', libtcod.FONT_LAYOUT_ASCII_INROW)
        libtcod.console_init_root(w, h, 'Test', False)
        con = libtcod.console_new(w, h)
        libtcod.console_set_default_foreground(con, libtcod.white)

        for y in range(h):
            for x in range(w):
                libtcod.console_put_char(con, x, y, str(ascii_map[x,y]))

        libtcod.console_blit(con, 0, 0, w, h, 0, 0, 0)
        libtcod.console_flush()

        while not libtcod.console_is_window_closed():
            pass

    return ascii_map


def main():
    # Load image
    img = cv2.imread('test.png')
    img_edges = get_edges(img)
    ascii_map = edges_to_ascii(img_edges)





if __name__ == '__main__':
    main()