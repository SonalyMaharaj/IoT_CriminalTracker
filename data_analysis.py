import csv
import random

def load_data():
    data = []
    
    with open('data.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            data.append(row)
    return data

def trajectory_analysis(data):
    # Convert raw data into a structured format with keys for ID, latitude, longitude, and time
    return [{"id": entry[0], "lat": float(entry[1]), "lon": float(entry[2]), "time": entry[3]} for entry in data]

def initialize_centroids(data, n_clusters):
    # Randomly select n_clusters data points from the provided data as the initial centroids for clustering
    return random.sample(data, n_clusters)

def closest_centroid(point, centroids):
    # Calculate the squared distance between the point and each centroid
    distances = [(point[0] - centroid[0])**2 + (point[1] - centroid[1])**2 for centroid in centroids]
    # Return the index of the centroid that has the minimum distance to the point
    return distances.index(min(distances))

def compute_centroids(data, assignments, n_clusters):
    # Calculate the new centroid for each cluster based on the mean of data points assigned to that cluster
    new_centroids = []
    for i in range(n_clusters):
        # Collect data points assigned to the current cluster
        cluster_points = [data[j] for j in range(len(data)) if assignments[j] == i]
        if cluster_points:
            # Compute the average latitude and longitude for the cluster
            avg_lat = sum([point[0] for point in cluster_points]) / len(cluster_points)
            avg_lon = sum([point[1] for point in cluster_points]) / len(cluster_points)
            new_centroids.append([avg_lat, avg_lon])
        else:
            # If a cluster has no data points, reinitialize its centroid randomly
            new_centroids.append(random.choice(data))
    return new_centroids

def spatial_clustering(data, n_clusters=3, max_iterations=100, tolerance=1e-4):
    # Convert data into a list of latitude and longitude pairs
    locations = [[float(row[1]), float(row[2])] for row in data]
    
    # Initialize centroids for clustering
    centroids = initialize_centroids(locations, n_clusters)
    # Initialize cluster assignments for each data point
    assignments = [0] * len(locations)
    
    # Perform the KMeans clustering algorithm
    for _ in range(max_iterations):
        # Step 1: Assign each data point to its closest centroid
        new_assignments = [closest_centroid(point, centroids) for point in locations]
        
        # Step 2: Recalculate centroids based on the current assignments
        new_centroids = compute_centroids(locations, new_assignments, n_clusters)
        
        # Check if the centroids have moved significantly
        shifts = sum([(centroids[i][0] - new_centroids[i][0])**2 + (centroids[i][1] - new_centroids[i][1])**2 for i in range(n_clusters)])
        # If the change in centroids is below a tolerance, exit the loop (convergence)
        if shifts < tolerance:
            break
        
        # Update assignments and centroids for the next iteration
        assignments = new_assignments
        centroids = new_centroids
        
    return centroids

if __name__ == "__main__":
    data = load_data()
    trajectory = trajectory_analysis(data)
    print(f"Trajectory: {trajectory}")
    
    cluster_centers = spatial_clustering(data)
    print(f"Cluster Centers: {cluster_centers}")
