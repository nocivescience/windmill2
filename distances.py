from manim import *
import itertools as it
class DistanceScene(Scene):
    CONFIG={
        'colors':[RED,BLUE,GREEN,YELLOW,PURPLE,ORANGE],
    }
    def construct(self):
        colors=it.cycle(self.CONFIG['colors'])
        lines=VGroup()
        for _ in range(40):
            line,number=self.line_distance()
            random_point=self.get_random_point()
            line_number=VGroup(line,number).move_to(random_point).set_color(next(colors))
            line_number.scale(np.random.random())
            lines.add(line_number)
        self.play(Write(lines))
        for t in np.random.uniform(1,4,10):
            self.play(*[line.animate.put_start_and_end_on(LEFT,RIGHT*t) for line in lines])
        self.wait()
    def line_distance(self):
        line=Line(LEFT,RIGHT)
        number=self.number_line(line)
        return line, number
    def number_line(self,line):
        number=DecimalNumber(line.get_length())
        number.next_to(line,UP,buff=SMALL_BUFF)
        number.add_updater(lambda m: m.set_value(line.get_length()))    
        return number
    def get_random_point(self):
        return np.array([
            [
                np.random.uniform(-config["frame_x_radius"],config["frame_x_radius"]),
                np.random.uniform(-config["frame_y_radius"],config["frame_y_radius"]),
                0
            ]
        ])