from manim import *
class Gyros(VGroup):
    def __init__(self,**kwargs):
        VGroup.__init__(self,**kwargs)
        points=self.get_random_points()
        windmills=self.get_windmill(points)
        dots=self.get_dots(points)
        self.add(dots,windmills)
    def get_random_points(self,n_points=11,width=None,height=None):
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
        ])
    def get_windmill(self,points):
        windmills=VGroup()
        for point in points:
            angle=TAU*np.random.random()
            windmill=Line(LEFT,RIGHT)
            windmill.set_length(2*config['frame_width'])
            windmill.move_to(point)
            windmill.rotate(angle, about_point=point)
            windmills.add(windmill)
        return windmills
class WindmillScene(Scene):
    def construct(self):
        gyros=Gyros()
        self.add(gyros)
        self.wait(2)