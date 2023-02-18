import sys
from datetime import date
from http.cookiejar import MozillaCookieJar
from pathlib import Path

import requests

puzzles_endpoint = 'https://edge.games.nyti.nyt.net/svc/crosswords/v3/35806626/puzzles.json'
puzzle_print_url_format = 'https://www.nytimes.com/svc/crosswords/v2/puzzle/print/%s.pdf'
puzzle_url_format = 'https://www.nytimes.com/svc/crosswords/v2/puzzle/%s.pdf'

# File date is the short month name, two-digit day, and two-digit year (e.g. "Jan0123" for January 1, 2023)
# https://docs.python.org/3.9/library/datetime.html#strftime-and-strptime-format-codes
file_date_format = '%b%d%y'

publish_type_suffix = {
    'Daily': '',      # The daily puzzle, no file suffix (e.g. "Jan0123.pdf")
    'Variety': '.2',  # Includes acrostics and other variety puzzles (e.g. "Jan0123.2.pdf")
    'Assorted': '.3'  # Includes "A Little Variety" puzzles (e.g. "Jan0123.3.pdf")
}


def download(puzzle_type: str, pub_year: int = 2023):
    # Set default query parameters for all puzzle types.
    # For Acrostic and Variety puzzles, we can call the API a year at a time without hitting any limits.
    params = {
        'sort_order': 'asc',
        'sort_by': 'print_date',
        'date_start': f'{pub_year}-01-01',
        'date_end': f'{pub_year}-12-31'
    }

    # The format_type and publish_type parameters need to be set differently depending on the type of puzzle.
    if puzzle_type == 'acrostic':
        # Acrostics have only one format type
        params['format_type'] = 'acrostic'
    elif puzzle_type == 'variety':
        # Variety puzzles have multiple format types, and also require publish_type to be set
        params['format_type'] = 'pdf,normal,diagramless'
        params['publish_type'] = 'variety,assorted'
    else:
        print(f'Invalid puzzle type: {puzzle_type}')
        return

    # Set the output directory for the puzzle files.
    out_dir = f'out/{puzzle_type}'
    # Create the directory if it does not already exist.
    Path(out_dir).mkdir(parents=True, exist_ok=True)

    response = requests.get(puzzles_endpoint, params).json()

    with requests.Session() as session:
        # Load cookies from cookies.txt, which is presumed to be in the Netscape format.
        cookies = MozillaCookieJar('cookies.txt')
        cookies.load()
        session.cookies = cookies

        def download_file(file_name: str, solution=False):
            # Append solution suffix if the solution file is desired
            suffix = '.ans' if solution else ''

            # Download the puzzle file.
            # It should be small enough to fit into memory, so we do not have to stream to disk.
            puzzle = session.get(puzzle_print_url_format % f'{file_name}{suffix}')
            if puzzle.status_code != 200:
                if solution:
                    # Fall back to using the puzzle ID if download fails.
                    # This can happen if the puzzle solution has not been published in the paper yet.
                    puzzle = session.get(puzzle_url_format % f'{puzzle_id}{suffix}')
                    if puzzle.status_code != 200:
                        print(f'The solution for {file_name} is not yet available')
                        return
                else:
                    print(f'Error downloading {file_name}: {str(puzzle.content).strip()}')
                    return

            # Save the downloaded file to disk.
            dest_path = f'{out_dir}/{file_name}{suffix}.pdf'
            print(f'Saving {dest_path}')
            with open(dest_path, 'wb') as f:
                f.write(puzzle.content)

        for result in response['results']:
            puzzle_id = result['puzzle_id']
            publish_type = result['publish_type']
            # The download URL includes the formatted file date and optional suffix in the file name.
            file_date = date.fromisoformat(result['print_date']).strftime(file_date_format)
            file_name_base = f'{file_date}{publish_type_suffix[publish_type]}'
            # Download the puzzle file
            download_file(f'{file_name_base}')
            # Download the solution file
            download_file(f'{file_name_base}', solution=True)


if __name__ == '__main__':
    download(puzzle_type=sys.argv[1])
