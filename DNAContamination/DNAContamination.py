
from SuffixTree import SuffixTree
from TreeContaminationDegree import TreeContaminationDegree
class DNAContamination:

    """A private nested class that extends the class SuffixTree"""
    class _SuffixTreePlus(SuffixTree):
        """This private function return the root of the SuffixTree"""
        def _get_root(self):
            return self._make_position(self._root)

    """This function build a DNAContamination object; it takes in input the
    string s to verify and the contamination threshold l"""
    def __init__(self, s, l):
        self._s = s
        self._l = l
        self._C = TreeContaminationDegree()


    """This function adds contaminant c to the set C and saves the degree of contamination of s by c"""
    def addContaminant(self, c):
        S = (self._s, c)
        suff_tree = self._SuffixTreePlus(S)
        sub = []
        root = suff_tree._get_root()
        i = 0
        while i <= len(c)-self._l:
            pos_to_see = suff_tree.child(root, c[i:])
            if pos_to_see is not None and len(suff_tree.getNodeMark(pos_to_see)) > 1:
                last_pos = self._analize_child(suff_tree, pos_to_see, i, c)
                if suff_tree.getNodeDepth(last_pos)>= self._l:
                    to_ins = suff_tree.pathString(last_pos)
                    if self._notin(sub,to_ins, i):
                        sub += [(to_ins, i)]
            i +=1
        self._C.__setitem__(len(sub), c)

    """This is a private function that is used to check that the string to ins is a maximal string and it is not contained in others"""
    def _notin(self, sub, to_ins, index_to_ins):
        for index, s in enumerate(sub):
            if len(s[0]) > len(to_ins) and to_ins in s[0] and index_to_ins <= s[1] + len(s[0]):
                return False
        return True

    """This is a private function called by addContaminant in order to find the longest matching of substrings starting 
        from a parent and going down on its children in the SuffixTree """
    def _analize_child(self, s_tree, parent, i, c):
        parent_depth = s_tree.getNodeDepth(parent)
        if parent_depth+i<len(c):
            pos_child = s_tree.child(parent, c[i+parent_depth:])
        else:
            return parent

        while pos_child is not None and len(s_tree.getNodeMark(pos_child))>1:
            parent = pos_child
            child_depth = s_tree.getNodeDepth(pos_child)
            if child_depth+i< len(c):
                pos_child = s_tree.child(pos_child, c[i+child_depth:])
            else:
                return pos_child
        return parent

    """This function returns the k contaminants with larger degree of contamination among the added contaminants."""
    def getContaminants(self, k):
        to_ret = []
        if not self._C.is_empty():
            max = self._C.find_max()
            to_ret += [max[1]]
            max_pos = self._C.find_position(max[0])
            pos = max_pos
            for i in range(k-1):
                tmp = self._C.before(pos)
                to_ret += [tmp.element()._value]
                pos = tmp
        return to_ret









