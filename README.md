# randasm
Dead simple, retargetable random generator of assembly source files.

This Python module is meant to generate standalone, complete assembly source files. 
Each file will contain a configurable number of randomly selected instructions with parameters chosen randomly. 
Each instruction (or instruction block) is generated independently form all previous instructions.

The instructions and their parameters, as well as the general shape of the complete file, is defined for each *target* in a YAML file. The target-dependent information includes both the CPU and the assembler whose syntax is to be used -- this module generates *assembly* files, not binaries.

(The format of the YAML template file will be described here eventually.)



## Installation

This is an installable Python module; you can use [pip](https://docs.python.org/2.7/installing/index.html) directly form this repo:

`   pip install git+https://github.com/jaruiz/randasm --process-dependency-links`

Presumably you will be doing that in a [virtual environment](https://virtualenv.pypa.io/en/stable/).

The module relies on some data that is stored in the package directory so bear that in mind if you chose to just copy the code to your project.

*(I hesitate to move this module into PyPi, it's so irrelevant. I may do so when it becomes somewhat stable.)*


## Usage

After installation, you get two new commands:

```   
  randasm
  randasm-quickcheck
```

Running `randasm --help` gets you this help text:

```
  usage: randasm [-h] [--target {mcs51-asem51,i8080-asl}] [--target-def FILE]
                 [-n NUM] [--raw]

  Build random assembly program source for the specified target (CPU/Assembler)

  optional arguments:
    -h, --help            show this help message and exit
    --target {mcs51-asem51,i8080-asl}
                          select one of the predefined targets
    --target-def FILE     select user-supplied target definition file
    -n NUM, --num NUM     number of instructions
    --raw                 emit only random instructions with no assembly wrapper

  See README.md for a longer description, including an explanation of the target
  file format.
```

As you see, the help text refers to this README file and this file refers to the help text... for the time being that information will have to suffice.

As for the `randasm-quickcheck` script, it's a small self-check script that builds a number of random files and assembles them with the assembler executable of your choice.  
For instance, this will build and assemble 4 random files for the MCS51/ASEM51 target, with ~200 instructions each:

```
    randasm-quickcheck mcs51-asem51 ~/dev/tools/asem51/asem 200 4
```

That's the path to my local copy of [asem51](http://plit.de/asem-51/) in there, you need to supply yours.   
Running this will get you a bunch of object files in an `./output` directory _OR_ error messages. 



## Caveats

This is a work in progress. Specifically:

* This readme file needs to be fleshed out, including a description of the template yaml file.
* The `--target-def` option has not been tested.
* The generated code has been assembled but it has never been tried in simulation.
* The templates may need to incorporate init code, which would introduce a dependence on the simulation platform.
* The i8080 template file does not have any jump instructions.
* The code generation script could use a few comments in some non-evident code spots.




## Disclaimer

I have worked in real CPU testing projects professionally in the past. This module contains no code and no ideas *at all* from my previous work and it will remain that way. 



