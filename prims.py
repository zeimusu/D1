import numpy as np
from operator import itemgetter


bookexample = np.array(
    [[None, 'A', 'B', 'C', 'D', 'E'],
     ['A', None, 27, 12, 23, 74],
     ['B', 27, None, 47, 15, 71],
     ['C', 12, 47, None, 28, 87],
     ['D', 23, 15, 28, None, 75],
     ['E', 74, 71, 87, 75, None]
     ])
personexample = np.array(
    [
        [None, 'A', 'B', 'C', 'L', 'O'],
        ['A', None, 431, 531, 544, 503],
        ['B', 431, None, 109, 120, 68],
        ['C', 531, 109, None, 152, 105],
        ['L', 544, 120, 152, None, 56],
        ['O', 503, 68, 105, 56, None]
    ])

June13 = np.array([
    [None,'A','B','C','D','E','F'],
    ['A',None,15,6,9,None,None],
    ['B',15,None,12,None,14,None],
    ['C',6,12,None,7,10,None],
    ['D',9,None,7,None,11,17],
    ['E',None,14,10,11,None,5],
    ['F',None,None,None,17,5,None]
])

networkexample = np.array(
    [
        [None, 'A', 'B', 'C', 'D', 'E', 'F'],
        ['A', None, 120, 200, 140, 135, 250],
        ['B', 120, None, 230, 75, 130, 80],
        ['C', 200, 230, None, 160, 160, 120],
        ['D', 140, 75, 160, None, 200, 85],
        ['E', 135, 130, 160, 200, None, 150],
        ['F', 250, 80, 120, 85, 150, None]
    ])
gasexample = np.array(
    [
        [None, 'T', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
        ['T', None, 120, 150, None, 120, 100, None, 70, 180],
        ['A', 120, None, 60, 60, 90, None, 210, 160, 40],
        ['B', 150, 60, None, 20, None, 180, 170, None, 50],
        ['C', None, 60, 20, None, 40, 160, 150, 140, 60],
        ['D', 120, 90, None, 40, None, 130, None, 110, None],
        ['E', 100, None, 180, 160, 130, None, None, 30, None],
        ['F', None, 210, 170, 150, None, None, None, 150, 200],
        ['G', 70, 160, None, 140, 110, 30, 150, None, 200],
        ['H', 180, 40, 50, 60, None, None, 200, 200, None],
    ])

roadexample = np.array([
    [None,
     'Penrith', 'Newcastle', 'Durham', 'Sunderland', 'Middlesbrough', 'Rippon', 'York', 'Leeds'],
    ['Penrith',       None, 72,   56,   None, 68,   69,   None, 84],
    ['Newcastle',     72,   None, 13,   12,   None, None, None, None],
    ['Durham',        56,   13,   None, 11,   20,   42,   None, None],
    ['Sunderland',    None, 12,   11,   None, 15,   None, None, None],
    ['Middlesbrough', 68,   None, 20,   15,   None, 31,   46,   None],
    ['Rippon',        69,   None, 42,   None, 31,   None, 22,   26],
    ['York',          None, None, None, None, 46,   22,   None, 24],
    ['Leeds',         84,   None, None, None, None, 26,   24,   None]
])


class Prims():

    def __init__(self, distance_matrix):
        if isinstance(distance_matrix, str):
            self.distance_matrix = self.import_csv(distance_matrix)
        else:
            self.distance_matrix = distance_matrix
        if not (np.transpose(self.distance_matrix) 
                == self.distance_matrix).all():
            raise ValueError("Not a symmetric matrix")
        self.fix_Nones()
        self.column_indices = []
        self.arc_list = []
        self.distance_list = []
        self.labels = self.distance_matrix[0, :]

    def import_csv(self,filename):
        distance_matrix = np.genfromtxt(filename, delimiter=",", dtype=object)
        distance_matrix = try_int(distance_matrix)
        print(distance_matrix)
        return distance_matrix

    def fix_Nones(self):
        """None in a matrix can be better represented as infinity
        since it means it is impossible to join the two node"""
        self.distance_matrix[self.distance_matrix == np.array(None)] = np.inf

    def find_minimum_in_column(self, column):
        return min(
            enumerate(
                self.distance_matrix[
                    1:,
                    column]),
            key=itemgetter(1))

    def find_minimum_in_columns(self):
        search_columns = self.distance_matrix[1:, self.column_indices]
        flat_index = np.argmin(search_columns)
        index = np.unravel_index(flat_index, search_columns.shape)
        prev_index = self.column_indices[index[1]]
        next_index = index[0] + 1
        return (prev_index, next_index, search_columns[index])

    def find_column_from_label(self, label):
        return np.where(self.labels == label)[0][0]

    def solve(self):
        node = self.distance_matrix[0, 1]
        row = 1

        while self.distance_matrix.shape[0] > 2:
            # Label the column corresponding to the last vertex
            column = self.find_column_from_label(node)
            self.column_indices.append(column)

            # delete the row of that column
            self.distance_matrix = np.delete(
                self.distance_matrix, (row), axis=0)
            # find the minimum value among labelled columns
            prev_index, row, value = self.find_minimum_in_columns()

            # add that arc to the tree
            prev_node = self.distance_matrix[0, prev_index]
            node = self.distance_matrix[row, 0]
            self.arc_list.append((prev_node, node))
            self.distance_list.append(value)

def try_int(x):
    try:
        return int(x)
    except ValueError:
        s= x.decode("utf-8")
        if s:
            return s
        else:
            return None

try_int = np.vectorize(try_int, otypes=[object])


#p = Prims('ireland_table.csv')
p= Prims(June13)
p.solve()

print(p.arc_list)
print(sum(p.distance_list))
