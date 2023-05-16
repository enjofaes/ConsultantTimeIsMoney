# -*- coding: utf-8 -*-
"""
Created on Sun May 14 09:51:01 2023

@author: efaes
"""

import tkinter as tk
from datetime import datetime, timedelta
import pyperclip
import pandas as pd
import os

os.chdir(r"C:\Users\efaes\Documents\Programming\6.Time_tracker")
class TimeLeft:
    """Main application class for the time tracker GUI"""
    def __init__(self, start_time, target_time, break_start_time):
        self.start_time = datetime.strptime(start_time, "%H:%M:%S").time()
        self.target_time = datetime.strptime(target_time, "%H:%M:%S").time()
        self.break_start_time = timedelta(hours=float(break_start_time))
        self.paused = False
        self.break_start = None
        self.total_break_time = self.break_start_time

        self.root = tk.Tk()
        self.root.geometry('300x200')
        self.root.attributes('-alpha', 0.7)
        self.root.attributes('-topmost', 1)
        self.root.configure(bg='black')

        self.label_left = tk.Label(self.root, text="", fg='white', bg='black', font=("Helvetica", 24))
        self.label_left.pack(pady=10)

        self.label_passed = tk.Label(self.root, text="", fg='white', bg='black', font=("Helvetica", 24))
        self.label_passed.pack(pady=10)

        self.label_break = tk.Label(self.root, text="", fg='white', bg='black', font=("Helvetica", 24))
        self.label_break.pack(pady=10)

        # Create a frame for the buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        # Create the pause and stop buttons and add them to the button frame
        self.button_pause = tk.Button(self.root, text="Break", command=self.toggle_pause, font=("Helvetica", 12), fg='black', bg='lightgrey')
        self.button_pause.pack(in_=button_frame, side="left")
        
        # Add a field to input the current task
        self.current_task = tk.Entry(self.root, font=("Helvetica", 24))
        self.current_task.pack(pady=10)

        # Add a button to move to the next task
        self.button_next_task = tk.Button(self.root, text="Next Task", command=self.next_task, font=("Helvetica", 12), fg='black', bg='lightgrey')
        self.button_next_task.pack(pady=10)

        # Initialize a list to store the tasks and their start and end times
        self.tasks = []
        
        self.button_stop = tk.Button(self.root, text="Stop", command=self.stop, font=("Helvetica", 12), fg='black', bg='lightgrey')
        self.button_stop.pack(in_=button_frame, side="right")

        self.update_clock()
        self.root.mainloop()

    def update_clock(self):
        """Updates the clock and break time labels"""
        now = datetime.now().time()
        target = datetime.combine(datetime.today(), self.target_time)
        start = datetime.combine(datetime.today(), self.start_time)
        if not self.paused:
            if now >= self.target_time:
                self.label_left.configure(text="Time's up!")
            else:
                time_left = target - datetime.now()
                formatted_time_left = "{} hours, {} minutes".format(time_left.seconds // 3600, (time_left.seconds // 60) % 60)
                self.label_left.configure(text="Time left: " + formatted_time_left)

            time_passed = datetime.now() - start - self.total_break_time
            formatted_time_passed = "{} hours, {} minutes".format(time_passed.seconds // 3600, (time_passed.seconds // 60) % 60)
            self.label_passed.configure(text="Time passed: " + formatted_time_passed)
        else:
            self.label_left.configure(text="On break")

        formatted_break_time = "{} hours, {} minutes".format(self.total_break_time.seconds // 3600, (self.total_break_time.seconds // 60) % 60)
        self.label_break.configure(text="Break time: " + formatted_break_time)

        self.root.after(60000, self.update_clock)

    def toggle_pause(self):
        """Toggles between break and continue states"""
        if not self.paused:
            self.paused = True
            self.button_pause.configure(text="Continue")
            self.break_start = datetime.now()
        else:
            self.paused = False
            self.button_pause.configure(text="Break")
            self.total_break_time += datetime.now() - self.break_start
            self.break_start = None

    def next_task(self):
        """Records the current task and its start and end times, and clears the entry field for the next task"""
        task = self.current_task.get()
        if task:  # if task field is not empty
            # If it's the first task of the day, start time is self.start_time, else it's the end time of the last task
            start_time = self.tasks[-1]['end_time'] if self.tasks else datetime.combine(datetime.today(), self.start_time)
            # End time is the current time
            end_time = datetime.now()
            # Record the task and its start and end times
            self.tasks.append({'task': task, 'start_time': start_time, 'end_time': end_time})
            # Clear the entry field
            self.current_task.delete(0, 'end')
            
    def stop(self):
        """Stops the time tracking and copies hours studied to clipboard"""
        if self.paused and self.break_start:
            self.total_break_time += datetime.now() - self.break_start
        time_passed = datetime.now() - datetime.combine(datetime.today(), self.start_time) - self.total_break_time
        hours_passed = time_passed.total_seconds() / 3600  # convert to hours in decimal format
        pyperclip.copy(str(hours_passed))  # copy to clipboard
        # Save the tasks to an Excel file
        df = pd.DataFrame(self.tasks)
        df.to_excel("tasks.xlsx", index=False)
        file_path = "tasks.xlsx"
        print(f"Saved tasks to: {os.path.abspath(file_path)}")
        self.root.destroy()  # close the window


if __name__ == "__main__":
    # Set your start and target times in HH:MM:SS format
    TimeLeft("6:35:00", "22:00:00", 2)