import tkinter as tk
from tkinter import ttk
from random import randint, random
from math import floor, inf

w=10

def rgb(a):
    return '#%02x%02x%02x' % a

def exp_wait(duration):
    if duration >= 1:
        canv.after(1)
    elif random() < duration: #lowest increment is 1, so clever with expected values...
        canv.after(1)
def observe_callbk(i,j,duration=5):
    update_scan()
    i_old = canv.itemconfig(array_gfx[i],'outline')[4]
    j_old = canv.itemconfig(array_gfx[j],'outline')[4]
    canv.itemconfig(array_gfx[i],outline='yellow')
    canv.itemconfig(array_gfx[j],outline='yellow')
    canv.tag_raise(array_gfx[i])
    canv.tag_raise(array_gfx[j])
    canv.update()
    exp_wait(duration)
    canv.itemconfig(array_gfx[i],outline=i_old)
    canv.itemconfig(array_gfx[j],outline=j_old)

def shuffle(a,observer=observe_callbk,duration=5):
    for i in range(0,len(a)-1,1):
        j = randint(i,len(a)-1)
        observer(i,j,duration)
        tmp = a[i]
        a[i] = a[j]
        a[j] = tmp
        
    update_scan()
 
def invert(a,observer=observe_callbk,duration=5):
    for i in range(0,int(len(a)/2)):
        j = len(a)-i-1
        observer(i,j,duration)
        tmp = a[i]
        a[i] = a[j]
        a[j] = tmp
        
    update_scan()
    
def flip(arr, k,observer=observe_callbk,duration=5):
    left = 0
    while left < k:
        observer(left,k,duration)
        arr[left], arr[k] = arr[k], arr[left]
        k -= 1
        left += 1

def max_index(arr, k,observer=observe_callbk,duration=5):
    index = 0
    for i in range(k):
        observer(index,i,duration)
        if arr[i] > arr[index]:
            index = i
    return index

def pancake(arr,observer=observe_callbk,duration=5):
    n = len(arr)
    while n > 1:
        maxdex = max_index(arr, n)
        flip(arr, maxdex)
        flip(arr, n - 1)
        n -= 1
    
    update_scan()
 
def selection(a,observer=observe_callbk,duration=5):
    for i in range(len(a)):
        min_j = -1
        for j in range(i, len(a)):
            observer(i,j,duration)
            if a[j] < a[min_j]:
                min_j = j
        
        #swap!
        tmp = a[min_j]
        a[min_j] = a[i]
        a[i] = tmp
        
    update_scan()
 
def insertion(a,observer=observe_callbk,duration=5):
    for j in range(1,len(a)):
        key = a[j]
        i = j-1
        observer(i,j,duration)
        while i >= 0 and a[i] > key:
            a[i+1]=a[i]
            i -= 1
            observer(i,j,duration)
        a[i+1]=key
        
    update_scan()

def bubble(a,observer=observe_callbk,duration=5):
    done=False
    j=0
    while not done:
        done=True
        for i in range(1,len(a)-j):
            observer(i,i-1,duration)
            if a[i-1] > a[i]:
                tmp = a[i-1]
                a[i-1] = a[i]
                a[i] = tmp
                done=False
        j += 1
        
    update_scan()

def merge_sort(a,observer=observe_callbk,duration=5):
    __merge_sort(a,0,len(a),observer,duration)
    update_scan()
    
def __merge_sort(a,p,r,observer=observe_callbk,duration=5):
    if p < r - 1:
        q = floor((p+r) * 0.5)
        __merge_sort(a,p,q)
        __merge_sort(a,q,r)
        merge(a,p,q,r,observer,duration)

def merge(a,p,q,r,observer=observe_callbk,duration=5):
    L=a[p:q]
    R=a[q:r]
    L.append(inf)
    R.append(inf)

    i=j=0
    for k in range(p,r):
        observer(min(p+i,q-1),min(q+j,r-1),duration)
    
        if L[i] <= R[j]:
            a[k] = L[i]
            i += 1
        else:
            a[k] = R[j]
            j += 1

def gnome(a,observer=observe_callbk,duration=5):
    pos=0
    while pos < len(a):
        observer(pos,max(0,pos-1))
        if pos == 0 or a[pos] >= a[pos-1]:
            pos += 1
        else:
            tmp = a[pos]
            a[pos] = a[pos-1]
            a[pos-1] = tmp
            pos -= 1

def update_scan():
    global array_num, array_gfx
    global height
    
    for idx, i in enumerate(array_num):
        color = rgb(((int(255-(255*i/width))),0,int(255*i/width)))
        canv.coords(array_gfx[idx],idx*w,height-i,(idx+1)*w,height)
        canv.itemconfig(array_gfx[idx],outline=color)

def on_rz_btn(ent, rt):
    global w, array_gfx, array_num
    
    try:
        x = int(ent.get())
        if x >= 1 and x <= 500:
            w=x
            for old in array_gfx:
                canv.delete(old)
            array_gfx = [canv.create_rectangle(i*w,0,(i+1)*w,height,outline=rgb(((int(255-(255*i/width))),0,int(255*i/width)))) for i in range(0,width,w)]
            array_num = [i for i in range(1,501,w)]
            update_scan()
            rt.destroy()
            
    except ValueError:
        pass

def show_resize():  
    r = tk.Toplevel(root,bg='gray')
    r.title("Resize")
    r.geometry("200x100")
    tk.Label(r,text='Pixels per Item?',bg='gray',fg='white').pack()
    ent = tk.Entry(r)
    ent.pack()
    but = tk.Button(r,text='Save',bg='black',fg='white',command=lambda: on_rz_btn(ent,r))
    but.pack()

if __name__ == "__main__":
    width,height=500,500
    #root window
    root = tk.Tk()
    ttk.Style(root).theme_use('alt')
    root.title("Sort")
    root.resizable(False,False)
    root.geometry(str(width) + 'x' + str(height))
    
    #canvas
    canv = tk.Canvas(root, height=height, width=width, bg='black')
    canv.grid()
    
    #MENU
    menubar = tk.Menu(root)
    configmenu = tk.Menu(menubar, tearoff=0)
    configmenu.add_command(accelerator='S',label='Shuffle',command=lambda: shuffle(array_num,duration=5))
    configmenu.add_separator()
    configmenu.add_command(accelerator='I',label='Insertion',command=lambda: insertion(array_num,duration=5))
    configmenu.add_command(accelerator='L',label='Selection',command=lambda: selection(array_num,duration=5))
    configmenu.add_command(accelerator='B',label='Bubble',command=lambda: bubble(array_num,duration=5))
    configmenu.add_command(accelerator='G',label='Gnome',command=lambda: gnome(array_num,duration=5))
    configmenu.add_command(accelerator='P',label='Pancake',command=lambda: pancake(array_num,duration=5))
    configmenu.add_command(accelerator='M',label='Merge',command=lambda: merge_sort(array_num,duration=0))
    configmenu.add_separator()
    configmenu.add_command(accelerator='S',label='Resize',command=lambda: show_resize())
    configmenu.add_command(accelerator='V',label='Invert',command=lambda: invert(array_num,duration=5))
    
    menubar.add_cascade(label="Menu", menu=configmenu)
    root.config(menu=menubar)
    
    array_gfx = [canv.create_rectangle(i*w,0,(i+1)*w,height,outline=rgb(((int(255-(255*i/width))),0,int(255*i/width)))) for i in range(0,width,w)]
    array_num = [i for i in range(1,501,w)]
    update_scan()
    root.mainloop()