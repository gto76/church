#!/usr/bin/python
#
# Usage: update-site.py 
# Generates README.md and single image webpages, as defined in
# photosrc.

from __future__ import print_function
import sys
import re

with open("template/template.html") as f:
  TEMPLATE = f.readlines()

def main():
  with open("photosrc") as f:
    lines = f.readlines()
  username = [line.replace("USERNAME=", "").strip() for line in lines if "USERNAME=" in line][0]
  reponame = [line.replace("REPONAME=", "").strip() for line in lines if "REPONAME=" in line][0]
  readmeLink = "https://github.com/" + username + "/" + reponame
  rootAddress = "http://" + username + ".github.io/" + reponame + "/site/"
  chain = [line.strip() for line in lines if not line.strip().startswith('#') and line.strip() and "USERNAME=" not in line]
  generateReadme(chain, username)
  generatePages(chain, readmeLink, rootAddress)

def generateReadme(chain, username):
  readme = "# Church\n\n"
  for img in chain:
    readme += getReadmeLine(img, username)
  f = open("README.md", "w")
  print(readme, file=f)

def getReadmeLine(img, username):
  return "[<img src=\"site/images/"+img+"\">](http://"+username+".github.io/" + reponame + "/site/"+changeExtensionToHtml(img)+")\n\n"

def generatePages(chain, readmeLink, rootAddress):
  for i in xrange(0, len(chain)):
    if i == 0:
      back = readmeLink
    else:
      back = rootAddress + changeExtensionToHtml(chain[i-1])
    if i == len(chain)-1:
      forward = readmeLink
    else:
      forward = rootAddress + changeExtensionToHtml(chain[i+1])
    page = ''.join(getPage(back, chain[i], forward, readmeLink))
    filename = "site/" + changeExtensionToHtml(chain[i])
    f = open(filename, "w")
    print(page, file=f)

def changeExtensionToHtml(string):
  return re.sub("png", "html", re.sub("jpg", "html", string))

def getPage(back, img, forward, home):
  return [line.replace("BACK", back).replace("IMAGE", "images/"+img).replace("FORWARD", forward).replace("HOME", home) for line in TEMPLATE]

if __name__ == '__main__':
  main()
