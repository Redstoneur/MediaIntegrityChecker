# MediaIntegrityChecker

**MediaIntegrityChecker** est un outil Python permettant de vérifier l'intégrité des fichiers multimédias et d'obtenir des informations détaillées sur les fichiers vidéo et audio. Il combine les bibliothèques `ffmpeg-python` et `pymediainfo` pour fournir une solution complète pour l'analyse des fichiers multimédias.

## Fonctionnalités

- Vérifie si les fichiers multimédias sont corrompus en utilisant `ffmpeg-python`.
- Extrait des informations détaillées sur les fichiers multimédias, telles que le codec, la durée, les dimensions, et le taux de rafraîchissement en utilisant `pymediainfo`.
- Compatible avec une variété de formats de fichiers multimédias, y compris `.avi`, `.mp4`, et plus.

## Installation

1. Installez FFmpeg sur votre système en suivant les instructions sur [FFmpeg.org](https://ffmpeg.org/download.html).

2. Installez les dépendances Python :

```sh
pip install ffmpeg-python pymediainfo
```

## Utilisation

1. Clonez le dépôt :

```sh
git clone https://github.com/votre-utilisateur/MediaIntegrityChecker.git
cd MediaIntegrityChecker
```

## Licence
