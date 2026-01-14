import tkinter as tk
from PIL import Image, ImageTk
import random

class AvatarWindow:
    """Avatar window with animations - designed to be thread-safe"""
    
    def __init__(self):
        self.WINDOW_SIZE = 300
        
        self.root = tk.Tk()
        self.root.title("Alisa")
        self.root.geometry(f"{self.WINDOW_SIZE}x{self.WINDOW_SIZE}+50+50")
        self.root.attributes("-topmost", True)
        self.root.overrideredirect(True)

        self.canvas = tk.Canvas(
            self.root,
            width=self.WINDOW_SIZE,
            height=self.WINDOW_SIZE,
            bg="white",
            highlightthickness=0
        )
        self.canvas.pack()

        # Enable dragging
        self.canvas.bind("<Button-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        
        # Enable right-click to close
        self.canvas.bind("<Button-3>", lambda e: self.root.quit())

        # Load images
        self.base_img = ImageTk.PhotoImage(
            Image.open(r"F:\Projects\Nexa\NexaAssistant\overlay\assets\base.png").resize((self.WINDOW_SIZE, self.WINDOW_SIZE))
        )

        self.eyes_closed_img = ImageTk.PhotoImage(
            Image.open(r"F:\Projects\Nexa\NexaAssistant\overlay\assets\eyes_closed.png").resize((self.WINDOW_SIZE, self.WINDOW_SIZE))
        )

        self.mouth_open_img = ImageTk.PhotoImage(
            Image.open(r"F:\Projects\Nexa\NexaAssistant\overlay\assets\mouth_open.png").resize((self.WINDOW_SIZE, self.WINDOW_SIZE))
        )

        self.canvas.create_rectangle(0, 0, self.WINDOW_SIZE, self.WINDOW_SIZE, fill="white", outline="")
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor="nw", image=self.base_img)

        # Animation state
        self.is_talking = False
        
        # Start blinking
        self.root.after(2000, self.blink)

    # ---------------- Drag window ----------------
    def start_drag(self, event):
        self.root._drag_x = event.x
        self.root._drag_y = event.y

    def on_drag(self, event):
        x = self.root.winfo_x() + event.x - self.root._drag_x
        y = self.root.winfo_y() + event.y - self.root._drag_y
        self.root.geometry(f"+{x}+{y}")

    # ---------------- Blink ----------------
    def blink(self):
        self.canvas.itemconfig(self.image_on_canvas, image=self.eyes_closed_img)
        self.root.after(120, lambda: self.canvas.itemconfig(self.image_on_canvas, image=self.base_img))
        self.root.after(random.randint(3000, 6000), self.blink)

    # ---------------- Talking animation ----------------
    def start_talking(self):
        """Start talking animation - can be called from any thread (thread-safe)"""
        if not self.is_talking:
            self.is_talking = True
            print("🗣️ Avatar: Starting talking animation")
            self.animate_mouth()

    def stop_talking(self):
        """Stop talking animation - can be called from any thread (thread-safe)"""
        print("🤐 Avatar: Stopping talking animation")
        self.is_talking = False
        self.canvas.itemconfig(self.image_on_canvas, image=self.base_img)

    def animate_mouth(self):
        """Animate mouth opening and closing with natural variation to simulate speech patterns"""
        if not self.is_talking:
            return
        
        # Add variation to simulate natural pauses in speech (punctuation, breathing, etc.)
        # 70% chance to open mouth - creates natural-looking pauses
        should_open = random.random() > 0.3
        
        if should_open:
            # Open mouth
            self.canvas.itemconfig(self.image_on_canvas, image=self.mouth_open_img)
            
            # Variable mouth open duration (50-90ms for natural variation)
            close_delay = random.randint(50, 90)
            self.root.after(close_delay, lambda: self._close_mouth_if_talking())
        
        # Variable animation loop interval (100-200ms)
        # Wider range creates more natural-looking pauses
        loop_delay = random.randint(100, 200)
        self.root.after(loop_delay, self.animate_mouth)
    
    def _close_mouth_if_talking(self):
        """Helper to close mouth only if still talking"""
        if self.is_talking:
            self.canvas.itemconfig(self.image_on_canvas, image=self.base_img)

    # ---------------- Public API ----------------
    def run(self):
        """Run the avatar window main loop"""
        self.root.mainloop()


# Legacy global API for backwards compatibility
WINDOW_SIZE = 300

root = None
canvas = None
base_img = None
eyes_closed_img = None
mouth_open_img = None
image_on_canvas = None
is_talking = False

def start_talking():
    global is_talking
    if not is_talking:
        is_talking = True
        animate_mouth()

def stop_talking():
    global is_talking
    is_talking = False
    if canvas and image_on_canvas:
        canvas.itemconfig(image_on_canvas, image=base_img)

def animate_mouth():
    if not is_talking:
        return
    if canvas and image_on_canvas:
        canvas.itemconfig(image_on_canvas, image=mouth_open_img)
        root.after(120, lambda: canvas.itemconfig(image_on_canvas, image=base_img))
        root.after(260, animate_mouth)

def run_avatar():
    """Legacy function - creates and runs avatar window"""
    global root, canvas, base_img, eyes_closed_img, mouth_open_img, image_on_canvas
    
    avatar = AvatarWindow()
    root = avatar.root
    canvas = avatar.canvas
    base_img = avatar.base_img
    eyes_closed_img = avatar.eyes_closed_img
    mouth_open_img = avatar.mouth_open_img
    image_on_canvas = avatar.image_on_canvas
    
    avatar.run()
