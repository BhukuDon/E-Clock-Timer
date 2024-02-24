from tkinter import Tk,PhotoImage,Label,Button,Canvas,Frame,W
from PIL import Image,ImageTk
from winotify import Notification, audio
from playsound import playsound

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


# ------------- UI ------------- #
class Clock():
    def __init__(self) -> None:
        
        self.work_session_count = 0
        self.mode = "idle"
        self.status = "stop"
        self.session_time = {"W":4, #mins
                             "B":2} #mins
        self.session = ["W","B","W","B","W","B","W","B","W","B"]
        self.session_index = 0
        self.current_time = 0
        self.speed = 1


        self.window = Tk()
        self.window.title("EClock | Pomodoro Timer")
        self.window.minsize(450,500)
        self.window.config(bg=BG_COLOR,
                           padx=25,
                           pady=25)
        icon = Image.open("assets\icon.ico")
        icon = ImageTk.PhotoImage(icon)
        self.window.iconphoto(False,icon)
        self.createUI()       
        self.window.mainloop()
        pass
    
    # ------------- UI ------------- #
    def createUI(self) -> None:
        icon = Image.open("assets\icon.png").resize((100,40))
        self.icon = ImageTk.PhotoImage(icon)
        self.red_dial = Image.open("assets/red-dial.png").resize((400,400))
        self.red_dial = ImageTk.PhotoImage(self.red_dial)
        self.green_dial = Image.open("assets\green-dial.png").resize((400,400))
        self.green_dial = ImageTk.PhotoImage(self.green_dial)
        self.blue_dial = Image.open("assets/blue-dial.png").resize((400,400))
        self.blue_dial = ImageTk.PhotoImage(self.blue_dial)
        self.reset_img = Image.open("assets/reset.png").resize((35,35))
        self.reset_img = ImageTk.PhotoImage(self.reset_img)
        self.play_img = Image.open("assets\play.png").resize((35,35))
        self.play_img = ImageTk.PhotoImage(self.play_img)
        self.pause_img = Image.open("assets\pause.png").resize((35,35))
        self.pause_img = ImageTk.PhotoImage(self.pause_img)
        self.done = Image.open("assets\done.png").resize((50,50))
        self.done = ImageTk.PhotoImage(self.done)
        self.minute_hand_img = Image.open("assets\minute-hand.png").resize((100,100))
        self.minute_hand_img = ImageTk.PhotoImage(self.minute_hand_img)
        self.second_hand_img = Image.open("assets\second-hand.png").resize((160,160))
        self.second_hand_img = ImageTk.PhotoImage(self.second_hand_img)
        self.dot = Image.open("assets\dot.png").resize((30,30))
        self.dot = ImageTk.PhotoImage(self.dot)

        logo_img = Label(image=self.icon,
                         bg=BG_COLOR,anchor=W)
        logo_img.grid(row=1,column=1,columnspan=3)

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
        clock_pin = self.clock.create_image(200,200,
                                          image = self.dot)

        self.clock.grid(row=3,column=1,columnspan=3) 

        self.play_pause_btn = Button(image=self.play_img,
                            bg=BG_COLOR,
                            activebackground=BG_COLOR,
                            borderwidth=0,
                            command=self.play_pause)
        self.play_pause_btn.grid(row=4,column=1)
        reset = Button(image=self.reset_img,
                            bg=BG_COLOR,
                            activebackground=BG_COLOR,
                            borderwidth=0,
                            command=self.reset)
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

    def reset(self) -> None:
        self.work_session_count = 0
        self.mode = "idle"
        self.status = "stop"
        self.session_index = 0
        self.current_time = 0
        self.work_session_count = 0
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
            self.second_hand_img = Image.open("assets\second-hand.png").resize((160,160))
            self.second_hand_img = ImageTk.PhotoImage(self.second_hand_img)
            self.clock.itemconfig(self.clock_second,image = self.second_hand_img)
            return
        
        to_rotate = degree * time
        
        self.second_hand_img = Image.open("assets\second-hand.png").resize((160,160)).rotate(-to_rotate)
        self.second_hand_img = ImageTk.PhotoImage(self.second_hand_img)

        self.clock.itemconfig(self.clock_second,image = self.second_hand_img)
        return

    def move_minute_hand(self,degree,time,reset=False) -> None:
        if reset == True:
            self.minute_hand_img = Image.open("assets\minute-hand.png").resize((100,100))
            self.minute_hand_img = ImageTk.PhotoImage(self.minute_hand_img)
            self.clock.itemconfig(self.clock_minute,image = self.minute_hand_img)
            
            return
        
        time = time//60 # in mins
        to_rotate = degree * time
        
        self.minute_hand_img = Image.open("assets\minute-hand.png").resize((100,100)).rotate(-to_rotate)
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
            
            self.reset()
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



Clock()

