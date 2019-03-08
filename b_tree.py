"""
Python code to implement functions for a B-Tree
"""
import bisect


M = 3  # 2T-1 way search tree (Restricted M as an odd value)
T = 2  # Every node except root must contain at least T-1 keys

class BTreeNode:
    """
    Data Structure of B-Tree Node.
    """

    def __init__(self, is_leaf):
        """
        Assume that there are n keys in the BTreeNode,
        there would be n+1 different address store in the array self.C,
        which are located at index 0~n of the array self.C
        """

        self.keys = []
        self.C = [None] * (2 * T)
        self.n = 0
        self.is_leaf = is_leaf  # True when node is leaf. Otherwise false.

class BTree:
    """
    B-Tree class
    """

    root = None
    t = T

    @staticmethod
    def print_node(node):
        """
        Print node (for debug).
        """

        print(f'node.keys : {node.keys}')
        printable_child_list = [child.keys if child is not None else None for child in node.C]
        print(f'node.C : {printable_child_list}')
        print(f'node.n : {node.n}')
        print(f'node.is_leaf : {node.is_leaf}')

    def traverse(self, node=root):
        """
        Method to traverse the given node and its child nodes.
        """

        if node is None:
            return

        # Traverse the subtree rooted with the child C[i] before
        # printing the key keys[i] in the given node.
        for i in range(node.n):
            self.traverse(node.C[i])
            print(f'{node.keys[i]}')
        self.traverse(node.C[node.n])

    def search(self, k, node=root) -> BTreeNode:
        """
        Method to search key k in the given node (and its child nodes).
        """

        # Find the first key greater than or equal to k
        i = bisect.bisect_left(node.keys, k)

        # If the found key is equal to k, return this node
        if i < node.n and node.keys[i] == k:
            return node

        # If the key is not found hear and this is a leaf node, return None.
        # Otherwise, search the subtree rooted with the child C[i].
        if node.is_leaf:
            return None
        return self.search(node.C[i], k)

    def insert(self, k):
        """
        New key should be inserted to a leaf node.
        There are 3 cases:
        1. The leaf has an empty space
            => just filled it in.
        2. The leaf is full, but its parent node has an empty space
            => _split_child
        3. The leaf is full and all its parents are also full
            => multiple _split_child (also the root), height += 1, new root
        """

        if self.root is None:
            self.root = BTreeNode(True)
            self.root.keys.append(k)
            self.root.n = 1
            return

        # Start from Case3.
        # Because "New key should be inserted to a leaf node",
        # root node is full implies Case3 happens.
        if self.root.n == (2 * self.t - 1):
            new_root = BTreeNode(False)
            new_root.C[0] = self.root

            self._split_child(0, new_root, self.root)

            # Check whether new_root.C[0] or new_root.C[1] (new_node)
            # should be the place to insert k.
            i = 0
            if new_root.keys[0] < k:
                i += 1
            self._root_not_full_insert(new_root.C[i], k)

            self.root = new_root

        # Case1 & Case2
        else:
            self._root_not_full_insert(self.root, k)

    def _root_not_full_insert(self, node, k):
        """
        Dealing with Case1 & Case2 of insert.
        Top-down Approach to check if _split_child is needed, until we step to a leaf. (Case2)
        Finally, insert the key k to the leaf. (Case1)
        """

        # Case1
        if node.is_leaf:
            # Insert the key k to node.keys
            bisect.insort(node.keys, k)
            node.n += 1

        # Case2
        else:
            # Find a child to step into it
            i = bisect.bisect_left(node.keys, k)

            # See if the found child is full
            if node.C[i].n == (2 * self.t - 1):
                # If the child is full, then split it.
                self._split_child(i, node, node.C[i])

                # Check whether node.C[i] or node.C[i+1] (new_node)
                # should be the place to insert k.
                if node.keys[i] < k:
                    i += 1

            self._root_not_full_insert(node.C[i], k)

    def _split_child(self, x, parent, node):
        """
        parent:
        C[x] points to the node.
         => poped_key should be assigned to keys[x],
            new_node should be assigned to C[x+1]


        Before split:
        node:
         n     C    K    C    ...   K         C
        2t-1 | c0 | k0 | c1 | ... | k(2t-2) | c(2t-1) |

        After split:
        node:
         n     C    K    C        ...   K         C         K      C
        t-1  | c0 | k0 | c1     | ... | k(t-2)  | c(t-1)  | None | None | ...

        new_node:
        n   C    K    C           ...   K         C         K      C
        t-1  | ct | kt | c(t+1) | ... | k(2t-2) | c(2t-1) | None | None | ...

        poped_key:
        k(t-1)
        """

        new_node = BTreeNode(node.is_leaf)
        new_node.n = self.t - 1

        # Copy the last t-1 keys (kt ~ k(2t-2)) of node to new_node and
        # copy the last t child (ct ~ c(2t-1)) of node to new_node
        new_node.keys = node.keys[-new_node.n:]  # new_node.n equals to t-1
        new_node.C[:self.t] = node.C[-self.t:]

        # Put poped_key to parent
        parent.keys.insert(x, node.keys[self.t - 1])
        parent.C.insert(x + 1, new_node)
        parent.C.pop()

        # Update n, keys, and C of node
        node.n = self.t - 1
        node.keys = node.keys[:node.n]
        for i in range(node.n + 1, len(node.C)):
            node.C[i] = None

        # Update n of parent
        parent.n += 1

    def delete(self, k):
        """
        Use a recursive function to remove the key k in the tree.
        All the possible cases are handled in the recursive function.
        This function only implements the parts of edge cases.
        """

        if self.root is None:
            print('The tree is empty')
            return

        self._remove(self.root, k)

        if self.root.n == 0:
            tmp = self.root
            if self.root.is_leaf:
                self.root = None
            else:
                # Happens when the only key in the root provided
                # to its left child for merge.
                self.root = self.root.C[0]
            del tmp

    def _remove(self, node, k):
        """
        Recursive function to find and remove the key k
        in this node and all its subtrees.
        """

        # Find the first key greater than or equal to k
        i = bisect.bisect_left(node.keys, k)

        # If the found key is equal to k, do the deletion
        if i < node.n and node.keys[i] == k:
            if node.is_leaf:
                node.keys[i:] = node.keys[i + 1:]
                node.n -= 1
            else:
                self._remove_from_non_leaf(i, node)
            return

        # The found key is greater than k and the node is a leaf implies that the key not exist.
        if node.is_leaf:
            print(f'The key {k} does not exist in the tree.')
            return

        # Otherwise, step into the child (recursion),
        # Check if node.C[i] will violate B-Tree definition after the deletion before recursion.
        if node.C[i].n < self.t:
            # node.C[i] will violate B-Tree definition after the deletion
            # (node.C[i].n - 1 < (self.t - 1))
            #  => Need to rotate or merge
            if i != 0 and node.C[i - 1].n >= self.t:
                self._right_rotate(i, node)
            elif i != node.n and node.C[i + 1].n >= self.t:
                self._left_rotate(i, node)
            else:
                if i == node.n:
                    self._merge(i - 1, node)
                else:
                    self._merge(i, node)

        if i > node.n:
            # Only happened when the last child of node is merged and gone.
            # (Before: i == node.n | After: i == node.n + 1)
            self._remove(node.C[i - 1], k)
        else:
            self._remove(node.C[i], k)

    def _remove_from_non_leaf(self, x, node):
        """
        Transform the problem into "remove from leaf" problem.

        Because of the B-Tree definitions,
        the immediate inorder predecessor or the immediate inorder successor is a leaf,
        we can replace the found key k with the predecessor/successor,
        and then remove the predecessor/successor located in subtrees of the node.

        However, we check if node.C[x] will violate B-Tree definition after the deletion
        before recursion (stepping into a child).
        There are 3 cases:
        1. node.C[x] is still a validate node after the deletion.
           (node.C[x].n - 1 >= (self.t - 1))
            => Replace k by predecessor, then step into node.C[x] to do the deletion.
        2. Case1 failed, but node.C[x+1] is still a validate node after the deletion.
           (node.C[x+1].n - 1 >= (self.t - 1))
            => Replace k by successor, then step into node.C[x+1] to do the deletion.
        3. Both Case1 and Case2 failed.
            => Merge node.C[x] and node.C[x+1], then step into node.C[x] to do the deletion.
        """

        # Case1
        if node.C[x].n >= self.t:
            predecessor = self._get_predecessor(x, node)
            node.keys[x] = predecessor
            self._remove(node.C[x], predecessor)
        # Case2
        elif node.C[x + 1].n >= self.t:
            successor = self._get_successor(x, node)
            node.keys[x] = successor
            self._remove(node.C[x + 1], successor)
        # Case3
        else:
            k = node.keys[x]
            self._merge(x, node)
            self._remove(node.C[x], k)

    @staticmethod
    def _right_rotate(x, node):
        """
        node:
           C        K        C    ...
         | c(x-1) | k(x-1) | cx | ...
        """

        child = node.C[x]
        left_sibling = node.C[x - 1]

        # 1. node.key[x - 1] goes down to the child as the first key
        child.keys.insert(0, node.keys[x - 1])

        # 2. The last key from left_sibling goes up to node
        node.keys[x - 1] = left_sibling.keys[left_sibling.n - 1]

        # Update child's child and n
        if not child.is_leaf:
            child.C.insert(0, left_sibling.C[left_sibling.n])  # Because left_sibling losts its last key
            child.C.pop()
        child.n += 1

        # Update left_sibling's keys, child, and n
        left_sibling.keys = left_sibling.keys[:-1]
        left_sibling.C[left_sibling.n] = None
        left_sibling.n -= 1

    @staticmethod
    def _left_rotate(x, node):  # borrowFromNext
        """
        node:
           C    K    C        ...
         | cx | kx | c(x+1) | ...
        """

        child = node.C[x]
        right_sibling = node.C[x + 1]

        # 1. node.key[x] goes down to the child as the last key
        child.keys.append(node.keys[x])

        # 2. The first key from right_sibling goes up to node
        node.keys[x] = right_sibling.keys[0]

        # Update child's child and n
        child.C[child.n + 1] = right_sibling.C[0]  # Because right_sibling losts its first key
        child.n += 1

        # Update right_sibling's keys, child, and n
        right_sibling.keys = right_sibling.keys[1:]
        if not right_sibling.is_leaf:
            right_sibling.C = right_sibling.C[1:] + [None]
        right_sibling.n -= 1

    @staticmethod
    def _merge(x, node):
        """
        Merge node.C[x] and node.C[x+1] as the updated node.C[x].
        node.C[x+1] replaced by node.C[x+2] after merging.

        Before:
        node:
           C    K    C        K        C
         | cx | kx | c(x+1) | k(x+1) | c(x+2)

        child:
         n        ...   C                K               C
        child.n | ... | c(child.n - 1) | k(child.n - 1)| c(child.n)

        right_sibling:
         n      ...   C              K             C
        sib.n | ... | c(sib.n - 1) | k(sib.n - 1)| c(sib.n)


        After:
        node:
           C    K        C        ...
         | cx | k(x+1) | c(x+2) | ...

        cx (updated child):
         n                    ...   C            K              C          ...
        child.n + 1 + sib.n | ... | c(child.n) | node.keys[x] | sib.C[0] | ...
        """

        child = node.C[x]
        sibling = node.C[x + 1]

        # 1. node.key[x] goes down to the child as the last key
        child.keys.append(node.keys[x])
        node.keys[x:] = node.keys[x + 1:]
        node.C[x + 1:] = node.C[x + 2:] + [None]

        # 2. Concat child.keys and right_sibling.keys
        child.keys += sibling.keys

        # 3. Copy all the right_sibling.C to child
        if not child.is_leaf:
            for i in range(sibling.n + 1):
                child.C[i + (child.n + 1)] = sibling.C[i]

        # Update child and node's n
        child.n += (1 + sibling.n)
        node.n -= 1

        # Free the memory occupied by right_sibling
        # Python only delete the variable name. The gc mechanism will be done automatically.
        del sibling

    @staticmethod
    def _get_predecessor(x, node):
        """
        Step into C[x],
        then keep stepping into the right most child until reaching a leaf.
        Return the last key of the leaf.
        """

        cur = node.C[x]
        while not cur.is_leaf:
            cur = cur.C[cur.n]

        return cur.keys[cur.n - 1]

    @staticmethod
    def _get_successor(x, node):
        """
        Step into C[x + 1],
        then keep stepping into the left most child until reaching a leaf.
        Return the first key of the leaf.
        """

        cur = node.C[x + 1]
        while not cur.is_leaf:
            cur = cur.C[0]

        return cur.keys[0]

"""
Driver program to test above functions.
The constructed B-Tree would be
                       15

           10                      20

    3,5           13         18         24

1,2  4  6,7  11,12  14  16,17  19  21,22  25,26

Inorder traversal result would be
1 2 3 4 5 6 7 10 11 12 13 14 15 16 17 18 19 20 21 22 24 25 26


The B-Tree after all the deletions whould be
               15,20

   5,12         18         24

3  10,11  14  17  19  21,22  25,26

Inorder traversal result would be
3 5 10 11 12 14 15 17 18 19 20 21 22 24 25 26
"""

# myTree = BTree()
# nums = [1, 3, 7, 10, 11, 13, 14, 15, 18, 16, 19, 24, 25, 26, 21, 4, 5, 20, 22, 2, 17, 12, 6]
# for num in nums:
#     myTree.insert(num)

# myTree.traverse(myTree.root)

# myTree.delete(6)
# myTree.delete(13)
# myTree.delete(7)
# myTree.delete(4)
# myTree.delete(2)
# myTree.delete(16)
# myTree.delete(1)

# myTree.traverse(myTree.root)


# This code is contributed by Sammy Wen.
