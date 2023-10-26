from tkinter import *
import random

GAME_HEIGHT=600
GAME_WIDTH=600
SIZE=30
count=10

class Kids:
    def __init__(self):
        self.speed=random.randint(25,100)
        self.dirvalue=0
        self.color=generate_random_color()
        self.coordinate=[0,0]
        self.bodypart=[]
        body=canvas.create_oval(0,0,SIZE,SIZE,fill=self.color,tag='kid')
        self.bodypart.append(body)
        self.move_timeout = None
def generate_random_color():
    # Generate random values for the red, green, and blue components
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    # Convert the values to hexadecimal format
    color_code = "#{:02X}{:02X}{:02X}".format(r, g, b)
    return color_code

def auto_move(kid,boo=True):
    
    if boo:
        global count
        dis=5
        if count<0:
            kid.dirvalue=random.randint(0,7)
            count=10
        count-=1
        if kid.dirvalue==0 and kid.coordinate[0]+dis+SIZE<GAME_HEIGHT and kid.coordinate[1]+dis+SIZE<GAME_WIDTH:
            kid.coordinate=[kid.coordinate[0]+dis,kid.coordinate[1]+dis]
            body=canvas.create_oval(kid.coordinate[0],kid.coordinate[1],kid.coordinate[0]+SIZE,kid.coordinate[1]+SIZE,fill=kid.color)
            kid.bodypart.append(body)
            if len(kid.bodypart)>1: 
                canvas.delete(kid.bodypart[0])
                del kid.bodypart[0]
            kid.move_timeout = root.after(kid.speed,auto_move,kid)
        elif kid.dirvalue==1 and kid.coordinate[0]+SIZE<GAME_HEIGHT :
            kid.coordinate=[kid.coordinate[0]+dis,kid.coordinate[1]]
            body=canvas.create_oval(kid.coordinate[0],kid.coordinate[1],kid.coordinate[0]+SIZE,kid.coordinate[1]+SIZE,fill=kid.color)
            kid.bodypart.append(body)
            if len(kid.bodypart)>1: 
                canvas.delete(kid.bodypart[0])
                del kid.bodypart[0]
            kid.move_timeout = root.after(kid.speed,auto_move,kid)
        elif kid.dirvalue==2 and kid.coordinate[0]+dis+SIZE<GAME_HEIGHT and kid.coordinate[1]-dis>0:
            kid.coordinate=[kid.coordinate[0]+dis,kid.coordinate[1]-dis]
            body=canvas.create_oval(kid.coordinate[0],kid.coordinate[1],kid.coordinate[0]+SIZE,kid.coordinate[1]+SIZE,fill=kid.color)
            kid.bodypart.append(body)
            if len(kid.bodypart)>1: 
                canvas.delete(kid.bodypart[0])
                del kid.bodypart[0]
            kid.move_timeout = root.after(kid.speed,auto_move,kid)
        elif kid.dirvalue==3 and kid.coordinate[1]-dis>0:
            kid.coordinate=[kid.coordinate[0],kid.coordinate[1]-dis]
            body=canvas.create_oval(kid.coordinate[0],kid.coordinate[1],kid.coordinate[0]+SIZE,kid.coordinate[1]+SIZE,fill=kid.color)
            kid.bodypart.append(body)
            if len(kid.bodypart)>1: 
                canvas.delete(kid.bodypart[0])
                del kid.bodypart[0]
            kid.move_timeout = root.after(kid.speed,auto_move,kid)
        elif kid.dirvalue==4 and kid.coordinate[0]-1>0 and kid.coordinate[1]-dis>0:
            kid.coordinate=[kid.coordinate[0]-1,kid.coordinate[1]-dis]
            body=canvas.create_oval(kid.coordinate[0],kid.coordinate[1],kid.coordinate[0]+SIZE,kid.coordinate[1]+SIZE,fill=kid.color)
            kid.bodypart.append(body)
            if len(kid.bodypart)>1: 
                canvas.delete(kid.bodypart[0])
                del kid.bodypart[0]
            kid.move_timeout = root.after(kid.speed,auto_move,kid)
        elif kid.dirvalue==5 and kid.coordinate[0]-dis>0:
            kid.coordinate=[kid.coordinate[0]-dis,kid.coordinate[1]]
            body=canvas.create_oval(kid.coordinate[0],kid.coordinate[1],kid.coordinate[0]+SIZE,kid.coordinate[1]+SIZE,fill=kid.color)
            kid.bodypart.append(body)
            if len(kid.bodypart)>1: 
                canvas.delete(kid.bodypart[0])
                del kid.bodypart[0]
            kid.move_timeout = root.after(kid.speed,auto_move,kid)
        elif kid.dirvalue==6 and kid.coordinate[0]-dis>0 and kid.coordinate[1]+dis+SIZE<GAME_WIDTH:
            kid.coordinate=[kid.coordinate[0]-dis,kid.coordinate[1]+dis]
            body=canvas.create_oval(kid.coordinate[0],kid.coordinate[1],kid.coordinate[0]+SIZE,kid.coordinate[1]+SIZE,fill=kid.color)
            kid.bodypart.append(body)
            if len(kid.bodypart)>1: 
                canvas.delete(kid.bodypart[0])
                del kid.bodypart[0]
            kid.move_timeout = root.after(kid.speed,auto_move,kid)
        elif kid.dirvalue==7 and kid.coordinate[1]+dis+SIZE<GAME_WIDTH:
            kid.coordinate=[kid.coordinate[0],kid.coordinate[1]+dis]
            body=canvas.create_oval(kid.coordinate[0],kid.coordinate[1],kid.coordinate[0]+SIZE,kid.coordinate[1]+SIZE,fill=kid.color)
            kid.bodypart.append(body)
            if len(kid.bodypart)>1: 
                canvas.delete(kid.bodypart[0])
                del kid.bodypart[0]
            kid.move_timeout = root.after(kid.speed,auto_move,kid)
        else:
            kid.move_timeout = root.after(kid.speed,auto_move,kid)

    else:
        pass
