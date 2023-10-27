from tkinter import *
import random

GAME_HEIGHT=600
GAME_WIDTH=600
SIZE=30
count=10
got=0
fastest=5
slowest=100
numOfKid=30
class Kids:
    def __init__(self):
        self.speed=random.randint(fastest,slowest)
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
    if kid.bodypart!=[]:
        if boo:
            global count
            dis=5
            if count<0:
                kid.dirvalue=random.randint(0,7)
                count=10
            count-=1
            if kid.dirvalue==0 and kid.coordinate[0]+dis+SIZE<GAME_HEIGHT and kid.coordinate[1]+dis+SIZE<GAME_WIDTH:
                kid.coordinate=[kid.coordinate[0]+dis,kid.coordinate[1]+dis]
                canvas.coords(kid.bodypart[0],kid.coordinate[0],kid.coordinate[1],kid.coordinate[0]+SIZE,kid.coordinate[1]+SIZE)
                kid.move_timeout = root.after(kid.speed,auto_move,kid)
            elif kid.dirvalue==1 and kid.coordinate[0]+SIZE<GAME_HEIGHT :
                kid.coordinate=[kid.coordinate[0]+dis,kid.coordinate[1]]
                canvas.coords(kid.bodypart[0],kid.coordinate[0],kid.coordinate[1],kid.coordinate[0]+SIZE,kid.coordinate[1]+SIZE)
                kid.move_timeout = root.after(kid.speed,auto_move,kid)
            elif kid.dirvalue==2 and kid.coordinate[0]+dis+SIZE<GAME_HEIGHT and kid.coordinate[1]-dis>0:
                kid.coordinate=[kid.coordinate[0]+dis,kid.coordinate[1]-dis]
                canvas.coords(kid.bodypart[0],kid.coordinate[0],kid.coordinate[1],kid.coordinate[0]+SIZE,kid.coordinate[1]+SIZE)
                kid.move_timeout = root.after(kid.speed,auto_move,kid)
            elif kid.dirvalue==3 and kid.coordinate[1]-dis>0:
                kid.coordinate=[kid.coordinate[0],kid.coordinate[1]-dis]
                canvas.coords(kid.bodypart[0],kid.coordinate[0],kid.coordinate[1],kid.coordinate[0]+SIZE,kid.coordinate[1]+SIZE)
                kid.move_timeout = root.after(kid.speed,auto_move,kid)
            elif kid.dirvalue==4 and kid.coordinate[0]-1>0 and kid.coordinate[1]-dis>0:
                kid.coordinate=[kid.coordinate[0]-1,kid.coordinate[1]-dis]
                canvas.coords(kid.bodypart[0],kid.coordinate[0],kid.coordinate[1],kid.coordinate[0]+SIZE,kid.coordinate[1]+SIZE)
                kid.move_timeout = root.after(kid.speed,auto_move,kid)
            elif kid.dirvalue==5 and kid.coordinate[0]-dis>0:
                kid.coordinate=[kid.coordinate[0]-dis,kid.coordinate[1]]
                canvas.coords(kid.bodypart[0],kid.coordinate[0],kid.coordinate[1],kid.coordinate[0]+SIZE,kid.coordinate[1]+SIZE)
                kid.move_timeout = root.after(kid.speed,auto_move,kid)
            elif kid.dirvalue==6 and kid.coordinate[0]-dis>0 and kid.coordinate[1]+dis+SIZE<GAME_WIDTH:
                kid.coordinate=[kid.coordinate[0]-dis,kid.coordinate[1]+dis]
                canvas.coords(kid.bodypart[0],kid.coordinate[0],kid.coordinate[1],kid.coordinate[0]+SIZE,kid.coordinate[1]+SIZE)
                kid.move_timeout = root.after(kid.speed,auto_move,kid)
            elif kid.dirvalue==7 and kid.coordinate[1]+dis+SIZE<GAME_WIDTH:
                kid.coordinate=[kid.coordinate[0],kid.coordinate[1]+dis]
                canvas.coords(kid.bodypart[0],kid.coordinate[0],kid.coordinate[1],kid.coordinate[0]+SIZE,kid.coordinate[1]+SIZE)
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
            
def catched(kid, x, y):
    global got
    if kid.bodypart!=[]:
        got+=1
        label.config(text=f"You got {got}")
        canvas.delete(kid.bodypart[0])
        del kid.bodypart[0]
    
def get_coordinates(event):
    x, y = event.x, event.y
    for kid in kids:
        if abs(x - kid.coordinate[0]) < SIZE and abs(y - kid.coordinate[1]) < SIZE:
            catched(kid,x,y)

def button_click(num):
    global fastest
    global slowest
    if num==1:
        lbone.config(text="Level set to Easy")
        fastest=40
        slowest=70
    elif num==2:
        lbone.config(text="Level set to Medium")
        fastest=20
        slowest=50
    elif num==3:
        lbone.config(text="Level set to Hard")
        fastest=5
        slowest=30
    elif num==4:
        lbone.config(text="Welcome to HELL:3")
        fastest=1
        slowest=5
def kid_count():
    global numOfKid
    temp=entry.get()
    numOfKid=int(temp)
    lbtwo.config(text=f"Number of kids set to {numOfKid}")

def create_second_window():
    # Create a new Toplevel window
    root2.destroy()
    
root2=Tk()
root2.resizable(False,False)
root2.geometry('600x600')
lbone=Label(root2,text="Level not set",font=('Ariel',15))
lbone.pack(padx=10,pady=10)
lbtwo=Label(root2,text="Number of kids not set",font=('Ariel',15))
lbtwo.pack(padx=10,pady=10)
btnone=Button(root2,text="Easy",font=('Ariel',12),bg='#f2ab4b',command=lambda: button_click(1))
btnone.pack(padx=10,pady=10)
btntwo=Button(root2,text="Medium",font=('Ariel',12),bg='#f2ab4b',command=lambda: button_click(2))
btntwo.pack(padx=10,pady=10)
btnthree=Button(root2,text="Hard",font=('Ariel',12),bg='#f2ab4b',command=lambda: button_click(3))
btnthree.pack(padx=10,pady=10)
btnfour=Button(root2,text="No! Don't think about it!",font=('Ariel',12),bg='#f70505',command=lambda: button_click(4))
btnfour.pack(padx=10,pady=10)
lbthree=Label(root2,text="Enter number of children",font=('Ariel',13))
lbthree.pack(padx=10,pady=10)
entry=Entry(width=10,font=('Ariel',13))
entry.pack(padx=10,pady=10)
entry.bind('<Return>', lambda event=None: kid_count())
button = Button(root2, text="Start Catching",bg='#337ab7',font=('Ariel',12), command=create_second_window)
button.pack(padx=10,pady=10)
 
root2.mainloop()

root=Tk()
root.title("Catch The Kids")
root.resizable(False,False)
label=Label(root,text="You got nothing",font=('Ariel',20),bg='#9C9492')
label.pack(expand=True,fill='both' )
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

for i in range(numOfKid):
    kid=Kids()
    kids.append(kid)
for kid in kids:
    auto_move(kid,boo=True)
canvas.bind("<Button-1>", get_coordinates)

root.mainloop()
