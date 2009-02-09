import time

from urllib2 import urlopen
from twisted.python import log, failure
from twisted.internet import defer, reactor
from twisted.internet.task import LoopingCall

from buildbot.changes import base, changes

class InvalidResultError(Exception):
    def __init__(self, value="InvalidResultError"):
        self.value = value
    def __str__(self):
        return repr(self.value)

class EmptyResult(Exception):
    pass

class NoMoreBuildNodes(Exception):
    pass

class NoMoreFileNodes(Exception):
    pass

class TinderboxResult:
    """I hold a list of dictionaries representing build nodes
        items = hostname, status and date of change"""
    
    nodes = []
    
    def __init__(self, nodes):
        self.nodes = nodes
    
    def __eq__(self, other):
        if len(self.nodes) != len(other.nodes):
            return False
        for i in range(len(self.nodes)):
            if self.nodes[i] != other.nodes[i]:
                return False
        
        return True
    
    def nodeForHostname(self, nameString):
        """returnt the node for a nameString"""
        for node in self.nodes:
            if nameString in node['hostname']:
                return node
        
        return None
    

class TinderboxParser:
    """I parse the pipe-delimited result from a Tinderbox quickparse query."""
    
    def __init__(self, tinderboxQuery):
        nodes = []
        f = urlopen(tinderboxQuery.geturl())
        s = f.read()
        f.close()
        lines = s.split('\n')
        for line in lines:
            if line == "": continue
            elements = line.split('|')
            if elements[0] == 'State': continue
            items = {'hostname': elements[2], 'status': elements[3], 'date': elements[4]}
            nodes.append(items)
        self.tinderboxResult = TinderboxResult(nodes)
    
    def getData(self):
        return self.tinderboxResult
    

class TinderboxPoller(base.ChangeSource):
    """This source will poll a tinderbox server for changes and submit
    them to the change master."""
    
    compare_attrs = ["tinderboxURL", "pollInterval", "tree", "branch"]
    
    parent = None # filled in when we're added
    loop = None
    volatile = ['loop']
    working = False
    
    def __init__(self, tinderboxURL, branch, tree="Firefox", machines=[], pollInterval=30):
        """
        @type   tinderboxURL:       string
        @param  tinderboxURL:       The base URL of the Tinderbox server
                                    (ie. http://tinderbox.mozilla.org)
        @type   tree:               string
        @param  tree:               The tree to look for changes in. 
                                    For example, Firefox trunk is 'Firefox'
        @type   branch:             string
        @param  branch:             The branch to look for changes in. This must
                                    match the 'branch' option for the Scheduler.
        @type   machines:           list
        @param  machines:           A list of machine names to search for. Changes will
                                    only register for machines that match individual 
                                    "machine" substrings
        @type   pollInterval:       int
        @param  pollInterval:       The time (in seconds) between queries for 
                                    changes
        """
        
        self.tinderboxURL = tinderboxURL
        self.tree = tree
        self.branch = branch
        self.machines = machines
        self.pollInterval = pollInterval
        self.previousChange = ''
        self.lastPoll = time.time()
        self.lastChange = time.time()
    
    def startService(self):
        self.loop = LoopingCall(self.poll)
        base.ChangeSource.startService(self)
        
        reactor.callLater(0, self.loop.start, self.pollInterval)
    
    def stopService(self):
        self.loop.stop()
        return base.ChangeSource.stopService(self)
    
    def describe(self):
        str = ""
        str += "Getting changes from the Tinderbox service running at %s " \
                % self.tinderboxURL
        str += "<br>Using tree: %s, branch %s, hostname %s" % (self.tree, self.branch, str(self.machines))
        return str
    
    def poll(self):
        if self.working:
            log.msg("Not polling Tinderbox because last poll is still working")
        else:
            self.working = True
            d = self._get_changes()
            d.addCallback(self._process_changes)
            d.addBoth(self._finished)
        return
    
    def _finished(self, res):
        assert self.working
        self.working = False
        
        # check for failure
        if isinstance(res, failure.Failure):
            log.msg("Tinderbox poll failed: %s" % res)
        return res
    
    def _make_url(self):
        # build the tinderbox URL
        url = self.tinderboxURL
        url += "/" + self.tree
        url += "/" + "quickparse.txt"
        
        return url
    
    def _get_changes(self):
        url = self._make_url()
        log.msg("Polling Tinderbox tree at %s" % url)
        
        self.lastPoll = time.time()
        # get the page, in pipe-delimited format
        return defer.maybeDeferred(urlopen, url)
    
    def _process_changes(self, query):
        try:
            tp = TinderboxParser(query)
            buildList = tp.getData()
        except InvalidResultError, e:
            log.msg("Could not process Tinderbox query: " + e.value)
            return
        except EmptyResult:
            return
        
        # check machine substring in result set
        result = TinderboxResult([])
        for machine in self.machines:
            node = buildList.nodeForHostname(machine)
            if node:
                result.nodes.append(node)
        if not result.nodes:
            return
        
        # see if there are any new changes
        if self.previousChange:
            if (self.previousChange == result.nodes):
                return
            oldResults = result.nodes
            result.nodes = []
            for node in oldResults:
                if node not in self.previousChange:
                    result.nodes.append(node)
            self.previousChange = oldResults
        else:
            self.previousChange = result.nodes
            return
        
        allBuildDates = []
        for buildNode in result.nodes:
            buildDate = int(buildNode['date'])
            if self.lastChange > buildDate:
                # change too old
                continue
            allBuildDates.append(buildDate)
            # ignore if build is busted
            if buildNode['status'] <> 'success':
                continue
            c = changes.Change(who = buildNode['hostname'],
                               files = ['TODO: filename goes here'],
                               comments = buildNode['status'],
                               branch = self.branch,
                               when = buildDate)
            self.parent.addChange(c)
        
        # do not allow repeats - count the last change as the largest
        # build start time that has been seen
        if allBuildDates:
            self.lastChange = max(allBuildDates)
    

