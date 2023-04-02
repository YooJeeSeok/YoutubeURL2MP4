## A project that converts YouTube URL to mp3(voices) files.
## 임시 주석 부분 모두 업데이트 필요

import yt_dlp
import os, shutil
import sys
import argparse
import time
from urllib.parse import urlparse

## 설치 확안
# 유튜브 URL 및 음성파일 경로 변수 선언
YOUTUBE_URL = '' # YOUTUBE_URL 저장 위치
FOLDER_PATH = '' # mp3 저장 위치


ydl_opts = {
    'outtmpl': "",
    'format' : 'bestaudio/best',
    'noplaylist' : True,
    'continue_dl' : True,
    'postprocessors' : [{
        'key':'FFmpegExtractAudio',
        'preferredcodec':'mp3',
        'preferredquality':'192',
    }],
}


def check_yt_url(arg):
    url = urlparse(arg)
    if all((url.scheme, url.netloc)):  # possibly other sections?
        if url.netloc in ("youtu.be", "youtube.com", "www.youtube.com"):
            return arg # return url in case you need the parsed object

        raise Exception("not a youtube url.")
    raise argparse.ArgumentTypeError('Invalid URL')


def get_yt_id(url:urlparse):
    yt_query = url.query
    if 'v=' in yt_query:
        return yt_query[2:].split('&')[0]
    else:
        return url.path.split('/')[-1]


if __name__ == "__main__":
    # url 파라미터 가져오기 및 youtube url 검사
    parser = argparse.ArgumentParser(description="argv options list")
    parser.add_argument(
        "-u",
        "--url",
        type=check_yt_url,
        help="foobar",
    )

    # 임시
    p_url = parser.parse_args().url
    print("args : ", p_url)

    if p_url is None:
        p_url = "https://youtube.com/watch?v=vGQmdhqlCb0&feature=share"
        # raise Exception("youtube link does not exist in argv")

    yt_url = urlparse(p_url)
    yt_id = get_yt_id(yt_url)

    ydl_opts['outtmpl'] = os.path.join(FOLDER_PATH, f"yt_{yt_id}")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.cache.remove()
        filenames = [p_url]

        ydl.download(filenames)

        print('complete')

