from tkinter import Tk,PhotoImage,Label,Button,Canvas,Frame,W,Toplevel,messagebox,Entry
from PIL import Image,ImageTk
from winotify import Notification, audio
from playsound import playsound
from scripts.config import Config
from scripts.pixela import Pixela 
from datetime import datetime as dt
# ------------- Constants ------------- #

RED_COLOR = "#F38181"
YELLOW_COLOR = "#FCE38A"
GREEN_COLOR = "#95E1D3"
BG_COLOR = "#EAFFD0"
PURPLE_COLOR = "#6B72C4"
FONT = ("Calibri",40,"bold")
BREAK_TOAST = Notification(
    app_id="E Clock",
    title="Break!",
    msg="Time for a break. But no KitKats.",
    duration="short",
    icon=r"D:\E-Clock-Timer\assets\icon.ico"
)
BREAK_TOAST.set_audio(audio.LoopingAlarm10,loop=False)
WORK_TOAST = Notification(
    app_id="E Clock",
    title="Work!!",
    msg="Time to get back to work.",
    duration="short",
    icon=r"D:\E-Clock-Timer\assets\icon.ico"
)
WORK_TOAST.set_audio(audio.LoopingAlarm10,loop=False)
COMPLETE_TOAST = Notification(
    app_id="E Clock",
    title="Complete!!!",
    msg="Hooray! Your hard work will payoff soon.",
    duration="short",
    icon=r"D:\Timer\EPomo-Timer\Assets\icon.png"
)
COMPLETE_TOAST.set_audio(audio.LoopingAlarm10,loop=False)
# ------------- Toast ------------- #
## change name to notification create a notification class
def break_toast()->None:
    BREAK_TOAST.show()

    playsound('assets/sounds/break.mp3')
    return
def work_toast()->None:
    WORK_TOAST.show()
    playsound("assets/sounds/work.mp3")
    return
def complete_toast()->None:
    COMPLETE_TOAST.show()
    playsound('assets/sounds/complete.mp3')
    return
TOAST = {
    "B" : break_toast,
    "W" : work_toast,
    "C" : complete_toast
}
config = Config()

# ------------- UI ------------- #
class UI():
    def __init__(self) -> None:
        
        self.work_session_count = 0
        self.mode = "idle" # work, idle, break
        self.status = "stop" # running
        self.session_time = {"W":30, #mins
                             "B":5} #mins
        self.session = ["W","B","W","B","W","B","W","B","W","B"]
        self.session_index = 0
        self.current_time = 0
        self.speed = 1000 # in ms
        self.work_done_sec = 0
        pass
    def create_window(self):
        self.window = Tk()
        self.window.title("Home | EClock")
        self.window.minsize(450,500)
        self.window.config(bg=BG_COLOR,
                           padx=25,
                           pady=25)
        self.window.minsize(1280,720)
        self.window.iconbitmap("assets\image\icon.ico")
        return self.create_window
    def clear(self):
        for child in self.window.winfo_children():
            child.destroy()
        return

