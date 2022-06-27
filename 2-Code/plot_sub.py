from manim import *
from subisom_prot import *

def colormol(molecule):
    if molecule=='C':
        return RED
    if molecule=='H':
        return WHITE
    if molecule=='O':
        return BLUE
    if molecule=='N':
        return GREEN
    if molecule=='S': 
        return ORANGE
    else:
        return black
    
prot1 = recup('lim14')
prot2 = recup('lim10')

offset1 = [min([at.point[i] for at in prot1.latom]) for i in [0,1,2]]

def no(l,offset=offset1):
    a,b,c = l[0]-offset[0], l[1]-offset[1], l[2]-offset[2]
    return [a-5,b-5,c] #[a/30-7, b/30-7, c/30] #c/2+5

class Protein(ThreeDScene):
    def construct(self):
     
        axes = ThreeDAxes((0, 10), (0, 10), (0, 10), 10,10,10)
        ld1 = [Dot3D(point=no(molec.point), color = colormol(molec.atom)) for molec in prot1.latom]
        ld2 = [Dot3D(point=no(molec.point), color = colormol(molec.atom)) for molec in prot2.latom]
        lines1 = tuple([Line3D(start=no(x), end=no(y), thickness=0.015, color=GREEN) for (x,y) in prot1.liaisons_sans_doublons() ])
        lines2 = tuple([Line3D(start=no(x), end=no(y), thickness=0.015, color=ORANGE) for (x,y) in prot2.liaisons_sans_doublons() ])
        self.add(*axes,*ld1,*ld2,*lines1,*lines2)
    
        self.set_camera_orientation( phi=3*PI/8, theta=PI/6, frame_center=(0,0,5) )
        self.camera.set_zoom(0.7)
        
#         self.begin_ambient_camera_rotation(rate=PI/4)
#         self.wait(5.3)
#         self.stop_ambient_camera_rotation()

#cd "C:\Users\Adrien Dubois\Desktop\TIPE\2-code"
#manim -spqk plot_sub.py