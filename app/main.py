import eel
import os
import sys
import glob
import shutil
sys.path.append('../')
from fullmatch_split import download_match, scene_detect, match_name, trim_video, delete_short_videos, make_video

# Set web files folder
eel.init('web')
eel.browsers.set_path('electron', 'node_modules/electron/dist/electron')
@eel.expose 
def get_match_name(link):
    return match_name(link)
    

@eel.expose 
def get_match_link(link):
    print("match link is: " + link)
    out = download_match(link, '../match_clip/')
    if out:
        return "Download complete! <br>"

@eel.expose 
def get_video_parameters(start_time, end_time):
    trim_video('../match_clip/', start_time, end_time)
    return "Done trimming video!<br>"


@eel.expose
def detect_scenes(overlay, link): 
    print(overlay)
    scene_detect('../match_clip/')
    match_name = get_match_name(link)
    delete_short_videos('../match_clip/')
    count = 0
    for filename in os.listdir('../match_clip/clips/'):
        make_video(match_name, f'../match_clip/clips/{filename}', count, overlay=overlay)
        count += 1
    #upload_videos()
    
    return "Done detecting scenes! Videos can be found in VIDEOS folder"

'''
def upload_videos():
    if os.path.isfile('../TiktokAutoUploader/CookiesDir/tiktok_session-user.cookie'):
        print("Cookies exist")
        os.chdir('..')
        videos = glob.glob('match_clip/clips/*_out.mp4')
        for video in videos:
            print(video)
            shutil.copy(video, 'TiktokAutoUploader/VideosDirPath')
            os.chdir('TiktokAutoUploader/')
            os.system(f'python cli.py upload --user user -v "0_out.mp4" -t "VCT"')


@eel.expose
def tiktok_login():
    if os.path.isfile('../TiktokAutoUploader/CookiesDir/tiktok_session-user.cookie'):
        print("Already logged in!")
    else:
        os.chdir('../TiktokAutoUploader/')
        os.system('python cli.py login -n user')
'''
        
    

eel.start('hello.html',mode='electron')
#eel.start('hello.html', mode='custom', cmdline_args=['node_modules/electron/dist/electron.exe', '.'])
