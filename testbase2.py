import datetime
from tkinter import *

main=Tk()
main.title("Timestamp")
main.geometry("400x400")

def update():
    datetimelabel.config(text=f"{datetime.datetime.now()}")
    timestamplabel.config(text=f"{datetime.datetime.now().timestamp()}")
    main.after(100,update)

datetimelabel=Label(main,text=f"{datetime.datetime.now()}",font=(("Arial",20)))
datetimelabel.place(x=50,y=100)

timestamplabel=Label(main,text=f"{datetime.datetime.now().timestamp()}",font=(("Arial",20)))
timestamplabel.place(x=50,y=150)

main.after(100,update)

main.mainloop()