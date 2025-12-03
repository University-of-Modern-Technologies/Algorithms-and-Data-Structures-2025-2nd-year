class Node:
    def __init__(self, key, color="skyblue"):
        self.left: Node | None = None
        self.right: Node | None = None
        self.val = key


def preorder_traversal(root):
    if root:
        print(root.val, end=" ")
        preorder_traversal(root.left)
        preorder_traversal(root.right)


def inorder_traversal(root):
    if root:
        inorder_traversal(root.left)
        print(root.val, end=" ")
        inorder_traversal(root.right)


def postorder_traversal(root):
    if root:
        postorder_traversal(root.left)
        postorder_traversal(root.right)
        print(root.val, end=" ")


if __name__ == "__main__":
    root = Node(1)
    root.left = Node(2)
    root.right = Node(3)
    root.left.left = Node(4)
    root.left.right = Node(5)
    root.right.left = Node(13)
    root.right.right = Node(15)

    print("Preorder traversal")
    preorder_traversal(root)

    print("\nInorder traversal")
    inorder_traversal(root)

    print("\nPostorder traversal")
    postorder_traversal(root)
