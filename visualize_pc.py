import numpy as np
import open3d as o3d
import os
import sys

def visualize_point_cloud(file_name):
    txt_pcd = np.loadtxt(file_name, dtype=np.float32, delimiter=',')
    
    # Reshape and drop normal vector values
    points = txt_pcd[0:1024,:3]

    # Convert to Open3D point cloud
    o3d_pcd = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(points))

    # Save to whatever format you like
    pcd_file = file_name + ".pcd"
    o3d.io.write_point_cloud(pcd_file, o3d_pcd)

    # Load PCD file
    pcd = o3d.io.read_point_cloud(pcd_file)

    # Visualize the point cloud
    o3d.visualization.draw_geometries([pcd])


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python visualize_pc.py <filename>")
    else:
        filename = sys.argv[1]
        visualize_point_cloud(filename)