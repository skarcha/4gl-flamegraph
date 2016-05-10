# Flame Graphs for 4Js Genero

This a script to convert Genero profiler output to a format suitable for [FlameGraph](http://www.brendangregg.com/flamegraphs.html).

Flame Graphs will allow you to visualize your programs bottlenecks.

Follow this steps:

## Usage

### 1. Capture profiler data

Run your program with "-p" param. It will output the profiler data on stderr:

```
$ fglrun -p your_program.42r 2> your_program_profiler.log
```

### 2. Convert profiler data to stacks

Use stackcollaps-4gl.py:

```
$ python stackcollapse-4gl.py your_program_profiler.log > your_program_profiler.folded
```

### 3. Generate FlameGraph

Generate FlameGraph using Brendan D. Gregg's [flamegraph.pl](https://github.com/brendangregg/FlameGraph):

```
$ ./flamegraph.pl your_program_profiler.folded > your_program_profiler.svg
```

You can also do all in one line:

```
$ python stackcollapse-4gl.py your_program_profiler.log | ./flamegraph.pl > your_program_profiler.svg
```

## Options

```
Usage: stackcollapse.4gl.py [options] [infile] > output.folded

    -ot   # Generate stacks using time spent per stack (default)
    -oc   # Generate stacks using number of calls per stack
```

## Limitations

The Genero profiler does not provide information about the module where a function is, so if your program
uses several modules, with functions with the same name, we will not be able to know which function is
in which module.

stackcollapse-4gl.py will try to identify each one using the number of calls, but you know, it's not a
100% secure method... ;) Anyway, it will do a good job in most of cases.
