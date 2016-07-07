class Constraint():
    """Represents an inequality in form
    ax + by + c >= 0
    """

    def __init__(self, a, b, c, strict=False, variables=("x", "y")):
        self.coeff = [a, b, c]
        self.strict = strict
        self.variables = variables

    def check_constraint(self, point):
        c = self.coeff
        value = c[0] * point[0] + c[1] * point[1] + c[2]
        if self.strict:
            return value > 0
        else:
            return value >= 0


class Problem():
    """ Expression has form [a,b] to represent ax + by"""

    def __init__(
            self,
            constraints,
            expression,
            maximise=True,
            variables=("x", "y")):
        self.constraints = constraints
        self.expression = expression
        self.maximise = maximise
        self.variables = variables
        self.polygon = []
        self.polygon_closed = False

    def add_constraint(self, constraint):
        self.constraints.append(constraint)

    def evaluate_at_point(self, point):
        """Essentially a dot product"""
        return sum([self.expression[i] * point[i] for i in range(len(point))])

    def solve(self):
        self.build_polygon()
        vertex_dict = {point: self.evaluate_at_point(point)
                       for point in self.polygon}

        if self.maximise:
            return max(vertex_dict, key=vertex_dict.get)
        else:
            return min(vertex_dict, key=vertex_dict.get)

    def build_polygon(self):
        if self.polygon == []:
            self.rebuild_polygon()
    
    def rebuild_polygon(self):
        points = {(0, 1): solve_sim(self.constraints[0], self.constraints[1])}

        for cons_index, constraint in enumerate(self.constraints[2:]):
            for c2_index, constraint2 in enumerate(
                    self.constraints[0:cons_index + 2]):
                point = solve_sim(constraint, constraint2)
                points[(c2_index, cons_index + 2)] = point
            self.clear_bad_points(points)
        self.polygon_closed = self.test_closed(points)
        self.polygon = points.values()

    def clear_bad_points(self, points):
        delete_list = []
        for cons_indices, point in points.items():
            other_constraints = (
                self.constraints[:cons_indices[0]] +
                self.constraints[cons_indices[0] + 1:cons_indices[1]] +
                self.constraints[cons_indices[1] + 1:])
            if not check_constraints(other_constraints, point):
                delete_list.append(cons_indices)
        for cons_indices in delete_list:
            del points[cons_indices]
    
    @staticmethod
    def test_closed(points):
        con_indices = list(points.keys())
        ordered_points = [con_indices[0]]
        del con_indices[0]
        while con_indices:
            line = ordered_points[-1][1] # second element of last point
            for i,p in enumerate(con_indices):
                if p[0] == line:
                    ordered_points.append(p)
                    del con_indices[i]
                    break
                elif p[1] == line:
                    ordered_points.append(tuple(reversed(p)))
                    del con_indices[i]
                    break
            else: # of the for loop if no suitable point is found
                return False
        if len(con_indices) > 0: 
            return False
        if ordered_points[-1][1] != ordered_points[0][0]:
            return False
        return True

       
    def bounding_box(self):
        self.build_polygon()
        if not self.polygon_closed:
            return None
        x_coords = [vertex[0] for vertex in self.polygon]
        y_coords = [vertex[1] for vertex in self.polygon]
        bottom_left = (min(x_coords),min(y_coords))
        top_right = (max(x_coords),max(y_coords))
        return (bottom_left,top_right)

    def solve_integer(self):
        box = self.bounding_box()
        if not box:
            return None
        optimum = op_value = None
        for x in range(int(box[0][0]), int(box[1][0])+1):
            for y in range(int(box[0][1]), int(box[1][1])+1):
                if check_constraints(self.constraints,(x,y)):
                    point_value = self.evaluate_at_point((x,y))
                    if optimum == None:
                        optimum = (x,y)
                        op_value = point_value
                    elif self.maximise and point_value > op_value:
                        optimum = (x,y)
                        op_value = point_value
                    elif not self.maximise and point_value < op_value:
                        optimum = (x,y)
                        op_value = point_value
        return optimum


        


def check_constraints(constraints, point):
    return all([constraint.check_constraint(point)
                for constraint in constraints])


def solve_sim(constraint1, constraint2):
    """solve a pair of simulataneous equations. use an inverse matrix method"""
    c1, c2 = constraint1.coeff, constraint2.coeff
    determinant = c1[0] * c2[1] - c1[1] * c2[0]
    if determinant == 0:
        raise ValueError("Singular matrix")
    x = (-c2[1] * c1[2] + c1[1] * c2[2]) / determinant
    y = (c2[0] * c1[2] - c1[0] * c2[2]) / determinant
    return (x, y)


def test1():
    constraints = [
        Constraint(-1, 0, 5),
        Constraint(0, 1, -2),
        Constraint(1, -1, 3),
        Constraint(-1, -1, 8)
    ]
    problem = Problem(constraints, (1, 2))  # maximise x+2y (2.5,5,5)
    print(problem.solve())
def test2():
    constraints = [
        Constraint(3,1,-12),
        Constraint(2,-1,0),
        Constraint(-1,3,0),
        Constraint(-6,-5,120)]
    problem_a = Problem(constraints,(1,0))
    problem_g = Problem(constraints,(2,5))
    problem_h = Problem(constraints,(2,5),maximise=False)
    problem_a.build_polygon()
    print(problem_a.polygon)
    print(problem_a.polygon_closed)
    print(problem_a.bounding_box())
    print(problem_a.solve())
    print(problem_a.solve_integer())


def test3():
    constraints= [
        Constraint(-3,-4,36),
        Constraint(-13,-9,117),
        Constraint(4,-5,10),
        Constraint(6,5,-30),
        Constraint(0,1,-2)
    ]
    problem = Problem(constraints,(1,2),maximise=True)
    problem.build_polygon()
    print(problem.polygon_closed)
    print(problem.bounding_box())
    print(problem.solve_integer())

test3()
