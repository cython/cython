import bisect, sys

# This module keeps track of arbitrary "states" at any point of the code. 
# A state is considered known if every path to the given point agrees on
# its state, otherwise it is None (i.e. unknown). 

# It might be useful to be able to "freeze" the set of states by pushing 
# all state changes to the tips of the trees for fast reading. Perhaps this
# could be done on get_state, clearing the cache on set_state (assuming 
# incoming is immutable). 

# This module still needs a lot of work, and probably should totally be 
# redesigned. It doesn't take return, raise, continue, or break into 
# account. 

_END_POS = ((unichr(sys.maxunicode)*10),())

class ControlFlow:

    def __init__(self, start_pos, incoming, parent):
        self.start_pos = start_pos
        self.incoming = incoming
        if parent is None and incoming is not None:
            parent = incoming.parent
        self.parent = parent
        self.tip = {}
        self.end_pos = _END_POS
        
    def start_branch(self, pos):
        self.end_pos = pos
        branch_point = BranchingControlFlow(pos, self)
        if self.parent is not None:
            self.parent.branches[-1] = branch_point
        return branch_point.branches[0]
    
    def next_branch(self, pos):
        self.end_pos = pos
        return self.parent.new_branch(pos)
        
    def finish_branch(self, pos):
        self.end_pos = pos
        self.parent.end_pos = pos
        return LinearControlFlow(pos, self.parent)
        
    def get_state(self, item, pos=_END_POS):
        return self.get_pos_state(item, pos)[1]
        
    def get_pos_state(self, item, pos=_END_POS):
        # do some caching
        if pos > self.end_pos:
            try:
                return self.tip[item]
            except KeyError:
                self.tip[item] = pos_state = self._get_pos_state(item, pos)
                return pos_state
        else:
            return self._get_pos_state(item, pos)
        
class LinearControlFlow(ControlFlow):

    def __init__(self, start_pos=(), incoming=None, parent=None):
        ControlFlow.__init__(self, start_pos, incoming, parent)
        self.events = {}
            
    def set_state(self, pos, item, state):
        if item in self.tip:
            del self.tip[item]
        if pos < self.start_pos:
            if self.incoming is not None:
                self.incoming.set_state(pos, item, state)
        else:
            if item in self.events:
                event_list = self.events[item]
            else:
                event_list = []
                self.events[item] = event_list
            bisect.insort(event_list, (pos, state))
            
        
    def _get_pos_state(self, item, pos):
        if pos > self.start_pos:
            if item in self.events:
                event_list = self.events[item]
                for event in event_list[::-1]:
                    if event[0] < pos:
                        return event
                        
        if self.incoming is not None:
            return self.incoming.get_pos_state(item, pos)
        
        else:
            return None, None
            
    def to_string(self, indent='', limit=None):
    
        if len(self.events) == 0:
            s = indent + "[no state changes]"
            
        else:
            all = []
            for item, event_list in self.events.items():
                for pos, state in event_list:
                    all.append((indent, pos, item, state))
            all.sort()
            all = ["%s%s: %s <- %s" % data for data in all]
            s = "\n".join(all)
        if self.incoming is not limit and self.incoming is not None:
            s = "%s\n%s" % (self.incoming.to_string(indent, limit=limit), s)
        return s
    
    
class BranchingControlFlow(ControlFlow):
    
    def __init__(self, start_pos, incoming, parent=None):
        ControlFlow.__init__(self, start_pos, incoming, parent)
        self.branches = [LinearControlFlow(start_pos, incoming, parent=self)]
        self.branch_starts = [start_pos]
        
    def set_state(self, pos, item, state):
    
        if item in self.tip:
            del self.tip[item]
        
        if pos < self.start_pos:
            self.incoming.set_state(pos, item, state)
        else:
            for branch_pos, branch in zip(self.branch_starts[::-1], self.branches[::-1]):
                if pos >= branch_pos:
                    branch.set_state(pos, item, state)
                    return
    
    def _get_pos_state(self, item, pos):
        if pos <= self.start_pos:
            return self.incoming.get_pos_state(item, pos)
        elif pos < self.end_pos:
            for branch_pos, branch in zip(self.branch_starts[::-1], self.branches[::-1]):
                if pos >= branch_pos:
                    return branch.get_pos_state(item, pos)
        else:
            last_pos, last_state = self.branches[0].get_pos_state(item, pos)
            if last_state is None:
                return None, None
            for branch in self.branches[1:]:
                other_pos, other_state = branch.get_pos_state(item, pos)
                if other_state is None or other_state != last_state:
                    return None, None
                elif last_pos is not other_pos:
                    last_pos = max(last_pos, other_pos)
            return last_pos, last_state

    def new_branch(self, pos):
        self.branches.append(LinearControlFlow(pos, self.incoming, parent=self))
        self.branch_starts.append(pos)
        return self.branches[-1]

    def to_string(self, indent='', limit=None):
        join = "\n%sor\n" % indent
        s = join.join([branch.to_string(indent+"    ", limit=self.incoming) for branch in self.branches])
        if self.incoming is not limit and self.incoming is not None:
            s = "%s\n%s" % (self.incoming.to_string(indent, limit=limit), s)
        return s
