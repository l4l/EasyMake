# EasyMake

> EasyMake is a simple compilation tool mainly for C-projects

Assume you have some project tree like this:

```
my-project
├── include
│   ├── other-api.h
│   └── srv-api.h
├── src
│   ├── cmd.c
│   ├── io
│   │   ├── buffer.c
│   │   └── cache.c
│   ├── main.c
│   └── net
│       ├── server.c
│       └── sys-dep.c
└── test
    ├── cmd-test.c
    ├── io
    │   ├── buffer-test.c
    │   └── cache-test.c
    └── net
        └── server-test.c
``` 

Pretty usual for c-like proj, huh? The reason of this tool is just one-python-file (and optionally some config files). It can handle this projects and produce (at unix) following build structure:

```
bin
├── libio.so
├── libnet.so
└── my-project
build
├── cmd.o
├── io
│   ├── buffer.o
│   └── cache.o
├── main.o
└── net
    ├── server.o
    └── sys-dep.o
```

## Env variables

Default tools, flags, project dir, etc can be changed via environment variables. Most of them has prefix EM\_ to the common name. Here is the list:

+ EM\_CC - compiler
+ EM\_EXT - extension (e.g '\*.c')
+ EM\_CFLAGS - flags for compilation
+ EM\_LDFLAGS - flags for linking
+ EM\_BUILD - building directory
+ EM\_DIST - binary directory
+ EM\_SRC - source file directory (e.g src/)
+ EM\_PROJ - project root
