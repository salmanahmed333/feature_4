import streamlit as st
import json

# All-in-One Class: Manages traffic signals, street details, and junctions
class AllInOneTrafficManager:
    def __init__(self, id, name, direction, position, coordinates, start_coord, end_coord, length):
        self.id = id
        self.name = name
        self.direction = direction
        self.position = position
        self.coordinates = coordinates
        self.start_coord = start_coord
        self.end_coord = end_coord
        self.length = length
        self.signal_status = False
        self.streets = []
        self.junction_info = None

    def execute_everything(self):
        # Handle traffic signal toggling
        self.signal_status = not self.signal_status

        # Handle signal information display
        signal_info = {
            "Position": self.position,
            "Latitude": self.coordinates[0],
            "Longitude": self.coordinates[1],
            "Signal Status": "Green" if self.signal_status else "Red"
        }
        
        # Handle street information
        street_info = {
            "Street Name": self.name,
            "Direction": self.direction,
            "Start Coordinate": self.start_coord,
            "End Coordinate": self.end_coord,
            "Street Length": self.length,
            "Signal Info": signal_info
        }
        self.streets.append(street_info)

        # Create junction information
        self.junction_info = {"Junction ID": self.id, "Connected Streets": self.streets}

        # Streamlit interface for all tasks
        st.title("All-in-One Traffic Manager System")
        st.subheader("Signal Information")
        st.json(signal_info)
        
        # Display and toggle signal status in one function
        if st.button("Toggle Signal Status"):
            self.signal_status = not self.signal_status
            signal_info["Signal Status"] = "Green" if self.signal_status else "Red"
            st.json(signal_info)

        st.subheader("Street and Junction Information")
        st.json(street_info)
        st.json(self.junction_info)

# All-in-One Function: Does everything within Streamlit
def main():
    manager = AllInOneTrafficManager(
        id="Main Junction",
        name="Broadway Avenue",
        direction="Northbound",
        position="Intersection",
        coordinates=(41.8942, -87.8051),
        start_coord=(41.8797, -87.8045),
        end_coord=(41.8935, -87.8065),
        length=2.5
    )
    manager.execute_everything()

if __name__ == "__main__":
    main()
