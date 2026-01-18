import os
import platform
from moviepy import ColorClip, TextClip, CompositeVideoClip, AudioFileClip, vfx, afx

# 1. SETUP CONSTANTS FIRST
# We define these at the top so the whole script can see them
size = (720, 1280)
duration = 10 

# 2. AUTO-DETECT FONT PATH
if platform.system() == "Linux":
    # Absolute path for the fonts we installed in main.yml
    font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
else:
    # Standard font for your Windows machine
    font_path = "Arial"

# 3. SETUP VIDEO BACKGROUND
background = ColorClip(size=size, color=(0, 50, 100), duration=duration)

# 4. SETUP TEXT
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
    print(f"Primary font failed: {e}. Using basic fallback.")
    # Simple fallback that doesn't rely on specific font files
    text = TextClip(
        text="Weather Report", 
        font_size=50, 
        color="white", 
        duration=duration
    ).with_position('center')

# 5. HANDLE AUDIO AND EXPORT
try:
    # Check if music exists before loading
    if os.path.exists("weather_music.mp3"):
        audio = AudioFileClip("weather_music.mp3")
        audio = audio.with_effects([afx.AudioLoop(duration=duration)])
        
        final_video = CompositeVideoClip([background, text])
        final_video = final_video.with_audio(audio)
    else:
        print("Music file not found, creating video without audio.")
        final_video = CompositeVideoClip([background, text])
    
    # Export the final file
    final_video.write_videofile("weather_report_with_music.mp4", fps=24)
    print("Success! Process complete.")

except Exception as e:
    print(f"Final Export Error: {e}")