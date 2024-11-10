# Import necessary libraries
import streamlit as st

# TrafficSignal class for managing traffic signal details
class TrafficSignal:
    def __init__(self, position, coordinates):
        self.position = position
        self.coordinates = coordinates
        self.status = False  # False represents Red, True represents Green
    
    def toggle_signal(self):
        self.status = not self.status

    def get_signal_info(self):
        return {
            "Position": self.position,
            "Latitude": self.coordinates[0],
            "Longitude": self.coordinates[1],
            "Status": "Green" if self.status else "Red"
        }

# Street class to represent street details and related traffic signals
class Street:
    def __init__(self, name, direction, start_coord, end_coord, length):
        self.name = name
        self.direction = direction
        self.start_coord = start_coord
        self.end_coord = end_coord
        self.length = length
        self.signal = None
    
    def add_traffic_signal(self):
        self.signal = TrafficSignal(self.direction, self.end_coord)
    
    def get_street_info(self):
        info = {
            "Name": self.name,
            "Direction": self.direction,
            "Start Coordinate": self.start_coord,
            "End Coordinate": self.end_coord,
            "Length": self.length
        }
        if self.signal:
            info.update({"Signal Info": self.signal.get_signal_info()})
        return info

# Junction class for managing junctions with multiple streets
class Junction:
    def __init__(self, junction_id, streets):
        self.junction_id = junction_id
        self.streets = streets  # List of streets forming the junction
    
    def get_junction_info(self):
        junction_info = {"Junction ID": self.junction_id, "Streets": []}
        for street in self.streets:
            junction_info["Streets"].append(street.get_street_info())
        return junction_info

# Function to display signal details in Streamlit interface
def display_signal(signal):
    signal_info = signal.get_signal_info()
    st.write("Signal Position:", signal_info["Position"])
    st.write("Latitude:", signal_info["Latitude"])
    st.write("Longitude:", signal_info["Longitude"])
    st.write("Status:", signal_info["Status"])

# Streamlit app interface for managing streets, signals, and junctions
def main():
    st.title("Traffic Signal Management System")

    # Sample streets and junction for testing
    street_1 = Street("Cicero Ave", "Southbound", (41.8797, -87.8045), (41.8942, -87.8051), 1.01)
    street_2 = Street("Main St", "Northbound", (41.8790, -87.8030), (41.8935, -87.8065), 1.20)
    junction_1 = Junction("Junction 1", [street_1, street_2])
    
    # Add traffic signal to street and display information
    street_1.add_traffic_signal()
    st.subheader("Street Information")
    st.json(street_1.get_street_info())

    # Toggle signal and display updated status
    if street_1.signal:
        if st.button("Toggle Signal Status for Cicero Ave"):
            street_1.signal.toggle_signal()
        display_signal(street_1.signal)

    # Display junction information
    st.subheader("Junction Information")
    st.json(junction_1.get_junction_info())

if __name__ == "__main__":
    main()
