from buildbot.steps.shell import Compile, ShellCommand

import os.path

import buildbotcustom.steps.misc
import buildbotcustom.steps.test
import buildbotcustom.steps.transfer
import buildbotcustom.steps.updates

from buildbotcustom.steps.misc import SetMozillaBuildProperties
from buildbotcustom.steps.test import AliveTest, CompareBloatLogs, \
  CompareLeakLogs, Codesighs, GraphServerPost
from buildbotcustom.steps.transfer import MozillaStageUpload
from buildbotcustom.steps.updates import CreateCompleteUpdateSnippet

from buildbot.steps.shell import SetProperty, WithProperties

GRAPH_SERVER = 'graphs.mozilla.org'
GRAPH_SELECTOR = '/server/collect.cgi'
GRAPH_BRANCH = 'comm-central'

def addLeakTestSteps(self,branch,platform,platformName):
        # we want the same thing run a few times here, with different
        # extraArgs
        env = platform['env']
        objdir = platform['platform_objdir']

        self.graphSelector = GRAPH_SELECTOR
        self.graphServer   = GRAPH_SERVER
        self.graphBranch   = GRAPH_BRANCH
        self.baseName      = platform['base_name']
        
        if platformName.startswith("win32"):
            moz_objdir = "%s\\mozilla" % objdir
        else:
            moz_objdir = "%s/mozilla" % objdir
        
        self.addStep(ShellCommand,
         command=['make', 'buildsymbols'],
         env=env,
         workdir='build/%s' % objdir,
         haltOnFailure=True,
         timeout=60*30,
        )

        self.addStep(SetProperty,
         command=['bash', '-c', 'pwd'],
         property='toolsdir',
         workdir='tools'
        )

        platform_minidump_path = {
            'linux': WithProperties('%(toolsdir:-)s/breakpad/linux/minidump_stackwalk'),
            'win32': WithProperties('%(toolsdir:-)s/breakpad/win32/minidump_stackwalk.exe'),
            'macosx': WithProperties('%(toolsdir:-)s/breakpad/osx/minidump_stackwalk'),
            }

        env['MINIDUMP_STACKWALK'] = platform_minidump_path[platformName]

        leak_threshold = platform.get('leak_threshold', branch.get('leak_threshold', 7261838))
        self.addStep(ShellCommand,
            env=env,
            command=['python','mailnews/test/performance/bloat/runtest.py',
                     '--objdir', objdir, 
                     '--bin', branch['appname'], 
                     '--brand', branch['brand_name'], 
                    ],
            warnOnFailure=True,
            haltOnFailure=True,
            flunkOnFailure=True,
        )
        self.addStep(ShellCommand,
         env=env,
         command=['cp', 'bloat.log', '../bloat.log'],
        )
        self.addStep(CompareBloatLogs,
         bloatLog='bloat.log',
         mozillaDir="/mozilla",
         env=env,
         testnameprefix='Mail',
         testname='Mail',
         workdir='.',
         haltOnFailure=False,
        )

        self.addStep(SetProperty,
          command=['python', 'build/mozilla/config/printconfigsetting.py',
          'build/objdir-tb/mozilla/dist/bin/application.ini',
          'App', 'BuildID'],
          property='buildid',
          workdir='.',
          description=['getting', 'buildid'],
          descriptionDone=['got', 'buildid']
        )
        self.addStep(SetProperty,
          command=['python', 'build/mozilla/config/printconfigsetting.py',
          'build/objdir-tb/mozilla/dist/bin/application.ini',
          'App', 'SourceStamp'],
          property='sourcestamp',
          workdir='.',
          description=['getting', 'sourcestamp'],
          descriptionDone=['got', 'sourcestamp']
        )

#        self.addStep(GraphServerPost,
#         server=self.graphServer,
#         selector=self.graphSelector,
#         branch=self.graphBranch,
#         resultsname=self.baseName,
#        )
        self.addStep(ShellCommand,
         env=env,
         command=['cp', 'malloc.log','../malloc.log',],
        )
        self.addStep(ShellCommand,
         env=env,
         command=['cp', 'sdleak.log', '../sdleak.log',],
        )
        self.addStep(CompareLeakLogs,
         mallocLog='../malloc.log',
         platform=platformName,
         leakFailureThreshold=leak_threshold,
         env=env,
         objdir=moz_objdir,
         testname='current',
         testnameprefix='Mail',
         haltOnFailure=False,
        )
#        self.addStep(GraphServerPost,
#         server=self.graphServer,
#         selector=self.graphSelector,
#         branch=self.graphBranch,
#         resultsname=self.baseName
#        )
        self.addStep(CompareLeakLogs,
         mallocLog='../malloc.log.old',
         platform=platformName,
         leakFailureThreshold=leak_threshold,
         env=env,
         objdir=moz_objdir,
         testname='previous',
         testnameprefix='Mail',
         haltOnFailure=False,
        )
        self.addStep(ShellCommand,
         env=env,
         workdir='.',
         command=['bash', '-c',
                  'perl build/mozilla/tools/trace-malloc/diffbloatdump.pl '
                  '--depth=15 --use-address /dev/null sdleak.log '
                  '> sdleak.tree']
        )
        self.addStep(ShellCommand,
          env=env,
          command=['cp', '../sdleak.log', '../sdleak.log.old'],
        )
        self.addStep(ShellCommand,
          env=env,
          command=['cp', '../malloc.log', '../malloc.log.old'],
        )
        self.addStep(ShellCommand,
          env=env,
          command=['cp', '../bloat.log', '../bloat.log.old'],
        )
        if platformName in ('macosx', 'linux'):
            self.addStep(ShellCommand,
             env=env,
             workdir='.',
             command=['cp', 'sdleak.tree', 'sdleak.tree.raw']
            )
            self.addStep(ShellCommand,
             env=env,
             workdir='.',
             timeout=60*60, # Very IO/CPU intensive, give it an hour to complete
             command=['/bin/bash', '-c', 
                      'perl '
                      'build/mozilla/tools/rb/fix-%s-stack.pl '
                      'sdleak.tree.raw '
                      '> sdleak.tree' % platformName]
            )
        self.addStep(ShellCommand,
         env=env,
         command=['perl', 'mozilla/tools/trace-malloc/diffbloatdump.pl',
                  '--depth=15', '../sdleak.tree.old', '../sdleak.tree'],
         haltOnFailure=False,
        )
        self.addStep(ShellCommand,
          env=env,
          command=['cp', '../sdleak.tree', '../sdleak.tree.old'],
        )

