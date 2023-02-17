import sys

import requests

puzzles_endpoint = "https://edge.games.nyti.nyt.net/svc/crosswords/v3/35806626/puzzles.json"
download_url_format = "https://www.nytimes.com/svc/crosswords/v2/puzzle/print/%s.pdf"


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

    response = requests.get(puzzles_endpoint, params)

    print(response.json())


if __name__ == '__main__':
    download(puzzle_type=sys.argv[1])
