from youtube_dl import YoutubeDL
import re
import clipboard
import json
import os

options = {
    'simulate': True,
    'noplaylist': True,
    'quiet': True,
    'writethumbnail': True,
    'format': 'mp4',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }, {'key': 'EmbedThumbnail'},],
}
pattern = re.compile(r'(?:\d\d:)?\d\d:\d\d (.+)')
url = ''
url_base = 'https://youtube.com/watch?v='
while url_base not in url:
    url = clipboard.paste()
    print(url)
    msg = 'retry' if url_base not in url else 'continue'
    input(f'Press enter to {msg}')

with YoutubeDL(options) as ydl:
    source = ydl.extract_info(url)
    source_id = source.get("id")
    folder_name = f'music-{source_id}'
    file_name = f'{folder_name}/videos-{source_id}.json'
    ydl.params['outtmpl'] = f'{folder_name}/%(title)s-%(id)s.%(ext)s'
    os.makedirs(folder_name, exist_ok=True)
    if not os.path.exists(file_name):
        try:
            source_description = source.get('description', None)
            names = pattern.findall(source_description)
            videos = []
            for name in names:
                search = f'ytsearch1:{name}'
                vid = ydl.extract_info(search)['entries'][0]
                vid = {key: vid.get(key) for key in ['id', 'artist', 'title']}
                vid['downloaded'] = False
                print(vid)
                videos.append(vid)
        finally:
            with open(file_name, 'w') as file:
                json.dump(videos, file, indent=2)
    try:
        with open(file_name, 'r') as file:
            videos = json.load(file)
        ydl.params['simulate'] = False
        ydl.params['quiet'] = False
        for video in videos:
            if not video.get('downloaded'):
                print(video)
                url = f'{url_base}{video.get("id")}'
                ydl.download([url])
                video['downloaded'] = True
            else:
                print(video, 'ready!')
    except Exception as exception:
        raise exception
    finally:
        with open(file_name, 'w') as file:
            json.dump(videos, file, indent=2)

