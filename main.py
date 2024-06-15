from moviepy.editor import VideoFileClip
from pymediainfo import MediaInfo

def check_file_integrity(file_path):
    try:
        # Essayer de charger le fichier vidéo avec moviepy
        clip = VideoFileClip(file_path)
        duration = clip.duration
        print(f"{file_path} is not corrupted. Duration: {duration} seconds.")
        clip.reader.close()
        clip.audio.reader.close_proc()
    except Exception as e:
        # Afficher les erreurs
        print(f"Error processing {file_path}: {e}")

def get_file_info(file_path):
    media_info = MediaInfo.parse(file_path)
    print(f"File information for {file_path}:")
    for track in media_info.tracks:
        if track.track_type == 'Video':
            print(f"  - Codec: {track.codec}")
            print(f"  - Duration: {track.duration} ms")
            print(f"  - Width: {track.width} pixels")
            print(f"  - Height: {track.height} pixels")
            print(f"  - Frame rate: {track.frame_rate} fps")
        elif track.track_type == 'Audio':
            print(f"  - Audio codec: {track.codec}")
            print(f"  - Channels: {track.channel_s}")
            print(f"  - Sample rate: {track.sampling_rate} Hz")

def main():
    # Exemple d'utilisation
    file_path = input("Enter the path to the video file: ")

    # Vérifier l'intégrité du fichier
    check_file_integrity(file_path)

    # Obtenir des informations détaillées sur le fichier
    get_file_info(file_path)

    return True

if __name__ == '__main__':
    if main():
        exit(0)
    else:
        exit(1)
