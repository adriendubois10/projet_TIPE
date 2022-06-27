from manim import *
from extract_PDB import *

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
    
def no(l):
    a,b,c = l[0], l[1], l[2]
    return [a/2,b/2,c/2+5] #[a/30-7, b/30-7, c/30]
    
prot = recup('lim_22_test')

    
class Protein(ThreeDScene):
    def construct(self):
     
        #axes = ThreeDAxes((0, 10), (0, 10), (0, 10), 10,10,10)
        ld = [Dot3D(point=no(molec.point), color = colormol(molec.atom)) for molec in prot.latom]
        print("Nombre d'atomes = ", len(ld))
        d = tuple( ld )
        lines = tuple([Line3D(start=no(x), end=no(y), color=GREY) for (x,y) in prot.liaisons_sans_doublons() ])
        self.add(*d, *lines)
    
        self.set_camera_orientation( phi=PI/3, theta=PI/3, frame_center=(0,0,5) )
        self.camera.set_zoom(0.6)
        
#         self.begin_ambient_camera_rotation(rate=PI/4)
#         self.wait(5.3)
#         self.stop_ambient_camera_rotation()

#cd "C:\Users\Adrien Dubois\Desktop\TIPE\2-code"
#manim -spqk plot_protein.py