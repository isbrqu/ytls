from youtube_dl import YoutubeDL
import re
import clipboard
import json

options = {
    'outtmpl': 'music/%(title)s-%(id)s.%(ext)s',
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
pattern = re.compile(r'(?:\d\d:)?\d\d:\d\d (.+)')
url_base = 'youtube.com/watch?v='
url = ''
while url_base not in url:
    url = clipboard.paste()
    print(url)
    msg = 'retry' if url_base not in url else 'continue'
    input(f'Press enter to {msg}')

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
    with open('videos.json', 'w') as file:
        json.dump(videos, file, indent=2)
    print('download...')
    ydl.params['simulate'] = False
    ydl.params['quiet'] = False
    for video in videos:
        print(video.get('id'), video.get('artist'), video.get('title'))
        url = f'{url_base}{video.get("id")}'
        ydl.download([url])

