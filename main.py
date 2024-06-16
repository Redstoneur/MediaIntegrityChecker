########################################################################################################################
### IMPORTS ############################################################################################################
########################################################################################################################

import argparse
import os
from enum import Enum
from typing import Optional, List, TypedDict

from moviepy.editor import VideoFileClip
from pymediainfo import MediaInfo


########################################################################################################################
### CLASSES ############################################################################################################
########################################################################################################################

class Status(Enum):
    """
    Enumération des statuts de l'intégrité des fichiers vidéo

    OK : Intégrité OK
    ERROR : Erreur d'intégrité
    """
    OK = 1
    ERROR = 2

    def __str__(self) -> str:
        """
        Convertir l'objet en chaîne de caractères

        :return: str
        """
        if self == Status.OK:
            return 'OK'
        else:
            return 'ERROR'


class VideoType(Enum):
    """
    Enumération des types de fichiers vidéo

    MP4: MPEG-4 Part 14
    AVI: Audio Video Interleave
    MOV: QuickTime Movie
    WMV: Windows Media Video
    MKV: Matroska Multimedia Container
    FLV: Flash Video
    WEBM: WebM
    OTHER: Autre
    """
    MP4 = 1
    AVI = 2
    MOV = 3
    WMV = 4
    MKV = 5
    FLV = 6
    WEBM = 7
    OTHER = 8

    def __str__(self) -> str:
        """
        Convertir l'objet en chaîne de caractères

        :return: str
        """
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
        """
        Obtenir le type de fichier vidéo à partir du chemin

        :param path: str
        :return: VideoType
        """
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


class VideoFileInfo(TypedDict):
    """
    Informations sur un fichier vidéo

    codec : str - Codec vidéo
    duration : int - Durée de la vidéo en millisecondes
    width : int - Largeur de la vidéo en pixels
    height : int - Hauteur de la vidéo en pixels
    frame_rate : float - Fréquence d'images de la vidéo en images par seconde
    audio_codec : str - Codec audio
    audio_channels : int - Nombre de canaux audio
    audio_sample_rate : int - Fréquence d'échantillonnage audio en Hertz
    """
    codec: str
    duration: int
    width: int
    height: int
    frame_rate: float
    audio_codec: str
    audio_channels: int
    audio_sample_rate: int


class VideoFileIntegrity(TypedDict):
    """
    Résultats de l'intégrité des fichiers vidéo dans un dossier

    status : str - Statut de l'intégrité
    duration : int - Durée de la vidéo en millisecondes
    error : str - Message d'erreur
    """
    status: Status
    duration: int
    error: str


class VideoFileInfoIntegrity(TypedDict):
    """
    Résultats de l'intégrité des fichiers vidéo dans un dossier

    integrity: VideoFolderIntegrity
    info: VideoInfo
    """
    integrity: VideoFileIntegrity
    info: Optional[VideoFileInfo]


class VideoFileIntegrityFast(TypedDict):
    """
    Résultats de l'intégrité des fichiers vidéo dans un dossier

    status : str - Statut de l'intégrité
    error : str - Message d'erreur
    """
    status: Status
    error: str


