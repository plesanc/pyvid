import argparse
import os
import time
import vlc

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
			if name in files[x]:
				return os.path.join(root, files[x])
	return -1

def find_show(path, name, season, episode):
	#Look for show
	for root, dirs, files in os.walk(path):
		if name in dirs:
			print('Found show:', name)
			path = os.path.join(path, name)
			break
		else:
			print('Could not find show:', name)
			return -1

	#Look for season
	season = 'Season_' + str(season)
	for root, dirs, files in os.walk(path):
		if season in dirs:
			print('Found:', season)
			path = os.path.join(path, season)
			break
		else:
			print('Could not find season:', season)
			return -1

	#Look for episode
	episode = 'E0' + str(episode)
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

	if (args.movie_name != "disabled"):
		# Look for movie
		print("Looking for Movie:", args.movie_name)
		media_location = find_movie('/home/chad/Videos/', args.movie_name)

	elif (args.show_name != "disabled"):
		# Look for tv show
		print("Looking for TV Show:", args.show_name, "Season", args.season, "Episode", args.episode)
		media_location = find_show('/home/chad/Videos/TV/', args.show_name, args.season, args.episode)
	
	# Check if succesfully found media
	if (media_location == -1):
		print("No File Found.")
		return
	print("Found media at: ", media_location)

	if (args.cast):
		print('Casting to Chromecast')
		### do casting here....
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
        print >> sys.stderr, '\nExiting by user request.\n'
        sys.exit(0)
