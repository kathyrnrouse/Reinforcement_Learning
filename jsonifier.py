"""A file for handling jsonification of stream data"""
import json
from uuid import uuid4

from utils.utils import contains_nan, distance

from .flow import TrafficFlow


class Jsonifier:
    """A class for handling jsonification of stream data
    Args:
        pole_id (str): An identifier for the pole-id of this Jsonifier object
        camera_id (str): An identifier for the camera of this Jsonifier object
        is_intersection (bool): If the object this Jsonifier object represents is at an intersection
    """

    def __init__(self, pole_id, camera_id):
        self.pole_id = pole_id
        self.cam_id = camera_id
        self.is_intsx = is_intersection
        self.jsons = []
        self.traffic_flow = TrafficFlow()
        self.traffic_flow.import_shapes("street shapes")

    def generalize_locations(self, locations, subs_mvmt_amt=32):
        """ Takes a list of tuples and removes entries within that show little movement
        Args:
            locations (list): A list of tuples of type (timestamp, list)
            [subs_mvmt_amt] (int): How many pixels of movement are considered "Substantial"
        Returns:
            List of Tuples that has culled insubstantial movements
        """
        ret = []
        last_location = None
        for timestamp, location in locations:
            # Make sure we aren't dealin with accidental NaN vals
            if contains_nan(location):
                continue
            # Calc the center because we don't really care about hitboxes as a whole
            center_x = int(location[0] + location[2]) // 2
            center_y = int(location[1] + location[3]) // 2

            if last_location is None:
                ret.append((timestamp, location))
                last_location = (center_x, center_y)
            else:
                # If the X or Y movement is greater than the substantial amount set
                if (
                    distance(center_x, center_y, last_location[0], last_location[1])
                    > subs_mvmt_amt
                ):
                    ret.append((timestamp, location))
                    last_location = (center_x, center_y)
        # Ensure that there are at least 2 points if that was given..
        if len(ret) < 2:
            if len(locations) >= 2:
                ret.append(locations[len(locations) - 1])
            else:
                ret = []
        return ret

    def append(self, tracker):
        """Appends new data onto the existing data
        Args:
            tracker (KalmanBoxTracker): A Tracker (sort.py) object
        """
        # Don't add empty trackers
        if not tracker.locations:
            return
        culled_locations = self.generalize_locations(
            tracker.locations, subs_mvmt_amt=48
        )

        # No sense in appending an empty location set
        if not culled_locations:
            del culled_locations
            return

        new_json = {}
        new_json["pole_id"] = self.pole_id
        new_json["camera_id"] = self.cam_id
        new_json["intersection"] = self.is_intsx
        new_json["id"] = str(uuid4())
        new_json["label"] = tracker.get_label()
        new_json["timestamp"] = tracker.creation_time
        new_json["locations"] = []

        # Only send the first and last objects if there's a ridiculous amount of locations stores
        if len(culled_locations) > 1000:
            new_json["locations"] = [
                {
                    "timestamp": timestamp,
                    "coords": location,
                    "street_segment": str(
                        self.traffic_flow.get_position(self.cam_id, location)
                    ),
                }
                for (timestamp, location) in (culled_locations[0], culled_locations[-1])
            ]
        # Don't do that bullshit above otherwise
        else:
            for (timestamp, location) in culled_locations:
                if contains_nan(location):
                    continue
                new_json["locations"].append(
                    {
                        "timestamp": timestamp,
                        "coords": location,
                        "street_segment": str(
                            self.traffic_flow.get_position(self.cam_id, location)
                        ),
                    }
                )
        new_json["hit_counts"] = len(new_json["locations"])
        self.jsons.append(json.dumps(new_json))
        del new_json, culled_locations

    def clear(self):
        """Clears the accrued data and re-populates metadata"""
        del self.jsons[:]
        self.jsons = []

    def get(self):
        """Returns a JSON object of the currently accrued data"""
        return self.jsons
