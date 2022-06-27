from manim import *
from generer_nuage import N

def no(l):
    a,b,c = l[0], l[1], l[2]
    return [a-5/2, b-5/2, c]

class relies(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes((-1, 6), (-1, 6), (-1, 6), 7, 7, 7).ticklabel()
        d = tuple( [Dot3D(point=no(x), color = RED) for x in N.liste] )
        
        def param_surface(u, v):
            return 0
        plan = Surface(lambda u, v: axes.c2p(u, v, param_surface(u, v)),resolution=11,v_range=[-1, 5],u_range=[-1, 5])
        plan.set_style(fill_opacity=0.2)
        
        lines = tuple( [Line3D(start=no(N.liste[i]), end=no(N.liste[i+1]), color=BLUE) for i in range(N.nbr-1)] )
        
        self.add(axes, *d, *lines, plan)
        
        self.set_camera_orientation(phi= 75 * DEGREES , theta = 25*DEGREES, focal_distance = 20,frame_center=(1,-2,4.5), zoom = 1 )

        
#manim -spqh plotrelies.py relies