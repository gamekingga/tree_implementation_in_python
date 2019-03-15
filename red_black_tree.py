"""
Python code to implement functions for a Red-Black-Tree
"""
from enum import Enum
class NodeColor(Enum):
    """
    For defining an RBTreeNode's color.
    """
    RED = 1
    BLACK = 2


class NullLeaf:
    """
    Data Structure of Red-Black-Tree NullLeaf Node.
    """
    def __init__(self, parent):
        self.val = None
        self.color = NodeColor.BLACK
        self.left = None
        self.right = None
        self.parent = parent
        self.is_null_leaf = True


class RBTreeNode:
    """
    Data Structure of Red-Black-Tree Node.
    """
    def __init__(self, val):
        self.val = val
        self.color = NodeColor.RED
        self.left = NullLeaf(self)
        self.right = NullLeaf(self)
        self.parent = None
        self.is_null_leaf = False


class RBTree:
    """
    Red-Black-Tree class
    """

    root = None

    @staticmethod
    def print_node(node):
        """
        Print node (for debug).
        """

        print(f'node.val : {node.val}')
        print(f'node.color : {node.color.name}')
        printable_left_child = node.left.val
        printable_right_child = node.right.val
        print(f'node.childs : {[printable_left_child, printable_right_child]}')
        print(f'node.parent : {node.parent.val if node.parent is not None else None}')
        print()

    def in_order(self, node=False):
        """
        Print Red-Black-Tree in inorder.
        """

        if node is False:
            node = self.root

        if self.root is None or node.is_null_leaf:
            return

        self.in_order(node.left)
        print(f'{node.val}')
        self.in_order(node.right)

    def level_order(self):
        """
        Print Red-Black-Tree in levelorder.

        levelorder: from root to leaf, from left to right if nodes are in the same level.
        """

        if self.root is None:
            return

        queue = [self.root]
        while queue:
            cur = queue.pop(0)
            print(f'{cur.val}')
            if not cur.left.is_null_leaf:
                queue.append(cur.left)
            if not cur.right.is_null_leaf:
                queue.append(cur.right)

    def lookup(self, key, node=False):
        """
        Identical to the implementation of AVL tree lookup.

        Recursive function to lookup the node which has the same value as the given key.
        Return the node if it meets the requirement.
        Return None if the node isn't exist.
        """

        if node is False:
            node = self.root

        if self.root is None or node.is_null_leaf:
            return None

        if key < node.val:
            return self.lookup(key, node.left) if not node.left.is_null_leaf else None
        if key > node.val:
            return self.lookup(key, node.right) if not node.right.is_null_leaf else None
        return node

    def insert(self, key):
        """
        There are 8 cases for _fix_insert_violation. We use 'XYc' string to represent every case.
         => [LLb, RRb, LRb, RLb, LLr, RRr, LRr, RLr]
        Assume the new node is named 'n', its parent is named 'p', its grandparent is named 'g'.
        X: Fill-in 'L' if g's left child is p, else fill-in 'R'.
        Y: Fill-in 'L' if p's left child is n, else fill-in 'R'.
        c: Fill-in 'b' if p's sibling (uncle (u)) is BLACK, else fill-in 'r'.
        """

        if self.root is None:
            self.root = RBTreeNode(key)
            self.root.color = NodeColor.BLACK
            return

        if self.lookup(key) is not None:
            print('The key already exists in the tree.')
            return

        # Step 1 - Perform normal BST insert
        new_node = RBTreeNode(key)
        _ = self._bst_insert(new_node, self.root)

        # Step 2 - Fix the violation after new_node inserted.
        self._fix_insert_violation(new_node)

        # Step 3 - keep self.root BLACK
        self.root.color = NodeColor.BLACK

    def delete(self, key):
        """
        1. If the deleted_node is internal node
            => Replace the val with its inorder predecessor
            => Point deleted_node to the predecessor
        2. If the deleted_node is RED
            => Just delete it.
        3. If the deleted_node is black with 1 RED child
            => Replace the deleted_node with the RED child.
            => Change the color to BLACK.
        4. If the deleted_node is black with 0 child or 1 BLACK child
            => Fix Double Black.
            There are 6 cases for Fix Double Black.
        """

        if self.root is None:
            print('The tree is empty.')
            return

        deleted_node = self.lookup(key)
        if deleted_node is None:
            print('The key does not exist in the tree')
            return

        # Step 1
        if deleted_node.left.is_null_leaf or deleted_node.right.is_null_leaf:
            pass
        else:
            predecessor = self._get_predecessor(deleted_node)
            deleted_node.val = predecessor.val
            deleted_node = predecessor

        # Step 2 & Step 3
        child = deleted_node.left if not deleted_node.left.is_null_leaf else deleted_node.right
        self._link_parent_and_child(deleted_node, child)
        if deleted_node.color == NodeColor.RED or child.color == NodeColor.RED:
            if child.color == NodeColor.RED:
                child.color = NodeColor.BLACK
            return

        # Step 4
        self._delete_case_1(child)

    def _bst_insert(self, new_node, node, parent=None):
        """
        Recursive function to insert key in subtree rooted with node
        and returns new root of subtree.
        """

        if node.is_null_leaf:
            new_node.parent = parent
            return new_node

        if new_node.val < node.val:
            node.left = self._bst_insert(new_node, node.left, node)
        elif new_node.val > node.val:
            node.right = self._bst_insert(new_node, node.right, node)
        return node

    def _fix_insert_violation(self, node):
        """
        Bottom-up solution for fixing the violation after new_node inserted.
        """

        if node == self.root or \
            node.color == NodeColor.BLACK or node.parent.color == NodeColor.BLACK:
            return

        parent = node.parent
        grand_parent = node.parent.parent

        if parent == grand_parent.left:
            uncle = grand_parent.right
            if uncle.color == NodeColor.RED:
                # [LLr, LRr], need to recolor.
                self._insert_recolor(node)
            else:
                # [LLb, LRb], need to rotate.
                if node == parent.left:  # LLb
                    self._right_rotate(grand_parent)
                    parent.color, grand_parent.color = grand_parent.color, parent.color
                else:  # LRb
                    self._left_rotate(parent)
                    self._right_rotate(grand_parent)
                    node.color, grand_parent.color = grand_parent.color, node.color
        else:
            uncle = grand_parent.left
            if uncle.color == NodeColor.RED:
                # [RRr, RLr], need to recolor.
                self._insert_recolor(node)
            else:
                # [RRb, RLb], need to rotate.
                if node == parent.right:  # RRb
                    self._left_rotate(grand_parent)
                    parent.color, grand_parent.color = grand_parent.color, parent.color
                else:  # RLb
                    self._right_rotate(parent)
                    self._left_rotate(grand_parent)
                    node.color, grand_parent.color = grand_parent.color, node.color

    def _insert_recolor(self, node):
        """
        The recolor process when inserting a new node.

        Graph for LLr case:

             (b) g                                 (r) g
               /   \                                 /   \
          (r) p (r) u       _recolor (n)        (b) p (b) u
             /           - - - - - - - - ->        /
        (r) n                                 (r) n

        The parameter 'node' is the 'n' in the graph.
        Step 1: Change the color of grand_parent as RED
        Step 2: Change the color of parent and uncle as BLACK
        Step 3: Keep going on _fix_insert_violation(grand_parent).
        """

        parent = node.parent
        grand_parent = node.parent.parent
        uncle = grand_parent.right if parent == grand_parent.left else grand_parent.left

        grand_parent.color = NodeColor.RED
        parent.color = NodeColor.BLACK
        uncle.color = NodeColor.BLACK
        self._fix_insert_violation(grand_parent)

    def _right_rotate(self, node):
        """
        Graph for LL case:

                    gg                                gg
                   /                                /
             (b) g                                p (r)
               /   \                            /   \
          (r) p (b) u      _right_rotate (g)   n (r) g (b)
             / \   / \    - - - - - - - - ->        / \
        (r) n  T1 T2 T3                            T1  u (b)
                                                      / \
                                                     T2 T3

        The parameter 'node' is the 'g' in the graph.
        (Step 0: left_child (p) is original node.left,
                 parent (gg) is original node.parent (node is its left or right child).)
        Step 1: Original g is the new left_child.right
        Step 2: Original left_child (p) is the parent's left or right child
        Step 3: Original left_child.right (T1) is the new node.left
        """

        # Check if the root would change after rotate
        if node == self.root:
            self.root = node.left

        # Step 0
        left_child = node.left
        parent = node.parent
        T1 = left_child.right

        # Perform rotation
        node.parent = left_child
        left_child.right = node

        left_child.parent = parent
        if parent is not None:
            if node == parent.left:
                parent.left = left_child
            else:
                parent.right = left_child

        T1.parent = node
        node.left = T1

    def _left_rotate(self, node):
        """
        Graph for RR case:

           gg                                       gg
            \                                        \
              g (b)                                (r) p
            /   \                                    /   \
           u (b) p (r)     _left_rotate (g)     (b) g (r) n
          / \   / \       - - - - - - - - ->       / \
         T1 T2 T3  n (r)                      (r) u  T3
                                                 / \
                                                T1 T2

        The parameter 'node' is the 'g' in the graph.
        (Step 0: right_child (p) is original node.right,
                 parent (gg) is original node.parent (node is its left or right child).)
        Step 1: Original g is the new right_child.left
        Step 2: Original right_child (p) is the parent's left or right child.
        Step 3: Original right_child.left (T3) is the new node.right
        """

        # Check if the root would change after rotate
        if node == self.root:
            self.root = node.right

        # Step 0
        right_child = node.right
        parent = node.parent
        T3 = right_child.left

        # Perform rotation
        node.parent = right_child
        right_child.left = node

        right_child.parent = parent
        if parent is not None:
            if node == parent.left:
                parent.left = right_child
            else:
                parent.right = right_child

        T3.parent = node
        node.right = T3

    @staticmethod
    def _get_predecessor(node):
        """
        Given a node, find its immediate inorder predecessor.
        """

        ret = node.left
        while not ret.right.is_null_leaf:
            ret = ret.right
        return ret

    def _link_parent_and_child(self, node, child):
        """
        Given a node and its child, link its parent with the child.
        (node is going to be deleted.)
        """

        child.parent = node.parent
        if node == self.root:
            self.root = child
        elif node == node.parent.left:
            node.parent.left = child
        else:  # node == node.parent.right
            node.parent.right = child

    def _delete_case_1(self, node):
        """
        Case 1: The node is self.root

            (DB)            (B)
            root   - - ->   root

        Step 0: Check if the node is self.root. Otherwise, step into case_2.
        (If case_1 matched and the given node is NullLeaf,
         it means the only node in the tree is going to be deleted.)
        Step 1: Terminate.
        """

        if node == self.root:
            if isinstance(node, NullLeaf):
                self.root = None
            return
        self._delete_case_2(node)

    def _delete_case_2(self, node):
        """
        Case 2: The sibling is RED

            (B) P                           (B) S
              /   \                           /   \
        (DB) N     S (R)     - - ->      (R) P     Y (B)
                  / \                       / \
             (B) X   Y (B)            (DB) N   X (B)

        Step 0: Check if case_2 matched. Otherwise, step into case_3.
        Step 1: _switch_color(parent, sibling)
        Step 2: _left_rotate(parent) / _right_rotate(parent)
        Step 3: Step into case_3.
        """

        parent = node.parent
        sibling = parent.right if node == parent.left else parent.left

        if sibling.color == NodeColor.RED:
            parent.color, sibling.color = sibling.color, parent.color
            if node == parent.left:
                self._left_rotate(parent)
            else:  # node == parent.right
                self._right_rotate(parent)

        self._delete_case_3(node)

    def _delete_case_3(self, node):
        """
        Case 3: ALL Black

            (B) P                       (DB) P
              /   \                        /   \
        (DB) N     S (B)     - - ->   (B) N     S (R)
                  / \                          / \
             (B) X   Y (B)                (B) X   Y (B)

        Step 0: Check if case_3 matched. Otherwise, step into case_4.
        Step 1: sibling.color = NodeColor.RED
        Step 2: Step into case_1 with parent as the argument.
        """

        parent = node.parent
        sibling = parent.right if node == parent.left else parent.left

        if parent.color == NodeColor.BLACK and sibling.color == NodeColor.BLACK and \
            sibling.left.color == NodeColor.BLACK and sibling.right.color == NodeColor.BLACK:
            sibling.color = NodeColor.RED
            self._delete_case_1(parent)
        else:
            self._delete_case_4(node)

    def _delete_case_4(self, node):
        """
        Case 4: The parent is RED, and the others are BLACK

            (R) P                        (R) P
              /   \                        /   \
        (DB) N     S (B)     - - ->   (B) N     S (B)
                  / \                          / \
             (B) X   Y (B)                (B) X   Y (B)

        Step 0: Check if case_4 matched. Otherwise, step into case_5.
        Step 1: _switch_color(parent, sibling)
        Step 2: Terminate.
        """

        parent = node.parent
        sibling = parent.right if node == parent.left else parent.left

        if parent.color == NodeColor.RED and sibling.color == NodeColor.BLACK and \
            sibling.left.color == NodeColor.BLACK and sibling.right.color == NodeColor.BLACK:
            parent.color, sibling.color = sibling.color, parent.color
            return
        self._delete_case_5(node)

    def _delete_case_5(self, node):
        """
        Case 5: The sibling is BLACK,
                the inside sibling child is RED, the outside sibling child is BLACK

        Right Sibling:

          (R/B) P                      (R/B) P
              /   \                        /   \
        (DB) N     S (B)     - - ->  (DB) N     X (B)
                  / \                            \
             (R) X   Y (B)                        S (R)
                                                   \
                                                    Y (B)

        Step 0: Check if case_5 matched. Otherwise, step into case_6.
        Step 1: _switch_color(sibling.left, sibling)
        Step 2: _right_rotate(sibling)
        Step 3: Step into case_6.


        Left Sibling:

                  P (R/B)                      P (R/B)
                /   \                        /   \
          (B) S      N (DB)  - - ->     (B) X     N (DB)
             / \                           /
        (B) Y   X (R)                 (R) S
                                         /
                                    (B) Y

        Step 0: Check if case_5 matched. Otherwise, step into case_6.
        Step 1: _switch_color(sibling.right, sibling)
        Step 2: _left_rotate(sibling)
        Step 3: Step into case_6.
        """

        parent = node.parent
        sibling = parent.right if node == parent.left else parent.left

        if sibling.color == NodeColor.BLACK:
            if node == parent.left and \
                sibling.left.color == NodeColor.RED and \
                sibling.right.color == NodeColor.BLACK:

                sibling.left.color, sibling.color = sibling.color, sibling.left.color
                self._right_rotate(sibling)

            elif node == parent.right and \
                sibling.left.color == NodeColor.BLACK and \
                sibling.right.color == NodeColor.RED:

                sibling.right.color, sibling.color = sibling.color, sibling.right.color
                self._left_rotate(sibling)

        self._delete_case_6(node)

    def _delete_case_6(self, node):
        """
        Case 6: The sibling is BLACK, the outside sibling child is RED

        Right Sibling:

          (R/B) P                       (R/B) S
              /   \                         /   \
        (DB) N     S (B)     - - ->    (B) P     Y (B)
                  / \                     / \
           (R/B) X   Y (R)           (B) N   X (R/B)

        Step 0: X
        Step 1: _switch_color(parent, sibling)
        Step 2: sibling.right.color = NodeColor.BLACK
        Step 3: _left_rotate(parent)
        Step 4: Terminate.


        Left Sibling:

                 P (R/B)                     S (R/B)
               /   \                       /   \
          (B) S     N (DB)   - - ->   (B) Y     P (B)
             / \                               / \
        (R) Y   X (R/B)                 (R/B) X   N (B)

        Step 0: X
        Step 1: _switch_color(parent, sibling)
        Step 2: sibling.left.color = NodeColor.BLACK
        Step 3: _right_rotate(parent)
        Step 4: Terminate.
        """

        parent = node.parent
        sibling = parent.right if node == parent.left else parent.left

        parent.color, sibling.color = sibling.color, parent.color
        if node == parent.left:
            sibling.right.color = NodeColor.BLACK
            self._left_rotate(parent)
        else:  # node == parent.right
            sibling.left.color = NodeColor.BLACK
            self._right_rotate(parent)

