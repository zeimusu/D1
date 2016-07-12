"""Defines a Class that can represent an activity on arc activty network
and a function that can generate a network from a precedence table"""
import precedence


class Network():
    """A network is represented by two dicts
    Each dict is keyed by a label. The values are instances of events and
    activities.

    The main method is "make_network_from_table". This builds a network from
    a table, and should be called to build the network
    """

    def __init__(self):
        """Initialise a network with a single source event, and no activities"""
        self._source_event = Event()
        self._sink_event = None
        self.events = dict()
        self.events[self._source_event.label] = self._source_event
        self.activities = dict()

    def add_activity_by_dummies(self, activity):
        """This method attaches a new activity arc to the network.
        It does this by means of dummies. Two new events are created, and the
        dependencies marked at the events. During this building stage, every
        activity added to the network generates an event with itself as the
        one dependency. This method createds dummy activities from each event
        that has a dependency of the activity. One dummy is created per
        dependency"""
        activity_node1, activity_node2 = Event(), Event()
        activity_node1.depends = activity.depends
        activity_node2.depends = [activity.label]
        activity.events = (activity_node1, activity_node2)

        self.activities[activity.label] = activity
        self.events[activity_node1.label] = activity_node1
        self.events[activity_node2.label] = activity_node2

        for dependency in activity.depends:
            start_event = self.activities[dependency].events[1]
            dummy = Dummy()
            dummy.events = (start_event, activity_node1)
            self.activities[dummy.label] = dummy

    def add_initial_activity(self, activity):
        """Activities with no dependencies are treated specially. They are
        directly connected to the source node by this method"""
        activity_node2 = Event()
        activity_node2.depends = [activity.label]
        activity.events = (self._source_event, activity_node2)
        self.events[activity_node2.label] = activity_node2
        self.activities[activity.label] = activity

    def is_in_network(self, activity_label):
        """Check if an activity, given by its label, is in the network"""
        return activity_label in set(self.activities.keys())

    def _find_terminal(self):
        """Find a terminal node, While the network is being built there may
        be several terminal nodes"""
        event_set = set(self.events.keys())
        for activity in self.activities.values():
            event_set.discard(activity.events[0].label)
        return event_set

    def _make_single_terminal(self):
        """When all the activities have been added, if there are more than one
        terminal node, then a single event is added, and linked by dummies from
        each terminal"""
        terminal_set = self._find_terminal()
        if len(terminal_set) == 0:
            return
        terminal_event = Event()
        for event_label in terminal_set:
            dummy = Dummy()
            terminal_event.depends += self.events[event_label].depends
            dummy.events = (self.events[event_label], terminal_event)
            self.activities[dummy.label] = dummy
        self.events[terminal_event.label] = terminal_event
        self._sink_event = terminal_event

    def _merge_dummy(self, dummy_label):
        """Dummies can be merged if possible, This method removes a dummy from
        the network, merging the events at the two ends, and taking care
        of dependencies of the events that are merged"""
        dummy = self.activities[dummy_label]
        node_to_merge = dummy.events[1]
        target_node = dummy.events[0]
        for activity_label in self.activities:
            if activity_label == dummy_label:
                continue
            activity = self.activities[activity_label]
            if activity.events[0].label == node_to_merge.label:
                activity.events = (target_node, activity.events[1])
            elif activity.events[1].label == node_to_merge.label:
                activity.events = (activity.events[0], target_node)
        target_node.depends = node_to_merge.depends
        if node_to_merge == self._sink_event:
            self._sink_event = target_node
        del self.activities[dummy_label]
        del self.events[node_to_merge.label]

    def out_activities(self, event_label):
        """Return a set of all activities that follow a given event, passed by
        label"""
        activity_labels = set()
        for a_label in self.activities:
            activity = self.activities[a_label]
            if activity.events[0].label == event_label:
                activity_labels.add(a_label)
        return activity_labels

    def in_activities(self, event_label):
        """Return of all activities that enter a given event. This differs from
        the event's dependencies, as it can include dummy activities"""
        activity_labels = set()
        for a_label in self.activities:
            activity = self.activities[a_label]
            if activity.events[1].label == event_label:
                activity_labels.add(a_label)
        return activity_labels

    def _remove_activity(self, activity_label):
        """Remove a dummy activity without merging the events at each end. Since
        this could result in a disconnected network, it should only be called on
        activity on duplicate arcs or on loops"""
        del self.activities[activity_label]

    def _is_removable(self, dummy_label):
        """A dummy activity is removable if it has the same start and end
        event, or it duplicates another activity"""
        end1, end2 = self.activities[dummy_label].events
        if end1 == end2:
            #print("remove loop")
            return True
        for activity in self.activities.values():
            if activity.events[0] == end1 and \
               activity.events[1] == end2 and \
               activity.label != dummy_label:
                #print("remove", dummy_label, "matches", a.label)
                return True
        return False

    def _is_mergeable(self, dummy_label):
        """Mergeable dummy activities are those that can be removed
        without changing the dependencies of any other events. Either this
        is becuase the dependencies of the event before the dummy is the same
        as after the dummy, or if all the nodes that follow an event have the
        same dependencies. In either case the two events can be merged and the
        dummy removed. However if removal of the dummy would lead to a double
        arc, then the dummy is not mergeable"""
        dummy = self.activities[dummy_label]
        if self._dummy_needed_to_prevent_double(dummy):
            return False

        if dummy.events[0].depends == dummy.events[1].depends:
            return True

        # do all the arcs that start from the the same event end at events
        # with the same dependencies
        dependencies_at_end = dummy.events[1].depends
        arcs_from_same_event = self.out_activities(dummy.events[0].label)

        return all(map(
            lambda x:
            self.activities[x].events[1].depends == dependencies_at_end,
            arcs_from_same_event))

    def _dummy_needed_to_prevent_double(self, dummy):
        """Check for the case in which merging a dummy would lead to two nodes
        having the same start and end events. We only check for non-dummy
        activities, as dummy activities having the same start and end events as
        another activity can be removed later."""
        dummy_start_event = dummy.events[0]
        dummy_end_event = dummy.events[1]

        for event in self.events.values():
            if self._is_linked(event, dummy_start_event) and\
               self._is_linked(event, dummy_end_event):
                return True
        return False

    def _is_linked(self, event1, event2):
        """Check if two events are linked by an activity"""
        for activity in self.activities.values():
            if activity.label[:5] == "dummy":
                continue  # only consider non-dummy links
            if (activity.events[0].label == event1.label and
                    activity.events[1].label == event2.label) or \
               (activity.events[0].label == event2.label and
                activity.events[1].label == event1.label):
                return True
        return False

    def renumber(self):
        """After mergeing dummy activities, the number of events will get
        irregular. This renumbers the events to make them numbered form 0 to
        n"""
        for i, event_label in enumerate(sorted(self.events)):
            if i == event_label:
                continue
            else:
                self._rename_event(event_label, i)

    def _rename_event(self, from_label, to_label):
        """Relabel and event, taking care of the reference to the event in the
        set of activities"""
        # the event label appears in the dict key, and the label property
        self.events[from_label].label = to_label
        self.events[to_label] = self.events[from_label]
        del self.events[from_label]

    def make_network_from_table(self, table):
        """The main method. Takes a precdence table formatted as a list of lists
        and fill out the activity tree. This is done in two stages: first add
        all the activities, linking each to the network by dummies, then purge
        down the network, removeing or merging dummies as possible. When no more
        removal is possible, the network is returned."""
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

        self._make_single_terminal()
    #    print(N.events,"\n", N.activities)

        # search through the network for removable dummies and mergable nodes
        # and remove them
        while True:
            action = ''
            act_label = None
            for act_label in self.activities:
                if act_label[:5] == "dummy" and self._is_removable(act_label):
                    action = 'remove'
                    break
                if act_label[:5] == "dummy" and self._is_mergeable(act_label):
                    action = 'merge'
                    break
            else:
                return self  # for else
                #-> have looped through and found no mergeable
            # after break -> have found mergable dummy
           # print(action, act_label)
            if action == 'merge':
                self._merge_dummy(act_label)
            elif action == 'remove':
                self._remove_activity(act_label)

    def print_dot(self, filename=None):
        """Write the graph as a .dot file"""
        if filename is None:
            graphname = "activity_network"
        else:
            graphname = filename
        dottext = "digraph {} {{\n".format(graphname)
        for activity in self.activities.values():
            if activity.label[:5] == "dummy":
                dottext += '{start} -> {end} [style = dotted];\n'.format(
                    start = activity.events[0].label,
                    end = activity.events[1].label)
                
            else:
                dottext += '{start} -> {end} [label = "{label}({length})"];\n'.format(
                    start=activity.events[0].label,
                    end=activity.events[1].label,
                    label=activity.label,
                    length=activity.length)
        dottext += "}"
        if filename is None:
            print(dottext)
        else:
            with open(filename, 'w') as dotfile:
                dotfile.write(dottext)


