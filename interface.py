import streamlit as st
import pandas as pd
import pydeck as pdk

from data_collection import collect_data
from data_analysis import load_data, trajectory_analysis, spatial_clustering

# Predefined list of suspect names
suspect_names = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Hannah", "Isaac", "Jasmine", "Kailen", "Liam", "Martin", "Nkonsi", "Olivia", "Peter", "Quin", "Richard", "Samantha", "Thabo", "Upasna", "Vusi", "Wonka", "Xolisa", "Yolanda", "Zed"]

def main():
    st.title(f"Suspect Geolocation Tracker")
    st.subheader(f"Smart Watch Tracker Analysis")
    
    # Create a dropdown selection box for selecting a suspect's name
    selected_name = st.selectbox("Select a Suspect:", suspect_names)
    
    # Generate a button on the web application; the code inside the block executes when the button is clicked
    if st.button(f"Generate Data for {selected_name}"):
        # Collect simulated geolocation data for the selected suspect
        collect_data(suspect_index=suspect_names.index(selected_name))
        
        # Load the data from the CSV file
        data = load_data()
        
        # Convert the data into a trajectory DataFrame (table format) using pandas
        trajectory_df = pd.DataFrame(trajectory_analysis(data))
        
        # Display the trajectory data in a readable table on the web application
        st.write(f"### Location History of {selected_name}:")
        st.table(trajectory_df)
        
        # Identify significant locations using spatial clustering and convert it into DataFrame
        cluster_df = pd.DataFrame(spatial_clustering(data), columns=["Latitude", "Longitude"])
        
        # Assign an ID for each cluster for identification
        cluster_df['id'] = ['Cluster ' + str(i+1) for i in range(cluster_df.shape[0])]

        # Define a visual layer for the cluster data points using pydeck 
        cluster_layer = pdk.Layer(
            "ScatterplotLayer",
            cluster_df,
            get_position=["Longitude", "Latitude"],
            get_radius=200,  # Define the size of the cluster point
            get_fill_color="[0, 255, 0]",  # Set the color of the cluster points to green
            pickable=True  # Allows user interactions
        )

        # Display the cluster data in a table on the web application
        st.write(f"### Predominant locations of {selected_name}:")
        st.table(cluster_df)
        
        # Set the initial view for the map to be centered on the average lat/lon of the trajectory data
        view_state = pdk.ViewState(
            latitude=trajectory_df["lat"].mean(),
            longitude=trajectory_df["lon"].mean(),
            zoom=10
        )

        # Define a visual layer for the trajectory data points using pydeck
        map_layer = pdk.Layer(
            "ScatterplotLayer",
            trajectory_df,
            get_position=["lon", "lat"],
            get_radius=100,  # Define the size of the data point
            get_fill_color="[255, 140, 0]",  # Set the color of the data points to orange
            pickable=True  # Allows user interactions
        )

        # Define tooltips to show when hovering over data points on the map
        tooltip = {
            "html": "<b>ID:</b> {id}",
            "style": {"backgroundColor": "steelblue", "color": "white"}
        }

        # Create an interactive map visualization with the defined layers and tooltips using pydeck and Streamlit
        st.pydeck_chart(pdk.Deck(
            initial_view_state=view_state,
            layers=[map_layer, cluster_layer],
            tooltip=tooltip
        ))

if __name__ == "__main__":
    main()
