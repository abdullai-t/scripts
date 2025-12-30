"""
Human PC Usage Simulator with Modern GUI
Simulates realistic human computer usage patterns
For legitimate automation tasks only

Install: pip install pyautogui customtkinter
"""

import pyautogui
import time
import random
import threading
import customtkinter as ctk
from datetime import datetime, timedelta

# Safety feature
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.05

class HumanSimulatorGUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Human PC Usage Simulator")
        self.root.geometry("600x950")
        self.root.resizable(True, True)
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Simulation state
        self.is_running = False
        self.is_paused = False
        self.simulation_thread = None
        self.start_time = None
        self.end_time = None
        self.pause_start_time = None
        self.total_paused_time = 0
        self.cycle_count = 0
        
        # Activity settings
        self.enable_mouse = ctk.BooleanVar(value=True)
        self.enable_typing = ctk.BooleanVar(value=True)
        self.enable_clicks = ctk.BooleanVar(value=True)
        self.enable_scrolling = ctk.BooleanVar(value=True)
        self.enable_shortcuts = ctk.BooleanVar(value=True)
        
        self.setup_ui()
        
    def setup_ui(self):
        # Title
        title = ctk.CTkLabel(
            self.root, 
            text="🖱️ Human PC Usage Simulator",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=20)
        
        # Duration Frame
        duration_frame = ctk.CTkFrame(self.root)
        duration_frame.pack(pady=20, padx=40, fill="x")
        
        ctk.CTkLabel(
            duration_frame,
            text="Duration",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)
        
        # Hours and Minutes Input
        time_input_frame = ctk.CTkFrame(duration_frame)
        time_input_frame.pack(pady=10)
        
        ctk.CTkLabel(time_input_frame, text="Hours:", font=ctk.CTkFont(size=14)).grid(row=0, column=0, padx=5, pady=5)
        self.hours_entry = ctk.CTkEntry(time_input_frame, width=80, placeholder_text="0")
        self.hours_entry.grid(row=0, column=1, padx=5, pady=5)
        self.hours_entry.insert(0, "1")
        
        ctk.CTkLabel(time_input_frame, text="Minutes:", font=ctk.CTkFont(size=14)).grid(row=0, column=2, padx=5, pady=5)
        self.minutes_entry = ctk.CTkEntry(time_input_frame, width=80, placeholder_text="0")
        self.minutes_entry.grid(row=0, column=3, padx=5, pady=5)
        self.minutes_entry.insert(0, "0")
        
        # Quick preset buttons
        preset_frame = ctk.CTkFrame(duration_frame)
        preset_frame.pack(pady=10)
        
        ctk.CTkButton(preset_frame, text="30 min", width=70, command=lambda: self.set_preset(0, 30)).grid(row=0, column=0, padx=5)
        ctk.CTkButton(preset_frame, text="1 hour", width=70, command=lambda: self.set_preset(1, 0)).grid(row=0, column=1, padx=5)
        ctk.CTkButton(preset_frame, text="2 hours", width=70, command=lambda: self.set_preset(2, 0)).grid(row=0, column=2, padx=5)
        ctk.CTkButton(preset_frame, text="4 hours", width=70, command=lambda: self.set_preset(4, 0)).grid(row=0, column=3, padx=5)
        
        # Activities Selection Frame
        activities_frame = ctk.CTkFrame(self.root)
        activities_frame.pack(pady=20, padx=40, fill="x")
        
        ctk.CTkLabel(
            activities_frame,
            text="Activities to Perform",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)
        
        # Checkboxes for activities
        checkbox_container = ctk.CTkFrame(activities_frame)
        checkbox_container.pack(pady=10)
        
        # Mouse activities
        mouse_frame = ctk.CTkFrame(checkbox_container)
        mouse_frame.grid(row=0, column=0, padx=20, pady=5, sticky="w")
        
        ctk.CTkCheckBox(
            mouse_frame,
            text="🖱️ Mouse Movement",
            variable=self.enable_mouse,
            font=ctk.CTkFont(size=13)
        ).pack(anchor="w", pady=3)
        
        ctk.CTkCheckBox(
            mouse_frame,
            text="👆 Clicking",
            variable=self.enable_clicks,
            font=ctk.CTkFont(size=13)
        ).pack(anchor="w", pady=3)
        
        ctk.CTkCheckBox(
            mouse_frame,
            text="🔄 Scrolling",
            variable=self.enable_scrolling,
            font=ctk.CTkFont(size=13)
        ).pack(anchor="w", pady=3)
        
        # Keyboard activities
        keyboard_frame = ctk.CTkFrame(checkbox_container)
        keyboard_frame.grid(row=0, column=1, padx=20, pady=5, sticky="w")
        
        ctk.CTkCheckBox(
            keyboard_frame,
            text="⌨️ Typing",
            variable=self.enable_typing,
            font=ctk.CTkFont(size=13)
        ).pack(anchor="w", pady=3)
        
        ctk.CTkCheckBox(
            keyboard_frame,
            text="⚡ Keyboard Shortcuts",
            variable=self.enable_shortcuts,
            font=ctk.CTkFont(size=13)
        ).pack(anchor="w", pady=3)
        
        # Select/Deselect all buttons
        select_buttons_frame = ctk.CTkFrame(activities_frame)
        select_buttons_frame.pack(pady=10)
        
        ctk.CTkButton(
            select_buttons_frame,
            text="Select All",
            command=self.select_all_activities,
            width=120,
            height=30,
            font=ctk.CTkFont(size=12)
        ).grid(row=0, column=0, padx=5)
        
        ctk.CTkButton(
            select_buttons_frame,
            text="Deselect All",
            command=self.deselect_all_activities,
            width=120,
            height=30,
            font=ctk.CTkFont(size=12)
        ).grid(row=0, column=1, padx=5)
        
        # Status Frame
        status_frame = ctk.CTkFrame(self.root)
        status_frame.pack(pady=20, padx=40, fill="both", expand=True)
        
        ctk.CTkLabel(
            status_frame,
            text="Status",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)
        
        # Status labels
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="⏸️ Idle",
            font=ctk.CTkFont(size=14)
        )
        self.status_label.pack(pady=5)
        
        self.cycle_label = ctk.CTkLabel(
            status_frame,
            text="Cycles: 0",
            font=ctk.CTkFont(size=12)
        )
        self.cycle_label.pack(pady=5)
        
        self.time_label = ctk.CTkLabel(
            status_frame,
            text="Time Remaining: --:--",
            font=ctk.CTkFont(size=12)
        )
        self.time_label.pack(pady=5)
        
        self.activity_label = ctk.CTkLabel(
            status_frame,
            text="Current Activity: None",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.activity_label.pack(pady=5)
        
        # Progress bar
        self.progress = ctk.CTkProgressBar(status_frame, width=400)
        self.progress.pack(pady=20)
        self.progress.set(0)
        
        # Log text area
        self.log_text = ctk.CTkTextbox(status_frame, height=180, width=500)
        self.log_text.pack(pady=10, padx=10)
        
        # Control Buttons
        button_frame = ctk.CTkFrame(self.root)
        button_frame.pack(pady=20)
        
        self.start_button = ctk.CTkButton(
            button_frame,
            text="▶️ Start Simulation",
            command=self.start_simulation,
            width=150,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="green",
            hover_color="darkgreen"
        )
        self.start_button.grid(row=0, column=0, padx=5)
        
        self.pause_button = ctk.CTkButton(
            button_frame,
            text="⏸️ Pause",
            command=self.pause_simulation,
            width=150,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="orange",
            hover_color="darkorange",
            state="disabled"
        )
        self.pause_button.grid(row=0, column=1, padx=5)
        
        self.stop_button = ctk.CTkButton(
            button_frame,
            text="⏹️ Stop Simulation",
            command=self.stop_simulation,
            width=150,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="red",
            hover_color="darkred",
            state="disabled"
        )
        self.stop_button.grid(row=0, column=2, padx=5)
        
        # Safety warning
        warning = ctk.CTkLabel(
            self.root,
            text="⚠️ Safety: Move mouse to top-left corner to abort",
            font=ctk.CTkFont(size=10),
            text_color="orange"
        )
        warning.pack(pady=5)
        
    def set_preset(self, hours, minutes):
        self.hours_entry.delete(0, 'end')
        self.hours_entry.insert(0, str(hours))
        self.minutes_entry.delete(0, 'end')
        self.minutes_entry.insert(0, str(minutes))
    
    def select_all_activities(self):
        self.enable_mouse.set(True)
        self.enable_typing.set(True)
        self.enable_clicks.set(True)
        self.enable_scrolling.set(True)
        self.enable_shortcuts.set(True)
    
    def deselect_all_activities(self):
        self.enable_mouse.set(False)
        self.enable_typing.set(False)
        self.enable_clicks.set(False)
        self.enable_scrolling.set(False)
        self.enable_shortcuts.set(False)
        
    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert("end", f"[{timestamp}] {message}\n")
        self.log_text.see("end")
        
    def update_status(self, status, activity=""):
        self.status_label.configure(text=status)
        if activity:
            self.activity_label.configure(text=f"Current Activity: {activity}")
        
    def start_simulation(self):
        try:
            hours = int(self.hours_entry.get() or 0)
            minutes = int(self.minutes_entry.get() or 0)
            
            if hours == 0 and minutes == 0:
                self.log("❌ Please enter a valid duration")
                return
            
            # Check if at least one activity is selected
            if not any([self.enable_mouse.get(), self.enable_typing.get(), 
                       self.enable_clicks.get(), self.enable_scrolling.get(), 
                       self.enable_shortcuts.get()]):
                self.log("❌ Please select at least one activity")
                return
                
            total_minutes = hours * 60 + minutes
            
            self.is_running = True
            self.is_paused = False
            self.cycle_count = 0
            self.start_time = time.time()
            self.end_time = self.start_time + (total_minutes * 60)
            self.total_paused_time = 0
            
            self.start_button.configure(state="disabled")
            self.pause_button.configure(state="normal", text="⏸️ Pause")
            self.stop_button.configure(state="normal")
            self.hours_entry.configure(state="disabled")
            self.minutes_entry.configure(state="disabled")
            
            # Log selected activities
            activities = []
            if self.enable_mouse.get():
                activities.append("Mouse Movement")
            if self.enable_clicks.get():
                activities.append("Clicking")
            if self.enable_scrolling.get():
                activities.append("Scrolling")
            if self.enable_typing.get():
                activities.append("Typing")
            if self.enable_shortcuts.get():
                activities.append("Shortcuts")
            
            self.log(f"✅ Starting simulation for {hours}h {minutes}m")
            self.log(f"📋 Active: {', '.join(activities)}")
            self.update_status("🟢 Running")
            
            # Start simulation in separate thread
            self.simulation_thread = threading.Thread(target=self.run_simulation, daemon=True)
            self.simulation_thread.start()
            
            # Start UI update loop
            self.update_ui()
            
        except ValueError:
            self.log("❌ Invalid duration format")
    
    def pause_simulation(self):
        if not self.is_paused:
            # Pause
            self.is_paused = True
            self.pause_start_time = time.time()
            self.pause_button.configure(text="▶️ Resume", fg_color="green", hover_color="darkgreen")
            self.log("⏸️ Simulation paused")
            self.update_status("🟡 Paused")
        else:
            # Resume
            self.is_paused = False
            if self.pause_start_time:
                pause_duration = time.time() - self.pause_start_time
                self.total_paused_time += pause_duration
                self.end_time += pause_duration  # Extend end time by pause duration
            self.pause_button.configure(text="⏸️ Pause", fg_color="orange", hover_color="darkorange")
            self.log("▶️ Simulation resumed")
            self.update_status("🟢 Running")
            
    def stop_simulation(self):
        self.is_running = False
        self.is_paused = False
        self.start_button.configure(state="normal")
        self.pause_button.configure(state="disabled", text="⏸️ Pause")
        self.stop_button.configure(state="disabled")
        self.hours_entry.configure(state="normal")
        self.minutes_entry.configure(state="normal")
        self.log("⏹️ Simulation stopped by user")
        self.update_status("⏸️ Stopped")
        
    def update_ui(self):
        if self.is_running:
            if not self.is_paused:
                elapsed = time.time() - self.start_time - self.total_paused_time
                total_duration = self.end_time - self.start_time
                remaining = max(0, self.end_time - time.time())
                
                # Update progress
                progress_value = min(1.0, elapsed / total_duration)
                self.progress.set(progress_value)
                
                # Update time remaining
                remaining_minutes = int(remaining // 60)
                remaining_seconds = int(remaining % 60)
                self.time_label.configure(text=f"Time Remaining: {remaining_minutes:02d}:{remaining_seconds:02d}")
            else:
                # Show paused status
                self.time_label.configure(text=f"Time Remaining: PAUSED")
            
            # Update cycle count
            self.cycle_label.configure(text=f"Cycles: {self.cycle_count}")
            
            # Schedule next update
            self.root.after(1000, self.update_ui)
            
    def run_simulation(self):
        try:
            while self.is_running and time.time() < self.end_time:
                # Wait while paused
                while self.is_paused and self.is_running:
                    time.sleep(0.1)
                    continue
                
                if not self.is_running:
                    break
                
                self.cycle_count += 1
                remaining_seconds = self.end_time - time.time()
                
                self.log(f"🔄 Cycle {self.cycle_count} started")
                
                # Determine which phase to run based on settings
                run_mouse_phase = self.enable_mouse.get() or self.enable_clicks.get() or self.enable_scrolling.get()
                run_typing_phase = self.enable_typing.get() or self.enable_shortcuts.get()
                
                # Check if we have enough time for a full cycle
                if remaining_seconds < 120:
                    if remaining_seconds > 60 and run_mouse_phase:
                        self.human_mouse_movement(60)
                        remaining_seconds = self.end_time - time.time()
                        if remaining_seconds > 0 and run_typing_phase:
                            self.human_typing_activity(int(remaining_seconds))
                    elif run_mouse_phase:
                        self.human_mouse_movement(int(remaining_seconds))
                    elif run_typing_phase:
                        self.human_typing_activity(int(remaining_seconds))
                    break
                
                # Phase 1: Mouse activity (if enabled)
                if not self.is_running:
                    break
                if run_mouse_phase:
                    self.human_mouse_movement(60)
                
                # Phase 2: Typing activity (if enabled)
                if not self.is_running:
                    break
                    
                # Wait while paused between phases
                while self.is_paused and self.is_running:
                    time.sleep(0.1)
                    continue
                    
                if not self.is_running:
                    break
                
                if run_typing_phase:
                    time.sleep(2)
                    self.human_typing_activity(60)
                
                # Small break between cycles
                if time.time() < self.end_time and self.is_running:
                    break_time = random.uniform(2, 5)
                    break_start = time.time()
                    while time.time() - break_start < break_time and self.is_running:
                        if self.is_paused:
                            while self.is_paused and self.is_running:
                                time.sleep(0.1)
                        else:
                            time.sleep(0.1)
                    
            if self.is_running:
                self.log(f"✅ Simulation completed! Total cycles: {self.cycle_count}")
                self.update_status("✅ Completed")
                self.is_running = False
                self.root.after(0, lambda: self.start_button.configure(state="normal"))
                self.root.after(0, lambda: self.pause_button.configure(state="disabled", text="⏸️ Pause"))
                self.root.after(0, lambda: self.stop_button.configure(state="disabled"))
                self.root.after(0, lambda: self.hours_entry.configure(state="normal"))
                self.root.after(0, lambda: self.minutes_entry.configure(state="normal"))
                
        except Exception as e:
            self.log(f"❌ Error: {str(e)}")
            self.is_running = False
            
    def human_mouse_movement(self, duration_seconds=60):
        screen_width, screen_height = pyautogui.size()
        start_time = time.time()
        
        self.update_status("🟢 Running", "Mouse Movement")
        
        # Build list of enabled actions
        available_actions = []
        if self.enable_mouse.get():
            available_actions.extend(['move'] * 50)
        if self.enable_clicks.get():
            available_actions.extend(['click'] * 20)
            available_actions.extend(['double_click'] * 5)
        if self.enable_scrolling.get():
            available_actions.extend(['scroll'] * 15)
        available_actions.extend(['idle'] * 10)
        
        if not available_actions:
            return
        
        while time.time() - start_time < duration_seconds and self.is_running:
            # Wait while paused
            while self.is_paused and self.is_running:
                time.sleep(0.1)
                continue
            
            if not self.is_running:
                break
                
            action = random.choice(available_actions)
            
            if action == 'move':
                x = random.randint(100, screen_width - 100)
                y = random.randint(100, screen_height - 100)
                pyautogui.moveTo(x, y, duration=random.uniform(0.5, 1.5), tween=pyautogui.easeInOutQuad)
                time.sleep(random.uniform(0.2, 0.8))
                
            elif action == 'click':
                time.sleep(random.uniform(0.1, 0.3))
                pyautogui.click()
                time.sleep(random.uniform(0.3, 1.0))
                
            elif action == 'scroll':
                pyautogui.scroll(random.randint(-3, 3) * 100)
                time.sleep(random.uniform(0.3, 0.8))
                
            elif action == 'double_click':
                time.sleep(random.uniform(0.1, 0.2))
                pyautogui.doubleClick()
                time.sleep(random.uniform(0.5, 1.2))
                
            elif action == 'idle':
                idle_time = random.uniform(1.0, 3.0)
                idle_start = time.time()
                while time.time() - idle_start < idle_time and self.is_running:
                    if self.is_paused:
                        while self.is_paused and self.is_running:
                            time.sleep(0.1)
                    else:
                        time.sleep(0.1)
                
    def human_typing_activity(self, duration_seconds=60):
        start_time = time.time()
        
        sentences = [
            "I need to finish this report by tomorrow.",
            "Let me check the documentation for this.",
            "The meeting is scheduled for next week.",
            "Can you send me the updated files?",
            "I'm working on the project requirements.",
            "This looks good, let me review it again.",
        ]
        
        self.update_status("🟢 Running", "Typing")
        
        # Build list of enabled actions
        available_actions = []
        if self.enable_typing.get():
            available_actions.extend(['type_sentence'] * 40)
            available_actions.extend(['type_word'] * 25)
            available_actions.extend(['delete'] * 10)
        if self.enable_shortcuts.get():
            available_actions.extend(['shortcut'] * 5)
        available_actions.extend(['pause'] * 20)
        
        if not available_actions:
            return
        
        while time.time() - start_time < duration_seconds and self.is_running:
            # Wait while paused
            while self.is_paused and self.is_running:
                time.sleep(0.1)
                continue
            
            if not self.is_running:
                break
                
            action = random.choice(available_actions)
            
            if action == 'type_sentence':
                sentence = random.choice(sentences)
                for char in sentence + " ":
                    if not self.is_running or self.is_paused:
                        break
                    pyautogui.write(char)
                    time.sleep(random.uniform(0.08, 0.18))
                time.sleep(random.uniform(0.5, 2.0))
                
            elif action == 'type_word':
                words = ["hello", "update", "review", "check", "complete"]
                word = random.choice(words) + " "
                for char in word:
                    if not self.is_running or self.is_paused:
                        break
                    pyautogui.write(char)
                    time.sleep(random.uniform(0.08, 0.18))
                time.sleep(random.uniform(0.3, 1.0))
                
            elif action == 'delete':
                for _ in range(random.randint(1, 5)):
                    if not self.is_running or self.is_paused:
                        break
                    pyautogui.press('backspace')
                    time.sleep(random.uniform(0.05, 0.15))
                time.sleep(random.uniform(0.2, 0.5))
                
            elif action == 'pause':
                pause_time = random.uniform(2.0, 5.0)
                pause_start = time.time()
                while time.time() - pause_start < pause_time and self.is_running:
                    if self.is_paused:
                        while self.is_paused and self.is_running:
                            time.sleep(0.1)
                    else:
                        time.sleep(0.1)
                
            elif action == 'shortcut':
                shortcuts = [['ctrl', 'c'], ['ctrl', 'v'], ['ctrl', 's']]
                pyautogui.hotkey(*random.choice(shortcuts))
                time.sleep(random.uniform(0.5, 1.5))
                
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    # Install: pip install pyautogui customtkinter
    app = HumanSimulatorGUI()
    app.run()