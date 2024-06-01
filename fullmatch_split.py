import os 
import moviepy.editor as mp
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import cv2 
import easyocr
from edit import make_video
import yt_dlp
from scenedetect import open_video, SceneManager, video_splitter, AdaptiveDetector
import glob 

download_status = {'complete': False}
reader = easyocr.Reader(['en'])

def postprocessor_hook(d): # For yt-dlp
    if d['status'] == 'finished':
        download_status['complete'] = True

def match_name(link):
    with yt_dlp.YoutubeDL() as ydl:
        info_dict = ydl.extract_info(link, download=False)
        return info_dict.get('title')
def download_match(link, download_dir):
    if os.path.isfile(f'{download_dir}/vid.webm'):
        print("Removing previous vid.webm")
        os.remove(f'{download_dir}/vid.webm')
    print("downloading match")
    ydl_opts = {
        'format': 'bestvideo[height=1080]+bestaudio/best',
        'outtmpl': f'{download_dir}/vid',
        'postprocessor_hooks': [postprocessor_hook],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(link)
    return download_status['complete']
    # Calling command from yt-dlp CLI - replaced with Python library 
    # command = f"yt-dlp -f 'bestvideo[height=1080]+bestaudio/best' -o 'match_clip/vid' --no-warnings {link} "
    # subprocess.call(command, shell=True)

def trim_video(download_dir, start_time, end_time):
    # Convert time to seconds
    h, m, s = map(int, start_time.split(':'))
    start_seconds = h * 3600 + m * 60 + s
    h, m, s = map(int, end_time.split(':'))
    end_seconds = h * 3600 + m * 60 + s
    # Calculating frames - replaced by extract_subclip
    #input_file = ffmpeg.input(f'{download_dir}/vid.webm')
    #fps = cv2.VideoCapture(f'{download_dir}/vid.webm').get(cv2.CAP_PROP_FPS)
    #output_file = ffmpeg.output(input_file.trim(start_frame=start_seconds * fps, end_frame=end_seconds * fps), f'{download_dir}/vid_out.webm')
    #ffmpeg.run(output_file)
    ffmpeg_extract_subclip(f'{download_dir}/vid.webm', start_seconds, end_seconds, targetname=f'{download_dir}/vid_out.webm')

    os.rename(f'{download_dir}/vid_out.webm', f'{download_dir}/vid.webm')


def scene_detect(download_dir):
    video = open_video(f'{download_dir}/vid.webm')
    if len(os.listdir(f'{download_dir}/clips/')) > 0: # If directory is not empty
        print("removing previous videos")
        files = glob.glob(f'{download_dir}/clips/*.mp4')
        for f in files:
            os.remove(f)
    scene_manager = SceneManager()
    scene_manager.add_detector(AdaptiveDetector()) # min_scene_len is in frames
    scene_manager.detect_scenes(video, show_progress=True, frame_skip=10)
    scenes = scene_manager.get_scene_list()
    video_splitter.split_video_ffmpeg(f'{download_dir}/vid.webm', scene_list=scenes, output_dir=f'{download_dir}/clips/', show_output=True, show_progress=True)

def delete_short_videos(folder_path, duration_min=8, duration_max=30):
    print("delete short videos")
    for filename in os.listdir(f'{folder_path}/clips/'):
        if filename.lower().endswith('.mp4'):
            video_path = os.path.join(f'{folder_path}/clips/', filename)
            video = mp.VideoFileClip(video_path)
            duration = video.duration # Check the duration of the video 
            video.close()
            if duration < duration_min or duration > duration_max:
                os.remove(video_path)
                print(f"Deleted {filename} (duration: {duration:.2f} seconds)")
    
    count = 0
    for filename in os.listdir(f'{folder_path}/clips/'):
        video = cv2.VideoCapture(f'{folder_path}/clips/{filename}')
        length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        video.set(1, (length/2))
        success,image = video.read()
        if success:
            cv2.imwrite("img/frame%d.jpg" % count, image)      
            result = reader.readtext(image)
            result = str(result).lower()
            print(result)
            keywords = ['clutch', 'ulutch', 'ace', 'replay', 'thrifty']
            contains_keywords = any(word in result for word in keywords)
            print(contains_keywords)
            if not contains_keywords:
                os.remove(f'{folder_path}/clips/{filename}')
            
            os.system('rm -rf img/*')
        
        count += 1
    
if __name__ == "__main__":
    #scene_detect('match_clip/')
    delete_short_videos('match_clip/')
    