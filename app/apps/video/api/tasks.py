import os
import subprocess


def convert_480p(source, video_id):
    output_dir = f"/app/media/videos/{video_id}/480p"
    os.makedirs(output_dir, exist_ok=True)
    target = f"{output_dir}/index.m3u8"
    cmd = f'/usr/bin/ffmpeg -i "{source}" -vf scale=854:480 -hls_time 10 -hls_playlist_type vod "{target}"'
    subprocess.run(cmd, shell=True)


def convert_720p(source, video_id):
    output_dir = f"/app/media/videos/{video_id}/720p"
    os.makedirs(output_dir, exist_ok=True)
    target = f"{output_dir}/index.m3u8"
    cmd = f'/usr/bin/ffmpeg -i "{source}" -vf scale=1280:720 -hls_time 10 -hls_playlist_type vod "{target}"'
    subprocess.run(cmd, shell=True)


def convert_1080p(source, video_id):
    output_dir = f"/app/media/videos/{video_id}/1080p"
    os.makedirs(output_dir, exist_ok=True)
    target = f"{output_dir}/index.m3u8"
    cmd = f'/usr/bin/ffmpeg -i "{source}" -vf scale=1920:1080 -hls_time 10 -hls_playlist_type vod "{target}"'
    subprocess.run(cmd, shell=True)