class Event():
    """A class representing an event. It records the event's label, dependencies
    and has space for the early and late times in the critical path
    algorithm."""
    event_number = 0

    def __init__(self, label=None):
        """Events are self labelling, if no label is passed, a new one is
        generated sequentially"""
        if label is None:
            self.label = Event.event_number
            Event.event_number += 1
        else:
            self.label = label
        self.depends = []
        self.early_time = None
        self.late_time = None

    def __str__(self):
        """pretty print an event"""
        return (str(self.label) +
                "->" +
                str(self.depends) +
                " [" +
                (str(self.early_time) if self.early_time is not None else "") +
                " | " +
                (str(self.late_time) if self.late_time is not None else "") +
                "]")

    __repr__ = __str__


class Activity():
    """A struct to store and event. It knows its label, length, dependencies,
    and the events at each end"""

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
    """A dummy activity, these are labeled automatically, with names starting
    'dummy'"""
    dummy_number = 1

    def __init__(self):
        """create a dummy, All dummies have length 0. Dependencies will be added
        later"""
        super().__init__("dummy" + str(Dummy.dummy_number), [], 0)
        Dummy.dummy_number += 1

def main():
    """run on one of the sample tables"""
    # import pprint
    activ_net = Network()
    activ_net.make_network_from_table(precedence.mix1)
    activ_net.renumber()
    #pprint.pprint(activ_net.events)
    #pprint.pprint(activ_net.activities)
    activ_net.print_dot()

if __name__ == "__main__":
    main()
