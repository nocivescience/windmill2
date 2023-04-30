from manim import *
import itertools as it
class Gyros(VGroup):
    CONFIG={
        'colors':[
            RED,
            GREEN,
            BLUE,
            YELLOW,
            PURPLE,
            ORANGE,
            PINK,
            TEAL,
        ],
        'windmill_style': {
            'stroke_width': 2,
        },
    }
    def __init__(self,**kwargs):
        VGroup.__init__(self,**kwargs)
        points=self.get_random_points()
        windmills=self.get_windmill(points)
        dots=self.get_dots(points)
        self.add(dots,windmills)
    def get_random_points(self,n_points=50,width=None,height=None):
        if width is None:
            width=config['frame_width']
        if height is None:
            height=config['frame_height']
        return np.array([
            [
                -width/2+np.random.random()*width,
                -height/2+np.random.random()*height,
                0
            ]
            for _ in range(n_points)
        ])
    def get_dots(self, points):
        return VGroup(*[
            Dot().move_to(point) for point in points
        ]).set_z_index(1)
    def get_windmill(self,points):
        windmills=VGroup()
        colors=it.cycle(self.CONFIG['colors'])
        for point in points:
            angle=TAU*np.random.random()
            windmill=Line(LEFT,RIGHT)
            windmill.point=point
            windmill.set_length(2*config['frame_width'])
            windmill.set_style(**self.CONFIG['windmill_style'])
            windmill.move_to(point)
            windmill.set_color(next(colors))
            windmill.rotate(angle, about_point=point)
            windmill.add_updater(lambda w, dt: self.update_windmill(w,dt))
            windmills.add(windmill)
        return windmills
    def update_windmill(self,windmill,dt):
        windmill.rotate(dt,about_point=windmill.point)
class WindmillScene(Scene):
    def construct(self):
        gyros=Gyros()
        self.add(gyros)
        self.wait(22)