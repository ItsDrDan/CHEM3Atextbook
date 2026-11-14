#!/usr/bin/env python3
"""Find where a phrase is spoken in ItsDrDan videos.
Usage: python3 tools/find_moment.py "<regex>" [videoId ...]
Reads ../games/data/transcripts.json (repo ItsDrDan/games; segments = [videoId, startSeconds, text]).
Prints videoId, m:ss, youtu.be link and the matching text. Always open the link and listen before citing a moment."""
import json, re, sys, os
here = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(here, '..', '..', 'games', 'data', 'transcripts.json')
d = json.load(open(path))
pat = re.compile(sys.argv[1], re.I)
only = set(sys.argv[2:])
for vid, start, text in d['segments']:
    if only and vid not in only: continue
    if pat.search(text):
        s = int(start)
        print(f"{vid}  {s//60}:{s%60:02d}  https://youtu.be/{vid}?t={s}  | {d['titles'].get(vid,'')[:50]} | {text[:110]}")
