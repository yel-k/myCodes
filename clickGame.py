from tkinter import *
import random   
def update_timer(a=0):
    global remaining_time
    global timer_id
    if remaining_time > 0:
        remaining_time -= 1
        timer_label.config(text=f"Time left: {remaining_time} seconds")
        if a==1:
            stop_timer()
        else:
            timer_id=root.after(1000, update_timer)
    else:
        timer_label.config(text="Time's up!")
        if arrone[0]<level*10:
            canvas.delete(ALL)
            canvas.create_text(canvas.winfo_width()/2,canvas.winfo_height()/2,font=('Ariel',30),
                       text="GAME OVER",fill='red',tag='gameover')
            arrone[0]=level*10
def stop_timer():
    # Cancel the scheduled update_timer() function call
    root.after_cancel(timer_id)
    
def generate_random_color():
    # Generate random values for the red, green, and blue components
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    # Convert the values to hexadecimal format
    color_code = "#{:02X}{:02X}{:02X}".format(r, g, b)
    return color_code

def get_coordinates(event):
    x, y = event.x, event.y
    clicked_object = canvas.find_closest(x,y)
    if arrone[0]==level*10:
        print("ok")
    else:
        x1=arrone[clicked_object[0]][0]
        y1=arrone[clicked_object[0]][1]
        x2=arrone[clicked_object[0]][2]
        y2=arrone[clicked_object[0]][3]
        if x1<=x<=x2 and y1<=y<=y2:
            arrone[0]=arrone[0]+1
            canvas.delete(clicked_object)
            if arrone[0]==level*10:
                canvas.delete(ALL)
                canvas.create_text(canvas.winfo_width()/2,canvas.winfo_height()/2,font=('Ariel',30),
                       text="WINNER",fill='red',tag='win')
                update_timer(1)
    
def button_click(num,root2):
    global level
    if num==1:
        level=1 
    elif num==2:
        level=2
    elif num==3:
        level=3
    root2.destroy()
    rt1()

def rt1():
    global root
    global timer_label
    global canvas
    global timer_id
    root=Tk()
    root.resizable(False,False)
    timer_label = Label(root, text=f"Time left: {remaining_time} seconds", font=('Ariel',12))
    timer_label.pack(side=TOP)
    timer_id = root.after(1000, update_timer)
    canvas=Canvas(root,width=WIDTH,height=HEIGHT,bg='#9C9492')
    canvas.pack()
    root.update()
    root_width=root.winfo_width()
    root_height=root.winfo_height()
    screen_width=root.winfo_screenwidth()
    screen_height=root.winfo_screenheight()
    x=int((screen_width/2)-(root_width/2))
    y=int((screen_height/2)-(root_height/2))
    root.geometry(f"{root_width}x{root_height}+{x}+{y}")
    for i in range(10*level):
        nextx=random.randint(10,50)
        nexty=random.randint(10,50)
        x=random.randint(0,WIDTH)
        if x+nextx >=WIDTH:
            x=WIDTH-nextx
        y=random.randint(0,WIDTH)
        if y+nexty >=HEIGHT:
            y=HEIGHT-nexty
        boo=random.randint(0,1)
        random_color = generate_random_color()
        if boo:
            canvas.create_rectangle(x,y,x+nextx,y+nexty,width=2,fill=random_color)
            arrone.append([x,y,x+nextx,y+nexty])
        else:
            canvas.create_oval(x,y,x+nextx,y+nexty,width=2,fill=random_color)
            arrone.append([x,y,x+nextx,y+nexty])
        canvas.bind("<Button-1>", get_coordinates)
    root.mainloop()

def rt2():
    global level
    root2=Tk()
    root2.resizable(False,False)
    canvas2=Canvas(root2,width=WIDTH,height=HEIGHT,bg='#9C9492')
    canvas2.pack()
    root2.update()
    root2_width=root2.winfo_width()
    root2_height=root2.winfo_height()
    screen_width=root2.winfo_screenwidth()
    screen_height=root2.winfo_screenheight()
    x=int((screen_width/2)-(root2_width/2))
    y=int((screen_height/2)-(root2_height/2))
    root2.geometry(f"{root2_width}x{root2_height}+{x}+{y}")
    canvas_width = canvas2.winfo_reqwidth()
    canvas_height = canvas2.winfo_reqheight()
    rect_width = 100  # Adjust rectangle width
    rect_height = 40  # Adjust rectangle height
    spacing = 40  # Adjust spacing between rectangles

    # Calculate the vertical position for centering
    y_center = (canvas_height - (3 * rect_height + 2 * spacing)) / 2
    for i in range(3):
        # Calculate the positions for the rectangle
        level_num = i + 1 
        x1 = (canvas_width - rect_width) / 2
        y1 = y_center + i * (rect_height + spacing)
        x2 = x1 + rect_width
        y2 = y1 + rect_height
        # Create the rectangle with centered text
        rect = canvas2.create_rectangle(x1, y1, x2, y2, fill="lightblue",outline="black")
        canvas2.create_text((x1 + x2) / 2,(y1 + y2) / 2, text=f"Level{i+1}",font=("Ariel",10))
        canvas2.tag_bind(rect, "<Button-1>", lambda event,num=level_num: button_click(num,root2))   
    root2.mainloop()

root=None
timer_label=None    
canvas=None
WIDTH=600
HEIGHT=600
arrone=[0]
level=0
remaining_time = 16
timer_id=0
rt2()

