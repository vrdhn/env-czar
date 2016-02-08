# env-czar

env-czar takes over environment variables.
you create several env.txt files 
and  use '+feature' / '-feature' to override env.txt settings


# installation

place the env-czar.py anywhere ( or git clone this repo )

put in your `~/.bashrc`

    e ()
    {
	eval $(/usr/bin/python3 <path_to_env-czar>/env-czar.py "$@")
    }


You are free to use any command instead of `e`
Specifying full path to python3 will help survive bad PATH.

Now you need to create lot of  env.txt files


# env.txt files & operation

env.txt file are like this

    sys PATH /usr/bin/
    :seperator MAVEN_OPTS <space>
    +java
    -sys

First symbol, name is what you'll use at command line to
turn on/off the fature. The other two are easy to guess.
generally there is no need of `-foo` pattern.

The value, if starts with './', indicates path relative to 
current directory, and gets converted to absolute path

the `env.txt` can be placed at several places in the directory tree.
When `e` is executed, the environment variables will be regenerated
based on all the env.txt files in the hiererchical path, and the 
env.txt in `HOME`.

The arguments to `e` can be used to force turn feature(s) off or on.

    e +foo  <--- turns foo feature on
    e -foo <--- turns foo fature off



# example

~/env.txt:

    java PATH /data/tools/jdk/bin
    maven PATH /data/tools/mvn/bin
    eclipse PATH /data/tools/eclipse
	
    my PATH ~/bin
    my PATH ~/scripts
    sys PATH /usr/bin

    +my
    +sys


~/projects/env.txt

    +java
    +maven

~/projects/prj1/env.txt

    prj PATH ~/projects/prj1/bin


and then the interactions:

    $ cd ~
    $ e
    $ cd ~/projects
    $ e
    $ cd ~/projects/prj1
    $ e

 
