from manim import *
class Windmill(Scene):
    CONFIG = {
        'dot_config': {
            'fill_color': YELLOW,
            'radius': 0.05, 
            'background_stroke_width': 2,
            'background_stroke_color': BLACK,   
        },
        'windmill_style': {
            'stroke_color': RED,
            'stroke_width': 2,
            'background_stroke_width': 3, 
            'background_stroke_color': BLACK,   
        },
        'windmill_length': 2*config['frame_width'],
        'windmill_rotation_speed': 0.25,
        'leave_shadown': False,
    }
    def get_random_point_set(self,n_points=11,width=6,height=6):
        return np.array([
            [
                -width/2+np.random.random()*width,
                -height/2+np.random.random()*height,
                0
            ]
            for _ in range(n_points)
        ])
    def get_dots(self,point_set):
        return VGroup(*[
            Dot(
                point,
                **self.CONFIG['dot_config']
            )
            for point in point_set
        ])
    def get_windmill(self,points,pivot=None, angle=TAU/8):
        line = Line(LEFT,RIGHT)
        line.set_length(self.CONFIG['windmill_length'])
        line.set_angle(angle)
        line.set_style(**self.CONFIG['windmill_style'])
        line.point_set=points
        if pivot is not None:
            line.pivot=pivot
        else:
            line.pivot=points[0]
        line.rot_speed=self.CONFIG['windmill_rotation_speed']
        line.add_updater(lambda l: l.move_to(l.pivot))
        return line
    def get_pivot_dot(self,windmill,color=BLUE_B):
        pivot_dot=Dot(color=color)
        pivot_dot.add_updater(lambda d: d.move_to(windmill.pivot))
        return pivot_dot
    def next_pivot_and_angle(self,windmill):
        curr_angle = windmill.get_angle()
        pivot = windmill.pivot
        non_pivots = np.array(filter(
            lambda p: not np.all(p == pivot),
            windmill.point_set
        ))
        angles = np.array([
            -(angle_of_vector(point - pivot) - curr_angle) % PI
            for point in non_pivots
        ])

        # Edge case for 2 points
        tiny_indices = angles < 1e-6
        if np.all(tiny_indices):
            return non_pivots[0], PI

        angles[tiny_indices] = np.inf
        index = np.argmin(angles)
        return non_pivots[index], angles[index]
class WindmillScene(Windmill):
    def construct(self):
        dots=self.get_dots(self.get_random_point_set())
        line=self.get_windmill(dots).set_z_index(-1)
        dot_pivot=self.get_pivot_dot(line)
        self.play(Create(dots))
        self.play(FadeIn(line),Create(dot_pivot))
        puntos=self.next_pivot_and_angle(line)
        puntos_dot=MathTex(puntos)
        self.play(Write(puntos_dot))
        self.wait(3)