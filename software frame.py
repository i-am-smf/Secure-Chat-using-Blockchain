from tkinter import *
import mysql.connector
import datetime

main=Tk()
main.title("Z Chat")
main.geometry("1200x700")
main.iconbitmap("icon.ico")
main.resizable(False,False)

class VerticalScrolledFrame:
    def __init__(self, master, **kwargs):
        width = kwargs.pop('width', None)
        height = kwargs.pop('height', None)
        bg = kwargs.pop('bg', kwargs.pop('background', None))
        self.outer = Frame(master, **kwargs)

        self.vsb = Scrollbar(self.outer, orient=VERTICAL)
        self.vsb.pack(fill=Y, side=RIGHT)
        self.canvas = Canvas(self.outer, highlightthickness=0, width=width, height=height, bg=bg)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        self.canvas['yscrollcommand'] = self.vsb.set

        self.canvas.bind("<Enter>", self._bind_mouse)
        self.canvas.bind("<Leave>", self._unbind_mouse)
        self.vsb['command'] = self.canvas.yview

        self.inner = Frame(self.canvas, bg=bg)
        self.canvas.create_window(4, 4, window=self.inner, anchor='nw',width=970)
        self.inner.bind("<Configure>", self._on_frame_configure)

        self.outer_attr = set(dir(Widget))

    def __getattr__(self, item):
        if item in self.outer_attr:
            return getattr(self.outer, item)
        else:
            return getattr(self.inner, item)

    def _on_frame_configure(self, event=None):
        x1, y1, x2, y2 = self.canvas.bbox("all")
        height = self.canvas.winfo_height()
        self.canvas.config(scrollregion = (0,0, x2, max(y2, height)))

    def _bind_mouse(self, event=None):
        self.canvas.bind_all("<4>", self._on_mousewheel)
        self.canvas.bind_all("<5>", self._on_mousewheel)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mouse(self, event=None):
        self.canvas.unbind_all("<4>")
        self.canvas.unbind_all("<5>")
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        """Linux uses event.num; Windows / Mac uses event.delta"""
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units" )
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units" )

    def __str__(self):
        return str(self.outer)

class ZchatDB:
    def __init__(self) -> None:

        self.connect = mysql.connector.connect(host='maple.db.ashhost.in', user='u926_wGN7NXcLux', passwd='N!.o0GycJTSTA0Jm3VpU.R1F',database="s926_chathistory")
        self.cur = self.connect.cursor()
    
    def insert(self,data_list):
        Game_ID = data_list[0]
        Game_Name = data_list[1]
        Category = data_list[2]
        Price = data_list[3]
        Discounted_Price = data_list[4]
        Rating = data_list[5]
        Friends_List = data_list[6]
        Player_Support = data_list[7]

        insert_query = '''
            INSERT INTO Games 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        '''
        data = (Game_ID, Game_Name, Category, Price, Discounted_Price, Rating, Friends_List, Player_Support)
        try:
            self.cur.execute(insert_query, data)
        except:
            self.__init__()
            self.insert()
        self.connect.commit()  

db=ZchatDB()

info_frame = Frame(main,background="#AFEEEE",width=200,height=700)
info_frame.place(x=1,y=1)

chatframe = VerticalScrolledFrame(main,background="#87CEFA",width=980,height=610)
chatframe.place(x=200,y=1)

def reload():

    try:
        chatframe.destroy()
    except:
        pass
    chatframe = VerticalScrolledFrame(main,background="#87CEFA",width=980,height=610)
    chatframe.place(x=200,y=1)

    update_scrollbar

textbox = Text(main,height=4,width=80,font=("Arial",15))
textbox.place(x=200,y=610)

send_button=Button(main,text="Send",font=("Arial",20),foreground="#000080",background="#AFEEEE",command=reload)
send_button.place(x=1090,y=625)


for i in range(1,110):
    if i%2==0:
        labelframe=LabelFrame(chatframe,text=datetime.datetime.now().__format__("%d-%m-%Y %H:%M:%S"))
        labelframe.pack(padx=10,pady=10,anchor=E)
    else:
        labelframe=LabelFrame(chatframe,text=datetime.datetime.now().__format__("%d-%m-%Y %H:%M:%S"))
        labelframe.pack(padx=10,pady=10,anchor=W)

    Label(labelframe,text=i,font=("Arial",12)).pack(anchor=E)

def update_scrollbar():
    chatframe.canvas.yview_moveto(1.0)

main.after(10,update_scrollbar)
main.mainloop()