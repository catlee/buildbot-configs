# -*- Python -*-

from buildbot.process.buildstep import BuildStep
from buildbot import buildset
from buildbot.buildset import BuildSet
from buildbot.scheduler import Scheduler
from buildbot.sourcestamp import SourceStamp
from buildbot.steps.shell import ShellCommand, WithProperties
from buildbot.process.buildstep import BuildStep
from buildbot.process.factory import BuildFactory
from buildbot.steps.transfer import FileDownload
from buildbot.status.builder import SUCCESS, WARNINGS, FAILURE, SKIPPED, EXCEPTION

import buildbotcustom.steps.misc
reload(buildbotcustom.steps.misc)
from buildbotcustom.steps.misc import FindFile, SetBuildProperty

import re, urllib, sys, os
from time import mktime, strptime, strftime, localtime
from datetime import datetime
from os import path
import copy
import re
import time

MozillaEnvironments = { }

# platform SDK location.  we can build both from one generic template.
# modified from vc8 environment
MozillaEnvironments['vc8perf'] = {
    "MOZ_CRASHREPORTER_NO_REPORT": '1',
    "MOZ_NO_REMOTE": '1',
    "NO_EM_RESTART": '1',
    "XPCOM_DEBUG_BREAK": 'warn',
    "CYGWINBASE": 'C:\\cygwin',
    "PATH": 'C:\\Python24;' + \
            'C:\\Python24\\Scripts;' + \
            'C:\\cygwin\\bin;' + \
            'C:\\WINDOWS\\System32;' + \
            'C:\\program files\\gnuwin32\\bin;' + \
            'C:\\WINDOWS;'
}

MozillaEnvironments['linux'] = {
    "MOZ_CRASHREPORTER_NO_REPORT": '1',
    "MOZ_NO_REMOTE": '1',
    "NO_EM_RESTART": '1',
    "XPCOM_DEBUG_BREAK": 'warn',
    "DISPLAY": ":0",
}

MozillaEnvironments['mac'] = {
    "MOZ_NO_REMOTE": '1',
    "NO_EM_RESTART": '1',
    "XPCOM_DEBUG_BREAK": 'warn',
    "MOZ_CRASHREPORTER_NO_REPORT": '1',
    # for extracting dmg's
    "PAGER": '/bin/cat',
}

class noMergeSourceStamp(SourceStamp):
    def canBeMergedWith(self, other):
        return False

class noMergeMultiScheduler(Scheduler):
    """Disallow build requests to be merged"""
    def __init__(self, numberOfBuildsToTrigger=2, **kwargs):
        self.numberOfBuildsToTrigger = numberOfBuildsToTrigger
        Scheduler.__init__(self, **kwargs)

    def fireTimer(self):
        self.timer = None
        self.nextBuildTime = None
        changes = self.importantChanges + self.unimportantChanges
        self.importantChanges = []
        self.unimportantChanges = []

        # submit
        for i in range(0, self.numberOfBuildsToTrigger):
            ss = noMergeSourceStamp(changes=changes)
            bs = buildset.BuildSet(self.builderNames, ss)
            self.submitBuildSet(bs)

