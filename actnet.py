class Network():

    def __init__(self):
        self._source_event = Event()
        self._sink_event = None
        self.events = dict()
        self.events[self._source_event.label] = self._source_event
        self.activities = dict()

    def add_activity_by_dummies(self, activity):
        activity_node1, activity_node2 = Event(), Event()
        activity_node1.depends = activity.depends
        activity_node2.depends = [activity.label]
        activity.events = (activity_node1, activity_node2)

        self.activities[activity.label] = activity
        self.events[activity_node1.label] = activity_node1
        self.events[activity_node2.label] = activity_node2

        for dependency in activity.depends:
            start_event = self.activities[dependency].events[1]
            d = Dummy()
            d.events = (start_event, activity_node1)
            self.activities[d.label] = d

    def add_initial_activity(self, activity):
        activity_node2 = Event()
        activity_node2.depends = [activity.label]
        activity.events = (self._source_event, activity_node2)
        self.events[activity_node2.label] = activity_node2
        self.activities[activity.label] = activity

    def is_in_network(self, activity_label):
        return activity_label in set(self.activities.keys())

    def _find_terminal(self):
        event_set = set(self.events.keys())
        for a in self.activities.values():
            event_set.discard(a.events[0].label)
        return event_set

    def make_single_terminal(self):
        terminal_set = self._find_terminal()
        if len(terminal_set) == 0:
            return
        terminal_event = Event()
        for event_label in terminal_set:
            d = Dummy()
            terminal_event.depends += self.events[event_label].depends
            d.events = (self.events[event_label], terminal_event)
            self.activities[d.label] = d
        self.events[terminal_event.label] = terminal_event
        self._sink_event = terminal_event

    def merge_dummy(self, dummy_label):
        dummy = self.activities[dummy_label]
        node_to_merge = dummy.events[1]
        target_node = dummy.events[0]
        for activity_label in self.activities:
            if activity_label == dummy_label:
                continue
            a = self.activities[activity_label]
            if a.events[0].label == node_to_merge.label:
                a.events = (target_node, a.events[1])
            elif a.events[1].label == node_to_merge.label:
                a.events = (a.events[0], target_node)
        target_node.depends = node_to_merge.depends
        if node_to_merge == self._sink_event:
            self._sink_event = target_node
        del self.activities[dummy_label]
        del self.events[node_to_merge.label]

    def out_activities(self, event_label):
        activity_labels = set()
        for a_label in self.activities:
            a = self.activities[a_label]
            if a.events[0].label == event_label:
                activity_labels.add(a_label)
        return activity_labels

    def in_activities(self, event_label):
        activity_labels = set()
        for a_label in self.activities:
            a = self.activities[a_label]
            if a.events[1].label == event_label:
                activity_labels.add(a_label)
        return activity_labels

    def is_mergeable(self, dummy_label):
        d = self.activities[dummy_label]
        if self.dummy_needed_to_prevent_double(d):
            return False

        if d.events[0].depends == d.events[1].depends:
            return True

        # do all the arcs that start from the the same event end at events
        # with the same dependencies
        dependencies_at_end = d.events[1].depends
        arcs_from_same_event = self.out_activities(d.events[0].label)

        return all(map(lambda x: self.activities[x].events[
                   1].depends == dependencies_at_end, arcs_from_same_event))
        # bug! haven't checked for double arcs!

    def dummy_needed_to_prevent_double(self, dummy):
        dummy_start_event = dummy.events[0]
        dummy_end_event = dummy.events[1]

        for e in self.events:
            if self.is_linked(self.events[e], dummy_start_event) and\
               self.is_linked(self.events[e], dummy_end_event):
                return True
        return False

    def is_linked(self, event1, event2):
        for a in self.activities.values():
            if (a.events[0].label == event1.label and
                a.events[1].label == event2.label) or \
               (a.events[0].label == event2.label and
                    a.events[1].label == event1.label):
                return True
        return False

    def renumber(self):
        for i, e in enumerate(sorted(self.events)):
            if i == e:
                continue
            else:
                self.rename_event(e, i)

    def rename_event(self, from_label, to_label):
        # the event label appears in the dict key, and the label property
        self.events[from_label].label = to_label
        self.events[to_label] = self.events[from_label]
        del self.events[from_label]

    def make_network_from_table(self, table):
        i = -1
        while len(table) > 0:
            i = i % len(table)
            task = table[i]
            if len(task[1]) == 0:
                activity = Activity(task[0], task[1], task[2])
                self.add_initial_activity(activity)
                del table[i]
            elif all(map(self.is_in_network, task[1])):
                activity = Activity(task[0], task[1], task[2])
                self.add_activity_by_dummies(activity)
                del table[i]
            else:
                i += 1

        self.make_single_terminal()
    #    print(N.events,"\n", N.activities)

        while True:
            for d in self.activities:
                if d[:5] == "dummy" and self.is_mergeable(d):
                    break
            else:
                return self  # for else  
                             #-> have looped through and found no mergeable
            # after break -> have found mergable dummy
            self.merge_dummy(d)