class VideoFile:
    """
    Fichier vidéo

    type: VideoType - Type de fichier vidéo
    path: str - Chemin du fichier vidéo
    Name: str - Nom du fichier vidéo
    """
    type: VideoType
    path: str
    Name: str

    def __init__(self, path: str):
        """
        Initialiser un fichier vidéo

        :param path: str - Chemin du fichier vidéo
        """
        self.path = path.replace('\\', '/')

        self.Name = self.path.split('/')[-1]
        self.type = VideoType.get_type(self.path)

    def __str__(self) -> str:
        """
        Convertir l'objet en chaîne de caractères

        :return: str
        """
        return f"{self.Name} ({self.type})"

    def check_file_integrity(self) -> int:
        """
        Vérifier l'intégrité du fichier vidéo

        :return: int - Durée de la vidéo en secondes
        """
        # Essayer de charger le fichier vidéo avec moviepy
        try:
            clip: VideoFileClip = VideoFileClip(self.path)
            duration: int = clip.duration
            clip.reader.close()
            clip.audio.reader.close_proc()
            return duration  # Retourner la durée de la vidéo en secondes
        except Exception as e:
            raise e

    def get_file_info(self) -> VideoFileInfo:
        """
        Obtenir les informations du fichier vidéo

        :return: VideoFileInfo - Informations du fichier vidéo
        """
        # Obtenir les informations du fichier vidéo avec pymediainfo
        try:
            media_info: MediaInfo = MediaInfo.parse(self.path)
            file_info: VideoFileInfo = {
                'codec': '',
                'duration': 0,
                'width': 0,
                'height': 0,
                'frame_rate': 0.0,
                'audio_codec': '',
                'audio_channels': 0,
                'audio_sample_rate': 0
            }
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

    def check_get_file_info(self) -> VideoFileInfoIntegrity:
        """
        Vérifier l'intégrité du fichier et obtenir ses informations

        :return: VideoFileInfoIntegrity - Informations du fichier vidéo
        """
        file_info: VideoFileInfoIntegrity = {
            'integrity': None,
            'info': None
        }

        # Vérifier l'intégrité du fichier
        try:
            duration: int = self.check_file_integrity()
            if duration is None:
                raise Exception(f"Error processing {self.Name}, file integrity check failed")
            file_info['integrity']: VideoFileIntegrity = {"status": Status.OK, "duration": duration, "error": ""}
        except Exception as e:
            file_info['integrity']: VideoFileIntegrity = {"status": Status.ERROR, "duration": 0, "error": str(e)}

        # Obtenir les informations du fichier
        # noinspection PyBroadException
        try:
            file_info['info']: VideoFileInfo = self.get_file_info()
        except Exception:
            file_info['info']: VideoFileInfo = None

        return file_info

    def check_get_file_info_fast(self) -> VideoFileIntegrityFast:
        """
        Vérifier l'intégrité du fichier et obtenir ses informations rapidement

        :return: VideoFileIntegrityFast - Informations du fichier vidéo
        """
        try:
            file_info = self.check_get_file_info()
            if file_info['integrity']['status'] == Status.ERROR:
                return {"status": Status.ERROR, "error": file_info['integrity']['error']}
        except Exception as e:
            return {"status": Status.ERROR, "error": str(e)}

    def check_get_file_info_verbose(self, named: bool = False) -> bool:
        """
        Vérifier l'intégrité du fichier et obtenir ses informations de manière détaillée avec du texte

        :param named: bool - True pour afficher le nom du fichier, False sinon
        :return: bool - True si le traitement a réussi, False sinon
        """
        if named:
            print(f"Processing {self.path} ...")

        # Vérifier l'intégrité du fichier et obtenir ses informations
        info_file: VideoFileInfoIntegrity = self.check_get_file_info()
        if info_file['integrity']['status'] == Status.ERROR:
            print(f"Error processing {self.Name}:\n{info_file['integrity']['error']}")
            return False

        print(f"File {self.Name} is OK, duration: {info_file['integrity']['duration']} seconds")

        if info_file['info'] is None:
            print(f"Error processing {self.Name}, could not get file information")
            return True

        print(f"File information for {self.Name}:")
        print(f"  - Codec: {info_file['info']['codec']}")
        print(f"  - Duration: {info_file['info']['duration']} ms")
        print(f"  - Width: {info_file['info']['width']} pixels")
        print(f"  - Height: {info_file['info']['height']} pixels")
        print(f"  - Frame rate: {info_file['info']['frame_rate']} fps")
        print(f"  - Audio codec: {info_file['info']['audio_codec']}")
        print(f"  - Audio channels: {info_file['info']['audio_channels']}")
        print(f"  - Audio sample rate: {info_file['info']['audio_sample_rate']} Hz")
        return True


class VideoFileInfoIntegrityFolder(TypedDict):
    """
    Résultats de l'intégrité des fichiers vidéo dans un dossier

    name : str - Nom du fichier vidéo
    integrity : VideoFolderIntegrity
    info : List[VideoInfo]
    """
    name: str
    integrity: VideoFileIntegrity
    info: VideoFileInfo


class VideoFileIntegrityFastFolder(TypedDict):
    """
    Résultats de l'intégrité des fichiers vidéo dans un dossier

    name : str - Nom du fichier vidéo
    file_status : VideoFileIntegrityFast - Statut de l'intégrité du fichier
    """
    name: str
    status: VideoFileIntegrityFast


