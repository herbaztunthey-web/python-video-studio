from moviepy import ColorClip, TextClip, CompositeVideoClip, AudioFileClip, vfx, afx
import os

# 1. Setup Video (Vertical)
size = (720, 1280)
duration = 10 
background = ColorClip(size=size, color=(0, 50, 100), duration=duration)

# 2. Setup Text - Using a font compatible with both Windows and GitHub (Linux)
# We use 'Liberation-Sans' because we installed it in our GitHub Action
try:
    text = TextClip(
        text="Daily Weather\nReport",
        font_size=80,
        color="white",
        font="Liberation-Sans", 
        method='caption',
        size=(600, None),
        text_align='center',
        duration=duration
    ).with_position('center')
except Exception:
    # Fallback for your local Windows machine if Liberation-Sans isn't installed there
    text = TextClip(
        text="Daily Weather\nReport",
        font_size=80,
        color="white",
        font="Arial", 
        method='caption',
        size=(600, None),
        text_align='center',
        duration=duration
    ).with_position('center')

# 3. Handle Audio and Looping
try:
    audio = AudioFileClip("weather_music.mp3")
    audio = audio.with_effects([afx.AudioLoop(duration=duration)])
    
    # 4. Combine Video and Audio
    final_video = CompositeVideoClip([background, text])
    final_video = final_video.with_audio(audio)
    
    # 5. Export
    final_video.write_videofile("weather_report_with_music.mp4", fps=24)
    print("Success! Your video now has sound.")

except Exception as e:
    print(f"Audio error: {e}")
    print("Check if 'weather_music.mp3' is in the folder.")