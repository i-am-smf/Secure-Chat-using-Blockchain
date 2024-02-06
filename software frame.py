from tkinter import *
import datetime

main=Tk()
main.geometry("1200x800")
main.resizable(False,False)

info_frame = Frame(main,background="#AFEEEE",width=200)
info_frame.pack(side=LEFT, fill=BOTH)

chatframe= Frame(main,background="#87CEFA")
chatframe.pack(side=RIGHT, fill=BOTH, expand=True)

for i in range(1,11):
    if i%2==0:
        labelframe=LabelFrame(chatframe,text=i)
        labelframe.pack(padx=10,pady=10,anchor=E)
    else:
        labelframe=LabelFrame(chatframe,text=i)
        labelframe.pack(padx=10,pady=10,anchor=W)

    Label(labelframe,text=datetime.datetime.now()).pack(anchor=E)

main.mainloop()