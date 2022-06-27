from manim import *
from cas_simple_nuage import *

N = rot_z(genererliaisonsunif(10,10)) #10 points
#M = rot_z(genererliaisonsunif(10,10))
M = rot_z(decalagex(N,2,0))

colorGOR = [color.Color(i) for i in ['#86f686', '#58d658', '#28ad28', '#ffff58', '#ffe500', '#ffc65c', '#f19c00', '#ff6464', '#ff4848', '#e70000']]
color_dist = color_dlines( distpoints(N,M) )

def no(l):
    a,b,c = l[0], l[1], l[2]
    return [a-5, b-5, c]
    
class DLines(ThreeDScene):
    def construct(self):
     
        axes = ThreeDAxes((0, 10), (0, 10), (0, 10), 10,10,10)
        #limits = tuple([Dot3D(point=no(x), color = YELLOW) for x in [[10,0,0],[0,10,0],[0,0,10]] ])
        #dn = tuple( [Dot3D(point=no(x), color = BLUE) for x in N.liste] )
        #dm = tuple( [Dot3D(point=no(x), color = PURPLE) for x in M.liste] )
        ln = tuple( [Line3D(start=no(N.liste[i]), end=no(N.liste[i+1]), color=WHITE, thickness=0.05) for i in range(N.nbr-1)] )
        lm = tuple( [Line3D(start=no(M.liste[i]), end=no(M.liste[i+1]), color=GREEN_B,thickness=0.05) for i in range(N.nbr-1)] )
        #lines = tuple([Line3D(start=no(N.liste[i]), end=no(M.liste[i]), color= colorGOR[ color_dist[i] ]) for i in range(N.nbr)])
        
        self.add(axes, *lm, *ln)#, *lines) #*dn, *dm,  *limits)
        self.set_camera_orientation( phi=PI/3, theta=PI/6, frame_center=(0,0,5) )
        self.camera.set_zoom(0.4)
        
        self.begin_ambient_camera_rotation(rate=PI/4)
        self.wait(3)
        self.stop_ambient_camera_rotation()

#cd "C:\Users\Adrien Dubois\Desktop\TIPE\cas_simple"
#manim -spqk plot_distlines.py
#manim -pqh plot_distlines.py --disable_caching