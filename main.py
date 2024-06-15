import argparse
from enum import Enum
from typing import Optional

from moviepy.editor import VideoFileClip
from pymediainfo import MediaInfo


class VideoType(Enum):
    MP4 = 1
    AVI = 2
    MOV = 3
    WMV = 4
    MKV = 5
    FLV = 6
    WEBM = 7
    OTHER = 8

    def __str__(self):
        if self == VideoType.MP4:
            return 'MP4'
        elif self == VideoType.AVI:
            return 'AVI'
        elif self == VideoType.MOV:
            return 'MOV'
        elif self == VideoType.WMV:
            return 'WMV'
        elif self == VideoType.MKV:
            return 'MKV'
        elif self == VideoType.FLV:
            return 'FLV'
        elif self == VideoType.WEBM:
            return 'WEBM'
        else:
            return 'OTHER'

    @staticmethod
    def get_type(path: str) -> "VideoType":
        if path.endswith('.mp4'):
            return VideoType.MP4
        elif path.endswith('.avi'):
            return VideoType.AVI
        elif path.endswith('.mov'):
            return VideoType.MOV
        elif path.endswith('.wmv'):
            return VideoType.WMV
        elif path.endswith('.mkv'):
            return VideoType.MKV
        elif path.endswith('.flv'):
            return VideoType.FLV
        elif path.endswith('.webm'):
            return VideoType.WEBM
        else:
            return VideoType.OTHER


class VideoInfo:
    codec: str
    duration: int
    width: int
    height: int
    frame_rate: float
    audio_codec: str
    audio_channels: int
    audio_sample_rate: int

    def __init__(self, codec: str, duration: int, width: int, height: int, frame_rate: float, audio_codec: str = "",
                 audio_channels: int = 0, audio_sample_rate: int = 0):
        self.codec = codec
        self.duration = duration
        self.width = width
        self.height = height
        self.frame_rate = frame_rate
        self.audio_codec = audio_codec
        self.audio_channels = audio_channels
        self.audio_sample_rate = audio_sample_rate

    def __str__(self):
        return (f"Codec: {self.codec}\nDuration: {self.duration} ms\nWidth: {self.width} pixels\n"
                f"Height: {self.height} pixels\nFrame rate: {self.frame_rate} fps\n"
                f"Audio codec: {self.audio_codec}\nAudio channels: {self.audio_channels}\n"
                f"Audio sample rate: {self.audio_sample_rate} Hz")

    def __repr__(self):
        return (f"VideoInfo(codec={self.codec}, duration={self.duration}, width={self.width}, height={self.height},"
                f" frame_rate={self.frame_rate}, audio_codec={self.audio_codec}, audio_channels={self.audio_channels},"
                f" audio_sample_rate={self.audio_sample_rate})")

    def __dict__(self) -> dict:
        return {
            'codec': self.codec,
            'duration': self.duration,
            'width': self.width,
            'height': self.height,
            'frame_rate': self.frame_rate,
            'audio_codec': self.audio_codec,
            'audio_channels': self.audio_channels,
            'audio_sample_rate': self.audio_sample_rate
        }


class VideoFile:
    type: VideoType
    path: str
    Name: str

    def __init__(self, path: str):
        self.path = path
        self.Name = path.split('/')[-1]
        self.type = VideoType.get_type(path)

    def __str__(self):
        return f"{self.Name} ({self.type})"

    def check_file_integrity(self) -> int:
        # Essayer de charger le fichier vidéo avec moviepy
        try:
            clip: VideoFileClip = VideoFileClip(self.path)
            duration: int = clip.duration
            clip.reader.close()
            clip.audio.reader.close_proc()
            return duration
        except Exception as e:
            raise e

    def get_file_info(self) -> VideoInfo:
        # Obtenir les informations du fichier vidéo avec pymediainfo
        try:
            media_info: MediaInfo = MediaInfo.parse(self.path)
            file_info: VideoInfo = VideoInfo("", 0, 0, 0, 0, "", 0, 0)
            for track in media_info.tracks:
                if track.track_type == 'Video':
                    file_info.codec = track.codec
                    file_info.duration = int(track.duration)
                    file_info.width = track.width
                    file_info.height = track.height
                    file_info.frame_rate = track.frame_rate
                elif track.track_type == 'Audio':
                    file_info.audio_codec = track.codec
                    file_info.audio_channels = track.channel_s
                    file_info.audio_sample_rate = track.sampling_rate
            return file_info
        except Exception as e:
            raise e

    def check_get_file_info(self) -> Optional[VideoInfo]:

        # Vérifier l'intégrité du fichier
        try:
            duration: int = self.check_file_integrity()
            if duration is None:
                raise Exception(f"Error processing {self.Name}, file integrity check failed")
        except Exception as e:
            raise Exception(f"Error processing {self.Name}, file integrity check failed :\n{e}")

        # Obtenir les informations du fichier
        try:
            file_info: VideoInfo = self.get_file_info()
        except Exception as e:
            raise Exception(f"Error processing {self.Name}, file information retrieval failed:\n{e}")

        return file_info

    def check_get_file_info_fast(self) -> bool:
        try:
            file_info = self.check_get_file_info()
            return file_info is not None
        except Exception as e:
            print(e)
            return False

    def check_get_file_info_verbose(self) -> bool:
        # Vérifier l'intégrité du fichier
        try:
            duration = self.check_file_integrity()
        except Exception as e:
            print(f"Error processing {self.Name}:\n{e}")
            return False

        print(f"File {self.Name} is OK, duration: {duration} seconds")

        # Obtenir les informations du fichier
        try:
            file_info = self.get_file_info()
        except Exception as e:
            print(f"Error processing {self.Name}:\n{e}")
            return False

        print(f"File information for {self.Name}:")
        print(f"  - Codec: {file_info.codec}")
        print(f"  - Duration: {file_info.duration} ms")
        print(f"  - Width: {file_info.width} pixels")
        print(f"  - Height: {file_info.height} pixels")
        print(f"  - Frame rate: {file_info.frame_rate} fps")
        print(f"  - Audio codec: {file_info.audio_codec}")
        print(f"  - Audio channels: {file_info.audio_channels}")
        print(f"  - Audio sample rate: {file_info.audio_sample_rate} Hz")

        return True


def main():
    Name = "MediaIntegrityChecker"
    Version = "1.0.0"
    Description = "A simple tool to check the integrity of video files and get their information"

    # Créer un analyseur d'arguments
    parser = argparse.ArgumentParser(prog=Name, description=Description)
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {Version}')
    parser.add_argument('-f', '--file_path', type=str, help='Path to the video file')

    # Analyser les arguments
    args = parser.parse_args()

    # Extraire les arguments
    file_path: str = args.file_path

    if file_path is None:
        file_path = input("Enter the path to the video file: ")

    # Créer un objet VideoFile
    video_file = VideoFile(file_path)

    return video_file.check_get_file_info_verbose()


if __name__ == '__main__':
    if main():
        exit(0)
    else:
        exit(1)
