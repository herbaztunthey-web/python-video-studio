import os
import platform
from moviepy import ColorClip, TextClip, CompositeVideoClip, AudioFileClip, vfx, afx

# ... (keep your Setup Video section the same)

# 2. Setup Text - Auto-detecting the correct font path
if platform.system() == "Linux":
    # Specific path for the fonts-liberation package on Ubuntu
    font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
else:
    # Use standard Arial for your Windows machine
    font_path = "Arial"

try:
    text = TextClip(
        text="Daily Weather\nReport",
        font_size=80,
        color="white",
        font=font_path, 
        method='caption',
        size=(600, None),
        text_align='center',
        duration=duration
    ).with_position('center')
except Exception as e:
    print(f"Font error: {e}. Attempting simple fallback.")
    text = TextClip(text="Weather Report", font_size=50, color="white", duration=duration).with_position('center')

# ... (keep the rest of your audio and export code the same)