# EasyMake - LGPL - kitsu

import os
from pathlib import Path
import re

BUILD_DIR = 'build'
DIST_DIR = 'bin'
SRC_DIR = 'src'

SOURCE_EXT = '.c'
COMPILED_EXT = '.o'
LINKED_EXT = '.so'

def die(msg):
    print("[Err]:", msg)
    exit(1)

def check_def(k, default='[undefined]', msg=(("env var \'%s\' is undefined") % (k))):
    t = os.getenv(k)
    if t is None:
        if default is '[undefined]':
            die(msg)
        else:
            return default
    return t

def compile_dir(cc, path, ext, flags, is_link):
    files = ''
    if type(ext) is list:
        for e in ext:
            files += ('*%s ' % e)
    elif type(ext) is str:
        files = ext
    else:
        die("Wrong file format")

    subdirs = []
    for i in path.iterdir():
        if i.is_dir():
            subdirs += i
        elif not re.search(re.escape(ext) + '$', i) is None:
            name = str(i)
            (dest, comp_param, comp_ext) = \
                    (DIST_DIR, '', LINKED_EXT) \
                if is_link else \
                    (BUILD_DIR / i, '-C', COMPILED_EXT)
            os.system('%s ' '%s '       '%s -o%s'   '%s '     '%s' % \
                      (cc,  comp_param, name, dest, comp_ext, flags))

    return subdirs

def compile(cc, ext, flags, is_link):
    p = Path(SRC_DIR)
    comp = lambda pth: compile_dir(cc, pth, ext, flags, is_link)
    sub = comp(p)
    for s in sub:
        sub += comp(s)

def create_req_dirs(l):
    for i in l:
        try:
            os.mkdir(i)
        except FileExistsError:
            pass

def main():
    cc = check_def('EM_CC')
    ext = check_def('EM_EXT', default=SOURCE_EXT)
    ext.replace('*', '') # wildcards will be added
    cflags = check_def('EM_CFLAGS', default='')
    ldflags = check_def('EM_LDFLAGS', default='')

    BUILD_DIR = check_def('EM_BUILD', default=BUILD_DIR)
    DIST_DIR = check_def('EM_DIST', default=DIST_DIR)
    SRC_DIR = check_def('EM_SRC', default=SRC_DIR)

    create_req_dirs([BUILD_DIR, DIST_DIR])

    compile(cc, ext, cflags, is_link=False)
    compile(cc, ext, ldlags, is_link=True)

if __name__ == '__main__':
    main()