# nyt-crossword-downloader

This is a command-line utility to download PDFs of the New York Times Acrostic and Variety puzzles.

## Quick Start

### Prerequisites

- Python 3 (tested with 3.9.x)
- Pipenv

### Install and Run

Install dependencies:
```shell
pipenv install
```

Log into your NYT account and save your nytimes.com cookies to `cookies.txt` (I suggest [Get cookies.txt][Get cookies.txt] for Chrome).

Run it:
```shell
pipenv run python main.py
```

Enter a year between 1997 and 2023. The program does its best to download all Acrostic and Variety puzzles published in that year.

Sample output:
```
Enter year to download: 2023
Loading cookies from "cookies.txt"... done.
Found 5 acrostic puzzles published in 2023. Downloading...
* Jan0123.2     => out/Acrostic/2023/Acrostic.Jan0123.pdf
* Jan0123.2.ans => out/Acrostic/2023/Acrostic.Jan0123.ans.pdf
* Jan1523.2     => out/Acrostic/2023/Acrostic.Jan1523.pdf
* Jan1523.2.ans => out/Acrostic/2023/Acrostic.Jan1523.ans.pdf
* Jan2923.2     => out/Acrostic/2023/Acrostic.Jan2923.pdf
* Jan2923.2.ans => out/Acrostic/2023/Acrostic.Jan2923.ans.pdf
* Feb1223.2     => out/Acrostic/2023/Acrostic.Feb1223.pdf
* Feb1223.2.ans => out/Acrostic/2023/Acrostic.Feb1223.ans.pdf 
* Feb2623.2     => out/Acrostic/2023/Acrostic.Feb2623.pdf 
* Feb2623.2.ans => ERROR! Not Found
Found 13 variety puzzles published in 2023. Downloading...
* Jan0123.3     => out/Variety/2023/A Little Variety.Jan0123.pdf
* Jan0123.3.ans => out/Variety/2023/A Little Variety.Jan0123.ans.pdf
* Jan0823.2     => out/Variety/2023/Building Blocks.Jan0823.pdf
* Jan0823.2.ans => out/Variety/2023/Building Blocks.Jan0823.ans.pdf
* Jan0823.3     => out/Variety/2023/A Little Variety.Jan0823.pdf
* Jan0823.3.ans => out/Variety/2023/A Little Variety.Jan0823.ans.pdf
* Jan1523.3     => out/Variety/2023/A Little Variety.Jan1523.pdf
* Jan1523.3.ans => out/Variety/2023/A Little Variety.Jan1523.ans.pdf
* Jan2223.2     => out/Variety/2023/Puns and Anagrams.Jan2223.pdf
* Jan2223.2.ans => out/Variety/2023/Puns and Anagrams.Jan2223.ans.pdf
* Jan2223.3     => out/Variety/2023/A Little Variety.Jan2223.pdf
* Jan2223.3.ans => out/Variety/2023/A Little Variety.Jan2223.ans.pdf
* Jan2923.3     => out/Variety/2023/A Little Variety.Jan2923.pdf
* Jan2923.3.ans => out/Variety/2023/A Little Variety.Jan2923.ans.pdf
* Feb0523.2     => out/Variety/2023/Two-for-One Crossword.Feb0523.pdf
* Feb0523.2.ans => out/Variety/2023/Two-for-One Crossword.Feb0523.ans.pdf
* Feb0523.3     => out/Variety/2023/A Little Variety.Feb0523.pdf
* Feb0523.3.ans => out/Variety/2023/A Little Variety.Feb0523.ans.pdf
* Feb1223.3     => out/Variety/2023/A Little Variety.Feb1223.pdf
* Feb1223.3.ans => out/Variety/2023/A Little Variety.Feb1223.ans.pdf
* Feb1923.2     => out/Variety/2023/Cryptic Crossword.Feb1923.pdf
* Feb1923.2.ans => out/Variety/2023/Cryptic Crossword.Feb1923.ans.pdf
* Feb1923.3     => out/Variety/2023/A Little Variety.Feb1923.pdf
* Feb1923.3.ans => out/Variety/2023/A Little Variety.Feb1923.ans.pdf
* Feb2623.3     => out/Variety/2023/A Little Variety.Feb2623.pdf
* Feb2623.3.ans => ERROR! Not Found
All done!
```

## Why?

As of March 1, 2023, the Times is [no longer publishing Acrostics and Variety puzzles online](https://twitter.com/NYTGames/status/1630923424552894464). But the PDFs are still available (at least for now) if you know where to look, and PDFs are better than nothing!

[Get cookies.txt]: https://chrome.google.com/webstore/detail/get-cookiestxt/bgaddhkoddajcdgocldbbfleckgcbcid