class Event():
    event_number = 0

    def __init__(self):
        self.label = Event.event_number
        Event.event_number += 1
        self.depends = []
        self.early_time = None
        self.late_time = None

    def __str__(self):
        return str(self.label) + "->" + str(self.depends)

    __repr__ = __str__


class Activity():

    def __init__(self, label, depends, length):
        self.label = label
        self.depends = depends
        self.length = length
        self.events = (None, None)

    def __str__(self):
        return str(
            str(self.events[0].label) +
            "-" +
            str(self.label) +
            "(" +
            str(self.length) +
            ")-" + str(self.events[1].label))

    __repr__ = __str__


class Dummy(Activity):
    dummy_number = 1

    def __init__(self):
        super().__init__("dummy" + str(Dummy.dummy_number), [], 0)
        Dummy.dummy_number += 1

p1 = [
    ["A", [], 1],
    ["B", [], 1],
    ["C", ["A"], 1],
    ["D", ["A"], 1],
    ["E", ["B"], 1],
    ["F", ["C", "E"], 1],
    ["G", ["D", "F"], 1]
]

long_no_dum = [
    ["A", [], 1],
    ["B", [], 1],
    ["C", ["A"], 1],
    ["D", ["A"], 1],
    ["E", ["B"], 1],
    ["F", ["B"], 1],
    ["G", ["D"], 1],
    ["H", ["D"], 1],
    ["I", ["C", "E"], 1],
    ["J", ["F"], 1],
    ["K", ["G", "I", "J"], 1],
    ["L", ["H", "K"], 1]
]


p2 = [
    ["A", [], 1],
    ["B", [], 1],
    ["C", ["A", "B"], 1],
    ["D", ["A"], 1]
]  # a table that requires 1 dummy

fiveBQ5 = [
    ["P", [], 1],
    ["Q", [], 1],
    ["R", ["P"], 1],
    ["S", ["P"], 1],
    ["T", ["P", "Q"], 1],
]

umergeable = [
    ["A", [], 1],
    ["B", [], 1],
    ["C", [], 1],
    ["D", ["A", "B"], 1],
    ["E", ["A", "C"], 1],
    ["F", ["B", "C"], 1]
]

p = [  # a long and complex table, that nevertheless doesn't need dummies
    # 2 critial paths with length 54.
    ["A", [], 10],
    ["B", [], 14],
    ["C", ["A"], 11],
    ["D", ["B"], 5],
    ["E", ["B"], 15],
    ["F", ["B"], 20],
    ["G", ["C", "D"], 8],
    ["H", ["C", "D"], 12],
    ["I", ["G"], 16],
    ["J", ["E", "H"], 10],
    ["K", ["E", "H"], 21],
    ["L", ["E", "H"], 6],
    ["M", ["I", "J"], 9],
    ["N", ["F", "L"], 12],
]

impossible = [ #nothing checks for this kind of situation. It will cause the 
               #algorithm to hang
    ["A",[],1],
    ["B",["C"],1],
    ["C",["D"],1],
    ["D",["B","A"],1]
]

def main():
    import pprint
    n = Network()
    n.make_network_from_table(p)
    n.renumber()
    print(n.events)
    pprint.pprint(n.activities)
    print(n._source_event, n._sink_event)

if __name__ == "__main__":
    main()
