import time

MOVEMENT = 0x0000
MISSILE  = 0x0001

s_width,s_height = 500,500
g_width,g_height = 600,600
default_rad = 50

DISPLAY_BOUNDS = True

class Box:
    def __init__(self,*pts, root=None, halo=True, col='black'):
        if len(pts) == 2: #(x1,y3)
            x1, y1 = pts  #unpack
            pts = ([x1] * 3) + ([y1] * 4) + [x1]
        elif len(pts) == 4:
            x1, y1, x3, y3 = pts
            pts = [x1,y1,x1,y3,x3,y3,x3,y1]
        elif len(pts) != 8:
            raise ValueError
 
        #print(pts)
        self.col = col
        self.pts = pts
        self.root = root
        if self.root:
            self.assign_visual_mapping(root)
            
        if halo:
            self.halo = self.create_halo(default_rad)
         
    def edge(self,x,y,err=0.0):
        bitmap = [False] * 4
        x1, y1, x3, y3 = self.pts[0],self.pts[1],self.pts[4],self.pts[3]
        
        bitmap[0] = abs(x - x1) <= err and y >= y1 and y <= y3 #left
        bitmap[1] = abs(y - y1) <= err and x >= x1 and x <= x3 #top
        bitmap[2] = abs(x - x3) <= err and y >= y1 and y <= y3 #right
        bitmap[3] = abs(y - y3) <= err and x >= x1 and x <= x3 #bottom
        
        return bitmap if any(bitmap) else None
         
    def halo_collide(self,x,y):
        collide_map = [False] * 4
        for idx, h in enumerate(self.halo):
            if h.__in__(x,y):
                collide_map[idx] = True
                
        if any(collide_map):
            return collide_map #[left,top,right,down]
        return None
            
    def __in__(self,x,y,err=0.0):
        x1, y1, x3, y3 = self.pts[0],self.pts[1],self.pts[4],self.pts[3]
        return x >= x1 - err and x <= x3 + err and y >= y1 - err and y <= y3 + err
            
    def create_halo(self, r):
        x1, y1, x3, y3 = self.pts[0],self.pts[1],self.pts[4],self.pts[3]
        r2 = r >> 1
        
        if DISPLAY_BOUNDS:
            cols = ['red','white','orange','cyan']
        else:
            cols = ['','','','']
        
        return [
            Box(x1-r2,y1-r2,x1+r2,y3+r2,halo=False, col=cols[0]), #left
            Box(x1-r2,y1-r2,x3+r2,y1+r2,halo=False, col=cols[1]), #top
            Box(x3-r2,y1-r2,x3+r2,y3+r2,halo=False, col=cols[2]), #right
            Box(x1-r2,y3-r2,x3+r2,y3+r2,halo=False, col=cols[3]), #down
        ]
            
            
    def assign_visual_mapping(self, root):
        if self.root:
            self.root.delete(self.img)
        self.img = root.create_polygon(self.pts, fill='', outline=self.col)
        self.root = root

obj_map1 = [
        Box(-120,-60),
        Box(-250,250), #bounding
]

def byte(i):
    return i.to_bytes(1,'little')