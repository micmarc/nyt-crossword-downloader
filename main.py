import sys

from downloader import download

if __name__ == '__main__':
    _, puzzle_type, year = sys.argv
    download(puzzle_type=puzzle_type, pub_year=int(year))
