from flask import flash, redirect, url_for
import re
import requests
import wget
import os
import subprocess


def download_video(url):
    directory = os.path.join(os.path.dirname(__file__), 'Videos')

    try:
        html = requests.get(url)
    except requests.exceptions.RequestException:
        flash('Please Enter a Valid URL', 'active')
        return redirect(url_for('facebook.home'))

    try:
        HD = re.search('hd_src:"(.+?)"', html.text)[1]
        HDurl = HD.replace('hd_src:"','')
    except TypeError:
        return get_sd(html, directory)
    else:
        wget.download(HDurl, directory)

    return directory


def get_sd(html, directory):
    try:
        SD = re.search('sd_src:"(.+?)"', html.text)[1]
        SDurl = SD.replace('sd_src:"','')
    except TypeError:
        flash('Cannot Download a video from a closed group Sorry...', 'active')
        return redirect(url_for('facebook.home'))
    else:
        wget.download(SDurl, directory)


def convert(directory, filename):
    path = os.path.join(directory, filename)
    output = os.path.join(os.path.dirname(__file__), 'Audio', filename.replace('mp4', 'mp3'))

    cmd = f'ffmpeg -i "{path}" "{output}"'
    subprocess.run(cmd, shell=True) # running the command
    
    os.remove(path)
    return output

def get_filename(directory):
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        return filename
