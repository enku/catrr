# catrr

This is a small command-line program that takes a list of filename arguments
and each time it's called with the same arguments writes the contents of the
next file to standard output, in round-robin fashion. I use this to select
from a directory of wallpaper for [larry](https://github.com/enku/larry). I
probably could have accomplished the same thing by wiring together some Linux
utilities, but that's not interesting.

So for example:

```
$ echo foo > a
$ echo bar > b
$ echo baz > c
$ catrr a b c
foo
$ catrr a b c
bar
$ catrr a b c
baz
$ catrr a b c
foo
```
