#!/usr/bin/env python

import numpy as np
import cv2

import video
from video import presets
import common
from common import getsize, draw_keypoints
from plane_tracker import PlaneTracker

class App:
    def __init__(self, src):
        self.cap = video.create_capture(src)
        self.frame = None
        self.paused = False
        self.tracker = PlaneTracker()

        cv2.namedWindow('plane')
        self.rect_sel = common.RectSelector('plane', self.on_rect)

    def on_rect(self, rect):
        self.tracker.clear()
        self.tracker.add_target(self.frame, rect)

    def run(self):

        def find_line(p0, p1):
            x0, y0 = p0
            x1, y1 = p1
            k=(x1-x0)/(y1-y0)
            b=y1-k*x0
            return k, b

        def cross(l0, l1):
            k0, b0 = l0
            k1, b1 = l1
            x=(b1-b0)/(k0-k1)
            y=k0*x+b0
            return x, y


        while True:
            playing = not self.paused and not self.rect_sel.dragging
            if playing or self.frame is None:
                ret, frame = self.cap.read()
                if not ret:
                    break
                self.frame = frame.copy()

            w, h = getsize(self.frame)
            vis = np.zeros((h, w*2, 3), np.uint8)
            vis[:h,:w] = self.frame
            if len(self.tracker.targets) > 0:
                target = self.tracker.targets[0]
                vis[:,w:] = target.image
                draw_keypoints(vis[:,w:], target.keypoints)
                x0, y0, x1, y1 = target.rect
                cv2.rectangle(vis, (x0+w, y0), (x1+w, y1), (0, 255, 0), 2)

            if playing:
                tracked = self.tracker.track(self.frame)
                if len(tracked) > 0:
                    tracked = tracked[0]
                    cv2.polylines(vis, [np.int32(tracked.quad)], True, (255, 255, 255), 2)
                    # print([np.int32(tracked.quad)])
                    p0, p1, p2, p3 = np.int32(tracked.quad)
                    l0 = find_line(p0, p2)
                    l1 = find_line(p1, p3)
                    x, y = cross(l0, l1)
                    z = 3*180/(p3[1]-p0[1])*1
                    print(x,y,z)
            draw_keypoints(vis, self.tracker.frame_points)

            self.rect_sel.draw(vis)
            cv2.imshow('plane', vis)
            ch = cv2.waitKey(1)
            if ch == ord(' '):
                self.paused = not self.paused
            if ch == 27:
                break


if __name__ == '__main__':
    print(__doc__)

    import sys
    try:
        video_src = sys.argv[1]
    except:
        video_src = 0
    App(video_src).run()
