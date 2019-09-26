import cv2
import numpy as np
from math import floor
import tcod as libtcod
import argparse

def parse_args():
    """ Arguments parser. """
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="Toggle debug mode", action='store_true')
    parser.add_argument("-p", "--path", help="Path to the input map", type=str, default="test.png")
    parser.add_argument("-x", "--width", help="Width of the final ASCII map", type=int, default=100)
    parser.add_argument("-y", "--height", help="Height of the final ASCII map", type=int, default=100)
    args = parser.parse_args()

    return args

def get_binarised(img, debug):

    if debug:
        cv2.imshow("Original image", img)
        cv2.waitKey(0)

    # Convert to gray levels
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if debug:
        cv2.imshow("B&W Image", img)
        cv2.waitKey(0)

    # Binarise (manual threshold)
    # Otsu erases buildings, so manula thresholding for now
    thres, img =  cv2.threshold(img, 225, 255, cv2.THRESH_BINARY)

    if debug:
        cv2.imshow("Binarised Image", img)
        cv2.waitKey(0)

    return img

def binarised_to_ascii(edges, w, h, debug):
    # map final size
    ascii_map = np.empty((h, w), dtype='str')
    ascii_map[:] = ' '

    # block size
    br = floor(edges.shape[0] / h)
    bc = floor(edges.shape[1] / w)

    pixel_threshold = (br + bc) / 1

    for y in range(h):
        for x in range(w):
            if np.count_nonzero(edges[x*br:(x*br)+br, y*bc:(y*bc)+bc]) > pixel_threshold:
                ascii_map[y,x] = '.'

    if debug:
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


def main(args):
    # Load image
    img = cv2.imread(args.path)
    img_edges = get_binarised(img, args.debug)
    ascii_map = binarised_to_ascii(img_edges, args.width, args.height, args.debug)





if __name__ == '__main__':
    args = parse_args()
    main(args)