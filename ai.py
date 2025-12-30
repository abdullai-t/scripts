"""
Human PC Usage Simulator
Simulates realistic human computer usage patterns
For legitimate automation tasks only
"""

import pyautogui
import time
import random

# Safety feature - move mouse to corner to abosend Thanks for sending that information over. The meeting is scheduled for next week. I'm working on the project requirements.Thanks for sending that information over. check Can you send me the updated files? 
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.05

def move_mouse_naturally(x, y, duration=0.5):
    """Move mouse with bezier-like curve and slight randomness"""
    offset_x = random.randint(-3, 3)
    offset_y = random.randint(-3, 3)
    pyautogui.moveTo(x + offset_x, y + offset_y, duration=duration, tween=pyautogui.easeInOutQuad)

def type_naturally(text, min_interval=0.05, max_interval=0.15):
    """Type text with random intervals and occasional mistakes"""
    for i, char in enumerate(text):
        # Occasionally make a "typo" and correct it
        if random.random() < 0.02:  # 2% chance of typo
            wrong_char = random.choice('abcdefghijklmnopqrstuvwxyz')
            pyautogui.write(wrong_char)
            time.sleep(random.uniform(0.1, 0.3))
            pyautogui.press('backspace')
            time.sleep(random.uniform(0.1, 0.2))
        
        pyautogui.write(char)
        
        # Longer pause after punctuation
        if char in '.,!?':
            time.sleep(random.uniform(0.2, 0.5))
        else:
            time.sleep(random.uniform(min_interval, max_interval))

def human_mouse_movement(duration_seconds=60):
    """Simulate human-like mouse movements"""
    screen_width, screen_height = pyautogui.size()
    start_time = time.time()
    
    print(f"Phase 1: Mouse activity for {duration_seconds} seconds...")
    
    while time.time() - start_time < duration_seconds:
        action = random.choices(
            # ['move', 'click', 'scroll', 'double_click', 'idle'],
            ['move', 'scroll', 'idle'],
            weights=[50, 20, 30]
        )[0]
        
        if action == 'move':
            # Random movement
            x = random.randint(100, screen_width - 100)
            y = random.randint(100, screen_height - 100)
            move_mouse_naturally(x, y, duration=random.uniform(0.5, 1.5))
            time.sleep(random.uniform(0.2, 0.8))
            
        elif action == 'click':
            # Click at current or nearby position
            offset_x = random.randint(-50, 50)
            offset_y = random.randint(-50, 50)
            current_x, current_y = pyautogui.position()
            target_x = max(0, min(screen_width, current_x + offset_x))
            target_y = max(0, min(screen_height, current_y + offset_y))
            move_mouse_naturally(target_x, target_y, duration=random.uniform(0.3, 0.7))
            time.sleep(random.uniform(0.1, 0.3))
            pyautogui.click()
            time.sleep(random.uniform(0.3, 1.0))
            
        elif action == 'scroll':
            # Scroll up or down
            scroll_amount = random.randint(-3, 3)
            pyautogui.scroll(scroll_amount * 100)
            time.sleep(random.uniform(0.3, 0.8))
            
        elif action == 'double_click':
            # Double click
            time.sleep(random.uniform(0.1, 0.2))
            pyautogui.doubleClick()
            time.sleep(random.uniform(0.5, 1.2))
            
        elif action == 'idle':
            # Simulate reading/thinking
            time.sleep(random.uniform(1.0, 3.0))
    
    print("Mouse activity complete!")

def human_typing_activity(duration_seconds=60):
    """Simulate human typing patterns"""
    start_time = time.time()
    
    # Sample text patterns humans might type
    sentences = [
        "I need to finish this report by tomorrow.",
        "Let me check the documentation for this.",
        "The meeting is scheduled for next week.",
        "Can you send me the updated files?",
        "I'm working on the project requirements.",
        "This looks good, let me review it again.",
        "I'll get back to you on that shortly.",
        "The data shows some interesting patterns.",
        "We should schedule a follow-up meeting.",
        "Thanks for sending that information over.",
    ]
    
    print(f"\nPhase 2: Typing activity for {duration_seconds} seconds...")
    
    while time.time() - start_time < duration_seconds:
        action = random.choices(
            ['type_sentence', 'type_word', 'delete', 'pause', 'shortcut'],
            weights=[40, 25, 10, 20, 5]
        )[0]
        
        if action == 'type_sentence':
            sentence = random.choice(sentences)
            type_naturally(sentence + " ", min_interval=0.08, max_interval=0.18)
            time.sleep(random.uniform(0.5, 2.0))
            
        elif action == 'type_word':
            words = ["hello", "update", "review", "check", "complete", "send", "file", "data"]
            word = random.choice(words)
            type_naturally(word + " ", min_interval=0.08, max_interval=0.18)
            time.sleep(random.uniform(0.3, 1.0))
            
        elif action == 'delete':
            # Delete a few characters (simulate correction)
            delete_count = random.randint(1, 5)
            for _ in range(delete_count):
                pyautogui.press('backspace')
                time.sleep(random.uniform(0.05, 0.15))
            time.sleep(random.uniform(0.2, 0.5))
            
        elif action == 'pause':
            # Simulate thinking/reading
            time.sleep(random.uniform(2.0, 5.0))
            
        elif action == 'shortcut':
            # Common keyboard shortcuts
            shortcuts = [
                # ['ctrl', 'c'],  # copy
                # ['ctrl', 'v'],  # paste
                # ['ctrl', 's'],  # save
                ['ctrl', 'a'],  # select all
            ]
            shortcut = random.choice(shortcuts)
            pyautogui.hotkey(*shortcut)
            time.sleep(random.uniform(0.5, 1.5))
    
    print("Typing activity complete!")

