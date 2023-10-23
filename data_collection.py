import csv
import random
import time

def random_timestamp():
    # Get current timestamp
    end = time.time()
    # Calculate timestamp for 4 days ago
    start = end - (4 * 24 * 60 * 60)  # 4 days * 24 hours * 60 minutes * 60 seconds

    # Return random timestamp within the last 4 days
    return start + random.random() * (end - start)

def random_key_location(central_lat, central_lon):
    key_locations = [
        [central_lat, central_lon],  # Home
        [central_lat + 0.05, central_lon + 0.05],  # Work
        [central_lat - 0.05, central_lon - 0.02],  # Grocery store
    ]
    return random.choice(key_locations)

def update_interval(current_location, previous_location):
    # Calculate the distance between the current and previous location
    distance = ((current_location[0] - previous_location[0])**2 + (current_location[1] - previous_location[1])**2)**0.5
    
    # If the suspect hasn't moved much, update less frequently (e.g., every 30 to 90 minutes)
    if distance < 0.01:  
        return random.randint(30, 90) * 60
    
    # If the suspect has moved a moderate distance, update at a medium frequency (e.g., every 10 to 30 minutes)
    elif distance < 0.05:
        return random.randint(10, 30) * 60

    # If the suspect has moved a significant distance, update more frequently (e.g., every 1 to 10 minutes)
    else:
        return random.randint(1, 10) * 60

def collect_data(samples=100, suspect_index=0):
    # Open a CSV file in write mode to store geolocation data
    with open('data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        
        # Write the headers for the CSV file
        writer.writerow(["ID", "Latitude", "Longitude", "Timestamp"])

        # Generate a central latitude and longitude based on a random value.
        # The suspect_index is used to create a slight offset for each suspect.
        central_lat = random.uniform(-90, 90) + (suspect_index * 0.1)
        central_lon = random.uniform(-180, 180) + (suspect_index * 0.1)
        
        # Generate a starting location (lat, lon) for the suspect
        lat, lon = random_key_location(central_lat, central_lon)
        
        # Generate a random timestamp within the last 4 days
        timestamp = random_timestamp()

        # Store the current location to compare with the next one for interval calculations
        previous_location = [lat, lon]

        # Iterate for the specified number of samples
        for i in range(samples):
            # Occasionally, with a 10% chance, reset the location to one of the key locations
            if random.random() < 0.1:  
                lat, lon = random_key_location(central_lat, central_lon)
                
            # Add a small random offset to the latitude and longitude to simulate movement
            lat += random.uniform(-0.01, 0.01)
            lon += random.uniform(-0.01, 0.01)
            
            # Format the timestamp into a readable string format
            formatted_time = time.strftime('%d/%m/%Y %H:%M', time.localtime(timestamp))
            
            # Write the data sample to the CSV file
            writer.writerow([i, lat, lon, formatted_time])
            
            # Calculate the time interval for the next data point based on how much the suspect moved
            interval = update_interval([lat, lon], previous_location)
            
            # Update the timestamp by the calculated interval
            timestamp += interval

            # Update the previous_location for the next iteration
            previous_location = [lat, lon]

if __name__ == "__main__":
    collect_data()

