import sys

from downloader import download

if __name__ == '__main__':
    download(puzzle_type=sys.argv[1], pub_year=2023)
