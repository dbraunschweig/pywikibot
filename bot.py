#!/usr/bin/env python

import math
import os
import re

def cleanup():
    for root, dirs, files in os.walk("/Users/dave/Desktop"):
        for name in files:
            if(name.find(".txt") >= 0):
                filename = os.path.join(root, name)
                print(filename)
                file = open(filename, "r")
                text = file.read()
                file.close()
                match = re.match("^.*Reset Options Hide Answer", text, flags=re.DOTALL)
                if(match != None):
                    start = len(match.group(0))
                    text = text[start:]

                match = re.match("^.*\\ Explanation", text, flags=re.DOTALL)
                if(match != None):
                    end = len(match.group(0))
                    text = text[:end - 14]

                file = open(filename, "w")
                file.write(text)
                file.close()


def combine():
    text = ""
    for root, dirs, files in os.walk("/Users/dave/Desktop"):
        for name in files:
            if(name.find(".txt") >= 0):
                filename = os.path.join(root, name)
                print(filename)
                file = open(filename, "r")
                text += filename + "\n"
                text += file.read()
                file.close()

    filename = "/Users/dave/Desktop/combined.txt"
    file = open(filename, "w")
    file.write(text)
    file.close()


def networking():
    filename = "/Users/dave/Desktop/youtube.txt"
    file = open(filename, "r")
    text = file.readlines()
    file.close()
    for line in text:
        match = re.search('data-video-title="[^"]*"', line)
        if match == None:
            continue
        title = match.group(0)
        title = title.replace('data-video-title="', '')
        title = title.replace('"', '')

        match = re.search('data-video-id="[^"]*"', line)
        if match == None:
            continue
        id = match.group(0)
        id = id.replace('data-video-id="', '')
        id = id.replace('"', '')

        print("# Watch [https://www.youtube.com/watch?v=" + id + " YouTube: " + title + "].")

#cleanup()
#combine()
#networking()


file = open("/Users/dave/Desktop/Categories.txt", "r+")
text = file.read()
lines = text.split("\n")
for line in lines:
    if line.find("Error") != 0:
        print(line)

exit(0)

import requests
url = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikiversity/all-access/user/Topic%3AAbenaki/daily/20151001/20160229'
result = requests.get(url)
print(result.json())

text = ""
for root, dirs, files in os.walk("/Users/dave/Desktop/Lammle"):
    for name in files:
        if(name.find(".txt") >= 0):
            filename = os.path.join(root, name)
            print(filename)
            try:
                file = open(filename, "r+")
                text = file.read()
                result = text.replace('"', '')
    #            if text != result:
    #                file.write(text)
                file.close()
            except:
                print("  Error.")
