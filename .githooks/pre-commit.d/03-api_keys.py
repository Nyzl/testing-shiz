#!/usr/local/bin/python3

import subprocess, sys, os, re, argparse

def main():

regexs = {
    "AWS Key": "[a-z0-9\/+]{40}",
    "Possible Key": "[a-z0-9_]{39}",
    "Possible Password": "(pass(word)? ?= ?[\"\'\`].*?[\"\'\`])"
}

prog = re.compile(pattern)
result = prog.match(string)

if __name__ == '__main__':
    main()
