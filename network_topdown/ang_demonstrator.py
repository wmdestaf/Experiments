from math import floor, sqrt, sin, cos, tan, radians

def collide_ray(x1, y1, ang, objs):
    MAX_RAY_LEN = 300
    dx = cos(ang)
    dy = sin(ang)
    
    x, y = x1, y1
    
    while sqrt( (x - x1)**2 + (y - y1)**2 ) < MAX_RAY_LEN:
        
        #determine how many dx's we are away from a multiple of 10
        if dx > 0: #towards positive 10
            ddx = ( 10 - (x%10) ) / dx
        else: 
            ddx = (x % 10) / dx
            
        if dy > 0: #towards positive 10
            ddy = ( 10 - (y%10) ) / dy
        else: 
            ddy = (y % 10) / dy
            
        dd = min(ddx, ddy)
        x += dd * dx
        y += dd * dy
        
        print(x,y,ddx,ddy,dd)
    
    
if __name__ == "__main__":
    x = float(input("X: "))
    y = float(input("Y: "))
    t = radians(float(input("Theta: ")))
    collide_ray(x,y,t,None)