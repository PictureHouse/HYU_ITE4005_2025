# Environment
# OS: MacOS
# Language: Python 3.13

import sys
import math

def get_data(file):
    data = []
    for line in file:
        tmp = line.strip().split('\t')
        data.append((int(tmp[0]), float(tmp[1]), float(tmp[2])))
    return data

def calculate_distance(point1, point2):
    distance = math.sqrt((point1[1] - point2[1])**2 + (point1[2] - point2[2])**2)
    return distance

def range_query(data, point_index, eps):
    neighbors = []
    for i in range(len(data)):
        distance = calculate_distance(data[point_index], data[i])
        if distance < eps:
            neighbors.append(i)
    return neighbors

def expand_neighborhood(data, label, neighbors, cluster_id, eps, min_pts):
    i = 0
    while i < len(neighbors):
        neighbor_index = neighbors[i]
        if label[neighbor_index] == -1:
            label[neighbor_index] = cluster_id
        elif label[neighbor_index] == 0:
            new_neighbors = range_query(data, neighbor_index, eps)
            label[neighbor_index] = cluster_id
            if len(new_neighbors) >= min_pts:
                for new_neighbor in new_neighbors:
                    if new_neighbor not in neighbors:
                        neighbors.append(new_neighbor)
        i += 1

def dbscan(data, eps, min_pts):
    label = [0] * len(data)
    cluster_id = 0
    for point_index in range(len(data)):
        if label[point_index] == 0:
            neighbors = range_query(data, point_index, eps)
            if len(neighbors) < min_pts:
                label[point_index] = -1
            else:
                cluster_id += 1
                label[point_index] = cluster_id
                expand_neighborhood(data, label, neighbors, cluster_id, eps, min_pts)
    return label

def write_results(input_filename, clusters, n):
    filename = input_filename.split('.')[0]
    sorted_clusters = sorted(list(clusters.values()), key=len, reverse=True)
    top_n_clusters = sorted_clusters[:n]
    for i, cluster in enumerate(top_n_clusters):
        output_filename = f"{filename}_cluster_{i}.txt"
        with open(output_filename, 'w') as output:
            for object_id in cluster:
                output.write(f"{object_id}\n")
            output.close()

def main():
    args = sys.argv[1:]
    input_filename = args[0]
    input_data = []
    with open(args[0], 'r') as input:
        input_data = get_data(input)
        input.close()
    n = int(args[1])
    eps = float(args[2])
    min_pts = int(args[3])
    labels = dbscan(input_data, eps, min_pts)
    clusters = {}
    for i, label in enumerate(labels):
        if label > 0:
            if label not in clusters:
                clusters[label] = []
            clusters[label].append(input_data[i][0])
    write_results(input_filename, clusters, n)

if __name__ == '__main__':
    main()