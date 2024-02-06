from tkinter import *
import datetime

main=Tk()
main.title("Z Chat")
main.geometry("1200x800")
main.iconbitmap("icon.ico")
main.resizable(False,False)

info_frame = Frame(main,background="#AFEEEE",width=200)
info_frame.pack(side=LEFT, fill=BOTH)

chatframe= Frame(main,background="#87CEFA")
chatframe.pack(side=RIGHT, fill=BOTH, expand=True)

for i in range(1,11):
    if i%2==0:
        labelframe=LabelFrame(chatframe,text=datetime.datetime.now().__format__("%d-%m-%Y %H:%M:%S"))
        labelframe.pack(padx=10,pady=10,anchor=E)
    else:
        labelframe=LabelFrame(chatframe,text=datetime.datetime.now().__format__("%d-%m-%Y %H:%M:%S"))
        labelframe.pack(padx=10,pady=10,anchor=W)

    Label(labelframe,text=i).pack(anchor=E)

main.mainloop()