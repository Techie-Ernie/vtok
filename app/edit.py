import ffmpeg
import moviepy.editor as mp
import os
import shutil 
import glob 

def make_video(match_name, input_file, count, overlay=False):
    overlay_img_path = '../overlays/overlay.png'
    input_stream = ffmpeg.input(input_file)
    # Box blur with radius 20
    background_stream = input_stream.filter("boxblur", 20)
    name = str(count)
    print(name)
    ffmpeg.output(background_stream, f"../match_clip/clips/{name}_bg.mp4").run()
    small = mp.VideoFileClip(input_file)
    if small.duration >= 8: 
        if overlay:
            bg = mp.ImageClip(f'{overlay_img_path}').set_duration(small.duration)
            small =  small.set_position((-400, 420)) # Set position on screen 
            bg = bg.resize((1080,1920))        
            final_video = mp.CompositeVideoClip([bg, small]) # Overlay the small screen over the blurred background
            final_video.write_videofile(f'../match_clip/clips/{match_name}_{name}_out.mp4')
            final_video.close()
            files = glob.glob('../match_clip/clips/*_out.mp4')
            for f in files:
                print(f)
                shutil.move(f, '../VIDEOS/')
        else:
            bg = mp.VideoFileClip(f'../match_clip/clips/{name}_bg.mp4')
            small =  small.set_position((-400, 420)) # Set position on screen 
            bg = bg.resize((1080,1920))
            bg = bg.crop(x_center=540, y_center=960, width=1080, height=1920) # Potrait format
            final_video = mp.CompositeVideoClip([bg, small]) # Overlay the small screen over the blurred background
            final_video.write_videofile(f'../match_clip/clips/{match_name}_{name}_out.mp4')
            final_video.close()
            files = glob.glob('../match_clip/clips/*_out.mp4')
            for f in files:
                print(f)
                shutil.move(f, '../VIDEOS/')
            
    else: # If video is too short, simply remove the video 
        os.remove(input_file) 

