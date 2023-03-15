from downloader import download

if __name__ == '__main__':
    # try:
    year = int(input('Enter year to download: '))
    # except ValueError:
    #     print('ERROR: Invalid year!')
    #     exit(1)

    success = download(puzzle_type='acrostic', pub_year=year) and download(puzzle_type='variety', pub_year=year)
    if success:
        print('All done!')
    else:
        print('There was an issue downloading puzzles.')