"""
Two driver programs to test above functions.
"""

"""
1. Test every cases of insert.
The constructed Red-Black-Tree would be
                            7(b)
            4(r)                            9(b)
    2(b)            5(b)            8(b)            10(b)
1(r)    3(r)            6(r)

Inorder traversal result would be
1 2 3 4 5 6 7 8 9 10
Levelorder traversal result would be
7 4 9 2 5 8 10 1 3 6
"""
# myTree = RBTree()
# myTree.insert(3)
# myTree.insert(4)
# myTree.insert(5)
# myTree.insert(10)
# myTree.insert(9)
# myTree.insert(8)
# myTree.insert(7)
# myTree.insert(1)
# myTree.insert(2)
# myTree.insert(6)
# print('Inorder traversal result is')
# myTree.in_order()
# print('Levelorder traversal result is')
# myTree.level_order()

"""
2. Test every cases of delete.
The constructed Red-Black-Tree would be
                       20(b)
       10(b)                         30(b)
   2(b)     17(b)           25(r)               40(r)
1(r)     15(r) 19(r)   21(b)     28(b)     34(b)     50(b)
                         24(r) 26(r)    32(r) 35(r)

Levelorder traversal result would be
20 10 30 2 17 25 40 1 15 19 21 28 34 50 24 26 32 35

Let's do the deletion.
The order of cases/steps is:  (mirror: sibling == parent.left)
delete(50):  Case 6(mirror)
delete(40):  Step 3
delete(2):   Step 3
delete(15):  Step 2
delete(17):  Step 3
delete(24):  Step 2
delete(21):  Case 5 -> Case 6
delete(32):  Case 4
delete(26):  Step 1 -> 25 -> Case 4
delete(19):  Case 3(mirror) -> 10 -> Case 3 -> 20 -> Case 1
delete(25):  Step 3
delete(1):   Step 2
delete(20):  Step 1 -> 10 -> Case 2 -> Case 4
delete(35):  Step 2
delete(34):  Case 5(mirror) -> Case 6(mirror)
delete(30):  Case 3(mirror) -> 28 -> Case 1
delete(28):  Step 3
delete(10):  Case 1 (self.root = None)
"""
# from red_black_tree import *
# myTree = RBTree()
# nums = [10, 15, 2, 20, 30, 40, 50, 1, 25, 17, 21, 24, 28, 34, 32, 26, 35, 19]
# for num in nums:
#     myTree.insert(num)
#
# myTree.level_order()
#
# nums = [50, 40, 2, 15, 17, 24, 21, 32, 26, 19, 25, 1, 20, 35, 34, 30, 28, 10]
# for num in nums:
#     myTree.delete(num)
#
