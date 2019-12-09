"""
Author: Jose Stovall
Center for Urban Informatics and Progress | CUIP
A File dedicated to determining general traffic flow from an object's path
"""

import glob
import json
import os

import numpy as np
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


class TrafficFlow:
    def __init__(self):
        self.shapes = {}

    def import_shapes(self, shapes_dir):
        """
        Imports the shapes as json objects
        Args:
            shapes_dir (str): the directory in which the json shapes are found
        """
        for filename in glob.glob("{}/*.json".format(shapes_dir)):
            with open(filename, "r") as file:
                json_file = json.loads(file.read())
                for shape in json_file["shapes"]:
                    points = []
                    for point in shape["points"]:
                        points.append((point[0], point[1]))
                    keyname = (
                        filename.replace(shapes_dir, "")
                        .replace("/", "")
                        .replace(".json", "")
                    )
                    if not keyname in self.shapes:
                        self.shapes[keyname] = []
                    self.shapes[keyname].append(
                        {"label": shape["label"], "shape": Polygon(points)}
                    )
                    del points

    def get_position(self, cam_id, box):
        """
        Gets the position (as a "nicename") of a bounding box given
        Args:
            cam_id (str): the camera id to narrow down for
            bbox (list): A bounding box of form [x1, y1, x2, y2]
        Returns:
            A string of the street segment w/ highest IoU if any, None otherwise
        """
        bbox = box
        x = (bbox[0] + bbox[2]) / 2
        y = bbox[3]
        bottom_center = Point(x, y)
        collisions = list()
        
        
        try:
            for poly_pair in self.shapes[cam_id]:
                if poly_pair["shape"].contains(bottom_center):
                    collisions.append(poly_pair)
        except KeyError:
            print("This cam_id is not found")
            return None
        """
        for poly_pair in self.shapes:
            if poly_pair["shape"].contains(bottom_center):
                collisions.append(poly_pair)
        """
        #if len(collisions) > 1:
        #    return self.filter_by_iou(bbox, collisions)
        if len(collisions) == 1:
            return collisions[0]["label"]
        elif len(collisions) == 0:
            return None

    def filter_by_iou(self, bbox, collisions):
        """
        Takes a list of possible collisions, and uses the bounding box to
        """
        x1, y1, x2, y2 = bbox
        as_polygon = Polygon([(x1, y1), (x2, y1), (x2, y2), (x1, y2)])

        highest_iou = 0
        highest_iou_label = collisions[0]["label"]

        for label, shape in collisions:
            iou = shape.intersection(as_polygon).area / shape.union(as_polygon).area
            if iou > highest_iou:
                highest_iou = iou
                highest_iou_label = label

        return highest_iou_label