def stop_kids():
    for kid in kids:
        if kid.move_timeout:
            root.after_cancel(kid.move_timeout)
            kid.move_timeout = None
            
def they_comming(kid, x, y):
    disx = x - kid.coordinate[0]
    disy = y - kid.coordinate[1]
    
    if abs(disx) > 1 or abs(disy) > 1:
        # Calculate the movement increments for x and y
        stepx = min(5, abs(disx)) if disx != 0 else 0
        stepy = min(5, abs(disy)) if disy != 0 else 0
        
        if disx > 0:
            kid.coordinate[0] += stepx
        elif disx < 0:
            kid.coordinate[0] -= stepx
        
        if disy > 0:
            kid.coordinate[1] += stepy
        elif disy < 0:
            kid.coordinate[1] -= stepy
        
        # Update the position on the canvas
        canvas.coords(kid.bodypart[0], kid.coordinate[0], kid.coordinate[1], kid.coordinate[0] + SIZE, kid.coordinate[1] + SIZE)
        
        # Schedule the next movement
        kid.move_timeout = root.after(kid.speed, they_comming, kid, x, y)
    
def get_coordinates(event):
    x, y = event.x, event.y
    isIn=[False]*len(kids)
    for idx,kid in enumerate(kids):
        if abs(x - kid.coordinate[0]) < SIZE and abs(y - kid.coordinate[1]) < SIZE:
            isIn[idx]=True
    if all(isIn):
        for kid in kids:
            auto_move(kid,boo=True)
    else:
        stop_kids()
        for kid in kids:
            they_comming(kid,x,y)
    
root=Tk()
root.title("Call The Kids")
root.resizable(False,False)
canvas=Canvas(root,width=GAME_WIDTH,height=GAME_HEIGHT,bg='#9C9492')
canvas.pack()
root.update()
root_width=root.winfo_width()
root_height=root.winfo_height()
screen_width=root.winfo_screenwidth()
screen_height=root.winfo_screenheight()
x=int((screen_width/2)-(root_width/2))
y=int((screen_height/2)-(root_height/2))
root.geometry(f"{root_width}x{root_height}+{x}+{y}")
kids=[]

for i in range(30):
    kid=Kids()
    kids.append(kid)
for kid in kids:
    auto_move(kid,boo=True)
canvas.bind("<Button-1>", get_coordinates)

root.mainloop()