class MozillaWgetLatest(ShellCommand):
    """Download built Firefox client from nightly staging directory."""
    haltOnFailure = True
    
    def __init__(self, url, filenameSearchString, branch="HEAD", fileURL="",
                 command=None, **kwargs):
        ShellCommand.__init__(self, **kwargs)
        self.addFactoryArguments(url=url,
                                 filenameSearchString=filenameSearchString,
                                 branch=branch, fileURL=fileURL,
                                 command=command)
        self.url = url
        self.filenameSearchString = filenameSearchString
        self.branch = branch
        self.fileURL = fileURL
        self.command = command or ["wget"]
    
    def getFilename(self):
        return self.filename
    
    def describe(self, done=False):
        return ["Wget Download"]

    def setBuild(self, build):
        ShellCommand.setBuild(self, build)
        self.changes = build.source.changes
        self.fileURL = self.changes[-1].files[0]
        self.filename = os.path.basename(self.fileURL)
        self.setProperty("fileURL", self.fileURL)
        self.setProperty("filename", self.filename)
        timestamp_re = re.compile('[^\d]*(\d*-\d*-\d*_\d*:\d*).*')
        #lie about start time
        match = timestamp_re.search(self.fileURL)
        if match:
            try:
                timestamp = int(time.mktime(time.strptime(match.group(1), '%Y-%m-%d_%H:%M')))
                self.changes[-1].when = timestamp
            except:
                pass
    
    def start(self):
        self.setCommand(["wget", "-nv", "-N", "--no-check-certificate", self.fileURL])
        ShellCommand.start(self)
    
    def evaluateCommand(self, cmd):
        superResult = ShellCommand.evaluateCommand(self, cmd)
        if SUCCESS != superResult:
            return FAILURE
        if None != re.search('ERROR', cmd.logs['stdio'].getText()):
            return FAILURE
        return SUCCESS


class MozillaTryServerWgetLatest(MozillaWgetLatest):
    def evaluateCommand(self, cmd):
        # Strip the platform and extension off of the filename.
        # The rest of it is the identifier.
        identifier = self.getProperty("filename").rsplit('-', 1)[0]
        # Grab the submitter out of the dir name. CVS and Mercurial builds
        # are a little different, so we need to try fairly hard to find
        # the e-mail address.
        dir = path.basename(path.dirname(self.getProperty("fileURL")))
        who = ''
        for section in dir.split('-'):
            if '@' in section:
                who = section
                break

        msg =  'TinderboxPrint: %s\n' % who
        msg += 'TinderboxPrint: %s\n' % identifier
        self.addCompleteLog("header", msg)

        superResult = ShellCommand.evaluateCommand(self, cmd)
        if SUCCESS != superResult:
            return FAILURE
        if None != re.search('ERROR', cmd.logs['stdio'].getText()):
            return FAILURE
        return SUCCESS
    

class MozillaInstallZip(ShellCommand):
    """Install given file, unzipping to executablePath"""
    
    def __init__(self, filename="", branch="", command=None, **kwargs):
        ShellCommand.__init__(self, **kwargs)
        self.addFactoryArguments(filename=filename, branch=branch,
                                 command=command)
        self.filename = filename
        self.branch = branch
        self.command = command or ["unzip", "-o"]
    
    def describe(self, done=False):
        return ["Install zip"]
    
    def start(self):
        # removed the mkdir because this happens on the master, not the slave
        if not self.filename:
            if self.branch:
                self.filename = self.getProperty("filename")
            else:
                return FAILURE
        if self.filename:
            self.command = self.command[:] + [self.filename]
        ShellCommand.start(self)
    
    def evaluateCommand(self, cmd):
        superResult = ShellCommand.evaluateCommand(self, cmd)
        if SUCCESS != superResult:
            return FAILURE
        if None != re.search('ERROR', cmd.logs['stdio'].getText()):
            return FAILURE
        if None != re.search('Usage:', cmd.logs['stdio'].getText()):
            return FAILURE
        return SUCCESS
    

