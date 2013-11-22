#!/usr/bin/env python

import cmd
import logging
import os
import sys

from pyechonest import config, song, artist
config.ECHO_NEST_API_KEY="DCXFDKEYEASLME4NL"
keys = ['C','C#','D','Eb','E','F','F#','G','Ab','A','Bb','B']

if len(sys.argv) < 3:
  sys.exit(1)

name = sys.argv[1]
title = sys.argv[2]
echoresults = song.search(artist=name, title=title) 
if not echoresults:
  print "no info on echo's nest"
  sys.exit(1)

songinfo = echoresults[0]
audio = songinfo.get_audio_summary()
key = keys[audio['key']]
minor = "m"
if audio['mode'] == '0':
  minor = ""
print "%s by %s, in the key of %s%s" % (songinfo.title, songinfo.artist_name, key, minor)
