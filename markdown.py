"""
 Markdown.py
 0. just print whatever is passed in to stdin
 0. if filename passed in as a command line parameter, 
    then print file instead of stdin
 1. wrap input in paragraph tags
 2. convert single asterisk or underscore pairs to em tags
 3. convert double asterisk or underscore pairs to strong tags
"""

import fileinput
import re

foundBQ = False

def convertStrong(line):
  line = re.sub(r'\*\*(.*)\*\*', r'<strong>\1</strong>', line)
  line = re.sub(r'__(.*)__', r'<strong>\1</strong>', line)
  return line

def convertEm(line):
  line = re.sub(r'\*(.*)\*', r'<em>\1</em>', line)
  line = re.sub(r'_(.*)_', r'<em>\1</em>', line)
  return line

def converth1(line):
  line = re.sub(r'#(.*)',r'<h1>\1</h1>',line)
  return line 
def converth2(line):
  line = re.sub(r'##(.*)',r'<h2>\1</h2>',line)
  return line 
def converth3(line):
  line = re.sub(r'###(.*)',r'<h3>\1</h3>',line)
  return line 

def convertBlockQuote(line):
  global foundBQ
  if line[0] == '>' and not foundBQ:
    foundBQ = True
    line = re.sub(r'>(.*)',r'<blockquote>\1',line)
  elif line[0] == '>':
    line = line[1:]
  elif line[0] != '>' and foundBQ:
    foundBQ = False
    line = re.sub(r'(.*)',r'</blockquote>\1',line)
  return line

def convertp(line):
  if '<blockquote>' == line[0:12]:
    line = '<blockquote>' + '<p>' + line[12:] + '</p>'
  elif '</blockquote>' in line[0:13]:
    line = '</blockquote>' + '<p>' + line[13:] + '</p>'
  else:
    line = '<p>' + line + '</p>'
  return line

for line in fileinput.input():
  line = line.rstrip() 
  line = convertBlockQuote(line)
  line = convertStrong(line)
  line = convertEm(line)
  line = converth3(line)
  line = converth2(line)
  line = converth1(line)
  line = convertp(line)
  print line,