class MozillaUpdateConfig(ShellCommand):
    """Configure YAML file for run_tests.py"""
   
    def __init__(self, branch, executablePath, branchName, addOptions=[],
                 useSymbols=False, **kwargs):
        ShellCommand.__init__(self, **kwargs)
        self.addFactoryArguments(branch=branch, executablePath=executablePath,
                                 branchName=branchName, addOptions=addOptions,
                                 useSymbols=useSymbols)
        self.branch = branch
        self.exePath = executablePath
        self.branchName = branchName
        self.addOptions = addOptions
        self.useSymbols = useSymbols

    def setBuild(self, build):
        ShellCommand.setBuild(self, build)
        self.title = build.slavename
        self.changes = build.source.changes
        self.buildid = strftime("%Y%m%d%H%M", localtime(self.changes[-1].when))
        if not self.command:
            self.setCommand(["python", "PerfConfigurator.py", "-v", "-e", self.exePath, "-t", self.title, "-b", self.branch, "-d", self.buildid, "-i", self.buildid, "--branchName", self.branchName] + self.addOptions)

    def describe(self, done=False):
        return ["Update config"]
    
    def evaluateCommand(self, cmd):
        superResult = ShellCommand.evaluateCommand(self, cmd)
        if SUCCESS != superResult:
            return FAILURE
        stdioText = cmd.logs['stdio'].getText()
        if None != re.search('ERROR', stdioText):
            return FAILURE
        if None != re.search('USAGE:', stdioText):
            return FAILURE
        configFileMatch = re.search('outputName\s*=\s*(\w*?.yml)', stdioText)
        if not configFileMatch:
            return FAILURE
        else:
            self.setProperty("configFile", configFileMatch.group(1))
        return SUCCESS
    

class MozillaRunPerfTests(ShellCommand):
    """Run the performance tests"""
    
    def __init__(self, branch, command=None, **kwargs):
        ShellCommand.__init__(self, **kwargs)
        self.addFactoryArguments(branch=branch, command=command)
        self.branch = branch
        self.command = command or ["python", "run_tests.py"]
    
    def describe(self, done=False):
        return ["Run performance tests"]
    
    def createSummary(self, log):
        summary = []
        for line in log.readlines():
            if "RETURN:" in line:
                summary.append(line.replace("RETURN:", "TinderboxPrint:"))
            if "FAIL:" in line:
                summary.append(line.replace("FAIL:", "TinderboxPrint:FAIL:"))
        self.addCompleteLog('summary', "\n".join(summary))
    
    def start(self):
        """docstring for start"""
        self.command = copy.copy(self.command)
        self.command.append(self.getProperty("configFile"))
        ShellCommand.start(self)
    
    def evaluateCommand(self, cmd):
        superResult = ShellCommand.evaluateCommand(self, cmd)
        stdioText = cmd.logs['stdio'].getText()
        if SUCCESS != superResult:
            return FAILURE
        if None != re.search('ERROR', stdioText):
            return FAILURE
        if None != re.search('USAGE:', stdioText):
            return FAILURE
        if None != re.search('FAIL:', stdioText):
            return WARNINGS
        return SUCCESS

class MozillaInstallTarBz2(ShellCommand):
    """Install given file, unzipping to executablePath"""
    
    def __init__(self, filename="", branch="", command=None, **kwargs):
        ShellCommand.__init__(self, **kwargs)
        self.addFactoryArguments(filename=filename, branch=branch,
                                 command=command)
        self.filename = filename
        self.branch = branch
        self.command = command or ["tar", "-jvxf"]
    
    def describe(self, done=False):
        return ["Install tar.bz2"]
    
    def start(self):
        if not self.filename:
            if self.branch:
                self.filename = self.getProperty("filename")
            else:
                return FAILURE
        if self.filename:
            self.command = self.command[:] + [self.filename]
        ShellCommand.start(self)
    
    def evaluateCommand(self, cmd):
        superResult = ShellCommand.evaluateCommand(self, cmd)
        if SUCCESS != superResult:
            return FAILURE
        return SUCCESS

class MozillaInstallTarGz(ShellCommand):
    """Install given file, unzipping to executablePath"""
    
    def __init__(self, filename="", branch="", command=None, **kwargs):
        ShellCommand.__init__(self, **kwargs)
        self.addFactoryArguments(filename=filename, branch=branch,
                                 command=command)
        self.filename = filename
        self.branch = branch
        self.command = command or ["tar", "-zvxf"]
    
    def describe(self, done=False):
        return ["Install tar.gz"]
    
    def start(self):
        if not self.filename:
            if self.branch:
                self.filename = self.getProperty("filename")
            else:
                return FAILURE
        if self.filename:
            self.command = self.command[:] + [self.filename]
        ShellCommand.start(self)
    
    def evaluateCommand(self, cmd):
        superResult = ShellCommand.evaluateCommand(self, cmd)
        if SUCCESS != superResult:
            return FAILURE
        return SUCCESS

