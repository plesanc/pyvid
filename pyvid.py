import argparse
import os

# look further: https://pymotw.com/2/argparse/

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
def find_file(path, name):
	for root, dirs, files in os.walk(path):
		for x in range(0, len(files)):
			if name in files[x]:
				return os.path.join(root, files[x])
	return -1

def find_dir(path, name, season):
	for root, dirs, files in os.walk(path):
		print(dirs)

## Find media location
def find_media(path, name, season, episode):
	## Look for matching media
	# for movie, have season = 0 & episode = 0
	if (season == 0 & episode == 0):
		# look for movie in root dir
		return find_file(path, name)
	else:
		# look for a show
		directory = find_dir(path, name, season)
		return directory
		# if (directory == -1)




## Main loop
def main():

	if (args.verbose):
		print('cast', args.cast)
		print('autoplay', args.autoplay)
		print('movie_name', args.movie_name)
		print('show_name', args.show_name)
		print('season', args.season)
		print('episode', args.episode)

	if (args.movie_name != "disabled"):
		# Look for movie
		print("Looking for:", args.movie_name)
		media_location = find_media('/home/chad/Videos/', args.movie_name, 0, 0)

	elif (args.show_name != "disabled"):
		# Look for tv show
		print("Looking for:", args.show_name, "Season", args.season, "Episode", args.episode)
		media_location = find_media('/home/chad/Videos/', args.movie_name, args.season, args.episode)
	
	if (media_location == -1):
		print("No File Found.")
		return
	print("Found media at: ", media_location)



	if (args.cast):
		print('Casting to Chromecast')

main()
