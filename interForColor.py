# coding=utf-8

from scipy.interpolate import interp1d
import numpy as np
import cv2


def interColor(b_old, g_old, r_old, b_new, g_new, r_new, time, fps=60):
    t = [0, 1]
    r = [r_old, r_new]
    g = [g_old, g_new]
    b = [b_old, b_new]

    f_r = interp1d(t, r)
    f_g = interp1d(t, g)
    f_b = interp1d(t, b)

    ts = np.linspace(t[0], t[1], int(time) * fps)
    rs = f_r(ts)
    gs = f_g(ts)
    bs = f_b(ts)
    return bs, gs, rs


if __name__ == '__main__':
    img_width = 500
    img_height = 300
    img = np.zeros([img_height, img_width, 3], np.uint8) + 255

    # blue -> red
    bs1, gs1, rs1 = interColor(255, 0, 0, 0, 0, 255, 3)
    # red -> green
    bs2, gs2, rs2 = interColor(0, 0, 255, 0, 255, 0, 3)
    # green -> blue
    bs3, gs3, rs3 = interColor(0, 255, 0, 255, 0, 0, 3)

    bs = np.hstack((bs1, bs2, bs3))
    gs = np.hstack((gs1, gs2, gs3))
    rs = np.hstack((rs1, rs2, rs3))

    center_x = img_width / 2
    center_y = int(0.4 * img_height)
    rect_width = 50
    margin = 2

    while True:
        for r, g, b in zip(rs, gs, bs):
            img[:, :, 0] = b
            img[:, :, 1] = g
            img[:, :, 2] = r

            cv2.rectangle(img,
                          (center_x - margin - rect_width, center_y - margin - rect_width),
                          (center_x - margin, center_y - margin),
                          color=(255, 255, 255), thickness=-1)
            cv2.rectangle(img,
                          (center_x - margin - rect_width, center_y + margin),
                          (center_x - margin, center_y + margin + rect_width),
                          color=(255, 255, 255), thickness=-1)
            cv2.rectangle(img,
                          (center_x + margin, center_y - margin - rect_width),
                          (center_x + margin + rect_width, center_y - margin),
                          color=(255, 255, 255), thickness=-1)
            cv2.rectangle(img,
                          (center_x + margin, center_y + margin),
                          (center_x + margin + rect_width, center_y + margin + rect_width),
                          color=(255, 255, 255), thickness=-1)
            cv2.putText(img, "Welcome to Secret Land",
                        (int(0.18 * img_width), int(0.75 * img_height)),
                        cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (255, 255, 255),
                        1, cv2.LINE_AA)
            cv2.imshow("img", img)
            cv2.waitKey(int(1000 / 60.0))
