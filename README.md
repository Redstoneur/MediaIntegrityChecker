# MediaIntegrityChecker

---

![License](https://img.shields.io/github/license/Redstoneur/MediaIntegrityChecker)
![Top Language](https://img.shields.io/github/languages/top/Redstoneur/MediaIntegrityChecker)
![Python Version](https://img.shields.io/badge/python-3.8-blue)
![Size](https://img.shields.io/github/repo-size/Redstoneur/MediaIntegrityChecker)
![Contributors](https://img.shields.io/github/contributors/Redstoneur/MediaIntegrityChecker)
![Last Commit](https://img.shields.io/github/last-commit/Redstoneur/MediaIntegrityChecker)
![Issues](https://img.shields.io/github/issues/Redstoneur/MediaIntegrityChecker)
![Pull Requests](https://img.shields.io/github/issues-pr/Redstoneur/MediaIntegrityChecker)

---

![Forks](https://img.shields.io/github/forks/Redstoneur/MediaIntegrityChecker)
![Stars](https://img.shields.io/github/stars/Redstoneur/MediaIntegrityChecker)
![Watchers](https://img.shields.io/github/watchers/Redstoneur/MediaIntegrityChecker)

---

![Latest Release](https://img.shields.io/github/v/release/Redstoneur/MediaIntegrityChecker)
![Release Date](https://img.shields.io/github/release-date/Redstoneur/MediaIntegrityChecker)

---

## Description

**MediaIntegrityChecker** est un outil Python combinant moviepy et pymediainfo pour vérifier l'intégrité des
fichiers multimédias et obtenir des informations détaillées sur les codecs, la durée, les dimensions, et plus encore.
Idéal pour s'assurer que vos fichiers vidéo et audio sont utilisables et non corrompus.

## Fonctionnalités

**MediaIntegrityChecker** offre les fonctionnalités suivantes :

- Vérification de l'intégrité des fichiers vidéo.
- Récupération d'informations détaillées sur les fichiers vidéo, y compris :
    - Codec
    - Durée
    - Dimensions (largeur et hauteur)
    - Taux de trame (fps)
    - Codec audio
    - Canaux audio
    - Taux d'échantillonnage audio

## Installation

1. Clonez le dépôt :

  ```sh
  git clone https://github.com/Redstoneur/MediaIntegrityChecker.git
  cd MediaIntegrityChecker
  ```

2. Installez les dépendances Python :

  ```sh
  pip install -r requirements.txt
  ```

## Utilisation

Pour utiliser **MediaIntegrityChecker**, suivez les étapes suivantes :

1. Exécutez le script Python `main.py` avec l'argument `-f` suivi du chemin vers le fichier vidéo que vous souhaitez
   vérifier. Par exemple :

  ```sh
  python main.py -f /path/to/your/video.mp4
  ```

## Licence

Ce projet est sous licence `GNU General Public License v3.0`. Voir le fichier `LICENSE` pour plus d'informations.
