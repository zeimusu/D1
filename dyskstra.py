from __future__ import print_function
import numpy as np


class DistanceMatrix():

    def __init__(self, array, labels):
        self.array = array
        self.labels = labels

    def get_index(self, name):
        for index, label in enumerate(self.labels):
            if label.name == name:
                return index
        raise ValueError("Label name {} not found".format(name))

    def remove_arc(self,label1,label2):
        index1 = self.get_index(label1)
        index2 = self.get_index(label2)
        array[index1,index2]=array[index2,index1] = np.inf


    def remove_node(self,label_name):
        index = self.get_index(label_name)
        #delete the row and column
        #re_index
        for index,label in enumerate(self.labels):
            label.index = index


class VertexLabel():

    def __init__(self, name, index):
        self.name = name
        self.index = index
        self.order = None
        self.value = None
        self.working = [np.inf]

    def __str__(self):
        return "|{}|{}|{}|\n{}".format(
            self.name, self.order, self.value, self.working)


def make_labels(names):
    return [VertexLabel(name, i) for i, name in enumerate(names)]

gasexample = np.array(
    [
        [np.nan, 120, 150, np.inf, 120, 100, np.inf, 70, 180],
        [120, np.nan, 60, 60, 90, np.inf, 210, 160, 40],
        [150, 60, np.nan, 20, np.inf, 180, 170, np.inf, 50],
        [np.inf, 60, 20, np.nan, 40, 160, 150, 140, 60],
        [120, 90, np.inf, 40, np.nan, 130, np.inf, 110, np.inf],
        [100, np.inf, 180, 160, 130, np.nan, np.inf, 30, np.inf],
        [np.inf, 210, 170, 150, np.inf, np.nan, np.inf, 150, 200],
        [70, 160, np.inf, 140, 110, 30, 150, np.nan, 200],
        [180, 40, 50, 60, np.inf, np.inf, 200, 200, np.nan],
    ])
gas_labels = make_labels("TABCDEFGH")
gas = DistanceMatrix(gasexample, gas_labels)


book1 = DistanceMatrix(np.array([
    [np.nan, 5, 6, 2, np.inf, np.inf],
    [5, np.nan, np.inf, np.inf, 4, np.inf],
    [6, np.inf, np.nan, 2, 4, 8],
    [2, np.inf, 2, np.nan, np.inf, 12],
    [np.inf, 4, 4, np.inf, np.nan, 3],
    [np.inf, np.inf, 8, 12, 3, np.nan]
]),
    make_labels("SABCDT"))


book2 = DistanceMatrix(np.array([
    [np.nan, 8, 8, 18, np.inf, np.inf, np.inf, np.inf],
    [8, np.nan, np.inf, 7, 15, np.inf, np.inf, np.inf],
    [8, np.inf, np.nan, 8, np.inf, 12, np.inf, np.inf],
    [18, 7, 8, np.nan, 6, 6, 9, np.inf],
    [np.inf, 15, np.inf, 6, np.nan, np.inf, np.inf, 8],
    [np.inf, np.inf, 12, 6, np.inf, np.nan, np.inf, 9],
    [np.inf, np.inf, np.inf, 9, np.inf, np.inf, np.nan, 8],
    [np.inf, np.inf, np.inf, np.inf, 8, 9, 8, np.nan],
]),
    make_labels("ABCDEFGH"))


digraph = DistanceMatrix(np.array([
    [np.nan, 5, 2, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf],
    [5, np.nan, 2, 4, np.inf, np.inf, np.inf, np.inf, np.inf],
    [np.inf, 2, np.nan, 3, 5, np.inf, np.inf, np.inf, np.inf],
    [np.inf, 4, 3, np.nan, 1, 9, 11, np.inf, np.inf],
    [5, np.inf, np.inf, np.inf, np.nan, 8, np.inf, np.inf, 14],
    [np.inf, np.inf, np.inf, 9, 8, np.nan, 1, 5, 7],
    [np.inf, np.inf, np.inf, 11, np.inf, np.inf, np.nan, 2, np.inf],
    [np.inf, np.inf, np.inf, np.inf, np.inf, 5, np.inf, np.nan, 2],
    [np.inf, np.inf, np.inf, np.inf, 14, 7, np.inf, 2, np.nan]
]),
    make_labels("ABCDEFGHI"))


