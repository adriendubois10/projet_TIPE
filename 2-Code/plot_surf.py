from manim import * 
from generer_nuage import *

N = rotation_z(genererliaisonsunif(10,10)) #10 points
M = rotation_z(genererliaisonsunif(10,10))

colorGOR = [color.Color(i) for i in ['#86f686', '#58d658', '#28ad28', '#ffff58', '#ffe500', '#ffc65c', '#f19c00', '#ff6464', '#ff4848', '#e70000']]
c = color_dlines(aires_liste(N,M))

#Translation à l'origine

def no(l):
    a,b,c = l[0], l[1], l[2]
    return [a-5, b-5, c]
    
class DSurf(ThreeDScene):
    def construct(self):
     
        axes = ThreeDAxes((0, 10), (0, 10), (0, 10), 10,10,10)
        limits = tuple([Dot3D(point=no(x), color = YELLOW) for x in [[10,0,0],[0,10,0],[0,0,10]] ])
        dn = tuple( [Dot3D(point=no(x), color = BLUE) for x in N.liste] )
        dm = tuple( [Dot3D(point=no(x), color = PURPLE) for x in M.liste] )
        testS = Surface( lambda u, v: paramtriangle(u, v, no(N.liste[0]) , no(M.liste[0]), no(M.liste[1])) )
        #S1 = tuple([Surface( lambda u, v: paramtriangle(u, v, no(N.liste[k]) , no(M.liste[k]), no(M.liste[k+1])) , fill_color=RED, fill_opacity = 1) for k in range(N.nbr-1)])
        #S2 = tuple([Surface( lambda u, v: paramtriangle(u, v, no(N.liste[k]) , no(N.liste[k+1]), no(M.liste[k+1])) , fill_color=YELLOW, fill_opacity=0.8) for k in range(N.nbr-1)])
        
        self.add(axes, *dn, *dm,  *limits, testS)
        self.set_camera_orientation( phi=PI/3, theta=PI/6, frame_center=(0,0,5) )
        self.camera.set_zoom(0.4)
        
        #self.begin_ambient_camera_rotation(rate=PI/4)
        #self.wait(3)
        #self.stop_ambient_camera_rotation()

#cd "C:\Users\Adrien Dubois\Desktop\TIPE\cas_simple"
#manim -spqm plot_surf.py
#manim -pqh plot_surf.py --disable_caching
        
        