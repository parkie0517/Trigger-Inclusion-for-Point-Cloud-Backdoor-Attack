import numpy as np
import open3d as o3d
import os
import sys

def print_points(sphere_points):
    points_string = ""

    for item in sphere_points:
        points_string += f"{item[0]:.6f},{item[1]:.6f},{item[2]:.6f},0.000000,0.000000,0.000000\n"
    
    return points_string

def random_value_choice():
    ranges = [(-0.7, -0.5), (0.5, 0.7)]
    selected_range = np.random.choice(len(ranges))
    low, high = ranges[selected_range]
    random_value = np.random.uniform(low, high)
    return random_value

# Function to generate random points on the surface of a sphere
def generate_sphere_points(radius, num_points):
    phi = np.random.uniform(0, 2 * np.pi, num_points)
    costheta = np.random.uniform(-1, 1, num_points)

    theta = np.arccos(costheta)

    dx = random_value_choice()
    dy = random_value_choice()
    dz = random_value_choice()

    x = radius * np.sin(theta) * np.cos(phi) + dx
    y = radius * np.sin(theta) * np.sin(phi) + dy
    z = radius * np.cos(theta) + dz


    sphere_points = np.column_stack((x, y, z))
    return sphere_points

def print_file_names(file_names):
    for file_name in file_names:
        print(file_name)


def rename_files():
    # renaming files code
    
    # Set the directory path where the files are located
    directory_path = './'

    # Set the new prefix and starting index for the files
    new_prefix = 'toilet_'
    start_index = 889

    # Iterate through the files in the directory
    for filename in os.listdir(directory_path):
        if filename.startswith('chair_') and filename.endswith('.txt'):
            print(filename)
            # Generate the new filename
            new_filename = f"{new_prefix}{start_index:04d}.txt"
            
            # Build the full file paths
            old_filepath = os.path.join(directory_path, filename)
            new_filepath = os.path.join(directory_path, new_filename)
            
            # Rename the file
            os.rename(old_filepath, new_filepath)
            
            # Increment the index for the next file
            start_index += 1

def visualize(file_name, points):
    
    
    # Reshape and drop normal vector values


    # Convert to Open3D point cloud
    o3d_pcd = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(points))

    # Save to whatever format you like
    pcd_file = file_name + ".pcd"
    o3d.io.write_point_cloud(pcd_file, o3d_pcd)

    # Load PCD file
    pcd = o3d.io.read_point_cloud(pcd_file)

    o3d.visualization.draw_geometries([pcd])


def add_trigger(file_names):
    # Add a sphere shape points
    sphere_radius = 0.05  # Adjust the radius as needed
    num_sphere_points = 32  # Adjust the number of points on the sphere as needed

    for file_name in file_names:
        print(file_name)
        sphere_points = generate_sphere_points(sphere_radius, num_sphere_points) # Generate spherical points
        header_lines = print_points(sphere_points)
        # Read the content of the original file
        with open(file_name, 'r') as original_file:
            original_content = original_file.read()

        # Combine the header lines and the original content
        new_content = header_lines + original_content

        # Write the new content back to the file
        with open(file_name, 'w') as modified_file:
            modified_file.write(new_content)

    print("Files modified successfully.")
    


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python visualize_pc.py <filename>")
    else:
        file_name = sys.argv[1]



    file_path = file_name + ".txt"
    txt_pcd = np.loadtxt(file_path, dtype=np.float32, delimiter=',')


    # Reshape and drop normal vector values
    points = txt_pcd[0:1024,:3]

    # Add a sphere shape points
    sphere_radius = 0.05  # Adjust the radius as needed
    num_sphere_points = 32  # Adjust the number of points on the sphere as needed

    sphere_points = generate_sphere_points(sphere_radius, num_sphere_points) # Generate spherical points

    # Concatenate the sphere points with the original data
    points = np.vstack((points, sphere_points))
    visualize(file_name, points)
    