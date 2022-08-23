from youtube_dl import YoutubeDL
import datetime
import re

options = {
    'simulate': True,
    'noplaylist': True,
    'quiet': True,
}
url = 'https://www.youtube.com/watch?v=fs2zUYQN9QA'
pattern = re.compile(r'\d\d:\d\d:\d\d (.+)')

with YoutubeDL(options) as ydl:
    video = ydl.extract_info(url)
    value = video.get('description', None)
    names = pattern.findall(value)
    for name in names:
        video = ydl.extract_info(f'ytsearch1:{name}')['entries'][0]
        print('name', name)
        print('title', video.get('title'))
        print('artist', video.get('artist'))
        print('duration', datetime.timedelta(seconds=int(video.get('duration'))))
        print('url', f'https://youtube.com/watch?v={video.get("id")}')
        print()
