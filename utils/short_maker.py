from moviepy.editor import VideoFileClip, concatenate_videoclips
from .reddit_scraper import download_reddit

import time, random, string, os


def short_maker(path_out, urls, resolution = (720, 1280)):
    vids = []
    duration = 0
    urls_used = []
    
    for url in urls:
        print(url)
        path_vid = 'content/videos/' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        download_reddit(url.replace('\n', ''), path_vid)
        time.sleep(1)
        
        try:
            video = VideoFileClip(path_vid+'.mp4')
            duration += video.duration
            if duration <= 60:
                urls_used.append(url)
                vids.append(video.resize(width = resolution[0]).set_pos('center'))
                
            else:
                print('\nSome videos could not be included as they exceed 60 seconds of video!\n')
                break
            
        except: pass
    
    compose = concatenate_videoclips(vids, method='compose').resize(resolution).set_pos('center')
    compose.write_videofile(path_out, fps=30, threads=80, codec="libx264")

    return urls_used