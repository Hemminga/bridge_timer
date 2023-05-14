# import time
# import threading
import time
import tkinter as tk
from tkinter import ttk, PhotoImage

# https://www.youtube.com/watch?v=FJeXp5yZd-g


class BridgeTimer:
    def __init__(self):

        self.state = {
            "time_set": 1,  # Programmed time in minutes
            "pause_set": 2,  # Pause time set in minues
            "state": "Running",  # Several possibilities: Running, Started, Paused, Stopped, Programming
            "current": 0,  # Time in seconds
            "blinking": False
        }

        self.root = tk.Tk()
        self.root.geometry("600x300")
        self.root.title("Pomodoro Bridge Timer")
        # https://www.delftstack.com/howto/python-tkinter/how-to-set-window-icon-in-tkinter/
        # noinspection PyProtectedMember,PyUnresolvedReferences
        self.root.tk.call('wm', 'iconphoto', self.root._w, PhotoImage(file='tomato.png'))

        # Define grid on 'root'
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.root.columnconfigure(3, weight=1)
        self.root.columnconfigure(4, weight=1)
        self.root.rowconfigure(0, weight=3)
        # self.root.rowconfigure(1, weight=1)

        self.text_variable = tk.StringVar(value="00:00")
        self.label_time = ttk.Label(
            self.root,
            textvariable=self.text_variable,
            font=("Digital Dismay", 128),
            foreground="red")
        self.label_time.grid(column=0, row=0, columnspan=5)

        self.button_start = ttk.Button(self.root, text="Start", command=lambda: self.start('Start'))
        self.button_stop = ttk.Button(self.root, text="Stop", command=self.stop)
        self.button_prog = ttk.Button(self.root, text="Prog")
        self.button_plus = ttk.Button(self.root, text="+")
        self.button_min = ttk.Button(self.root, text="-")
        buttons = [self.button_start, self.button_stop, self.button_prog, self.button_plus, self.button_min]
        for button in range(len(buttons)):
            buttons[button].grid(column=button, row=1)

        self.statusbar = tk.Label(self.root, text=self.state['state'], bd=1, relief=tk.SUNKEN, anchor=tk.W)

        self.statusbar.grid(column=0, row=2, columnspan=5, sticky=tk.EW)

        # The clock will be started. Every other event will be triggered by bottons
        self.launch_clock()
        self.root.mainloop()

    def set_state(self, state):
        print(f'Change state to {state}')
        if state not in ['Running', 'Started', 'Paused', 'Stopped', 'Programming']:
            print(f"state {state} not in ['Running', 'Started', 'Paused', 'Stopped', 'Programming']")
        self.state['state'] = state
        self.statusbar.configure(text=self.state['state'])

    def launch_clock(self):
        """
        When the clock is started it will count incrementally from zero.
        self.state['state'] will be 'Running'

        :return:
        """
        # Stop if the 'Stop' button is clicked
        if self.state['state'] == 'Stopped':
            return
        pause = 1000
        hrs = self.state["current"] // 60 * 60
        mins = self.state["current"] // 60
        secs = self.state["current"] % 60
        string = f"{mins:02}:{secs:02}"
        if self.state["current"] > 60 * 60:
            self.state['blinking'] = not self.state['blinking']
            string = f"{hrs:02}:{mins:02}"
            pause = 500
        if self.state["blinking"]:
            string = f"{hrs:02}.{mins:02}"
        else:
            if self.state["state"] == "Running":
                self.state["current"] += 1

        self.text_variable.set(string)
        self.label_time.after(pause, self.launch_clock)

    def stop(self):
        if self.state['state'] == 'Stopped':
            self.state['current'] = 0
            self.text_variable.set('00:00')
        else:
            # Do not change state['current']; We may continue from here ('pause')
            self.set_state('Stopped')

    def start(self, action=''):
        """
        Countdown running
        :param action: The button click, either '' (default) or 'Start' (-> clicked)
        :return:
        """
        print(f"{self.state['current']}")
        if action == '' and self.state['state'] == 'Stopped':
            # Stop the clock
            return
        if action == 'Start' and self.state['state'] == 'Started':
            # Already running
            return
        if action == 'Start' and self.state['state'] != 'Started':
            # Starting a clock that is not already running
            if self.state['current'] == 0:
                self.state['current'] = self.state['time_set'] * 60
        if self.state['state'] != 'Started':
            self.set_state('Started')
        self.run()

    def pause(self):
        self.state['current'] = self.state['pause_set'] * 60
        self.set_state('Paused')
        self.run()

    def run(self):
        pause = 1000
        self.state["current"] -= 1
        hrs = self.state["current"] // 60 * 60
        mins = self.state["current"] // 60
        secs = self.state["current"] % 60
        string = f"{mins:02}:{secs:02}"
        self.text_variable.set(string)
        if self.state['current'] == 0:
            print('Change state')
            time.sleep(1)
            if self.state['state'] == 'Started':
                self.pause()
            elif self.state['state'] == 'Paused':
                self.start()
            return
        self.label_time.after(pause, self.run)


if __name__ == "__main__":
    BridgeTimer()
