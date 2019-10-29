# subassert

Converts subtitles in SSA/ASS format to SRT.


## Usage

    $ ./subassert.py <input-file>

If the file has multiple tracks or they are named something else than `''`, you
can list the tracks with `./subassert -l <input-file>` and extract a given track:

    $ ./subassert.py -t <track> <input-file>

The SRT will be printed to stdout, redirect it with your shell to save to a file:

    $ ./subassert.py <input-file> > newsub.srt


## Development

Install test helpers:

    $ ./configure

Run tests:

    $ ./test