class MozillaInstallDmg(ShellCommand):
    """Install given file, copying to workdir"""
    
    def __init__(self, filename="", branch="", command=None, **kwargs):
        ShellCommand.__init__(self, **kwargs)
        self.addFactoryArguments(filename=filename, branch=branch,
                                 command=command)
        self.filename = filename
        self.branch = branch
        self.command = command or ["bash", "installdmg.sh", "$FILENAME"]
    
    def describe(self, done=False):
        return ["Install dmg"]
    
    def start(self):
        if not self.filename:
            if self.branch:
                self.filename = self.getProperty("filename")
            else:
                return FAILURE

        self.command = self.command[:]
        for i in range(len(self.command)):
            if self.command[i] == "$FILENAME":
                self.command[i] = self.filename
        ShellCommand.start(self)
    
    def evaluateCommand(self, cmd):
        superResult = ShellCommand.evaluateCommand(self, cmd)
        if SUCCESS != superResult:
            return FAILURE
        return SUCCESS

class MozillaInstallDmgEx(ShellCommand):
    """Install given file, copying to workdir"""
    #This is a temporary class to test the new InstallDmg script without affecting the production mac machines
    # if this works everything should be switched over the using it

    def __init__(self, filename="", branch="", command=None, **kwargs):
        ShellCommand.__init__(self, **kwargs)
        self.addFactoryArguments(filename=filename, branch=branch,
                                 command=command)
        self.filename = filename
        self.branch = branch
        self.command = command or ["expect", "installdmg.ex"]

    def describe(self, done=False):
        return ["Install dmg"]

    def start(self):
        if not self.filename:
            if self.branch:
                self.filename = self.getProperty("filename")
            else:
                return FAILURE
        if self.filename:
            self.command = self.command[:] + [self.filename]
        ShellCommand.start(self)

    def evaluateCommand(self, cmd):
        superResult = ShellCommand.evaluateCommand(self, cmd)
        if SUCCESS != superResult:
            return FAILURE
        return SUCCESS


