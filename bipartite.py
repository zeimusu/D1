class Vertex():

    def __init__(self, label):
        self.label = label
    def __str__(self):
        return str(self.label)
    def __repr__(self):
        return "Vertex({})".format(str(self.label))

class Edge():

    def __init__(self, vertex1, vertex2, weight=1):
        self.ends = (vertex1, vertex2)
        self.weight = weight


class Bipartite(dict):
    """A bipartite graph consisting two lists of vertices, and a list of
    edges. Each edge joins a vertex in the first
    """

    def __init__(self, vertices, edges):
        for v in vertices:
            self.add_vertex(v)
        for e in edges:
            self.add_edge(e)

    def vertices(self):
        return list(self.keys())

    def add_vertex(self, v):
        self[v] = {}

    def add_edge(self, edge):
        v1, v2 = edge.ends
        self[v1][v2] = self[v2][v1] = edge

    def neighbours(self,vertex):
        return self[vertex].keys()

    def unmatched_vertex_left(self, matching):
        """A matching is a dictionary. keys from the left,
        values in the grihg"""
        left_nodes = list(matching.keys())
        for v in self.vertices():
            if v not in left_nodes:
                return v

    def alternating_path(self, matching, start_vertex):
        #start_vertex = self.unmatched_vertex_left(matching)
        path = [[start_vertex]]
        while True:
            #go forward on path not in matching
            try:
                matched_vertex = matching[path[-1][0]]
            except KeyError:
                matched_vertex = None
            next_vs = set(self.neighbours(path[-1][0]))
            if matched_vertex: 
                next_vs.remove(matched_vertex)
            next_vertex = next_vs.pop()
            path[-1].append(next_vertex)
            for left,right in matching.items():
                if next_vertex == right:
                    path.append([left])
                    print(path)
                    break
            else:
                return path

    def is_complete(self, matching):
        return len(matching) == len(self.vertices())//2

    
        

def improve_matching(matching, path):
    for edge in path:
        matching[edge[0]] = edge[1]


vs = {label: Vertex(label)
      for label in ['A', 'B', 'H', 'I', 'L', 'R',
                    '1', '2', '3','4','5','6']}
es = [
    Edge(p[0], p[1]) for p in [
        (vs['A'],vs['1']),
        (vs['A'],vs['3']),
        (vs['B'],vs['4']),
        (vs['H'],vs['2']),
        (vs['H'],vs['3']),
        (vs['I'],vs['1']),
        (vs['L'],vs['3']),
        (vs['L'],vs['4']),
        (vs['L'],vs['5']),
        (vs['R'],vs['5']),
        (vs['R'],vs['6']),
    ]]
bg = Bipartite(list(vs.values()), es)

matching = {vs['A']: vs['1'], vs['H']: vs['3'], vs['L']: vs['4'],
            vs['R']:vs['5']}


print(matching)
while not bg.is_complete(matching):
    vertex = bg.unmatched_vertex_left(matching)
    path = bg.alternating_path(matching, vertex)
    improve_matching(matching,path)

print(matching)
