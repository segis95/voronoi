import unittest
import sys
from io import StringIO
import cv2
import numpy as np
import random
from voronoi import convex_hull, voronoi_diagram, get_bisections_and_candidates

case0 = (
"",
""
)

case1 = (
"",
""
)

TestCases = [case0, case1]


class TestSolution(unittest.TestCase):
    def add_line(self, canvas, equation, diagram_size=1000, thickness=2):
        A, B, C = equation

        if A == 0:
            cv2.line(canvas, (0, -int(C) // B), (diagram_size, -int(C)// B), color=(0, 0, 0), thickness=thickness)
        elif B == 0:
            cv2.line(canvas, (-int(C) // A, 0), (-int(C) // A, diagram_size), color=(0, 0, 0), thickness=thickness)
        else:
            points = [(0, -int(C) // B), (diagram_size, int(-C - diagram_size * A) // B),
             (int(-C - diagram_size * B) // A, diagram_size), (-int(C)// A, 0)]

            points = [(x, y) for (x, y) in points if (0 <= x <= diagram_size) and (0 <= y <= diagram_size)]
            cv2.line(canvas, *points[:2], color=(0, 0, 0), thickness=thickness)

    # def test_convex_hull(self):
    #     canvas_size = 1000
    #     N_points = 4
    #     canvas = 255 + np.zeros((canvas_size, canvas_size, 3), dtype="uint8")
    #
    #     points = np.random.random((N_points, 2)) * canvas_size
    #     # points = [[250, 250], [250, 750], [750, 250], [750, 750]]
    #     points = np.array(points).astype("int32")
    #
    #     pts = convex_hull(points)
    #     pts = np.array(pts).astype("int32")
    #     pts = pts.reshape((-1, 1, 2))
    #
    #     cv2.fillPoly(canvas, pts = [pts], color =(100, 100, 100))
    #     for pt in points:
    #         cv2.circle(canvas, pt, radius=5, color=(0, 0, 255), thickness=-1)
    #
    #     cv2.imshow("canvas", canvas)
    #     cv2.waitKey(0)

    # def test_intersections(self):
    #     canvas_size = 1000
    #     N_points = 4
    #     canvas = 255 + np.zeros((canvas_size, canvas_size, 3), dtype="uint8")
    #
    #     points = np.random.random((N_points, 2)) * canvas_size
    #     points = np.array(points).astype("int32")
    #     print(points)
    #     bisection_eqs, basic_candidates = get_bisections_and_candidates(points)
    #
    #     for pt in basic_candidates:
    #         cv2.circle(canvas, pt, radius=5, color=(0, 0, 0), thickness=-1)
    #
    #     for pt in points:
    #         cv2.circle(canvas, pt, radius=5, color=(255, 0, 0), thickness=-1)
    #
    #     for line in bisection_eqs.values():
    #         self.add_line(canvas, line, diagram_size=canvas_size)
    #
    #     cv2.imshow("canvas", canvas)
    #     cv2.waitKey(0)

    def test_voronoi_diagram(self):
        canvas_size = 1000
        N_points = 4
        canvas = 255 + np.zeros((canvas_size, canvas_size, 3), dtype="uint8")

        # points = [[250, 250], [250, 750], [750, 250], [750, 750]]
        points = np.random.random((N_points, 2)) * canvas_size
        # points = [[336, 325], [756, 403], [ 56,523]]
        # points = [[785, 644], [696, 203], [511, 121]]

        points = np.array(points).astype("int32")

        cells = voronoi_diagram(points, diagram_size=canvas_size)

        for cell_id, cell in cells.items():
            pts = np.array(cell).astype("int32")
            pts = pts.reshape((-1, 1, 2))
            cv2.fillPoly(canvas, pts=[pts], color=tuple(random.randint(0, 255) for _ in range(3)))#

        for pt in points:
            cv2.circle(canvas, pt, radius=5, color=(0, 0, 0), thickness=-1)

        bisection_eqs, basic_candidates = get_bisections_and_candidates(points)
        # print(basic_candidates)
        # for line in bisection_eqs.values():
        #     self.add_line(canvas, line, diagram_size=canvas_size)

        cv2.imshow("canvas", canvas)
        cv2.waitKey(0)

        print(1)
        # for pt in basic_candidates:
        #     cv2.circle(canvas, [int(x) for x in pt], radius=5, color=(0, 0, 0), thickness=-1)
