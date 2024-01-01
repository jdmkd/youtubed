from django.http import HttpResponse
from django.shortcuts import redirect, render
import yt_dlp
import requests
import re
# Create your views here.

def index(request):
    return render(request,"ytd_app/index.html")

def download_videos(request):
    global context

    if request.method=="POST":
        video_url = request.POST["youtube_url"]
        regex = r'^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+'
        print(video_url)
        if not re.match(regex,video_url):
            return HttpResponse('Enter correct url.')
        # if 'm.' in video_url:
        #     video_url = video_url.replace(u'm.', u'')

        # elif 'youtu.be' in video_url:
        #     video_id = video_url.split('/')[-1]
        #     video_url = 'https://www.youtube.com/watch?v=' + video_id

        # if len(video_url.split("=")[-1]) < 11:
        #     return HttpResponse('Enter correct url.')

        ydl_opts = {}
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                meta = ydl.extract_info(video_url, download=False)
        except yt_dlp.DownloadError as e:
            print(f"Error extracting video information: {e}")
            return HttpResponse('Error extracting video information.')
        video_audio_streams = []

        for m in meta.get('formats', []):
            file_size = m.get('filesize')
            if file_size is not None:
                file_size = f'{round(int(file_size) / 1000000,2)} MB'

                resolution = 'Audio'
            
                if m.get('height') is not None:
                    resolution = f"{m.get('height')}x{m.get('width')}"

                video_audio_streams.append({
                    'resolution': resolution,
                    'extension': m['ext'],
                    'file_size': file_size,
                    'video_url': m['url'],
                    'acodec':m.get('acodec', ''),
                    'dcodec':m.get('dcodec', ''),
                    
                })

        video_audio_streams = video_audio_streams[::-1]

        duration_seconds = int(meta['duration'])
        duration_formatted = f'{duration_seconds // 60:02}:{duration_seconds % 60:02}'
        context = {
            'title': meta.get('title', ''), 
            'streams': video_audio_streams,
            'description': meta.get('description', ''), 
            'likes': meta.get('like_count', 0),
            'thumb': meta['thumbnails'][3]['url'] if len(meta.get('thumbnails', [])) > 3 else '',
            'duration': duration_formatted,
            'views': f'{int(meta.get("view_count", 0)):,}'
        }
        return render(request, 'ytd_app/index.html', context)

    return render(request, 'ytd_app/index.html', context)