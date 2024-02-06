from tkinter import *

main=Tk()

info_frame=Frame(main,background="#7AC5CD",border=5,width=100)
info_frame.pack(side="left",fill=Y)

for i in range(1,10):
    label1=Label(info_frame,text="Text 1").pack()

for i in range(1,10):
    label1=Label(main,text="Text 1").pack()

main.mainloop()