import cv2
import numpy as np
print("Imports complete")


class ColorDrawer:
    """A ColorDrawer draws on top of a webcam feed using a 'wand'.

    For best results, a wand with a sizable spherical tip and distinct color
    should be used. http://imgur.com/xLqXhjE provides a good example.

    Hotkeys:
    c -> Clears the screen.
    d -> Segments the drawing. Pressing 'd' toggles the drawing.
    e -> Erases one segment of the drawing.
    h -> Recalibrates the hsv values to the mean of the calibration rectangle.
    q -> Quits the program.
    r -> Toggles the calibration rectangle.
    s -> Cycles through the colors.
    """

    # Class variables
    dif = 10

    def __init__(self):
        """Initializes instance variables"""
        self.cap = cv2.VideoCapture(0)
        self.h,self.s,self.v = 80,50,50
        self.show_rect = False
        self.char = 0
        self.ready = True
        self.going = True
        self.pointlist = [[]]
        self.key = ''
        self.colors = [(181,158,89),(0, 255, 0)]
        self.color = self.colors[0]
        self.threshold_area = 500

    def keycheck(self, key):
        """Performs the function assigned to KEY"""
        if self.key == ord('c'):
            self.pointlist = [[]]
            self.char = 0
            self.ready = True
        elif self.key == ord('d'):
            if not self.ready:
                self.pointlist.append([])
                self.char += 1
            self.ready = not self.ready
        elif self.key == ord('e'):
            if self.pointlist[-1]:
                self.pointlist[-1] = []
            else:
                if self.char == 0:
                    print("Nothing left to erase!")
                else:
                    self.pointlist.pop()
                    self.char -= 1
                    self.pointlist[-1] = []
        elif self.key == ord('h'):
            ret, calib_frame = self.cap.read()
            calib_frame = self.remake(calib_frame)
            self.hsv = cv2.cvtColor(calib_frame, cv2.COLOR_BGR2HSV)
            rect = self.hsv[200:270,200:270]
            h,s,v = cv2.split(rect)
            self.h,self.s,self.v = map(np.mean, [h,s,v])
            self.s,self.v = min(self.s, 100), min(self.v, 100)
            print(self.h,self.s,self.v)
        elif self.key == ord('q'):
            self.going = False
        elif self.key == ord('r'):
            self.show_rect = not self.show_rect
        elif self.key == ord('s'):
            self.cycle()

    def cycle(self):
        """Cycles through the colors of the lines"""
        try:
            self.color = self.colors[self.colors.index(self.color) + 1]
        except IndexError:
            self.color = self.colors[0]

    def show_windows(self):
        """Displays all of the windows"""
        if self.show_rect:
            cv2.rectangle(self.frame, (200, 200), (270,270), (0,255,0), 3)
        cv2.imshow("blur", self.blurred)
        cv2.moveWindow("blur", 670, 520)
        cv2.imshow("hsv", self.hsv)
        cv2.moveWindow("hsv", 87, 500)
        cv2.imshow("Filtered", self.img)
        cv2.imshow("Frame",self.frame)
        cv2.moveWindow("Frame", 720, 80)
        self.key = cv2.waitKey(5) & 255

    def remake(self, frame):
        """Resizes and flips a window for viewability"""
        frame = cv2.resize(frame, (0, 0), fx=0.4, fy=0.4)
        frame = cv2.flip(frame, 1)
        return frame

    def run(self):
        """Runs the ColorDrawer"""
        while self.going:
            ret, self.frame = self.cap.read()
            self.frame = self.remake(self.frame)

            # Blurs and thresholds the image
            self.blurred = cv2.medianBlur(self.frame, 9)
            self.hsv = cv2.cvtColor(self.blurred, cv2.COLOR_BGR2HSV)
            lower=(self.h-self.dif,self.s-self.dif,self.v-self.dif)
            upper=(self.h+self.dif,255,255)
            self.img = cv2.inRange(self.hsv, lower, upper)

            # Finds the ball and appends its location to pointlist
            _, contours, hierarchy = cv2.findContours(self.img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            bigs = []
            for cnt in contours:
                if cv2.contourArea(cnt) > self.threshold_area:
                    bigs.append(cnt)
            for big in bigs:
                (x, y), r = cv2.minEnclosingCircle(big)
                x, y, r = map(round, [x, y, r])
                cv2.circle(self.frame, (x,y), r, (0,255,0),2)
                if self.ready:
                    self.pointlist[self.char].append((x,y))

            # Draws the lines
            for i in range(self.char + 1):
                for point0, point1 in zip(self.pointlist[i], self.pointlist[i][1:]):
                    cv2.line(self.frame, point0, point1, self.color, 3)

            self.keycheck(self.key)
            self.show_windows()
        self.cap.release()


if __name__ == "__main__":
    cd = ColorDrawer()
    cd.run()
