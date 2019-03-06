"""
Python code to implement functions for a Binary Search Tree
"""

class TreeNode:
    """
    Generic tree node class
    """
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.height = 1

class BST:
    """
    Python class for a Binary Search Tree
    """

    def lookup(self, root, key):
        """
        Recursive function to lookup the node which has the same value as the given key.
        Return the node if it meets the requirement.
        Return None if the node isn't exist.
        """

        if not root:
            return None

        if key < root.val:
            return self.lookup(root.left, key) if root.left is not None else None
        if key > root.val:
            return self.lookup(root.right, key) if root.right is not None else None
        return root

    def insert(self, root, key):
        """
        Recursive function to insert key in subtree rooted with node
        and returns new root of subtree.
        """

        if not root:
            return TreeNode(key)

        if key < root.val:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)

        root.height = 1 + max(self._get_height(root.left), self._get_height(root.right))

        return root

    def delete(self, root, key):
        """
        Recursive function to delete a node with the given key from subtree with given root.
        It returns root of the modified subtree.
        """

        if not root:
            return root

        if key < root.val:
            root.left = self.delete(root.left, key)
        elif key > root.val:
            root.right = self.delete(root.right, key)
        else:
            # The node to be deleted only have a right child
            # or it is a leaf node.
            if root.left is None:
                temp = root.right
                root = None
                return temp

            # The node to be deleted only have a left child.
            if root.right is None:
                temp = root.left
                root = None
                return temp

            # The node to be deleted have both left and right child.
            # Replace value with the immediate in_order successor (must be a leaf)
            # and then remove that successor.
            temp = self._get_successor(root)
            root.val = temp.val
            root.right = self.delete(root.right, temp.val)

        root.height = 1 + max(self._get_height(root.left), self._get_height(root.right))

        return root

    def pre_order(self, root):
        """
        Print BST in preorder.
        """

        if not root:
            return

        print(f"{root.val}")
        self.pre_order(root.left)
        self.pre_order(root.right)

    def in_order(self, root):
        """
        Print BST in inorder.
        """

        if not root:
            return

        self.in_order(root.left)
        print(f"{root.val}")
        self.in_order(root.right)

    def post_order(self, root):
        """
        Print BST in postorder.
        """

        if not root:
            return

        self.post_order(root.left)
        self.post_order(root.right)
        print(f"{root.val}")

    @staticmethod
    def _get_successor(node):
        """
        Given a node, find its immediate in_order successor.
        """

        if node.right is None:
            return node.right

        ret = node.right
        while ret.left is not None:
            ret = ret.left
        return ret

    @staticmethod
    def _get_height(node):
        """
        Given a node, return its height.
        Return 0 if the given parameter is None.
        """

        if node is None:
            return 0

        return node.height

"""
Driver program to test above functions
The constructed AVL Tree would be:
            50
          /    \
         30    70
        / \    / \
       20 40  60 80

Inorder traversal result would be
20 30 40 50 60 70 80 
"""

# myTree = BST()
# root = None
# nums = [50, 30, 20, 40, 70, 60, 80]
# for num in nums:
#     root = myTree.insert(root, num)
# 
# myTree.in_order(root)
# print(myTree.lookup(root, 5))
# print(myTree.lookup(root, 9))
# for num in nums:
#     root = myTree.delete(root, num)
#     myTree.in_order(root)


# This code is contributed by Sammy Wen.