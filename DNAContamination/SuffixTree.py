

class SuffixTree:
    """Class implementing the ADT SuffixTree"""


    #---------------------Nested _SuffixTreeNode class----------------------------
    class _SuffixTreeNode:
        """Non public class for storing a node"""

        def __init__(self, start=None, stop=None, parent=None, mark=None, child=None):
            """At the creation of a node we set the range of the substring that it contains,
            and the word which contains the substring from start to stop; we also inizialize
            the dict of children's node, the reference to its parent, and the depth of its
            parent."""
            self._start = start
            self._stop = stop
            self._parent = parent
            if parent is None or parent._start is None or parent._stop is None:
                self._parent_depth = 0
            else:
                self._parent_depth = parent._parent_depth + parent._stop - parent._start
            self._mark = ()
            self._add_mark(mark)
            if child is None:
                self._child = {}
            else:
                self._child = child

        def _add_mark(self, mark):
            if mark not in self._mark:
                if not isinstance(mark, tuple):
                    self._mark += (mark, )
                else:
                    self._mark += mark

        def _add_child(self, p_child, first_c):
            self._child.__setitem__(first_c, p_child)


    #--------------------Nested SuffixTreePosition class--------------------------
    class SuffixTreePosition:
        """An abstraction representing the location of an element of the tree"""

        def __init__(self, container, node):
            self._container = container
            self._node = node

        def _getstart(self):
            """It returns the value of start of the referenced node"""
            return self._node._start

        def _getstop(self):
            """It returns the value of stop of the referenced node """
            return self._node._stop

        def _getmark(self):
            return self._node._mark

        def _getchild(self):
            return self._node._child

        def __eq__(self, other):
            return type(other) is type(self) and other._node is self._node

        def __ne__(self, other):
            return not (self==other)

    #---------------------utility methods---------------------------------------
    def _validate(self, p):
        """Return associated node, if position p is valid. """
        if not isinstance(p, self.SuffixTreePosition):
          raise TypeError('p must be proper Position type')
        if p._container is not self:
          raise ValueError('p does not belong to this container')
        if p._node._parent is p._node:      # convention for deprecated nodes
          raise ValueError('p is no longer valid')
        return p._node

    def _make_position(self, node):
        """Return Position instance for given node, or None if node is None"""
        return self.SuffixTreePosition(self, node) if node is not None else None

    #-------------------SuffixTree constructor---------------------------------
    """Create a Suffix Tree starting from the tuple S of strings each node
        of the tree, except the root, is marked with a reference to those strings in S for which
        there is a suffix going through node u; moreover, the substring associated to each
        node must not be explicitly represented in the tree"""
    def __init__(self, S):
        self._root = self._SuffixTreeNode()
        self._words = S
        parent = self._root
        mark = 0
        for s in S:
            mark += 1
            for i in range(len(s)):
                self._find_match(parent, mark, len(s)-i-1)


    """This function is private and is called by init method in order to add a new node to the tree, 
        having as attributes the parameters passed"""
    def _add_node(self, start, stop, parent, mark, str, child=None):
        new_node = self._SuffixTreeNode(start, stop, parent, mark, child)
        new_pos = self._make_position(new_node)
        if start == len(str):
            c='$'
        else:
            c = str[start]
        if child is not None:
            parent._child = {}
            for i in child.values():
                child_nod = self._validate(i)
                child_nod._parent = new_node


        parent._add_child(new_pos, c)


    """This function is private and is called by init in order to check the node to which add a new child """
    def _find_match(self, parent, mark_to_insert, index_to_ins):
        string_to_ins = self._words[mark_to_insert-1]
        if(index_to_ins < len(string_to_ins)):
            suffix_to_ins = string_to_ins[index_to_ins:]
        else:
            suffix_to_ins = '$'


        find = parent._child.get(suffix_to_ins[0])


        if find is not None:
            find_node = self._validate(find)
            find_string = self._words[find._getmark()[0] - 1]
            find_suffix = find_string[find._getstart():find._getstop()]
            #controllo fino a quale indice sono compatibili
            eq = 0
            while eq < len(suffix_to_ins) and eq < len(find_suffix) and suffix_to_ins[eq] == find_suffix[eq]:
                eq += 1
            old_mark = find._getmark()
            find_node._add_mark(mark_to_insert)


            if eq == len(find_suffix) and len(find_node._child) != 0 :
                self._find_match(find_node, mark_to_insert, index_to_ins + eq)

            elif suffix_to_ins[0]!='$' and not(eq == len(find_suffix) and eq == len(suffix_to_ins)):
                old_stop = find._getstop()
                find_node._stop = find._getstart()+eq
                if len(find_node._child) != 0:
                    self._add_node(find_node._stop, old_stop, find_node, old_mark, find_string, find_node._child)
                else:
                    self._add_node(find_node._stop, old_stop, find_node, old_mark, find_string)
                self._add_node(index_to_ins + eq, len(string_to_ins), find_node, mark_to_insert, string_to_ins)


        else:
            self._add_node(index_to_ins, len(string_to_ins), parent, mark_to_insert, string_to_ins)



    #------------------Public methods----------------------------------------
    """This function returns the substring that labels the node of the SuffixTree
        to which Position P refers, or it throws an exception if P
        is invalid."""
    def getNodeLabel(self, P):
        node = self._validate(P)
        index = node._mark[0] - 1
        s = self._words[index]
        return s[node._start : node._stop]


    """This function returns the substring associated to the path in T from the root to
        the node to which position P refers (it throws an exception if P is invalid)"""
    def pathString(self, P):
        node = self._validate(P)
        if self._make_position(self._root) == P:
            return ''
        else:
            return self.pathString(self._make_position(node._parent)) + self.getNodeLabel(self._make_position(node))


    """This function returns the length of substring associated to the path in
        the Suffix Tree from the root to the node to which position
        P refers, or it throws an exception if P is invalid."""
    def getNodeDepth(self, P):
        node = self._validate(P)
        return node._parent_depth + node._stop - node._start


    """This function returns the mark of the node u of the suffix Tree to which
       position P refers, or it throws an exception if P is invalid."""
    def getNodeMark(self, P):
        node = self._validate(P)
        return node._mark


    """This function returns the position of the child u of the node of the Suffix Tree
        to which position P refers such that either s is a prefix of the substring labeling u,
        or the substring labeling u is a prefix of s, if it exists, and it returns None
        otherwise (it throws an exception if P is invalid or s is empty)."""
    def child(self, P, s):
        node_parent = self._validate(P)
        position_child = node_parent._child.get(s[0])
        if len(s) == 0:
            raise ValueError('s has no correct length')
        if position_child is not None:
            node_child = self._validate(position_child)
            child_label = self.getNodeLabel(position_child)

            for i in range(min(len(s),len(child_label))):
                if(child_label[i]!=s[i]):
                    return None

            return position_child
        return None



