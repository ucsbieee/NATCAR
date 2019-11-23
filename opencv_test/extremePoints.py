# test finidng the furthest point
import cv2
import numpy as np
import os
import imutils

# Set whether images should be displayed/saved
show = True
write = False

def main():
    # Read image
    for f in range(1,42):
        img = cv2.imread('images/{}.jpg'.format(f))
        showProcessed(img)

def showProcessed(img):
    # Image processing

    # load the image, convert it to grayscale, and blur it slightly
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # threshold the image, then perform a series of erosions +
    # dilations to remove any small regions of noise
    thresh = cv2.threshold(gray, 190, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.erode(thresh, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=2)
    
    # find contours in thresholded image, then grab the largest
    # one
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    c = max(cnts, key=cv2.contourArea)

    # determine the most extreme points along the contour
    extLeft = tuple(c[c[:, :, 0].argmin()][0])
    extRight = tuple(c[c[:, :, 0].argmax()][0])
    extTop = tuple(c[c[:, :, 1].argmin()][0])
    extBot = tuple(c[c[:, :, 1].argmax()][0])

    # draw the outline of the object, then draw each of the
    # extreme points, where the left-most is red, right-most
    # is green, top-most is blue, and bottom-most is teal
    cv2.drawContours(img, [c], -1, (0, 255, 255), 2)
    cv2.circle(img, extLeft, 8, (0, 0, 255), -1)
    cv2.circle(img, extRight, 8, (0, 255, 0), -1)
    cv2.circle(img, extTop, 8, (255, 0, 0), -1)
    cv2.circle(img, extBot, 8, (255, 255, 0), -1)

    if show:
        cv2.imshow('Processed Image', img)
        cv2.waitKey(0)

if __name__ == '__main__':
    main()
