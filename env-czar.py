#!/usr/bin/env python3

# License: GPL v3 or later



import os
import os.path
import sys



def make_absolute(lvl,x):
    if len(x) < 2:
        return x
    ## a stupid assumptin that 1st two args are not ./<fo> (-:
    return( [ (os.path.realpath(os.path.join(lvl,k))
              if (k[0:2] == './') else k)
             for k in x])



def read_envtxt(dir):
    ret = []
    try:
        with  open(os.path.join(dir,'env.txt')) as et:
            ret = [ x.split() for x in et.readlines()]
        return [ make_absolute(dir,x) for x in ret if x != [] ]
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
## some env-vars may want to define seperators.. also map <space> is ' '
def mapsep(x):
    if x == '<space>': return ' '
    return x
seperators = { x[1]:mapsep(x[2]) for x  in envtxts if x[0] == ':seperator' }



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
tools=set()
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
        tools.add(t[0])
        if t[1] not in envvars: envvars[t[1]] = []
        envvars[t[1]].extend(t[2:])
        
for v in envvars:
    sep = seperators.get(v,':')
    print('%s="%s";export %s;'%(v,sep.join([ "%s"%(x) for x in envvars[v]]),v))


print('_tools=%s; export _tools;echo SEL: $_tools;' % ( ':'.join(selected)))
print('echo TOOLS: %s;' % ( ':'.join(tools)))
print('_evars=%s; export _evars;echo VARS: $_evars;' % ( ':'.join(envvars)))    

