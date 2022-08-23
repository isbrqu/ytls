from youtube_dl import YoutubeDL

options = {
    'simulate': True,
}
url = 'https://www.youtube.com/watch?v=fs2zUYQN9QA'
with YoutubeDL(options) as ydl:
    video = ydl.extract_info(url)
    value = video.get('description', None)
    print(value)
