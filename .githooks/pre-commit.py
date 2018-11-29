#!/usr/local/bin/python3
"""
This is a git commit-hook which can be used to check if huge files
 where accidentally added to the staging area and are about to be
 committed.
If there is a file which is bigger then the given "max_file_size"-
 variable, the script will exit non-zero and abort the commit.
This script is meant to be added as a "pre-commit"-hook. See this
 page for further information:
    http://progit.org/book/ch7-3.html#installing_a_hook
In order to make the script work probably, you'll need to set the
 above path to the python interpreter (first line of the file)
 according to your system (under *NIX do "which python" to find out).
Also, the "git_binary_path"-variable should contain the absolute
 path to your "git"-executable (you can use "which" here, too).
See the included README-file for further information.
The script was developed and has been confirmed to work under
 python 3.2.2 and git 1.7.7.1 (might also work with earlier versions!)
"""

# The maximum file-size for a file to be committed:
max_file_size = 512 # in KB (= 1024 byte)
# The path to the git-binary:
git_binary_path = "/usr/bin/git"

# ---- DON'T CHANGE THE REST UNLESS YOU KNOW WHAT YOU'RE DOING! ----

import subprocess, sys, os, re, argparse

BLACKLIST = [
    b'BEGIN RSA PRIVATE KEY',
    b'BEGIN DSA PRIVATE KEY',
    b'BEGIN EC PRIVATE KEY',
    b'BEGIN OPENSSH PRIVATE KEY',
    b'BEGIN PRIVATE KEY',
    b'PuTTY-User-Key-File-2',
    b'BEGIN SSH2 ENCRYPTED PRIVATE KEY',
    b'BEGIN PGP PRIVATE KEY BLOCK',
]

"""
This function will return a human-readable filesize-string
 like "3.5 MB" for it's given 'num'-parameter.
From http://stackoverflow.com/questions/1094841
"""
def sizeof_fmt(num):
    for x in ['bytes','KB','MB','GB','TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0

def check_size(file):
    stat = os.stat(file[3:])
    if stat.st_size > (max_file_size*1024):
        print("'"+file_s[3:]+"' is too huge to be commited!",
            "("+sizeof_fmt(stat.st_size)+")")
        sys.exit(1)

def detect_private_key(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check')
    args = parser.parse_args(argv)

    private_key_files = []

    for filename in args.filenames:
        with open(filename, 'rb') as f:
            content = f.read()
            if any(line in content for line in BLACKLIST):
                private_key_files.append(filename)

    if private_key_files:
        for private_key_file in private_key_files:
            print('Private key found: {}'.format(private_key_file))
            sys.exit(1)
    else:
        return 0

# Now, do the checking:
try:
    print("Checking for files bigger then "+sizeof_fmt(max_file_size*1024))
    text = subprocess.check_output(
    [git_binary_path, "status", "--porcelain", "-uno"],
		stderr=subprocess.STDOUT).decode("utf-8")
    file_list = text.splitlines()

	# Check all files:
    for file in file_list:
        check_size(file)



	# Everything seams to be okay:
    detect_private_key()
    print("No badness found")
    sys.exit(0)

except subprocess.CalledProcessError:
	# There was a problem calling "git status".
	print("Oops...")
	sys.exit(12)

# regexs = {
#     "AWS Key" =< "['\\\"][a-z0-9\/+]{40}['\\\"]",
#     "Google Key" =< "['\\\"][a-z0-9_]{39}['\\\"]",
# }
