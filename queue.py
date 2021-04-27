class Node:
    def __init__(self, data, next_node):
        self.data = data
        self.next_node = next_node


class Queue:
    def __init__(self):
        self.head = None
        self.tail = None

    def enqueue(self, data):
        # Case 1: If queue is empty
        if self.head is None and self.tail is None:
            self.head = self.tail = Node(data, None)
            return

        # Case 2: Non-empty queue
        self.tail.next_node = Node(data, None)
        self.tail = self.tail.next_node
        return

    def dequeue(self):
        # Case 1: If queue is empty
        if self.head is None and self.tail is None:
            return None
        # Case 2: If queue has only one element
        elif self.head == self.tail:
            removed = self.head
            self.head = self.tail = None
            return removed
        # Case 3: Queue has multiple elements
        else:
            removed = self.head
            self.head = self.head.next_node
            return removed
        return
