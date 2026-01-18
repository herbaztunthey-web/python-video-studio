from moviepy import ColorClip, TextClip, CompositeVideoClip, AudioFileClip, vfx, afx

# 1. Setup Video (Vertical)
size = (720, 1280)
duration = 10 # Let's make it 10 seconds
background = ColorClip(size=size, color=(0, 50, 100), duration=duration)

# 2. Setup Text
text = TextClip(
    text="Daily Weather\nReport",
    font_size=80,
    color="white",
    font="C:/Windows/Fonts/arial.ttf",
    method='caption',
    size=(600, None),
    text_align='center',
    duration=duration
).with_position('center')

# 3. Handle Audio and Looping
try:
    # Load your mp3 file
    audio = AudioFileClip("weather_music.mp3")
    
    # Loop the audio to match the video duration (MoviePy v2.x way)
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