import tkinter as tk
from tkinter import ttk
from math import floor, sqrt

INV2 = 1 / sqrt(2)

def clamp_and_bound(position, dx, dy, bounds):
    if len(bounds) != 4:
        raise ValueError
        
    min_x = bounds[0]
    max_x = bounds[1]
    min_y = bounds[2]
    max_y = bounds[3]
    
    #should dx push the position out of bounds, reduce dx to push to *exactly* the bound
    if pos[0] + dx < min_x:
        dx = min(0,min_x - pos[0])
    elif pos[0] + dx > max_x:
        dx = min(0,max_x - pos[0])
        
    #should dy '         '
    if pos[1] + dy < min_y:
        dy = min(0,min_y - pos[1])
    elif pos[1] + dy > max_y:
        dy = min(0,max_y - pos[0])
        
    return (dx, dy)
    
def normalize(x, min_x, max_x):
    x     += min_x
    max_x += min_x
    min_x += min_x
    return (x-min_x) / (max_x - min_x)

def game_loop():
    global canv, keydowns, pos, player_img, xspeed, yspeed
    
    #calculate movement 
    dx = keydowns[2] - keydowns[0]
    dy = keydowns[3] - keydowns[1]
    diag = 1 if not (dx and dy) else INV2
    dx_p = floor(xspeed * dx * diag)
    dy_p = floor(yspeed * dy * diag)
    
    #potentially clamp dx and dy
    #TODO: codify bounds more reasonably
    dx_p, dy_p = clamp_and_bound(pos,dx_p,dy_p,[-250,250,-250,250])
    
    #move canvas, canvas image, and internal marker
    canv.move(player_img,dx_p,dy_p)
    pos[0] += dx_p
    pos[1] += dy_p
    

#    canv.xview_moveto(0)
#    canv.yview_moveto(0)
#    canv.xview_scroll((300-250) + pos[0],tk.UNITS)
#    canv.yview_scroll((300-250) + pos[1],tk.UNITS)
    
    
    canv.xview_scroll(dx_p,tk.UNITS)
    canv.yview_scroll(dy_p,tk.UNITS)
    
    
    print(pos,dx_p,dy_p)
    #actually pan the camera
    '''
    if dx:
        canv.xview_scroll(dx, tk.UNITS)
    if dy:
        canv.yview_scroll(dy, tk.UNITS)
    '''
    canv.update()
    canv.after(25, game_loop)

def keyup(e):
    #print('up', e.keysym_num)
    k = e.keysym_num
    if k >= 65361 and k <= 65364: #arrow keys
        keydowns[k-65361] = 0
    
    
def keydown(e):
    #print('down', e.keysym_num)
    k = e.keysym_num
    if k >= 65361 and k <= 65364: #arrow keys
        keydowns[k-65361] = 1

if __name__ == "__main__":
    #main window
    s_width,s_height = 500,500
    root = tk.Tk()
    ttk.Style(root).theme_use('alt')
    root.title("Shooter")
    root.resizable(False,False)
    root.geometry(str(s_width) + 'x' + str(s_height))
    
    root.bind("<KeyPress>", keydown)
    root.bind("<KeyRelease>", keyup)
    
    #canvas
    canv = tk.Canvas(root, bg='green', height=500, width=500, scrollregion=(-300,-300,300,300))
    canv["xscrollincrement"] = 1
    canv["yscrollincrement"] = 1
    #scroll the canvas to fit around our position '0,0' as the center
    canv.xview_scroll(-250, tk.UNITS)
    canv.yview_scroll(-250, tk.UNITS)
    canv.grid()

    #GAME VARIABLES
    keydowns = [0]*4
    pos  = [0, 0]
    epos = [0, 0]
    
    #existent images
    canv.create_rectangle(-100,-100,-90,-90)
    canv.create_rectangle(90,100,100,90)
    
    canv.create_polygon([-250,-250,-250,250,250,250,250,-250],fill='',outline='black')
    
    #player image
    r = 50
    player_img = canv.create_oval(pos[0] - floor(r/2), pos[0] - floor(r/2), 
                                  pos[0] + floor(r/2), pos[0] + floor(r/2))
    enemy_img  = canv.create_oval(epos[0] - floor(r/2), epos[0] - floor(r/2), 
                                  epos[0] + floor(r/2), epos[0] + floor(r/2), outline='cyan')
    xspeed = 5
    yspeed = 5
    
    game_loop()
    root.mainloop()