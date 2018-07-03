import argparse
import sys
import os
import time
import vlc

## USAGE
#
# Simple Movie:
# python3 pyvid.py -m Watchmen
#
# TV Series from the start:
# python3 pyvid.py -a -t Workaholics
# 
# Specific Episode:
# python3 pyvid.py -a -t Workaholics -s 3 -e 12

parser = argparse.ArgumentParser()
parser.add_argument('-v', action='store_true', default=False, dest='verbose')
parser.add_argument('-c', action='store_true', default=False, dest='cast')
parser.add_argument('-a', action='store_true', default=False, dest='autoplay')
parser.add_argument('-m', action='store', default="disabled", dest='movie_name')
parser.add_argument('-t', action='store', default="disabled", dest='show_name')
parser.add_argument('-s', action='store', default=1, dest='season')
parser.add_argument('-e', action='store', default=1, dest='episode')
args = parser.parse_args()

## Find file in directory
def find_movie(path, name):
	for root, dirs, files in os.walk(path):
		for x in range(0, len(files)):
			# Look for partial name matches
			if name in files[x]:
				return os.path.join(root, files[x])
	return -1

def find_show(path, name, season, episode):
	# Look for show
	show_found = False
	for root, dirs, files in os.walk(path):
		for x in range(0, len(dirs)):
			# Look for partial name matches
			if name in dirs[x]:
				print('Found show:', dirs[x])
				path = os.path.join(path, dirs[x])
				show_found = True
				break

	if (show_found == False):
		print('Could not find show:', name)
		return -1

	# Error check season number
	season = str(season)
	season_array = list(season)
	if (len(season_array) > 2 or season == 0):
		print('Invalid Season Number')
		return -1

	# Remove any leading zeros
	if (season_array[0] == str(0)):
		print('Removing Leading Zero')
		season = season_array[1]

	# Create parsable season string
	season = 'Season_' + str(season)

	# Look for season
	for root, dirs, files in os.walk(path):
		if season in dirs:
			print('Found:', season)
			path = os.path.join(path, season)
			break
		else:
			print('Could not find season:', season)
			return -1

	# Error check episode number
	episode = str(episode)
	episode_array = list(episode)
	if (len(episode_array) > 2 or season == 0):
		print('Invalid Season Number')
		return -1

	# Remove any leading zeros
	if (episode_array[0] == str(0)):
		print('Removing Leading Zero')
		episode = episode_array[1]

	# Create parsable episode string
	print(len(episode))
	if (len(episode) == 1):
		episode = 'E0' + str(episode)
	else:
		episode = 'E' + str(episode)

	# Look for episode
	for root, dirs, files in os.walk(path):
		for x in range(0, len(files)):
			if episode in files[x]:
				return os.path.join(path, files[x])
		print('Could not find Episode', episode)
		return -1

	return -1

## Main loop
def main_loop():

	if (args.verbose):
		print('cast', args.cast)
		print('autoplay', args.autoplay)
		print('movie_name', args.movie_name)
		print('show_name', args.show_name)
		print('season', args.season)
		print('episode', args.episode)

	media_location = -1

	# Look for movie
	if (args.movie_name != "disabled"):
		print('Looking for Movie:', args.movie_name)
		media_location = find_movie('/home/chad/Videos/', args.movie_name)

	# Look for tv show
	elif (args.show_name != "disabled"):
		print('Looking for TV Show:', args.show_name, 'Season', args.season, 'Episode', args.episode)
		media_location = find_show('/home/chad/Videos/TV/', args.show_name, args.season, args.episode)
	
	# Check if succesfully found media
	if (media_location == -1):
		print('No File Found.')
		return
	print('Found media at: ', media_location)

	# Cast media to chromcast
	if (args.cast):
		print('Casting to Chromecast')
		### do casting here....

		# while media is playing it would be helpful to be able to pass commands through to mkchromecast
		while 1:
			time.sleep(1)

	# Watch media locally using VLC
	else:
		print('Launching VLC...')
		

		# Create instane of VLC and create reference to movie.
		vlcInstance = vlc.Instance()
		media = vlcInstance.media_new(media_location)
		# Create new instance of vlc player
		player = vlcInstance.media_player_new()
		# Load movie into vlc player instance
		player.set_media(media)

		player.play()

		#there are ways to pause etc through the vlc API, look into this..

		while 1:
			time.sleep(1)

if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        print('\nExitting by keyboard interrupt.\n')
        sys.exit(0)
