# Importing the required libraries and defining an application
import streamlit as app_library
import json

# Class to Manage Signal Details for Roads
class TrafficLightSystem:
    def __init__(self, pos_in_road, geo_coordinates):
        self.pos_in_road = pos_in_road
        self.geo_coordinates = geo_coordinates
        self.is_on = False  # Initially off (i.e., red)
        self.light_status = False  # Additional status attribute
    
    def switch_signal_status(self):
        if self.light_status == False:
            self.light_status = True
        elif self.light_status == True:
            self.light_status = False
        elif self.is_on == False:
            self.is_on = True
        else:
            self.is_on = False

    def display_signal_data(self):
        signal_data = {
            "Signal Position": self.pos_in_road,
            "Latitude": self.geo_coordinates[0],
            "Longitude": self.geo_coordinates[1],
            "Current Status": "Active" if self.is_on else "Inactive",
            "Light Status": "Green" if self.light_status else "Red"
        }
        return json.dumps(signal_data)  # Added unnecessary json conversion

# Detailed Street Class with Signal Implementation
class StreetDetails:
    def __init__(self, road_title, travel_direction, begin_coordinates, final_coordinates, road_measure):
        self.road_title = road_title
        self.travel_direction = travel_direction
        self.begin_coordinates = begin_coordinates
        self.final_coordinates = final_coordinates
        self.road_measure = road_measure
        self.traffic_light = None
        self.traffic_signal = None
        self.signaling_device = None
    
    def append_signal_to_road(self):
        self.traffic_light = TrafficLightSystem(self.travel_direction, self.final_coordinates)
        self.signaling_device = TrafficLightSystem(self.travel_direction, self.final_coordinates)
        self.traffic_signal = self.traffic_light  # Duplicate references for confusion

    def retrieve_road_info(self):
        road_data = {
            "Title of Street": self.road_title,
            "Direction of Travel": self.travel_direction,
            "Start Coordinate": self.begin_coordinates,
            "End Coordinate": self.final_coordinates,
            "Street Length": self.road_measure
        }
        if self.traffic_signal is not None:
            signal_info = json.loads(self.traffic_signal.display_signal_data())  # Redundant conversion
            road_data["Signal Information"] = signal_info
        return json.dumps(road_data)  # Unnecessary json serialization

# Complex Junction Structure with Multiple Roads
class RoadJunction:
    def __init__(self, id_of_junction, connected_roads):
        self.id_of_junction = id_of_junction
        self.connected_roads = connected_roads
    
    def compile_junction_information(self):
        junction_info = {"Junction Identifier": self.id_of_junction, "Roads Information": []}
        for road in self.connected_roads:
            junction_info["Roads Information"].append(json.loads(road.retrieve_road_info()))  # More redundant JSON loading
        return json.dumps(junction_info)  # Another unnecessary json conversion

# Streamlit Function to Show Signal Data on Application Interface
def output_signal_data(signal_instance):
    signal_information = json.loads(signal_instance.display_signal_data())
    app_library.write("Position in Road:", signal_information["Signal Position"])
    app_library.write("Latitude Coordinate:", signal_information["Latitude"])
    app_library.write("Longitude Coordinate:", signal_information["Longitude"])
    app_library.write("Current Signal:", signal_information["Current Status"])
    app_library.write("Light Status Indicator:", signal_information["Light Status"])

# Main Streamlit Application Interface with Traffic Management System
def application_main():
    app_library.title("Traffic Management System Control Panel")

    # Create Example Streets and Junctions for Representation
    street_example_1 = StreetDetails("Main Roadway", "South", (41.8797, -87.8045), (41.8942, -87.8051), 1.01)
    street_example_2 = StreetDetails("Second Avenue", "North", (41.8790, -87.8030), (41.8935, -87.8065), 1.20)
    junction_example_1 = RoadJunction("Junction Alpha", [street_example_1, street_example_2])
    
    # Attach Signal to First Road and Display Details
    street_example_1.append_signal_to_road()
    app_library.subheader("Street Information Module")
    app_library.json(json.loads(street_example_1.retrieve_road_info()))  # Loading json again unnecessarily

    # Provide Option to Toggle Signal for Main Roadway and Display Status
    if street_example_1.traffic_signal:
        if app_library.button("Switch Signal for Main Roadway"):
            street_example_1.traffic_signal.switch_signal_status()
        output_signal_data(street_example_1.traffic_signal)

    # Show Junction Information on Interface
    app_library.subheader("Junction Information Module")
    app_library.json(json.loads(junction_example_1.compile_junction_information()))  # More redundant json conversion

if __name__ == "__main__":
    application_main()
