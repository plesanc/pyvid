import vlc
import argparser

parser = argparse.ArgumentParser()
parser.add_argument('filename')
parser.add_argument('seekTime')
parser.add_argument('display')
args = parser.parse_args()


if display == v
	# VLC
	vlc filename
elif display == c
	# Chromcast
	python3 /home/chad/mkchromecast/mkchromecast.py -n "Chizziecast TV" --video -i filename --control --seek seekTime
