from manim import *
class WindmillScene(Scene):
    CONFIG={
        'dot_config': {
            'fill_color': RED,
            'radius': 0.05,
            'background_stroke_width': 2,   
            'background_stroke_color': GREY,
        },
        'windmill_style': {
            'stroke_color': BLUE_A,
            'stroke_width': 2,
            'background_stroke_width': 3,
            'background_stroke_color': GREY,
        },
        'windmill_length': 2*config['frame_width'],
        'windmill_rotation_speed': 0.25,
        'leave_shadown': False,
        'final_run_time': 2,
        'windmill_rotation_speed': 0.5,
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
    def get_dots(self,points):
        return VGroup(*[
            Dot(point, **self.CONFIG['dot_config'])
            for point in points
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
    def get_pivot_dot(self,windmill, color=YELLOW):
        pivot_dot=Dot(windmill.pivot, color=color)
        pivot_dot.add_updater(lambda d: d.move_to(windmill.pivot))
        return pivot_dot
    def next_pivot_and_angle(self,windmill):
        curr_angle=windmill.get_angle()
        pivot=windmill.pivot
        non_pivot_points=list(filter(lambda p: not np.all(p==pivot),windmill.point_set))
        angles=np.array([
            -(angle_of_vector(p-pivot)-curr_angle)%PI
            for p in non_pivot_points
        ])
        index=np.argmin(angles)
        return non_pivot_points[index], angles[index]
    def rotate_to_next_pivot(self,windmill, max_time=None, added_anims=None):
        new_non_pivot,angle=self.next_pivot_and_angle(windmill)
        change_pivot_at_end=True
        if added_anims is None:
            added_anims=[]
        run_time=angle/windmill.rot_speed
        if max_time is not None and run_time>max_time:
            ratio=max_time/run_time
            rate_func=(lambda t: ratio*t)
            run_time=max_time
            change_pivot_at_end=False
        else:
            rate_func=linear
        for anim in added_anims:
            if anim.run_time>run_time:
                anim.run_time=run_time
        self.play(
            Rotate(
                windmill,
                -angle,
                rate_func=rate_func,
                run_time=run_time,
            ),
            *added_anims,
        )
        if change_pivot_at_end:
            windmill.pivot=new_non_pivot
        return run_time
    def let_windmill_run(self, windmill, time):
        anims_from_last_hit=[]
        while time>0:
            last_run_time=self.rotate_to_next_pivot(
                windmill,
                max_time=time,
                added_anims=anims_from_last_hit,
            )
            time-=last_run_time
    def construct(self):
        points=self.get_random_point_set()
        dots=self.get_dots(points).set_z_index(1)
        windmill=self.get_windmill(points)
        dot_pivot=self.get_pivot_dot(windmill)
        for mob in [dots,windmill,dot_pivot]:
            self.play(Create(mob))
        self.rotate_to_next_pivot(windmill)
        run_time=self.rotate_to_next_pivot(windmill) # si sacvo esto queda la caga
        self.let_windmill_run(windmill, 3)
        self.wait()