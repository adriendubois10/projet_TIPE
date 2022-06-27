from manim import *
from cas_simple_nuage import N

def no(l):
    a,b,c = l[0], l[1], l[2]
    return [a-5/2, b-5/2, c]

class Test(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes((-1, 6), (-1, 6), (-1, 6), 7, 7, 7)
        d = tuple( [Dot3D(point=no(x), color = RED) for x in N.liste] )
        d1, d2, d3 = Dot3D(point=no([5,0,0]),color=GREEN), Dot3D(point=no([0,5,0]),color=BLUE), Dot3D(point=no([0,0,5]),color=YELLOW)
        def param_surface(u, v):
            return 0
        plan = Surface(lambda u, v: axes.c2p(u, v, param_surface(u, v)),resolution=11,v_range=[-1, 5],u_range=[-1, 5])
        plan.set_style(fill_opacity=0.3)
        self.set_camera_orientation(phi= 80 * DEGREES , theta = 10*DEGREES, focal_distance = 20,frame_center=(1,-2,4.5), zoom = 1 )
        self.add(axes, plan,d1, d2, d3, *d)
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(20*PI)
        self.stop_ambient_camera_rotation()
        
#cd "C:\Users\Adrien Dubois\Desktop\TIPE\cas_simple     
#manim -spqh plotnuagedepoint.py nuage