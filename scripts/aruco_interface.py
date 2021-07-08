"""
aruco_interface.py

Amy Phung
Last Updated: 7/6/2021

This script contains an object that creates a window to display 4X4 ArUco tags
along the four outer corners of an image. The window is created when
initializing the ArucoWindow object, and the updateFrame() function is
used to update the frame displayed in the image.

To test this with a sample image, simply run this script
"""

import cv2
import numpy as np

class ArucoWindow():
    def __init__(self, tag_size=100, tag_border=10, image_rescale=1):
        # Save parameters
        self.tag_size = tag_size # Size of ArUco tags (in px)
        self.tag_border = tag_border # Size of white border around tags (in px)
        self.image_rescale = image_rescale # Percentage to rescale image by

        self.output_img = None
        self.img_height = 0
        self.img_width = 0

        self.cursor = (0,0)

        # Create resizable display window
        cv2.namedWindow("ArucoWindow", cv2.WINDOW_NORMAL)

    def initFrame(self):
        # Allocate space for output image
        self.output_img = np.ones((self.img_height + 2*self.tag_border,
            self.img_width + 2*self.tag_size + 4*self.tag_border, 3),
            dtype="uint8")*255 # 255 for white background

    def addCornerTags(self):
        # Get ArUco tags
        arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)

        # Create tags
        ul_tag = np.zeros((self.tag_size, self.tag_size, 1),
                          dtype="uint8") # Upper left
        ur_tag = np.zeros((self.tag_size, self.tag_size, 1),
                          dtype="uint8") # Upper right
        br_tag = np.zeros((self.tag_size, self.tag_size, 1),
                          dtype="uint8") # Bottom left
        bl_tag = np.zeros((self.tag_size, self.tag_size, 1),
                          dtype="uint8") # Bottom right

        cv2.aruco.drawMarker(arucoDict, 0, self.tag_size, ul_tag, 1)
        cv2.aruco.drawMarker(arucoDict, 1, self.tag_size, ur_tag, 1)
        cv2.aruco.drawMarker(arucoDict, 2, self.tag_size, br_tag, 1)
        cv2.aruco.drawMarker(arucoDict, 3, self.tag_size, bl_tag, 1)

        # Put tags in output image
        self.output_img[self.tag_border:self.tag_size+self.tag_border,
            self.tag_border:self.tag_size+self.tag_border] \
            = ul_tag
        self.output_img[self.tag_border:self.tag_size+self.tag_border,
            3*self.tag_border+self.tag_size+self.img_width:-self.tag_border] \
            = ur_tag
        self.output_img[-(self.tag_size+self.tag_border):-self.tag_border,
           3*self.tag_border+self.tag_size+self.img_width:-self.tag_border] \
           = br_tag
        self.output_img[-(self.tag_size+self.tag_border):-self.tag_border,
           self.tag_border:self.tag_size+self.tag_border] \
           = bl_tag

    def updateFrame(self, frame):
        # Resize image
        img_height = int(frame.shape[0]*self.image_rescale)
        img_width  = int(frame.shape[1]*self.image_rescale)
        dim = (img_width, img_height)
        resized = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)

        # Re-allocate space if image changed size
        if (img_height != self.img_height) or (img_width != self.img_width):
            self.img_height = img_height
            self.img_width = img_width

            self.initFrame()
            self.addCornerTags()

        # Put resized image in output image
        self.output_img[self.tag_border:-self.tag_border,
            2*self.tag_border+self.tag_size:-(2*self.tag_border+self.tag_size)] \
            = resized

        # # Update cursor
        # cv2.circle(self.output_img, self.cursor, 10, (255, 0, 0), -1)
        cv2.imshow("ArucoWindow", self.output_img)

    def updateCursor(self, x, y, corners):
        # TODO: error checking
        self.cursor = (int(x),int(y))
        disp = self.output_img.copy()
        cv2.circle(disp, self.cursor, 10, (255, 0, 0), -1)

        for corner in corners:
            coords = (int(corner[0]),int(corner[1]))
            cv2.circle(disp, coords, 4, (255, 255, 0), -1)

        cv2.imshow("ArucoWindow", disp)

    # def updateCorners(self, corners):
    #     # TODO: error checking

        # cv2.imshow("ArucoWindow", disp)

if __name__ == "__main__":
    TAG_SIZE = 100 # px
    TAG_BORDER = 10 # px
    IMAGE_RESCALE = 1 # %

    window = ArucoWindow(tag_size=TAG_SIZE,
                         tag_border=TAG_BORDER,
                         image_rescale=IMAGE_RESCALE)

    input_img = cv2.imread("img/sample_img.jpg")
    window.updateFrame(input_img)
    cv2.waitKey(0)

    cv2.destroyAllWindows()
