from youtube_dl import YoutubeDL
import re
import csv

options = {
    'outtmpl': 'music/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'simulate': True,
    'noplaylist': True,
    'quiet': True,
    'writethumbnail': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }, {'key': 'EmbedThumbnail'},],
}
url = 'https://www.youtube.com/watch?v=fs2zUYQN9QA'
pattern = re.compile(r'\d\d:\d\d:\d\d (.+)')

with YoutubeDL(options) as ydl:
    video = ydl.extract_info(url)
    value = video.get('description', None)
    names = pattern.findall(value)
    videos = []
    for name in names:
        search = f'ytsearch1:{name}'
        video = ydl.extract_info(search)['entries'][0]
        print(video.get('id'), video.get('artist'), video.get('title'))
        videos.append({
            'id': video.get('id'),
            'artist': video.get('artist'),
            'title': video.get('title')
        })
        break
    print('download...')
    ydl.params['simulate'] = False
    ydl.params['quiet'] = False
    for video in videos:
        print(video.get('id'), video.get('artist'), video.get('title'))
        url = f'https://youtube.com/watch?v={video.get("id")}'
        ydl.download([url])