def parse_duration(duration_str):
    """Parse duration string like '4.15' into total minutes"""
    try:
        parts = duration_str.split('.')
        hours = int(parts[0])
        minutes = int(parts[1]) if len(parts) > 1 else 0
        
        if minutes >= 60:
            print("Warning: Minutes should be less than 60. Using 59 instead.")
            minutes = 59
            
        total_minutes = hours * 60 + minutes
        return total_minutes
    except:
        print("Invalid format! Using default: 1 hour")
        return 60

def simulate_human_usage():
    """Main function: simulate realistic human PC usage"""
    print("=" * 60)
    print("Human PC Usage Simulator")
    print("=" * 60)
    
    # Get duration from user
    print("\nHow long should the simulation run?")
    print("Format: H.MM (e.g., 4.15 = 4 hours 15 minutes)")
    print("         or just H (e.g., 2 = 2 hours)")
    duration_input = input("Enter duration: ").strip()
    
    total_minutes = parse_duration(duration_input)
    hours = total_minutes // 60
    minutes = total_minutes % 60
    
    print(f"\nSimulation will run for: {hours} hour(s) {minutes} minute(s)")
    print(f"Total cycles: approximately {total_minutes // 2}")
    
    print("\nStarting in 5 seconds...")
    print("SAFETY: Move mouse to top-left corner to abort anytime!")
    print("\nEach cycle (2 minutes):")
    print("  - 1 minute: Mouse movements, clicks, scrolling")
    print("  - 1 minute: Typing, editing, keyboard shortcuts")
    print("=" * 60)
    
    time.sleep(5)
    
    # Get screen info
    screen_width, screen_height = pyautogui.size()
    print(f"\nScreen size: {screen_width}x{screen_height}")
    
    # Calculate end time
    end_time = time.time() + (total_minutes * 60)
    cycle_count = 0
    
    # Run cycles until time is up
    while time.time() < end_time:
        cycle_count += 1
        remaining_seconds = end_time - time.time()
        remaining_minutes = int(remaining_seconds // 60)
        
        print(f"\n{'='*60}")
        print(f"CYCLE {cycle_count} | Time remaining: {remaining_minutes} minutes")
        print(f"{'='*60}")
        
        # Check if we have enough time for a full cycle
        if remaining_seconds < 120:
            # Run partial cycle with remaining time
            if remaining_seconds > 60:
                print("Running final mouse activity...")
                human_mouse_movement(60)
                remaining_seconds = end_time - time.time()
                if remaining_seconds > 0:
                    print("Running final typing activity...")
                    human_typing_activity(int(remaining_seconds))
            else:
                print("Running final activity...")
                human_mouse_movement(int(remaining_seconds))
            break
        
        # Phase 1: Mouse activity (1 minute)
        human_mouse_movement(60)
        
        # Check if we still have time
        if time.time() >= end_time:
            break
        
        # Brief transition
        time.sleep(2)
        
        # Phase 2: Typing activity (1 minute)
        human_typing_activity(60)
        
        # Small break between cycles
        if time.time() < end_time:
            time.sleep(random.uniform(2, 5))
    
    print("\n" + "=" * 60)
    print(f"Simulation complete! Ran {cycle_count} cycle(s)")
    print("=" * 60)

if __name__ == "__main__":
    # Install required package first:
    # pip install pyautogui
    
    try:
        simulate_human_usage()
    except KeyboardInterrupt:
        print("\n\nSimulation aborted by user!")
    except Exception as e:
        print(f"\n\nError: {e}")