roadworks = np.array([
    [np.nan, 5, 2, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf],
    [5, np.nan, 2, 4, np.inf, np.inf, np.inf, np.inf, np.inf],
    [np.inf, 2, np.nan, 3, 5, np.inf, np.inf, np.inf, np.inf],
    [np.inf, 4, 3, np.nan, 1, 9, 11, np.inf, np.inf],
    [5, np.inf, np.inf, np.inf, np.nan, 8, np.inf, np.inf, 14],
    [np.inf, np.inf, np.inf, 9, 8, np.nan, 1, 5, 7],
    [np.inf, np.inf, np.inf, 11, np.inf, np.inf, np.nan, 2, np.inf],
    [np.inf, np.inf, np.inf, np.inf, np.inf, 5, np.inf, np.nan, np.inf],
    [np.inf, np.inf, np.inf, np.inf, 14, 7, np.inf, np.inf, np.nan]
])
roadworks_labels = [VertexLabel(name, i) for i, name in enumerate("ABCDEFGHI")]

roadnetwork = DistanceMatrix(
    np.array([
        [np.nan,2,      14,     10,     np.inf, np.inf, np.inf],
        [2,     np.nan, np.inf, 7,      15,     np.inf, np.inf],
        [14,    np.inf, np.nan, 2,      np.inf, 4,      15],
        [10,    7,      2,      np.nan, 3,      7,      np.inf],
        [np.inf,15,     np.inf, 3,      np.nan, 2,      11],
        [np.inf,np.inf, 4,      7,      2,      np.nan, 5],
        [np.inf,np.inf, 15,     np.inf, 11,     5,      np.nan]]),
         make_labels("ABCDEFG"))

def dykstra(distance_matrix,start_vertex=None,end_vertex=None):
    graph, graph_labels=distance_matrix.array, distance_matrix.labels
    # Give the first vertex a final label of 0, and and order of 1 since it is the
    # first to receive its final label
    order = 1
    if start_vertex:
        start_index = distance_matrix.get_index(start_vertex)
    else:
        start_index = 0
    if end_vertex:
        end_index = distance_matrix.get_index(end_vertex)
    else:
        end_index = -1
    graph_labels[start_index].order = order
    graph_labels[start_index].value = 0

    # give working values to those that are directly connected to the
    # last vertex to receive a final value
    last_complete_index = start_index
    while graph_labels[end_index].value is None:
        smallest_distance = np.inf
        smallest_index = None
        for index, distance in enumerate(graph[last_complete_index]):
            if graph_labels[index].order is not None:
                continue
            if np.isfinite(distance):
                # shortcut route? is
                # graph_labels[last_complete_index].value+distance
                if graph_labels[last_complete_index].value + \
                        distance < graph_labels[index].working[-1]:
                    # shortcut found
                    graph_labels[index].working.append(
                        graph_labels[last_complete_index].value + distance)
            if graph_labels[index].working[-1] < smallest_distance:
                smallest_distance = graph_labels[index].working[-1]
                smallest_index = index

        # the smallest working value now becomes a final value
        order += 1
        graph_labels[smallest_index].order = order
        graph_labels[smallest_index].value = graph_labels[
            smallest_index].working[-1]
        last_complete_index = smallest_index

    for v in graph_labels:
        print(v, '\n')
    print("------------------_")

    path = [graph_labels[end_index]]
    while path[-1].value != 0:
        for index, distance in enumerate(graph[:, path[-1].index]):
            if np.isfinite(distance) :
                if path[-1].value - distance == graph_labels[index].value:
                    path.append(graph_labels[index])
                    break
        else:
            # none of the arcs seems to fit
            raise Exception("Can't find path. ")

    for p in reversed(path):
        print(p.name, end=', ')
    print(path[0].value)


dykstra(roadnetwork)
