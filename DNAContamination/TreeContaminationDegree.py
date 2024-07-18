
from avl_tree import AVLTreeMap

class TreeContaminationDegree(AVLTreeMap):

    def __setitem__(self, k, v):
        """Assign value v to key k."""
        if self.is_empty():
          leaf = self._add_root(self._Item(k,v))     # from LinkedBinaryTree
        else:
            p = self._subtree_search(self.root(), k)
            item = self._Item(k,v)
            if p.key() <= k:
                leaf = self._add_right(p, item)        # inherited from LinkedBinaryTree
            else:
                leaf = self._add_left(p, item)         # inherited from LinkedBinaryTree
        self._rebalance_insert(leaf)                 # hook for balanced tree subclasses

    def _subtree_search(self, p, k):
        """Return Position of p's subtree having key k, or last node searched."""
        #if k == p.key():                                   # found match
          #return p
        if k < p.key():                                  # search left subtree
          if self.left(p) is not None:
            return self._subtree_search(self.left(p), k)
        else:                                              # search right subtree
          if self.right(p) is not None:
            return self._subtree_search(self.right(p), k)
        return p                                           # unsucessful search

