from tkinter import *
import random

def update_timer():
    global time
    try:
        t=int(entrytime.get())
        time=t*60
        labeltime.config(text=f"Time set to {time} seconds")
    except:
        labeltime.config(text="Invalid input. Please enter an integer.")

def count_time():
    global time
    
    if time>0:
        time-=1
        showtime.config(text=f"Remaining time: {time} seconds")
        root.after(1000,count_time)
    else:
        showtime.config(text="Time up")
        labelone.destroy()
        labeltwo.destroy()
        entrytwo.destroy()
        labelrw.destroy()
        labelscore.config(text=f"Your Total Score: {count}")

def create_text(letter_set):
    if letter_set == 0:
        letter = entryone.get()
        for i in letter:
            if i not in arrone and i!=" ":
                arrone.append(i)
    elif letter_set == 1:
        letter = "abcdefghijklmnopqrstuvwxyz"
    elif letter_set == 2:
        letter = "abcdefghijklmnopqrstuvwxyz0123456789"
    elif letter_set == 3:
        letter = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    for i in letter:
        if i not in arrone  and i!=" ":
            arrone.append(i)
    le=""
    for x in arrone:
        le+=x
    labeltwo.config(text=le)

def check_input():
        global word
        global count
        typer = entrytwo.get()
        if typer == word:
            labelrw.config(text="Right")
            count+=1
            entrytwo.delete(0, END)
            labelscore.config(text=f"Score: {count}")
            start_typing()
        else:
            labelrw.config(text='Wrong')
            entrytwo.delete(0, END)
            
            
def start_typing():
    if len(arrone)>0:
        global word
        global count
        if(count<1):
            labelone.pack_forget()
            labeltwo.pack_forget()
        showtime.pack(padx=10,pady=10)
        showtime.config(text=f"Remaining time: {time} seconds")
        labelone.pack(padx=10,pady=10)
        labeltwo.pack(padx=10,pady=10)
        labelone.config(text="Start Your Trainning")
        labeltwo.config(text="")
        btntwo.destroy()
        btnthree.destroy()
        btnfour.destroy()
        btn.destroy()
        entryone.destroy()
        labeltime.destroy()
        entrytime.destroy()

        word=""
        ranlen=random.randint(2,9)
        for i in range(ranlen):
            word+=arrone[random.randint(0,len(arrone)-1)]
        labeltwo.config(text=word)
        entrytwo.pack(padx=10,pady=10)
        entrytwo.bind('<Return>', lambda event:check_input())
        labelrw.pack(padx=10,pady=10)
        labelscore.pack(padx=10,pady=10)
        if(count<1):
            count_time()
    else:
        labelone.config(text="YOU CHOOSE NOTHING!!!")
    
root=Tk()
root.geometry('600x600')
arrone=[]
count=0
time=3600
showtime=Label(root,text="hi",font=('Ariel',14))
showtime.pack(padx=10,pady=10)
showtime.pack_forget()
labelone=Label(root,text="Enter the lettes or just choose sets or both:3",font=('Ariel',20))
labelone.pack(padx=10,pady=10)
labeltwo=Label(root,text="",font=('Ariel',20))
labeltwo.pack(padx=10,pady=10)
entryone=Entry(root,width=25,font=('Ariel',12))
entryone.pack(padx=10,pady=10)
entryone.bind('<Return>', lambda event=None: create_text(0))
btntwo=Button(root,text="Set 1: a to z",font=('Ariel',12),command=lambda:create_text(1))
btntwo.pack(padx=10,pady=10,ipadx=10,ipady=10)
btnthree=Button(root,text="Set 1: a to z and 0 to 9",font=('Ariel',12),command=lambda:create_text(2))
btnthree.pack(padx=10,pady=10,ipadx=10,ipady=10)
btnfour=Button(root,text="Set 1: a to z and A to Z and 0 to 9",font=('Ariel',12),command=lambda:create_text(3))
btnfour.pack(padx=10,pady=10,ipadx=10,ipady=10)
labeltime=Label(root,text="Set your time or not?(minute only)",font=('Ariel',14))
labeltime.pack(padx=10,pady=10)
entrytime=Entry(root,width=10,font=('Ariel',12))
entrytime.pack(padx=10,pady=10)
entrytime.bind('<Return>', lambda event: update_timer())
btn=Button(root,text="START TYPING",font=('Ariel',12),bg='#A18E83',command=start_typing)
btn.pack(ipadx=10,ipady=10)
entrytwo=Entry(root,width=25,font=('Ariel',20))
entrytwo.pack(padx=10,pady=10)
entrytwo.pack_forget()
labelrw=Label(root,text="",font=('Ariel',20))
labelrw.pack(padx=10,pady=10)
labelrw.pack_forget()
labelscore=Label(root,text=f"Score: {count}",font=('Ariel',22))
labelscore.pack(padx=10,pady=10)
labelscore.pack_forget()

root.mainloop()