class Home_UI(UI):
    def __init__(self,window) -> None:
        super().__init__()
        self.window = window
        self.window.title("Pixela Graph | E Clock")
        # remove all and create
        self.clear()    
        self.create_ui()


    
    def create_ui(self) -> None:

        if True: # icons
            icon = Image.open("assets\image\icon.png").resize((100,40))
            self.icon = ImageTk.PhotoImage(icon)
            self.red_dial = Image.open("assets/image/red-dial.png").resize((400,400))
            self.red_dial = ImageTk.PhotoImage(self.red_dial)
            self.green_dial = Image.open("assets\image\green-dial.png").resize((400,400))
            self.green_dial = ImageTk.PhotoImage(self.green_dial)
            self.blue_dial = Image.open("assets/image/blue-dial.png").resize((400,400))
            self.blue_dial = ImageTk.PhotoImage(self.blue_dial)
            self.reset_img = Image.open("assets/image/reset.png").resize((35,35))
            self.reset_img = ImageTk.PhotoImage(self.reset_img)
            self.play_img = Image.open("assets\image\play.png").resize((35,35))
            self.play_img = ImageTk.PhotoImage(self.play_img)
            self.pause_img = Image.open("assets\image\pause.png").resize((35,35))
            self.pause_img = ImageTk.PhotoImage(self.pause_img)
            self.complete_img = Image.open("assets\image\complete.png").resize((35,35))
            self.complete_img = ImageTk.PhotoImage(self.complete_img)
            self.done = Image.open("assets\image\done.png").resize((50,50))
            self.done = ImageTk.PhotoImage(self.done)
            self.minute_hand_img = Image.open("assets\image\minute-hand.png").resize((100,100))
            self.minute_hand_img = ImageTk.PhotoImage(self.minute_hand_img)
            self.second_hand_img = Image.open("assets\image\second-hand.png").resize((160,160))
            self.second_hand_img = ImageTk.PhotoImage(self.second_hand_img)
            self.dot = Image.open("assets\image\dot.png").resize((30,30))
            self.dot = ImageTk.PhotoImage(self.dot)


        logo_img = Label(image=self.icon,
                         bg=BG_COLOR,anchor=W)
        logo_img.grid(row=1,column=1)

        show_pixela_btn = Button(text="📊",
                              font=FONT,
                              borderwidth=0,
                              bg=BG_COLOR,
                              activebackground=BG_COLOR,
                              command=lambda : Pixela_UI(self.window),
                              fg=RED_COLOR,
                              activeforeground=RED_COLOR)
        show_pixela_btn.grid(row=1,column=2)

        settings_btn = Button(text="⚙",
                              font=FONT,
                              borderwidth=0,
                              bg=BG_COLOR,
                              activebackground=BG_COLOR,
                              command=self.setting)
        settings_btn.grid(row=1,column=3)

        self.title_text = Label(text="Timer",font = FONT,
                           bg=BG_COLOR,
                           fg=RED_COLOR)
        self.title_text.grid(row=2,column=1,columnspan=3)

        self.clock = Canvas(height=400,width=400,
                       bg=BG_COLOR,
                       highlightthickness=0)
        self.clock_face = self.clock.create_image(200,200,
                                  image = self.blue_dial)        
        self.clock_second = self.clock.create_image(200,200,
                                          image = self.second_hand_img)
        self.clock_minute = self.clock.create_image(200,200,
                                          image = self.minute_hand_img)
        self.clock.create_image(200,200,
                                          image = self.dot)
        self.clock.grid(row=3,column=1,columnspan=3,pady=(0,20)) 

        self.play_pause_btn = Button(image=self.play_img,
                            bg=BG_COLOR,
                            activebackground=BG_COLOR,
                            borderwidth=0,
                            command=self.play_pause)
        self.play_pause_btn.grid(row=4,column=1)
        
        self.complete_btn = Button(image=self.complete_img,
                            bg=BG_COLOR,
                            activebackground=BG_COLOR,
                            borderwidth=0,
                            command=self.complete)
        self.complete_btn.grid(row=4,column=2)

        reset = Button(image=self.reset_img,
                            bg=BG_COLOR,
                            activebackground=BG_COLOR,
                            borderwidth=0,
                            command=self.call_reset_timer)
        reset.grid(row=4,column=3)

        self.done_frame = Frame(self.window,width=400,
                        bg=BG_COLOR)
        self.done_frame.grid(row=5,column=1,columnspan=3,pady=(10,0))

        return 

    def update_ui(self) -> None:


        if self.mode == "idle":
            replace_text = "Timer"
            replace_clock_face = self.blue_dial
            
        elif self.mode == "work":
            replace_text = "Work"
            replace_clock_face = self.green_dial

        elif self.mode == "break":
            replace_text = "Break"
            replace_clock_face = self.red_dial

        self.title_text.configure(text=replace_text)
        self.clock.itemconfig(self.clock_face,image = replace_clock_face)
       
        # create done images
        for child in  self.done_frame.winfo_children():
            child.destroy()
        for _ in range(self.work_session_count):
            done_img = Label(self.done_frame,image=self.done,bg=BG_COLOR)
            done_img.pack(side="left",padx=5)


        if self.status == "stop" and self.mode == "idle":
            self.play_pause_btn.configure(image=self.play_img)

        elif self.status == "pause" and self.mode != "idle":
            self.title_text.configure(text="Paused")
            self.play_pause_btn.configure(image=self.play_img)

        elif self.status == "play" and self.mode != "idle":
            self.title_text.configure(text=replace_text)
            self.play_pause_btn.configure(image=self.pause_img)
        
        return

    def setting(self):
        Setting(self.window)
        return

    def play_pause(self) -> None:
        if self.status == "stop":
            self.status = "play"
            self.mode_change()

            # get min for timer and convert in second
            self.current_time = self.session_time[self.session[self.session_index] ] * 60
            self.start_timer()
        elif self.status == "play":
            # Do pause stuff
            self.status = "pause"
            self.pause_timer()
            print("Paused")
            self.update_ui()
        elif self.status == "pause":
            # Do play stuff
            self.status = "play"
            self.start_timer()
            self.update_ui()
        return

    def complete(self):
        if self.work_done_sec < 60:
            messagebox.showwarning("Warning!","Couldn't post the data.\nDo some work.")
            return
        worked_mins = self.work_done_sec//60
        token = config.read_value('pixela_token')
        user = config.read_value('pixela_user')
        graph_id = config.read_value('pixela_graph')[0]['graph_id']
        date = dt.now()
        date=date.strftime("%Y%m%d")
        Pixela().plot_pixel(token,user,graph_id,date,worked_mins)
        self.call_reset_timer()
        return

    def call_reset_timer(self) -> None:
        self.work_session_count = 0
        self.mode = "idle"
        self.status = "stop"
        self.session_index = 0
        self.current_time = 0
        self.work_session_count = 0
        self.work_done_sec = 0
        self.update_ui()
        self.move_minute_hand(0,0,True)
        self.move_second_hand(0,0,True)
        # create done images
        for child in  self.done_frame.winfo_children():
            child.destroy()
        try:
            self.pause_timer()
        except:
            pass

    def move_second_hand(self,degree,time,reset=False) -> None:
        if reset == True:
            self.second_hand_img = Image.open("assets\image\second-hand.png").resize((160,160))
            self.second_hand_img = ImageTk.PhotoImage(self.second_hand_img)
            self.clock.itemconfig(self.clock_second,image = self.second_hand_img)
            return
        
        to_rotate = degree * time
        
        self.second_hand_img = Image.open("assets\image\second-hand.png").resize((160,160)).rotate(-to_rotate)
        self.second_hand_img = ImageTk.PhotoImage(self.second_hand_img)

        self.clock.itemconfig(self.clock_second,image = self.second_hand_img)
        return

    def move_minute_hand(self,degree,time,reset=False) -> None:
        if reset == True:
            self.minute_hand_img = Image.open("assets\image\minute-hand.png").resize((100,100))
            self.minute_hand_img = ImageTk.PhotoImage(self.minute_hand_img)
            self.clock.itemconfig(self.clock_minute,image = self.minute_hand_img)
            
            return
        
        time = time//60 # in mins
        to_rotate = degree * time
        
        self.minute_hand_img = Image.open("assets\image\minute-hand.png").resize((100,100)).rotate(-to_rotate)
        self.minute_hand_img = ImageTk.PhotoImage(self.minute_hand_img)

        self.clock.itemconfig(self.clock_minute,image = self.minute_hand_img)
        return

    # ------------- Modes ------------- #
    def mode_change(self) -> None:
        if self.mode == "idle":
            # change to work
            self.mode = "work"

        elif self.mode == "work":
            # change to break
            self.mode = "break"

        elif self.mode == "break":
            # change to work or idle        
            self.mode = "work"
        
        self.update_ui()
        return

    def mode_complete(self) -> None:

        self.session_index += 1
        try:
            if self.session[self.session_index] == "W":
                self.mode = "work"
            elif self.session[self.session_index] == "B":
                self.work_session_count += 1
                self.mode = "break"
            
            self.current_time = self.session_time[self.session[self.session_index]] * 60
        except IndexError:
            TOAST["C"]()
            self.complete()
            self.call_reset_timer()
            return
        else:
            self.update_ui()
            TOAST[self.session[self.session_index]]()

            self.window.after(3000,self.start_timer)
        return

    # ------------- Timer ------------- #
    def start_timer(self) -> None:
        self.timer_id = self.window.after(1,self.countdown,self.current_time)
        return
    def pause_timer(self) -> None:
        self.window.after_cancel(self.timer_id)
        return

    def countdown(self,count) -> None:
        print(count)
        # get mode
        if self.mode == "work":
            self.work_done_sec += 1
        if count < 0:
            self.mode_complete()
            return
        session_type = self.session[self.session_index]
        full_time = self.session_time[session_type] # in mins
        minute_rotation = 360/full_time # degree
        second_rotation =  360/60 # degree
        self.current_time = self.current_time-1
        self.move_second_hand(second_rotation,full_time*60 - count)
        self.move_minute_hand(minute_rotation,full_time*60 - count)
        self.timer_id=self.window.after(self.speed,self.countdown,self.current_time)
        return

