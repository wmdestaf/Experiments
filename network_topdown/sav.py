	diag = 1 if not (dx and dy) else INV2
    dx_p = floor(xspeed * dx * diag)
    dy_p = floor(yspeed * dy * diag)
    
    dx_p, dy_p = clamp_and_bound(pos,dx_p,dy_p,[-250,250,-250,250])
    
    synchronize_out(pos[0], pos[1], dx_p, dy_p)
    
    #move canvas, canvas image, and internal marker
    canv.move(player_img,dx_p,dy_p)
    canv.xview_scroll(dx_p,tk.UNITS)
    canv.yview_scroll(dy_p,tk.UNITS)
    pos[0] += dx_p
    pos[1] += dy_p