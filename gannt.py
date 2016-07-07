import tkinter as tk
import critical


class Gannt(tk.Tk):

    def __init__(
            self,
            critical_act,
            non_critical,
            width,
            height,
            *args,
            **kwargs):
        super().__init__(*args, **kwargs)
        self.title = "Gannt Chart"
        self.canvas = tk.Canvas(self, width=width, height=height)
        self.canvas.pack()
        self.width = width
        self.height = height
        self.critical = critical_act
        self.non_critical = non_critical

    def _draw_critical(self, label, x0, y0, x1, y1):
        self.canvas.create_rectangle(x0, y0, x1, y1,
                                     fill='white')
        self.canvas.create_text((x0 + x1) // 2, (y0 + y1) // 2, text=label)

    def _draw_noncritical(self, label, x0, y0, x1, y1, x2):
        self.canvas.create_rectangle(x0, y0, x1, y1, fill='white')
        self.canvas.create_text((x0 + x1) // 2, (y0 + y1) // 2, text=label)
        self.canvas.create_rectangle(x1, y0, x2, y1,
                                     fill='black', stipple='gray25')


    def draw_gannt(self):
        max_time = self.critical[-1][2]
        paths = split_into_paths(self.critical)

        left_axis_space = 20
        right_space = 20
        top_axis_space = 20
        bottom_space = 20

        pixels_per_unit_time = (
            self.width - left_axis_space - right_space) / max_time
        box_height = ((self.height - top_axis_space - bottom_space) //
                      (len(self.non_critical) + len(paths)))

        self._draw_grid(max_time, left_axis_space,
                        right_space, top_axis_space, bottom_space,
                        pixels_per_unit_time)
        # draw the critical activities
        for i,critical_path in enumerate(paths):
            for c in critical_path:
                label = c[0]
                x0 = left_axis_space + c[1] * pixels_per_unit_time
                y0 = top_axis_space + i*box_height
                x1 = left_axis_space + c[2] * pixels_per_unit_time
                y1 = top_axis_space + (i+1)*box_height
                #print("crit", label, x0, y0, x1, y1)
                self._draw_critical(label, x0, y0, x1, y1)

        # draw the non critical on separate lines
        for i, n in enumerate(self.non_critical):
            label = n[0]
            x0 = left_axis_space + n[1] * pixels_per_unit_time
            y0 = top_axis_space + (len(paths)+i) * box_height
            x1 = left_axis_space + n[2] * pixels_per_unit_time
            y1 = top_axis_space + (len(paths)+i+1) * box_height
            x2 = left_axis_space + n[3] * pixels_per_unit_time
            print("non", label, x0, y0, x1, y1, x2)
            self._draw_noncritical(label, x0, y0, x1, y1, x2)

    def _draw_grid(self, max_time, left_axis_space,
                   right_space, top_axis_space, bottom_space,
                   pixels_per_unit_time):

        # I want to aim for lines every 50 pixels
        time_gap50 = 50 / pixels_per_unit_time
        standard_form = "{:e}".format(time_gap50)
        decimalpart, e, power = standard_form.partition('e')
        msd = float(decimalpart)
        power = int(power)
        if msd < 1.5:
            m = 1
        elif msd < 3:
            m = 2
        elif msd < 7:
            m = 5
        else:
            m = 10
        time_gap = m * 10**power
        pixel_gap = time_gap * pixels_per_unit_time

        x = left_axis_space
        time = 0
        while x < self.width - right_space:
            self.canvas.create_line(
                int(x),
                top_axis_space,
                int(x),
                self.height -
                bottom_space)
            self.canvas.create_text(x, top_axis_space // 2, text=str(time))
            x += pixel_gap
            time += time_gap

def split_into_paths(critical):
    paths  = [[critical[0]]]

    for i in range(1, len(critical)):
        new_paths =[]
        for p in paths:
            if p[-1][2] == critical[i][1]:
                p.append(critical[i])
            elif p[-1][1] == critical[i][1]:
                new_paths.append(p[:])
                new_paths[-1][-1] =  critical[i]
        if len(new_paths)>0:
            paths += new_paths
    return paths 


def main():
    psimple = [
        ["A", [], 2],
        ["B", [], 7],
        ["C", ["A"], 4],
        ["D", ["A"], 3],
        ["E", ["C"], 2],
        ["F", ["B", "D"], 4],
        ["G", ["B"], 1]
    ]
    
    p = [
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
    c = critical.Critical_Network()
    c.make_network_from_table(psimple)
    c.forward_pass()
    c.back_pass()
    c.set_critical()

    i = Gannt(c.critical, c.non_critical, 600, 400)
    i.draw_gannt()
    i.mainloop()

if __name__ == "__main__":
    main()


