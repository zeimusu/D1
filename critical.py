from actnet import Network
import precedence

class Critical_Network(Network):

    def __init__(self):
        self.critical = []
        self.non_critical = []
        super().__init__()

    def forward_pass(self):
        self._source_event.early_time = 0
        while self._sink_event.early_time is None:
            for event_label in self.events:
                e = self.events[event_label]
                if e.early_time is not None:
                    continue
                all_early_times = []
                incoming_activities = self.in_activities(event_label)
 #               print(event_label, incoming_activities)
                for a_label in incoming_activities:
                    a = self.activities[a_label]
                    prev_early_time = a.events[0].early_time
                    if prev_early_time is None:
                        break
                    all_early_times.append(prev_early_time + a.length)
                else:  # for else
                    e.early_time = max(all_early_times)

    def back_pass(self):
        self._sink_event.late_time = self._sink_event.early_time

        while self._source_event.late_time is None:
            for event_label in self.events:
                e = self.events[event_label]
                if e.late_time is not None:
                    continue
                all_late_times = []
                outgoing_activities = self.out_activities(event_label)
#                print(event_label, outgoing_activities)
                for a_label in outgoing_activities:
                    a = self.activities[a_label]
                    following_late_time = a.events[1].late_time
                    if following_late_time is None:
                        break
                    all_late_times.append(following_late_time - a.length)
                else:  # for else
                    e.late_time = min(all_late_times)

    def calculate_times(self):
        self.forward_pass()
        self.back_pass()

    def is_critical(self, activity_label):
        return self.float(activity_label) == 0

    def float(self, activity_label):
        a = self.activities[activity_label]
        start_event = a.events[0]
        end_event = a.events[1]
        return end_event.late_time - start_event.early_time - a.length

    def set_critical(self):
        for a_label in self.activities:
            if a_label[:5] == "dummy":
                continue
            a = self.activities[a_label]
            act_float = self.float(a_label)
            est = a.events[0].early_time
            eft = est + a.length
            lft = eft + act_float
            if act_float == 0:
                self.critical.append([a_label, est, eft])
            else:
                self.non_critical.append([a_label, est, eft, lft])

        self.critical.sort(key=lambda x: (x[1], x[2]))
        self.non_critical.sort(key=lambda x: (x[1], x[2]))

    def split_into_paths(self):
        critical = self.critical
        paths = [[critical[0]]]

        for i in range(1, len(critical)):
            new_paths = []
            for p in paths:
                if p[-1][2] == critical[i][1]:
                    p.append(critical[i])
                elif p[-1][1] == critical[i][1]:
                    new_paths.append(p[:])
                    new_paths[-1][-1] = critical[i]
            if len(new_paths) > 0:
                paths += new_paths
        return paths


def make_dot(critical_network):
    """Draw a graph in dot format from a network with floats calculated
    the critical activities are highlighted"""
    dot_text = 'digraph critical {\nrankdir=LR;\n'
    
    for event in critical_network.events.values():
        #add a all events with record type
        dot_text += '{label} [shape=record, label="<f0> {early}|<f1> \
{late}"];\n'.format(label=event.label, 
                early=event.early_time, 
                late=event.late_time)
    dot_text += 'edge [color=red];\n'
    for arc in critical_network.critical:
        #[label, start, end]
        activity_label = arc[0]
        activity = critical_network.activities[activity_label]
        event1, event2 = activity.events
        dot_text+='{event1label} -> {event2label} \
[label="{act_label}"];\n'.format(event1label=event1.label, 
                                event2label=event2.label, 
                                act_label=activity_label)
    dot_text+='edge [color=black];\n'
    for arc in critical_network.non_critical:
        activity_label = arc[0]
        activity = critical_network.activities[activity_label]
        event1, event2 = activity.events
        dot_text+='{event1label} -> {event2label} \
[label="{act_label}"];\n'.format(event1label=event1.label, 
                                event2label=event2.label,
                                act_label=activity_label)
    for arc_label in critical_network.activities:
        if arc_label[:5] == 'dummy':
            activity = critical_network.activities[arc_label]
            event1, event2 = activity.events
            dot_text += '{e1label} -> {e2label} [style=dotted];\n'.format(
                e1label=event1.label,
                e2label=event2.label)
    dot_text+="}"
    print(dot_text)



def main():
    c = Critical_Network()
    c.make_network_from_table(precedence.mix1)
    c.renumber()

    c.forward_pass()
    for e in c.events:
        ee = c.events[e]
    c.back_pass()

    for e in c.events:
        ee = c.events[e]


    c.set_critical()
    #print(c.critical)
    #print(c.non_critical)
    #print(c.split_into_paths())

    make_dot(c)

if __name__ == "__main__":
    main()
