#!/usr/bin/env python
from __future__ import unicode_literals, print_function

import commands
import os
import platform
import sys
from virtualenv import create_environment

colors = { "red": "31"
         , "green": "32"
         , "yellow": "33"
         , "gray": "37"
          }

def bail(msg):
    if platform.system() not in ('Windows'):
        msg = "\x1b[31m" + msg + "\x1b[0m"
    print(msg, file=sys.stderr)
    sys.exit(1)


# Check Python version.
# =====================

if sys.version_info < (2, 7):
    msg = "Gittip requires Python 2.7.x. You're using %s."
    bail(msg % platform.python_version())


# Check for existing virtualenv.
# ==============================

if os.path.isdir("env"):
    bail("""\
Directory 'env' already exists. Bailing, because bootstrap.py expects to be
able to create that directory. Have you already run bootstrap.py?""")
elif os.path.exists("env"):
    bail("""\
File 'env' exists (though it's not a directory). Bailing, because bootstrap.py
expects to be able to create that directory itself. What have you done?!""")


# Check for activated virtualenv.
# ===============================

if 'VIRTUAL_ENV' in os.environ:
    bail("""\
You're in a virtualenv. Please deactivate it and run again, because
bootstrap.py expects to create its own virtualenv.""")
if 'WORKING_ENV' in os.environ:
    bail("""\
You're in a workingenv (really?!). Please deactivate it and run again, because
bootstrap.py expects to create its own virtualenv.""")

create_environment( "env"
                  , site_packages=False
                  , clear=False
                  , unzip_setuptools=True
                  , use_distribute=True
                  , prompt="[gittip] "
                  , search_dirs=['vendor']
                  , never_download=True
                  , no_setuptools=True
                  , no_pip=False
                   )

WELCOME = """\
==============================================================================

                             Welcome to Gittip!
                             ~~~~~~~~~~~~~~~~~~

              Source:      https://github.com/gittip/www.gittip.com
              Production:  https://www.gittip.com/
              Local:       Right here! :D
              Help:        https://www.gittip.com/for/contributors/

------------------------------------------------------------------------------

Greetings, program! %(green)sSuccess!%(default_color)s You now have a so-called "Python virtual
environment" (a.k.a. a "virtualenv") at ./env/. Here's some real live %(ls)s
output:

    %(ls_output)s


This is your local development sandbox for Gittip. Next steps:

    1. %(green)s"Activate" your new virtualenv by running `%(activate)s`.%(default_color)s If
       your prompt sprouts a "[gittip] ", it worked. Activating a Python
       virtualenv configures your current shell session, and you need to do
       this every time you want to work with the virtualenv in a new shell
       session. To deactivate the virtualenv simply type "deactivate" (it can
       be tab-completed).

    2. %(green)sExplore the gittip cli.%(default_color)s Once you're in your virtualenv, you should
       have the gittip cli on your path. Try out the following commands to
       get started:

       [gittip] %(prompt)s gittip help
       [gittip] %(prompt)s gittip test
       [gittip] %(prompt)s gittip run


From here on out, everything happens with the gittip cli. Have fun! :)

=============================================================================="""

if platform.system() == 'Windows':
    listing = commands.getoutput("dir").splitlines()
    ls_output = "".join([line for line in listing if "env/" in line])
    if not ls_output:
        ls_output = "Eep!"
    welcome_config = { "green": ""
                     , "default_color": ""
                     , "activate": "env\\Scripts\\activate"
                     , "ls": "dir"
                     , "ls_output": ls_output
                     , "prompt": ">"
                      }
else:
    welcome_config = { "green": "\x1b[32m"
                     , "default_color": "\x1b[0m"
                     , "activate": "source env/bin/activate"
                     , "ls": "ls"
                     , "ls_output": commands.getoutput("ls -FGl | grep env/")
                     , "prompt": "$"
                      }
print(WELCOME % welcome_config)
