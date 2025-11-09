# Define and implement red-black tree here (each node value is an Event)

RED = True
BLACK = False

class Node:
    def __init__(self, key, value, color=RED):
        self.key = key          # typically event start datetime
        self.value = value      # the event object
        self.color = color      # RED or BLACK
        self.left = None
        self.right = None
        self.parent = None

class RedBlackTree:
    def __init__(self):
        self.nil = Node(None, None, color=BLACK)  # sentinel
        self.root = self.nil

    # Left rotate
    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.nil:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    # Right rotate
    def right_rotate(self, y):
        x = y.left
        y.left = x.right
        if x.right != self.nil:
            x.right.parent = y
        x.parent = y.parent
        if y.parent == None:
            self.root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x
        x.right = y
        y.parent = x

    # Insert node
    def insert(self, key, value):
        node = Node(key, value)
        node.left = self.nil
        node.right = self.nil
        node.parent = None

        y = None
        x = self.root

        while x != self.nil:
            y = x
            if node.key < x.key:
                x = x.left
            else:
                x = x.right

        node.parent = y
        if y == None:
            self.root = node
        elif node.key < y.key:
            y.left = node
        else:
            y.right = node

        node.color = RED
        self.insert_fixup(node)

    # Fix RB tree properties after insert
    def insert_fixup(self, z):
        while z.parent and z.parent.color == RED:
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if y and y.color == RED:
                    z.parent.color = BLACK
                    y.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        z = z.parent
                        self.left_rotate(z)
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self.right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y and y.color == RED:
                    z.parent.color = BLACK
                    y.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self.right_rotate(z)
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self.left_rotate(z.parent.parent)
        self.root.color = BLACK

    # In-order traversal to get sorted events
    def inorder(self, node=None, result=None):
        if result is None:
            result = []
        if node is None:
            node = self.root
        if node != self.nil:
            self.inorder(node.left, result)
            result.append(node.value)
            self.inorder(node.right, result)
        return result
