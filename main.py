from re import findall
from time import sleep

from requests import get

song_name = ""
song_lyric = ""
song_progress = 0
player_status = False


def get_song_info() -> tuple[str, int, int]:
    player = get("http://127.0.0.1:27232/player").json()
    m_song_name = player["currentTrack"]["name"]
    m_song_progress = player["progress"]
    m_song_id = player["currentTrack"]["id"]
    return m_song_name, m_song_progress, m_song_id


def get_song_lyrics(song_id: int) -> str:
    lyric = get(f"http://127.0.0.1:10754/lyric?id={song_id}").json()
    return lyric["lrc"]["lyric"]


def get_song_lyric(song_lyrics: str, song_progress: int) -> str:
    # 解析歌词字符串
    lyrics = findall(r'\[(\d+):(\d+\.\d+)](.*)', song_lyrics)
    current_lyric = ""

    for minute, second, lyric in lyrics:
        time_in_seconds = int(minute) * 60 + float(second)
        if time_in_seconds <= song_progress:
            current_lyric = lyric
        else:
            break

    return current_lyric


if __name__ == '__main__':
    player_status = True
    while True:
        song_name, now_song_progress, now_song_id = get_song_info()
        sleep(1)
        if song_progress == now_song_progress:
            print("No progress")
            player_status = False
            song_lyric = ""
            break
        song_progress = now_song_progress
        now_song_lyrics = get_song_lyrics(now_song_id)
        song_lyric = get_song_lyric(now_song_lyrics, now_song_progress)
        print(song_name)
        print(song_progress)
        print(song_lyric)
