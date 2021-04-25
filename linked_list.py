class Node:
    def __init__(self, data=None, next_node=None):
        self.data = data
        self.next_node = next_node


class LinkedList:
    # wrapper class to keep track of head and tail of the linked list
    def __init__(self):
        self.head = None
        self.last_node = None

    def print_linked_list(self):
        string_ll = ""

        node = self.head
        if node is None:
            print(None)
        while node:
            string_ll += f" {str(node.data)} ->"
            node = node.next_node

        # for the end of list
        string_ll += " None"

        print(string_ll)

    def to_list(self):
        l = []
        if self.head is None:
            return l

        node = self.head
        while node:
            l.append(node.data)
            node = node.next_node
        return l

    def insert_beginning(self, data):
        # for empty linked list
        if self.head is None:
            self.head = Node(data, None)
            self.last_node = self.head

        new_node = Node(data, self.head)
        self.head = new_node

    def insert_at_end(self, data):
        if self.head is None:
            self.insert_beginning(data)
            return

        self.last_node.next_node = Node(data, None)
        self.last_node = self.last_node.next_node

    def get_user_by_id(self, user_id):
        node = self.head
        while node:
            if node.data["id"] is int(user_id):
                return node.data
            node = node.next_node
        return None
