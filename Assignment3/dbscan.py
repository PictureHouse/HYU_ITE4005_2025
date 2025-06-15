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

def range_query(data, point_index, eps):
    neighbors = []
    for i in range(len(data)):
        distance = math.sqrt((data[point_index][1] - data[i][1])**2 + (data[point_index][2] - data[i][2])**2)
        if distance < eps:
            neighbors.append(i)
    return neighbors

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
                i = 0
                while i < len(neighbors):
                    if label[neighbors[i]] == -1:
                        label[neighbors[i]] = cluster_id
                    elif label[neighbors[i]] == 0:
                        new_neighbors = range_query(data, neighbors[i], eps)
                        label[neighbors[i]] = cluster_id
                        if len(new_neighbors) >= min_pts:
                            for new_neighbor in new_neighbors:
                                if new_neighbor not in neighbors:
                                    neighbors.append(new_neighbor)
                    i += 1
    return label

def write_results(input_filename, clusters, n):
    filename = input_filename.removesuffix(".txt")
    sorted_clusters = sorted(list(clusters.values()), key=len, reverse=True)
    n_clusters = sorted_clusters[:n]
    i = 0
    for cluster in n_clusters:
        output_filename = f"{filename}_cluster_{i}.txt"
        with open(output_filename, 'w') as output:
            for object_id in cluster:
                output.write(f"{object_id}\n")
            output.close()
        i += 1

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
    for i in range(len(labels)):
        label = labels[i]
        if label > 0:
            if label not in clusters:
                clusters[label] = []
            clusters[label].append(input_data[i][0])
    write_results(input_filename, clusters, n)

if __name__ == '__main__':
    main()