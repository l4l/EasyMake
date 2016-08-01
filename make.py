#!/bin/python
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

UNDEFINED = '[undefined]'

PROJ = UNDEFINED

def die(msg):
    print("[Err]:", msg)
    exit(1)

def check_def(k, default=UNDEFINED, msg=UNDEFINED):
    t = os.getenv(k)
    if t is None:
        if default is UNDEFINED:
            if msg is UNDEFINED:
                msg = "env var \'%s\' is undefined" % (k)
            die(msg)
        else:
            return default
    return t

def read_dir(p):
    dirs = []
    files = []
    for i in p.iterdir():
        if i.is_dir():
            dirs.append(i)
        else:
            files.append(i)

    return dirs, files

def compile_dir(cc, path, ext, flags):
    files = ''
    if type(ext) is list:
        for e in ext:
            files += ('*%s ' % e)
    elif type(ext) is str:
        files = ext
    else:
        die("Wrong file format")

    subdirs, files = read_dir(path)
    for f in files:
        name = str(f)
        if not re.search(re.escape(ext) + '$', name) is None:
            comp_ext = COMPILED_EXT
            dest = BUILD_DIR / f.relative_to('src/').with_suffix(comp_ext)
            comp_param = '-c'

            comp_arg = '%s ' '%s '       '%s -o%s'   '%s' % \
                       (cc,  comp_param, name, dest, flags)

            print("[Info]:", comp_arg)

            os.system(comp_arg)
    return subdirs

def compile(cc, ext, flags):
    p = Path(SRC_DIR)
    comp = lambda pth: compile_dir(cc, pth, ext, flags)
    sub = comp(p)
    for s in sub:
        try:
            os.mkdir(str(BUILD_DIR / s.relative_to('src/')))
        except FileExistsError:
            pass
        sub += comp(s)

def linked_file(path, comp_ext, is_shared=False):
    p = Path(DIST_DIR)
    if is_shared:
        return (p / ('lib' + path.stem)).with_suffix(comp_ext)
    else:
        return p / PROJ

def link_target(cc, path, ext, flags, is_shared):
    subdirs, files = read_dir(path)

    name = " ".join(list(map(lambda x: str(x), files)))
    comp_ext = LINKED_EXT
    dest = linked_file(path, comp_ext, is_shared=is_shared)

    if is_shared:
        flags += '-shared'

    comp_arg = '%s ' '%s -o%s '   '%s' % \
               (cc,  name, dest, flags)

    print("[Info]:", comp_arg)

    os.system(comp_arg)

    return subdirs

def link(cc, ext, flags):
    p = Path(BUILD_DIR)
    dirs = link_target(cc, p, ext, flags, False)
    for f in dirs:
        if f != []:
            dirs.append(link_target(cc, f, ext, flags, True))

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

    global BUILD_DIR
    global DIST_DIR
    global SRC_DIR
    global PROJ

    BUILD_DIR = check_def('EM_BUILD', default=BUILD_DIR)
    DIST_DIR = check_def('EM_DIST', default=DIST_DIR)
    SRC_DIR = check_def('EM_SRC', default=SRC_DIR)

    PROJ = Path(os.getenv('PWD')).name

    create_req_dirs([BUILD_DIR, DIST_DIR])

    compile(cc, ext, cflags)
    link(cc, ext, ldflags)

if __name__ == '__main__':
    main()
