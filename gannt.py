import critical
import precedence
import tkinter as tk

class Gannt():
    def __init__(
        self,
            critical_act,
            non_critical,
            width,
            height,
            *args,
            **kwargs):
        """Arguments:
        critical_act: list of critical activities, each one a list:
        [Label, start_time, end_time]
        non_critical: list of non_critical activities, each one a list
        [Label, start_time, early_end_time, late_end_time]
        width and height of the window
        any other arguments to be passed to tk.TK
        """
        raise NotImplementedError


    def draw(self):
        """Draw a complete gannt chart"""
        # Split the list of critical activities into critcial paths
        max_time = self.critical[-1][2]
        paths = split_into_paths(self.critical)

        # marginal space
        left_axis_space = 20
        right_space = 20
        top_axis_space = 20
        bottom_space = 20

        # calculate conversion rates for changing lenghts of time into
        # pixels
        pixels_per_unit_time = (
            self.width - left_axis_space - right_space) / max_time
        box_height = ((self.height - top_axis_space - bottom_space) //
                      (len(self.non_critical) + len(paths)))

        # draw a grid in the background, and label
        self._draw_grid(max_time, left_axis_space,
                        right_space, top_axis_space, bottom_space,
                        pixels_per_unit_time)

        # draw the critical activities one line per critical path.
        for i, critical_path in enumerate(paths):
            for c in critical_path:
                label = c[0]
                x0 = left_axis_space + c[1] * pixels_per_unit_time
                y0 = top_axis_space + i * box_height
                x1 = left_axis_space + c[2] * pixels_per_unit_time
                y1 = top_axis_space + (i + 1) * box_height
                #print("crit", label, x0, y0, x1, y1)
                self._draw_critical(label, x0, y0, x1, y1)

        # draw the non critical on separate lines
        for i, n in enumerate(self.non_critical):
            label = n[0]
            x0 = left_axis_space + n[1] * pixels_per_unit_time
            y0 = top_axis_space + (len(paths) + i) * box_height
            x1 = left_axis_space + n[2] * pixels_per_unit_time
            y1 = top_axis_space + (len(paths) + i + 1) * box_height
            x2 = left_axis_space + n[3] * pixels_per_unit_time
            #print("non", label, x0, y0, x1, y1, x2)
            self._draw_noncritical(label, x0, y0, x1, y1, x2)

    def _draw_grid(self, max_time, left_axis_space,
                   right_space, top_axis_space, bottom_space,
                   pixels_per_unit_time):
        """Draw a grid in the background, adapt the spaceing to the size of
        the chart"""

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
            self._draw_grid_line(x,top_axis_space, bottom_space)
            self._write_text(x, top_axis_space//2, time)
            x += pixel_gap
            time += time_gap



    def show(self):
        """Shows the gannt chart on the screen, if possible"""
        raise NotImplementedError

    def save(self, filename):
        """Save the gannt chart to disk, if possible"""
        raise NotImplementedError

class GanntPIL(Gannt):
    def __init__(
        self,
            critical_act,
            non_critical,
            width,
            height,
            *args,
            **kwargs):
        global Image, ImageDraw, ImageTk
        from PIL import Image, ImageDraw, ImageTk, ImageFont
        self.width = width
        self.height = height
        self.critical = critical_act
        self.non_critical = non_critical

        self.image = Image.new(mode='RGB', size=[width, height],color='white')
        self.drawable = ImageDraw.Draw(self.image)
#       self.font = ImageFont

    def _draw_critical(self,label,x0,y0,x1,y1):
        self.drawable.rectangle([x0,y0,x1,y1],fill='white',outline='black')
        self.drawable.text([(x0+x1)//2, (y0+y1)//2],label, fill='black')

    def _draw_noncritical(self,label,x0,y0,x1,y1,x2):
        self.drawable.rectangle([x0,y0,x1,y1],fill='white',outline='black')
        self.drawable.text([(x0+x1)//2, (y0+y1)//2],label, fill='black')
        self.drawable.rectangle([x1, y0, x2, y1], fill='#aaaaaa',outline='black')


    def show(self):
        root = tk.Tk()
        img = ImageTk.PhotoImage(self.image)
        panel = tk.Label(root, image = img)
        panel.pack(side='bottom', fill='both', expand= 'yes')
        root.mainloop()

    def save(self, filename):
       self.image.save(filename) 
    
    def _draw_grid_line(self, x,top_axis_space, bottom_space):
         self.drawable.line([ int(x), top_axis_space, int(x), self.height -
                             bottom_space], fill='black')

    def _write_text(self,x,y,text):
        self.drawable.text([x, 0], str(text) )
 

class GanntTk(tk.Tk, Gannt):
    """Draw a gannt chart from a list of critical and non critical activities
    """

    def __init__(
        self,
            critical_act,
            non_critical,
            width,
            height,
            *args,
            **kwargs):
        """Arguments:
        critical_act: list of critical activities, each one a list:
        [Label, start_time, end_time]
        non_critical: list of non_critical activities, each one a list
        [Label, start_time, early_end_time, late_end_time]
        width and height of the window
        any other arguments to be passed to tk.TK
        """
        super().__init__(*args, **kwargs)
        self.title( "Gannt Chart")
        self.canvas = tk.Canvas(self, width=width, height=height)
        self.canvas.pack()
        self.width = width
        self.height = height
        self.critical = critical_act
        self.non_critical = non_critical

    def _draw_grid_line(self, x,top_axis_space, bottom_space):
         self.canvas.create_line(
                int(x),
                top_axis_space,
                int(x),
                self.height -
                bottom_space)

    def _write_text(self,x,y,text):
        self.canvas.create_text(x, y, text=str(text))
 

    def _draw_critical(self, label, x0, y0, x1, y1):
        """Draw and label critical activity at the position indicated"""
        self.canvas.create_rectangle(x0, y0, x1, y1,
                                     fill='white')
        self.canvas.create_text((x0 + x1) // 2, (y0 + y1) // 2, text=label)

    def _draw_noncritical(self, label, x0, y0, x1, y1, x2):
        """draw a non-critical activity, with a box and shaded region for the
        float."""
        self.canvas.create_rectangle(x0, y0, x1, y1, fill='white')
        self.canvas.create_text((x0 + x1) // 2, (y0 + y1) // 2, text=label)
        self.canvas.create_rectangle(x1, y0, x2, y1,
                                     fill='black', stipple='gray25')

    def show(self):
        self.mainloop()


def split_into_paths(critical):
    """Convert from a list of activities into a list critical paths.
    Often there is only one critical path, but there may be several. One
    activity may be in several different critical paths"""
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


def main():
    """Run with some different examples"""

    c = critical.Critical_Network()
    c.make_network_from_table(precedence.new_prog)
    c.forward_pass()
    c.back_pass()
    c.set_critical()
    critical.make_dot(c,"act_net.dot")

    i = GanntPIL(c.critical, c.non_critical, 600,400)
    i.draw()
    i.show()
    i.save("gannt.png")

if __name__ == "__main__":
    main()