class TalosFactory(BuildFactory):
    """Create working talos build factory"""
        
    winClean   = ["touch temp.zip &", "rm", "-rf", "*.zip", "talos/", "firefox/"]
    macClean   = "rm -vrf *"   
    linuxClean = "rm -vrf *" 
      
    def __init__(self, OS, envName, buildBranch, branchName, configOptions, buildSearchString, buildDir, talosCmd, customManifest='', cvsRoot=":pserver:anonymous@cvs-mirror.mozilla.org:/cvsroot"):
        BuildFactory.__init__(self)
        if OS in ('linux', 'linuxbranch',):
            cleanCmd = self.linuxClean
        elif OS in ('win',):
            cleanCmd = self.winClean
        else:
            cleanCmd = self.macClean
        self.addStep(ShellCommand(
                           workdir=".",
                           description="Cleanup",
                           command=cleanCmd,
                           env=MozillaEnvironments[envName]))
        self.addStep(FileDownload(
                           mastersrc="scripts/count_and_reboot.py",
                           slavedest="count_and_reboot.py",
                           workdir="."))
        self.addStep(ShellCommand(
                           command=["cvs", "-d", cvsRoot, "co", "-d", "talos",
                                    "mozilla/testing/performance/talos"],
                           workdir=".",
                           description="checking out talos",
                           haltOnFailure=True,
                           flunkOnFailure=True,
                           env=MozillaEnvironments[envName]))
        self.addStep(FileDownload(
                           mastersrc="scripts/generate-tpcomponent.py",
                           slavedest="generate-tpcomponent.py",
                           workdir="talos/page_load_test"))
        if customManifest != '':
            self.addStep(FileDownload(
                           mastersrc=customManifest,
                           slavedest="manifest.txt",
                           workdir="talos/page_load_test"))
        self.addStep(ShellCommand(
                           command=["python", "generate-tpcomponent.py"],
                           workdir="talos/page_load_test",
                           description="setting up pageloader",
                           haltOnFailure=True,
                           flunkOnFailure=True,
                           env=MozillaEnvironments[envName]))
        self.addStep(MozillaTryServerWgetLatest(
                           workdir=".",
                           branch=buildBranch,
                           url=buildDir,
                           filenameSearchString=buildSearchString,
                           env=MozillaEnvironments[envName]))
        #install the browser, differs based upon platform
        if OS == 'linux':
            self.addStep(MozillaInstallTarBz2(
                               workdir=".",
                               branch=buildBranch,
                               haltOnFailure=True,
                               env=MozillaEnvironments[envName]))
        elif OS == 'linuxbranch': #special case for old linux builds
            self.addStep(MozillaInstallTarGz(
                           workdir=".",
                           branch=buildBranch,
                           haltOnFailure=True,
                           env=MozillaEnvironments[envName]))
        elif OS == 'win':
            self.addStep(MozillaInstallZip(
                               workdir=".",
                               branch=buildBranch,
                               haltOnFailure=True,
                               env=MozillaEnvironments[envName]))
            self.addStep(ShellCommand(
                               workdir="firefox/",
                               flunkOnFailure=False,
                               warnOnFailure=False,
                               description="chmod files (see msys bug)",
                               command=["chmod", "-v", "-R", "a+x", "."],
                               env=MozillaEnvironments[envName]))
        elif OS == 'tiger':
            self.addStep(FileDownload(
                           mastersrc="scripts/installdmg.sh",
                           slavedest="installdmg.sh",
                           workdir="."))
            self.addStep(MozillaInstallDmg(
                               workdir=".",
                               branch=buildBranch,
                               haltOnFailure=True,
                               env=MozillaEnvironments[envName]))
        else: #leopard
            self.addStep(FileDownload(
                           mastersrc="scripts/installdmg.ex",
                           slavedest="installdmg.ex",
                           workdir="."))
            self.addStep(MozillaInstallDmgEx(
                               workdir=".",
                               branch=buildBranch,
                               haltOnFailure=True,
                               env=MozillaEnvironments[envName]))
        if OS in ("tiger", "leopard"):
            self.addStep(FindFile(
             workdir="talos",
             filename="firefox-bin",
             directory="..",
             max_depth=4,
             property_name="exepath",
             name="Find executable",
             filetype="file"
            ))
        elif OS in ('xp', 'vista', 'win'):
            self.addStep(SetBuildProperty(
             property_name="exepath",
             value="../firefox/firefox"
            ))
        else:
            self.addStep(SetBuildProperty(
             property_name="exepath",
             value="../firefox/firefox-bin"
            ))
        exepath = WithProperties('%(exepath)s')

        self.addStep(MozillaUpdateConfig(
                           workdir="talos/",
                           branch=buildBranch,
                           branchName=branchName,
                           haltOnFailure=True,
                           executablePath=exepath,
                           addOptions=configOptions,
                           env=MozillaEnvironments[envName]))
        self.addStep(MozillaRunPerfTests(
                           warnOnWarnings=True,
                           workdir="talos/",
                           branch=buildBranch,
                           timeout=21600,
                           haltOnFailure=True,
                           command=talosCmd,
                           env=MozillaEnvironments[envName]))
        self.addStep(ShellCommand(
                           flunkOnFailure=False,
                           warnOnFailure=False,
                           alwaysRun=True,
                           workdir='.',
                           description="reboot after 1 test run",
                           command=["python", "count_and_reboot.py", "-f", "../talos_count.txt", "-n", "1", "-z"],
                           env=MozillaEnvironments[envName]))
