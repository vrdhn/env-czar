#!/usr/bin/env python3

# License: GPL v3 or later



import os
import os.path
import sys



def read_envtxt(dir):
    ret = []
    try:
        with  open(os.path.join(dir,'env.txt')) as et:
            ret = [ x.split() for x in et.readlines()]
        return [ x for x in ret if x != [] ]
    except:
        return ret        



def read_allenvtxt():
    ret = []
    dir = os.getcwd()
    home = os.environ['HOME']
    while dir != '/' and dir != home:
        ret.extend(read_envtxt(dir))
        dir = os.path.dirname(dir)
    ## Read HOME~
    ret.extend(read_envtxt(home))
    return ret

## contents of all envtxts in correct order
envtxts     = read_allenvtxt()
## user forced -foo/+foo in shell-session
selected   = [x for x in os.environ.get("_tools","").split(':') if x != '']
## +/- directives fron envtxt files
directives = [ x[0] for x  in envtxts if x[0][0] in set(['+','-'])]
## what envvars we changed last time user ran
envvars    =  { x:[] for x in os.environ.get("_evars","").split(':') if x != ''}
## command line .. what user wants to change
changes    = [x for x in sys.argv[1:] if x[0] in set(['+','-'])]




## Apply changes and update selected
for c in changes:
    if c[0] == '-':
        tofind = '+' + c[1:]
    else:
        tofind = '-' + c[1:]
    try:
        selected.remove(tofind)
    except:
        pass
    selected.append(c)

## Finally generate the values...
for t in envtxts:
    if t[0][0] in set(['+','-']):
        continue
    ok = False
    if ('+'+t[0]) in selected:
        ok = True
    elif ('-'+t[0]) in selected:
        ok = False
    else:
        if ('+'+t[0]) in directives:
            ok = True
        else:
            ok = False
    if ok:
        if t[1] not in envvars: envvars[t[1]] = []
        envvars[t[1]].extend(t[2:])
        
for v in envvars:
    print('%s=%s;export %s;'%(v,':'.join([ "%s"%(x) for x in envvars[v]]),v))


print('_tools=%s; export _tools;echo $_tools' % ( ':'.join(selected)))
print('_evars=%s; export _evars;echo $_evars' % ( ':'.join(envvars)))    

