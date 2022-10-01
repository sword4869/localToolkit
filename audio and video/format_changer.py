"""
pip install ffmpeg
"""

import subprocess 
source_file = r'/home/sword/Downloads/obama.flv'
dest_file = r'/home/sword/Downloads/obama.mp4'

def run(cmd):
    subprocess.run(cmd, shell=True)

cmd = f"ffmpeg -i {source_file} -strict -2 {dest_file}"
run(cmd)