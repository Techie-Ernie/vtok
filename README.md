# VTOK 1.0 
VTOK is a Python-based Electron app that can extract highlight reels from full VCT matches from any tournament (Masters, Champions, Regional Leagues, etc).

It takes 20 to 30 min to process one map (~40 mins in length).

## Installation
Ensure you have Python installed (this was tested on Python 3.10)


Clone this repository:

    git clone https://github.com/Techie-Ernie/vtok.git

Install required Python libraries:

    pip install -r requirements.txt

Run the program 
    
    cd vtok/app
    python main.py


## Directory Structure
    vtok
    ├── VIDEOS -> Final videos saved here
    ├── app -> Contains main.py, fullmatch_split.py and edit.py
    │   ├── node_modules
    │   └── web 
    ├── match_clip -> Full match is downloaded here
    │   └── clips -> Clips are processed in this folder
    └── overlays -> contains overlay.png which is used as a custom overlay
    



## How it works
**fullmatch_split.py** uses **pyscenedetect** to split the match into individual clips, then uses **OpenCV** to extract the middle frame of each clip, which is passed into **EasyOCR** to check for the presence of the word 'replay', 'clutch', or 'ace' in the frame. Valid videos are then passed into **edit.py** which converts them into a mobile-friendly video using **ffmpeg** and **Moviepy**.

## Sample Output
<video src="https://github.com/Techie-Ernie/vtok/assets/80609056/2a631b4b-0937-4345-b779-ef3e9d475390" width="320" height="480" controls></video>