class VideoFolder:
    """
    Dossier contenant des fichiers vidéo

    path : str - Chemin du dossier
    files : List[VideoFile] - Liste des fichiers vidéo
    """
    path: str
    files: List[VideoFile]

    def __init__(self, path: str):
        """
        Initialiser un dossier contenant des fichiers vidéo

        :param path: str - Chemin du dossier
        """
        self.path = path.replace('\\', '/')

        self.find_files()

    def add_file(self, file: VideoFile) -> None:
        """
        Ajouter un fichier vidéo au dossier

        :param file: VideoFile - Fichier vidéo
        :return: None
        """
        self.files.append(file)

    def find_files(self) -> None:
        """
        Trouver les fichiers vidéo dans le dossier

        :return: None
        """
        self.files = []
        files = VideoFolder.get_files(self.path)
        for file in files:
            if VideoType.get_type(file) != VideoType.OTHER:
                self.add_file(VideoFile(file))

    def get_files_count(self) -> int:
        """
        Obtenir le nombre de fichiers vidéo dans le dossier

        :return: int - Nombre de fichiers vidéo
        """
        return len(self.files)

    def check_files_integrity(self) -> {str: VideoFileIntegrity}:
        """
        Vérifier l'intégrité des fichiers vidéo dans le dossier

        :return: {str : VideoFileIntegrity} - Résultats de l'intégrité des fichiers vidéo
        """
        results = {}
        for file in self.files:
            try:
                duration = file.check_file_integrity()
                results[file.Name]: VideoFileIntegrity = {"status": "OK", "duration": duration, "error": ""}
            except Exception as e:
                results[file.Name]: VideoFileIntegrity = {"status": "Error", "duration": 0, "error": str(e)}
        return results

    def get_files_info(self) -> {str: VideoFileInfo}:
        """
        Obtenir les informations des fichiers vidéo dans le dossier

        :return: {str : VideoFileInfo} - Informations des fichiers vidéo
        """
        files_info: {str: VideoFileInfo} = {}
        for file in self.files:
            # noinspection PyBroadException
            try:
                files_info[file.Name] = file.get_file_info()
            except Exception:
                files_info[file.Name] = None
        return files_info

    def check_get_files_info(self) -> List[VideoFileInfoIntegrityFolder]:
        """
        Vérifier l'intégrité des fichiers et obtenir leurs informations

        :return: List[VideoFileInfoIntegrityFolder] - Informations des fichiers vidéo
        """
        # noinspection PyTypeChecker
        files_info: List[VideoFileInfoIntegrityFolder] = []
        for file in self.files:
            try:
                file_info = file.check_get_file_info()
                files_info.append(
                    {"name": file.Name, "integrity": file_info['integrity'], "info": file_info['info']}
                )
            except Exception as e:
                print(f"Error processing {file.Name}:\n{e}")
        return files_info

    def check_get_files_info_fast(self) -> List[VideoFileIntegrityFastFolder]:
        """
        Vérifier l'intégrité des fichiers et obtenir leurs informations rapidement

        :return: List[VideoFolderIntegrityFast] - Informations des fichiers vidéo
        """
        files_status: List[VideoFileIntegrityFastFolder] = []
        for file in self.files:
            file_status = file.check_get_file_info_fast()
            files_status.append({"name": file.Name, "status": file_status})
        return files_status

    def check_get_files_info_verbose(self, named: bool = False) -> bool:
        """
        Vérifier l'intégrité des fichiers et obtenir leurs informations de manière détaillée avec du texte

        :param named: bool - True pour afficher le nom du fichier, False sinon
        :return: bool - True si le traitement a réussi, False sinon
        """
        if named:
            print(f"Processing {self.path} [{self.get_files_count()} files] ...")
        for file in self.files:
            if not file.check_get_file_info_verbose(named=True):
                return False
        return True

    @staticmethod
    def get_files(path: str) -> list:
        """
        Obtenir la liste des fichiers dans un dossier

        :param path: str - Chemin du dossier
        :return: list - Liste des fichiers
        """
        path = path.replace('\\', '/')
        if not path.endswith('/'):
            path += '/'
        # Récupérer la liste des fichiers dans le dossier
        listdir: list = [path + e for e in os.listdir(path)]
        files: list = []
        for e in listdir:
            if os.path.isdir(e):
                files += VideoFolder.get_files(e)
            elif os.path.isfile(e):
                files.append(e)
        return files


########################################################################################################################
### MAIN ###############################################################################################################
########################################################################################################################

def main() -> bool:
    """
    Fonction principale

    :return: bool - True si le traitement a réussi, False sinon
    """
    name: str = "MediaIntegrityChecker"
    version: str = "1.2.0"
    description: str = "A simple tool to check the integrity of video files and get their information"

    # Créer un analyseur d'arguments
    parser = argparse.ArgumentParser(prog=name, description=description)
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {version}')
    parser.add_argument('-p', '--path', type=str, help='Path to the video file or folder')

    # Analyser les arguments
    args = parser.parse_args()

    # Extraire les arguments
    path = args.path

    auto: bool = True
    if path is None:
        auto = False
        path = input("Enter the path to the video file or folder: ")

    if not os.path.exists(path):
        print(f"Error: {path} does not exist")
        return False

    if os.path.isfile(path):
        if VideoType.get_type(path) == VideoType.OTHER:
            print(f"Error: {path} is not a video file")
            return False

        # Créer un objet VideoFile
        video_file = VideoFile(path)
        return video_file.check_get_file_info_verbose(named=auto)

    if os.path.isdir(path):
        # Créer un objet VideoFolder
        video_folder = VideoFolder(path)
        return video_folder.check_get_files_info_verbose(named=auto)


########################################################################################################################
### EXECUTION ##########################################################################################################
########################################################################################################################

if __name__ == '__main__':
    # Exécuter la fonction principale
    if main():
        exit(0)
    else:
        exit(1)
