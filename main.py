import sys

from downloader import download

if __name__ == '__main__':
    try:
        puzzle_type = sys.argv[1]
    except IndexError:
        print('ERROR: Invalid or missing puzzle type!')
        exit(1)

    try:
        year = int(input('Enter year to download: '))
    except ValueError:
        print('ERROR: Invalid year!')
        exit(1)

    download(puzzle_type=puzzle_type, pub_year=year)
