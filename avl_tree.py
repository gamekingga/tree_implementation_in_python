"""
Python code to implement functions for an AVL tree
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

# AVL tree class
class AVLtree:
    """
    AVL tree class
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

        # Step 1 - Perform normal BST
        if not root:
            return TreeNode(key)

        if key < root.val:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)

        # Step 2 - Update the height of the ancestor node
        # root.height = 1 + max(self._get_height(root.left), self._get_height(root.right))
        self._update_height(root)

        # Step 3 - Get the balance factor
        bf = self._get_balance_factor(root)

        # Step 4 - If the node is unbalanced, then try out the 4 cases:
        # (Use the comparison of the inserted key and the value of
        #  root.left/root.right to know which child tree the key inserted.)
        # Case 1 - Left Left
        if bf > 1 and key < root.left.val:
            return self.right_rotate(root)

        # Case 2 - Right Right
        if bf < -1 and key > root.right.val:
            return self.left_rotate(root)

        # Case 3 - Left Right
        if bf > 1 and key > root.left.val:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Case 4 - Right Left
        if bf < -1 and key < root.right.val:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def delete(self, root, key):
        """
        Recursive function to delete a node with given key from subtree with given root.
        It returns root of the modified subtree.
        """

        # Step 1 - Perform standard BST delete
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

        # If the tree has only one node, simply return it
        if root is None:
            return root

        # Step 2 - Update the height of the ancestor node
        self._update_height(root)

        # Step 3 - Get the balance factor
        bf = self._get_balance_factor(root)

        # Step 4 - If the node is unbalanced, then try out the 4 cases:
        # Case 1 - Left Left
        if bf > 1 and self._get_balance_factor(root.left) >= 0:
            return self.right_rotate(root)

        # Case 2 - Right Right
        if bf < -1 and self._get_balance_factor(root.right) <= 0:
            return self.left_rotate(root)

        # Case 3 - Left Right
        if bf > 1 and self._get_balance_factor(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Case 4 - Right Left
        if bf < -1 and self._get_balance_factor(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def left_rotate(self, A):
        """
               A (-2)                           (0) B
              / \                                 /   \
            AR   B (-1)    left_rotate (A)   (0) A    BR
                / \      - - - - - - - - ->    /  \   |N|
               BL BR                          AL  BL
                  |N|

        (Step 0: B is original A.right)
        Step 1: Original A (A) is the new B.left
        Step 2: Original B.left (BL) is the new A.right
        """

        B = A.right
        BL = B.left

        # Perform rotation
        B.left = A
        A.right = BL

        # Update heights
        self._update_height(A)
        self._update_height(B)

        # Return the new root
        return B

    def right_rotate(self, A):
        """
           (2) A                                 B (0)
              / \                              /   \
         (1) B  AR     right_rotate (A)       BL    A (0)
            / \       - - - - - - - - ->     |N|   /  \
           BL BR                                  BR  AR
          |N|

        (Step 0: B is original A.left)
        Step 1: Original A (A) is the new B.right
        Step 2: Original B.right (BR) is the new A.left
        """

        B = A.left
        BR = B.right

        # Perform rotation
        B.right = A
        A.left = BR

        # Update heights
        self._update_height(A)
        self._update_height(B)

        # Return the new root
        return B

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
    def _get_height(node):
        """
        Given a node, return its height.
        Return 0 if the given parameter is None.
        """

        if node is None:
            return 0

        return node.height

    @staticmethod
    def _update_height(node):
        """
        Given a node, update its height.
        """

        node.height = 1 + max(AVLtree._get_height(node.left), AVLtree._get_height(node.right))

    @staticmethod
    def _get_balance_factor(node):
        """
        Given a node, return its balance factor.
        """

        if not node:
            return 0

        return AVLtree._get_height(node.left) - AVLtree._get_height(node.right)

    @staticmethod
    def _get_successor(node):
        """
        Given a node, find its immediate inorder successor.
        """

        if node.right is None:
            return node.right

        ret = node.right
        while ret.left is not None:
            ret = ret.left
        return ret

"""
Driver program to test above function.
The constructed AVL Tree would be
            9
           /  \
          1    10
        /  \     \
       0    5     11
      /    /  \
     -1   2    6

Preorder traversal result would be
9 1 0 -1 5 2 6 10 11


The AVL Tree after deletion of 10
            1
           /  \
          0    9
        /     /  \
       -1    5     11
           /  \
          2    6

Preorder traversal result would be
1 0 -1 9 5 2 6 11
"""

# myTree = AVLtree()
# root = None
# nums = [9, 5, 10, 0, 6, 11, -1, 1, 2]
# for num in nums:
#     root = myTree.insert(root, num)

# print("Preorder traversal of the constructed AVL tree is")
# myTree.pre_order(root)

# key = 10
# root = myTree.delete(root, key)

# print(f"Preorder Traversal after deletion of {key}")
# myTree.pre_order(root)


# This code is contributed by Ajitesh Pathak, organized by Sammy Wen.