class Setting(UI):
    def __init__(self,window) -> None:
        super().__init__()
        self.window = window
        self.window.title("Pixela Graph | E Clock")
        # remove all and create
        self.clear()    
        self.create_ui()

    def create_ui(self):

        self.name_input = Entry(width=15)
        name_lb = Label( text="Enter Pixela Graph Name")
        reset_btn = Button(text="❌",
                           font=FONT,
                            borderwidth=0,
                            bg=BG_COLOR,
                            activebackground=BG_COLOR,
                            command=self.call_config_reset)
        create_btn = Button(text="Create",
                           font=FONT,
                            borderwidth=0,
                            bg=BG_COLOR,
                            activebackground=BG_COLOR,
                            command=self.call_create_pixela)
        back_btn = Button(text="back",command=self.back)
        back_btn.pack()
        name_lb.pack(side="top")
        self.name_input.pack(side="left")
        create_btn.pack(side="left")
        reset_btn.pack(side="right")
        return

    def back(self):
        Home_UI(self.window)
        return

    def call_config_reset(self):
        _is_ask = messagebox.askyesno("Confirmation", "You are about to reset the config file. It contains your Pixela Graph Credentials. If you continue you will lose all the Pixela graph data.\nDo you want to continue with the reset?") 
        if _is_ask is True:
            Config().reset()
        return

    def call_create_pixela(self):
        # check if already created
        if Config().read_value('pixela_token') != None:
            messagebox.showwarning("Failed!","User already created.")
            return False
        name = self.name_input.get()
        if name == " " or name == "":
            messagebox.showerror("Error!","Enter name for the graph.")
            return False
        if (Pixela().create(name)) == True:
            messagebox.showinfo("Success!",f"You've created a graph with the name: {name}.")
            return True
        messagebox.showerror("Error!","Some other error. Line 464")
        return False

