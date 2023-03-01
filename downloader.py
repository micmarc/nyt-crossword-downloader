from datetime import date
from http.cookiejar import MozillaCookieJar
from pathlib import Path

import filedate
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


def download(puzzle_type: str, pub_year: int = 2023, cookies_path: str = 'cookies.txt'):
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
        return False

    # Set the output directory for the puzzle files.
    out_dir = f'out/{puzzle_type}/{pub_year}'
    # Create the directory if it does not already exist.
    Path(out_dir).mkdir(parents=True, exist_ok=True)

    response = requests.get(puzzles_endpoint, params).json()

    with requests.Session() as session:
        # Load cookies from cookies.txt, which is presumed to be in the Netscape format.
        if not Path(cookies_path).exists():
            print(f'ERROR: Could not find cookies file "{cookies_path}". Did you forget to export your cookies?')
            return False

        cookies = MozillaCookieJar(cookies_path)
        cookies.load()
        session.cookies = cookies

        def download_file(solution=False):
            # Append solution suffix if the solution file is desired
            suffix = '.ans' if solution else ''

            # The file on the server
            source_file_name = f'{file_name_base}{suffix}'
            # The file to save - include the title for convenience
            title: str = result['title']
            # No title for a variety puzzle indicates no puzzle to download
            if puzzle_type == 'variety' and not title:
                print(f'Skipping variety puzzle "{source_file_name}" because it has no title')
                return

            # Replace path separator characters to avoid path issues.
            title = title.replace('/', '-').replace('\\', '_')
            dest_file_name = f'{title}.{file_date}{suffix}'

            # Do not download if the file already exists
            dest_path = f'{out_dir}/{dest_file_name}.pdf'
            if Path(dest_path).exists():
                print(f'Puzzle "{source_file_name}" already downloaded: "{dest_path}"')
                return

            # Download the puzzle file (newspaper version).
            # It should be small enough to fit into memory, so we do not have to stream to disk.
            puzzle = session.get(puzzle_print_url_format % source_file_name)
            if puzzle.status_code != 200:
                # Fall back to using the puzzle ID if download fails.
                # This is useful for older puzzles or solutions that have not been published in the paper yet.
                puzzle_id = result['puzzle_id']
                puzzle = session.get(puzzle_url_format % f'{puzzle_id}{suffix}')
                if puzzle.status_code != 200:
                    try:
                        error_text = puzzle.json()['errors'][0]
                    except ValueError:
                        # Response is not JSON, probably just plain text
                        error_text = puzzle.content.decode('utf8')
                    print(f'Error downloading "{source_file_name}" to "{dest_file_name}": {error_text}')
                    return

            # Save the downloaded file to disk.
            print(f'Saving "{source_file_name}" as "{dest_path}"')
            Path(dest_path).write_bytes(puzzle.content)

            # Update created and last modified dates to reflect the publish date.
            # This enables sorting the files by publish date if desired.
            file_meta = filedate.File(dest_path)
            file_meta.set(created=print_date, modified=print_date)

        results = response['results']
        if not results:
            print(f'No {puzzle_type} puzzles were published in {pub_year}.')
            return True

        print(f'Found {len(results)} {puzzle_type} puzzles published in {pub_year}. Downloading...')
        for result in results:
            publish_type = result['publish_type']
            # The download URL includes the formatted file date and optional suffix in the file name.
            print_date = result['print_date']
            file_date = date.fromisoformat(print_date).strftime(file_date_format)
            file_name_base = f'{file_date}{publish_type_suffix[publish_type]}'
            # Download the puzzle file
            download_file()
            # Download the solution file
            download_file(solution=True)

        return True
