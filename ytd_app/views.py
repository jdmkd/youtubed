import os
import platform
from django.shortcuts import redirect, render
from django.http import HttpResponse
from pytube import YouTube
import youtube_dl
import yt_dlp
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
from django.http import FileResponse
import mimetypes
import re
# Create your views here.

def index(request):
    return render(request,"ytd_app/index.html")

def download_videos(request):
    global context

    if request.method=="POST":
        video_url = request.POST["youtube_url"]
        # video_url='https://www.youtube.com/watch?v=V5En3Ks3OjE&pp=ygUEc29uZw%3D%3D'
        regex = r'^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+'
        # regex = (r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$\n")
        print(video_url)
        if not re.match(regex,video_url):
            print('nhi hoa')
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
        # print("")
        # print("value of meta ::::: ",type(meta),len(meta))
        # print("value of meta.keys() ::::: ",meta.keys())
        # print("")
        # print("value of id ::::: ",meta["id"])
        # print("value of title ::::: ",meta["title"])
        # print("value of formats ::::: ",meta["formats"])
        # print("value of thumbnails ::::: ",meta["thumbnails"])
        # print("value of channel_id ::::: ",meta["channel_id"])
        # print("value of channel_url ::::: ",meta["channel_url"])
        # print("value of duration ::::: ",meta["duration"])
        # print("value of webpage_url ::::: ",meta["webpage_url"])
        # print("value of _format_sort_fields ::::: ",meta["_format_sort_fields"])
        # print("value of uploader ::::: ",meta["uploader"])
        # print("value of uploader_id ::::: ",meta["uploader_id"])
        # print("value of uploader_url ::::: ",meta["uploader_url"])
        # print("value of availability ::::: ",meta["availability"])
        # print("value of original_url ::::: ",meta["original_url"])
        # print("value of webpage_url_basename ::::: ",meta["webpage_url_basename"])
        # print("value of webpage_url_domain ::::: ",meta["webpage_url_domain"])
        # print("value of extractor ::::: ",meta["extractor"])
        # print("value of display_id ::::: ",meta["display_id"])
        # print("value of fulltitle ::::: ",meta["fulltitle"])
        # print("value of duration_string ::::: ",meta["duration_string"])
        # print("value of _has_drm ::::: ",meta["_has_drm"])
        # print("value of epoch ::::: ",meta["epoch"])
        # print("value of requested_formats ::::: ",meta["requested_formats"])
        # print("value of format ::::: ",meta["format"])
        # print("value of format_id ::::: ",meta["format_id"])
        # print("value of protocol ::::: ",meta["protocol"])
        # print("value of ext ::::: ",meta["ext"])
        # print("value of filesize_approx ::::: ",meta["filesize_approx"])
        # print("value of format_note ::::: ",meta["format_note"])
        # print("value of tbr ::::: ",meta["tbr"])
        # print("value of width ::::: ",meta["width"])
        # print("value of height ::::: ",meta["height"])
        # print("value of resolution ::::: ",meta["resolution"])
        # print("value of dynamic_range ::::: ",meta["dynamic_range"])

        # print("")
        # print("value of format ::::: ",meta["format"])
        # print("value of format tyop ::::: ",type(meta["formats"]),len(meta["formats"]))
        # print("value of formats ::::: ",meta["formats"])
        # print("value of format 6 ::::: ",meta["format"][0])
        # print("")
        # print("filesize :: ",meta['filesize'])
        video_audio_streams = []

        for m in meta.get('formats', []):
            # print("m['dcodec'] :::",m.get('acodec'))

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
            # 'duration': round(int(meta['duration'])/60, 2), 
            'duration': duration_formatted,
            # 'views': f'{int(meta["view_count"]):,}'
            'views': f'{int(meta.get("view_count", 0)):,}'
        }
        return render(request, 'ytd_app/index.html', context)

    return render(request, 'ytd_app/index.html', context)


# def yt_url_info(request):
#     if request.method=="POST":
#         video_url = request.POST["youtube_url"]
#         # video_url='https://www.youtube.com/watch?v=V5En3Ks3OjE&pp=ygUEc29uZw%3D%3D'
#         print("video_url :",video_url)
#         try:
#             response = requests.get(video_url)
#             soup = BeautifulSoup(response.text, 'lxml')
#             meta = soup.find("meta", {"property": "og:image"})
#             print("meta :::",meta)
            
#             yt = YouTube(video_url)
#             all_streams = yt.streams.all()
#             all_streams_data = []
#             parsed_url = urlparse(video_url)
#             query_parameters = parse_qs(parsed_url.query)
#             # Get the video ID
#             video_id = query_parameters.get("v", [])[0]
#             print("video_id :::",video_id)
#             for stream in all_streams:
#                 all_streams_data.append(stream)
#                 print(f"itag : {stream.itag}, Resolution: {stream.resolution}, length :{yt.length}, Type: {stream.mime_type}, Video Codec: {stream.video_codec}, Audio Codec: {stream.audio_codec}, Filesize: {stream.filesize}")

#             if meta or all_streams_data:
#                 thumbnail_url = meta["content"]
#                 itag_data = [stream.itag for stream in all_streams_data]
#                 print("itag_data : ::: :",itag_data)
#                 print("itag_data type : ::: :",type(itag_data))
#                 return render(request,"ytd_app/index.html",{"all_streams":all_streams_data,"yt":yt,"thumbnail_url":thumbnail_url,"video_id":video_id})
#             else:
#                 return None
            
#         except Exception as e:
#             print(f"Errorx: {str(e)}")
#     else:
#         print("Error")  
#     return render(request,"ytd_app/index.html")


# def download_file_system_handling(request, video_url, video_itag):
# def download_file_system_handling(request,video_stream):
#     try:
#         # Replace with the actual path to the downloaded video
        
#         # print("video_stream.download(output_path=download_path) ::",video_stream.download(output_path=download_path))
#         print("video_stream.default_filename :",video_stream.default_filename)
#         if platform.system() == "Windows":
#             download_path = os.path.expanduser("~\\Downloads")
#         else:
#             download_path = os.path.expanduser("~/Downloads")
#         os.makedirs(download_path, exist_ok=True)
#         # video_stream.download(output_path=download_path)
#         video_path = os.path.join(download_path, video_stream.default_filename)
        
#         print("video_path ::",video_path)
#         # # Get the video file's name
#         # video_filename = os.path.basename(video_path)
#         # print("video_filename :",video_filename)
#         # # Set the Content-Disposition header to force download
#         # response = FileResponse(open(video_path, 'rb'))
#         # content_type, encoding = mimetypes.guess_type(video_path)
#         # response['Content-Type'] = content_type
#         # response['Content-Length'] = os.path.getsize(video_path)
#         # response['Content-Disposition'] = f'attachment; filename="{video_filename}"'
#         # print("response ::",response)
#         # return render(request,"ytd_app/index.html",{'video_path':video_path})
#         return video_path
    
#     except Exception as e:
#         return HttpResponse(f"Errorz: {str(e)}")