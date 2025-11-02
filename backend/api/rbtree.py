# Define and implement red-black tree here (each node value is an Event)

RED = True
BLACK = False

class RBNode:
    def __init__(self, event):
        self.event = event
        self.left = None
        self.right = None
        self.parent = None
        self.color = RED

class RedBlackTree:
    def __init__(self):
        self.root = None

    def insert(self, event):
        new_node = RBNode(event)

        if self.root is None:
            new_node.color = BLACK 
            self.root = new_node
            return

        current = self.root
        while True:
            if event.start_time < current.event.start_time:
                if current.left is None:
                    current.left = new_node
                    new_node.parent = current
                    break
                current = current.left
            else:
                if current.right is None:
                    current.right = new_node
                    new_node.parent = current
                    break
                current = current.right

        # self._fix_insert(new_node)  # balancing to be implemented later

    def inorder(self):
        result = []
        self._inorder_helper(self.root, result)
        return result

    def _inorder_helper(self, node, result):
        if node:
            self._inorder_helper(node.left, result)
            result.append(node.event)
            self._inorder_helper(node.right, result)

    # Rotation and balancing
    def _left_rotate(self, node):
        pass

    def _right_rotate(self, node):
        pass

    def _fix_insert(self, node):
        pass
