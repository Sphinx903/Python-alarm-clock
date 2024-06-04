import tkinter as tk
from datetime import datetime, timedelta
import winsound
import threading
import pyttsx3

class AlarmClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Alarm Clock")
        self.root.geometry("400x300")  # Set window dimensions to 300x200 pixels

        
        # Set Alarm Label
        self.label = tk.Label(root, text="Set Alarm (HH:MM:SS)")
        self.label.pack()
        
        # Alarm Time Entry
        self.entry = tk.Entry(root)
        self.entry.pack()
        
        # Task Label
        self.task_label = tk.Label(root, text="Task")
        self.task_label.pack()
        
        # Task Entry
        self.task_entry = tk.Entry(root)
        self.task_entry.pack()
        
        # Set Alarm Button
        self.set_button = tk.Button(root, text="Set Alarm", command=self.set_alarm)
        self.set_button.pack()
        
        # Time Remaining Label
        self.time_label = tk.Label(root, text="")
        self.time_label.pack()
        
        self.alarm_time = None
        self.alarm_active = False
        self.update_clock()
        
        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()
        
    def set_alarm(self):
        alarm_time_str = self.entry.get()
        self.task = self.task_entry.get()
        
        try:
            self.alarm_time = datetime.strptime(alarm_time_str, "%H:%M:%S")
        except ValueError:
            tk.messagebox.showerror("Error", "Invalid time format. Please use HH:MM:SS")
            return
        
        current_time = datetime.now()
        self.alarm_time = self.alarm_time.replace(year=current_time.year, month=current_time.month, day=current_time.day)
        
        if self.alarm_time < current_time:
            self.alarm_time += timedelta(days=1)
        
        self.time_label.config(text=f"Alarm set for {self.alarm_time.strftime('%H:%M:%S')} with task: {self.task}")
        
        self.alarm_thread = threading.Thread(target=self.wait_for_alarm)
        self.alarm_thread.daemon = True  # Allows the thread to close when the main program exits
        self.alarm_thread.start()
    
    def wait_for_alarm(self):
        time_difference = self.alarm_time - datetime.now()
        seconds_until_alarm = time_difference.total_seconds()
        if seconds_until_alarm > 0:
            self.root.after(int(seconds_until_alarm * 1000), self.trigger_alarm)
        
    def update_clock(self):
        if self.alarm_time:
            current_time = datetime.now()
            time_difference = self.alarm_time - current_time
            if time_difference.total_seconds() > 0:
                self.time_label.config(text=f"Time remaining: {str(time_difference).split('.')[0]}")
            else:
                self.time_label.config(text="Alarm time reached!")
        self.root.after(1000, self.update_clock)
        
    def trigger_alarm(self):
        self.alarm_active = True
        self.speak_task()
        self.play_sound()
        
    def play_sound(self):
        while self.alarm_active:
            winsound.Beep(440, 1000)  # Plays a 1-second beep at 440 Hz (A4)
            
    def speak_task(self):
        self.engine.say(f"Time to {self.task}")
        self.engine.runAndWait()
            
    def stop_alarm(self):
        self.alarm_active = False

if __name__ == "__main__":
    root = tk.Tk()
    app = AlarmClock(root)
    root.mainloop()