class Pixela_UI(UI):
    def __init__(self,window) -> None:
        super().__init__()
        if config.read_value("pixela_user") == None:
            messagebox.showwarning("Warning","User not found.\nCreate a new user in settings.")
            return
        self.window = window
        self.window.title("Pixela Graph | E Clock")
        self.window.minsize(1280,720)
        self.font_heading = ("Calibri",30,"bold")
        self.font_content = ("Calibri",20,"bold")

        # remove all and create
        self.clear()    
        self.create_ui()

    def get_data(self) -> None:
        user = config.read_value("pixela_user")
        graph_id = config.read_value("pixela_graph")[0]["graph_id"]

        Pixela().save_graph_svg(user,graph_id)

        data = Pixela().get_graph_stats(user,graph_id)
        self.date = dt.now()
        self.date = self.date.strftime("%B %d,%Y")
    
        today_hour_data = int(data["todaysQuantity"])
        self.today_hour_data = today_hour_data / 60

        avg_hour_data = int(data["avgQuantity"])
        self.avg_hour_data = avg_hour_data/60

        total_hour_data = int(data["totalQuantity"])
        self.total_hour_data = total_hour_data/60

        most_hour_data = int(data["maxQuantity"])
        self.most_hour_data = most_hour_data/60
        self.most_hour_date = (data["maxDate"])

        least_hour_data = int(data["minQuantity"])
        self.least_hour_data = least_hour_data/60
        self.least_hour_date = (data["minDate"])

        return

    def create_ui(self) -> None:
        self.get_data()

        ## try to make img show up wihtout using global variable
        global graph_img
        graph_img = Image.open("data\graph.png").resize((1170,243))
        graph_img = ImageTk.PhotoImage(graph_img)
        btn = Button(text="Back",command=self.return_back)
        btn.grid(row=0,column=1,columnspan=2)
        # canvas = Canvas(height=243,width=550)
        # canvas.create_image(277,60,image=graph_img)
        # canvas.pack()

        canvas = Label(image=graph_img)
        canvas.grid(row=1,column=1,columnspan=2)

        
        
        date_lb = Label(text= f"Date     ",
                        font=self.font_heading,
                        bg=BG_COLOR)
        date_lb2 = Label(text= self.date,
                        font=self.font_content,
                        bg=BG_COLOR)
        date_lb.grid(row=2,column=1)
        date_lb2.grid(row=2,column=2)

        today_hour_lb = Label(text="Today's hours",
                              font=self.font_heading,
                              bg=BG_COLOR)
        today_hour_lb2 = Label(text=self.today_hour_data,
                              font=self.font_content,
                              bg=BG_COLOR)
        today_hour_lb.grid(row=3,column=1)
        today_hour_lb2.grid(row=3,column=2)

        
        avg_hour_lb = Label(text="Avg hours",
                              font=self.font_heading,
                              bg=BG_COLOR)
        avg_hour_lb2 = Label(text=self.avg_hour_data,
                              font=self.font_content,
                              bg=BG_COLOR)
        avg_hour_lb.grid(row=4,column=1)
        avg_hour_lb2.grid(row=4,column=2)

        total_hour_lb = Label(text="Total hours",
                              font=self.font_heading,
                              bg=BG_COLOR)
        total_hour_lb2 = Label(text=self.total_hour_data,
                              font=self.font_content,
                              bg=BG_COLOR)
        total_hour_lb.grid(row=5,column=1)
        total_hour_lb2.grid(row=5,column=2)

        most_hour_lb = Label(text="Most hours",
                              font=self.font_heading,
                              bg=BG_COLOR)
        most_hour_lb2 = Label(text=self.most_hour_data,
                              font=self.font_content,
                              bg=BG_COLOR)
        most_hour_lb3 = Label(text=self.most_hour_date,
                              font=self.font_content,
                              bg=BG_COLOR)
        most_hour_lb.grid(row=6,column=1)
        most_hour_lb2.grid(row=6,column=2)
        most_hour_lb3.grid(row=6,column=3)

        least_hour_lb = Label(text="Least hours",
                              font=self.font_heading,
                              bg=BG_COLOR)
        least_hour_lb2 = Label(text=self.least_hour_data,
                              font=self.font_content,
                              bg=BG_COLOR)
        least_hour_lb3 = Label(text=self.least_hour_date,
                              font=self.font_content,
                              bg=BG_COLOR)
        least_hour_lb.grid(row=7,column=1)
        least_hour_lb2.grid(row=7,column=2)
        least_hour_lb3.grid(row=7,column=3)


        return
    
    def return_back(self):
        Home_UI(self.window)
        return

    pass
