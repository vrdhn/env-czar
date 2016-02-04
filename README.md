# env-czar

env-czar takes over environment variables

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


# env.txt files

env.txt file are like this

    sys PATH /usr/bin/

First symbol, name is what you'll use at command line to
turn on/off the fature. The other two are easy to guess.

They should be place at the 'root' folder of project,
env.txt placed at user's home directory will also be ready.


# opration

env-czar will read all the env.txt file, starting from
current directory and moving up till hitting home or /

env-czar has a list of active tools, which are managed
by the function 'e' in bashrc

    e foo  <--- turns foo feature on
    e -foo <--- turns foo fature off


