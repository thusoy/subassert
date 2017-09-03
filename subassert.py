#!/usr/bin/env python

import argparse
import sys
import textwrap
import re
from collections import namedtuple

Sub = namedtuple('Sub', 'start end text')

DIALOGUE_RE = re.compile(r'Dialogue: 0,([\d:.]+),([\d:.]+),(.*?),(?:.*?,){5}(.*)')
TEXT_SUB = re.compile(r'\{[^}]+\}')
TIME_RE = re.compile(r'(\d+):(\d{2}):(\d+).(\d+)')

def main():
    args = get_args()
    if args.list_tracks:
        list_tracks(args.input_ass_file)
    else:
        convert_file(args.input_ass_file, args.tracks)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_ass_file')
    parser.add_argument('-l', '--list-tracks', action='store_true')
    parser.add_argument('-t', '--tracks', default='')

    args = parser.parse_args()

    args.track = args.tracks.split(',')

    return args


def list_tracks(ass_file):
    with open(ass_file) as fh:
        for line in fh:
            track = extract_track(line)
            if track:
                tracks.add(track)

    if list_tracks:
        for track in sorted(tracks):
            print(track)


def convert_file(ass_file, tracks):
    # might not appear in order, sort them by start time
    subs = []
    with open(ass_file) as fh:
        for line in fh:
            sub = extract_line(line, tracks)
            if not sub:
                continue
            subs.append(sub)
    subs.sort()

    counter = 1
    for sub in subs:
        print('%d\n%s\n' % (counter, format_sub(sub)))
        counter += 1


def extract_line(line, tracks):
    match = DIALOGUE_RE.match(line)
    if not match:
        return
    start, end, track, text = match.groups()
    if tracks and not track in tracks:
        return

    text = TEXT_SUB.sub('', text).replace('\r', '')
    return Sub(start, end, text)


def format_sub(sub):
    return '%s --> %s\n%s' % (
        format_time(sub.start),
        format_time(sub.end),
        textwrap.fill(sub.text, 50),
    )


def extract_track(line):
    match = DIALOGUE_RE.match(line)
    if not match:
        return

    return match.group(3)


def format_time(timestr):
    hour, minute, second, part = TIME_RE.match(timestr).groups()
    second = float('%s.%s' % (second, part))
    return ('%02d:%02d:%06.3f' % (int(hour), int(minute), second)).replace('.', ',')


if __name__ == '__main__':
    main()
