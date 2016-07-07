# use "task" for things in the prec table, and "activity" for it in the graph
class Graph():

    def __init__(self):
        self.events = set()
        self.activites = []
        self._next_event = 0

    def add_event(self):
        self.events.add(self._next_event)
        self._next_event += 1
        return self._next_event - 1

    def add_activity_to_event(self, eventlabel, task):
        tasklabel = task[0]
        length = task[2]
        if eventlabel not in self.events:
            raise ValueError("Event {} not in network".format(eventlabel))
        self.activities.append((tasklabel, length, [eventlabel]))

# refactor as dict?
    def get_activity_by_label(self, activity_label):
        for activity in self.activities:
            if activity[0] == activity_label:
                return activity
        raise ValueError(
            "Activty {} not found in graph".format(activity_label))

    def add_event_to_activities(self, activity_list):
        event_label = self.add_event()
        for activity in self.activities:
            if activity[0] in activity_list:
                if len(activity[2]) > 1:
                    raise ValueError(
                        "Activity {} already has an end Event".format(
                            activity[0]))
                activity[2].append(event_label)
        return event_label

    def get_preceding(self, event):
        preceding_activities = set()
        for a in self.activities:
            try:
                if a[1][1] == event:
                    preceding_activities.add(event)
            except IndexError:
                pass
        return preceding_activities

    def is_open(self, task_label):
        for task in self.tasks:
            if task[0] == task_label and len(task[2]) == 1:
                return True
        return False

    def activity_in_graph(self, activity_label):
        for activity in self.activities:
            if activity[0] == activity_label:
                return True
        return False

    def check_requirements(self, activity_to_add, requirements):
        # Check the requirements are in the graph
        for requirement in requirements:
            if not self.task_in_graph(requirement):
                raise ValueError(
                    "requirement {} not met for task {}".format(
                        requirement, activity_to_add))

    def add_task(self, task):
        activity_to_add = task[0]
        requirements = task[1]
        #length = task[2]
        task_added_flag = task[3]

        # Refuse to add task that is already in graph
        # or if the requirements are not met
        if task_added_flag:
            raise ValueError(
                "Activity {} already added to graph".format(activity_to_add))
        self.check_requirements(activity_to_add, requirements)

# one easy possiblities are if there is a event(node) that has exactly the requirements
# Then add my activity to that event.
# another is if none of the requirements has an end activity yet.
# lets get a list of all the end events of each requirement

        requirement_activities = {
            requirement: self.get_activity_by_label(requirement)
            for requirement in requirements
        }

        # find or create an event that satisfies all the requirements
        # without breaking the unique determination rule.

        for event in self.events:
            preceding_activities = self.get_preceding(event)
            if preceding_activities == set(requirements):
                self.add_activity_to_event(event, task)
                return

        # so no single event in the graph is quite suitable.
        # so create the


precedence = [
    ['A', [], 2, False],
    ['B', [], 2, False],
    ['C', ['A'], 4, False],
    ['D', ['A'], 2, False],
    ['E', ['B'], 5, False],
    ['F', ['C', 'E'], 5, False],
    ['G', ['D', 'F'], 2, False],
]

dpres = [
    ['A', [], 1],
    ['B', [], 1],
    ['C', ['A', 'B'], 1],
    ['D', ['A'], 1]
]

graph = Graph()
event_number = 0
graph.add_event(event_number)
# search table for activities which don't depend on anything

for i, task in enumerate(precedence):

    if task[1] == []:
        graph.add_activity_to_event(event_number, task)
        task[3] = True

print("events:", graph.events, "\ntasks: ", graph.tasks)



# new strategy.

# add each task  by lot and lots of dummies connected
# then reduce the number of dummies


