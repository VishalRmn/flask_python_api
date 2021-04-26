# Python implementation of Hash Table Data Structure

# For each node in the hashtable, which will have a data portion and a pointer to the next node
class Node:
    def __init__(self, data, next_node):
        self.data = data
        self.next_node = next_node

# For each data portion in the hashtable, whih will have a key-value pair in it.


class Data:
    def __init__(self, key, value):
        self.key = key
        self.value = value


class HashTable:
    def __init__(self, table_size):
        # HashTable will have a predefined table size 'n', and each of these 'n' placeholders (addresses) will contain linked lists of nodes, based on their hash value.
        self.table_size = table_size
        # This will create a hash_table like this: [None, None, ... , None]
        self.hash_table = [None] * table_size

    # Method for calculating hash value based on key. The formula for calculating hash value can be changed to whatever suits best.
    # More efficient formulae with lower collision can be implemented.
    def custom_hash(self, key):
        hash_value = 0
        for i in key:
            hash_value += ord(i)
            hash_value = (hash_value * ord(i)) % self.table_size
        return hash_value

    # Method to add new node to the hash table
    def add_key_value(self, key, value):
        hashed_key = self.custom_hash(key)
        # Case 1: If the hashed address is empty
        if self.hash_table[hashed_key] is None:
            self.hash_table[hashed_key] = Node(Data(key, value), None)
        # Case 2: If the hashed address is non-empty
        else:
            node = self.hash_table[hashed_key]
            # Iterates till it reaches the end of the linked list at that hashed address, where the next points to None
            while node.next_node:
                node = node.next_node
            # Sets the next node of the final node as the new key-value pair
            node.next_node = Node(Data(key, value), None)

    def get_value(self, key):
        hashed_key = self.custom_hash(key)
        if self.hash_table[hashed_key] is not None:
            node = self.hash_table[hashed_key]
            # If the hashed address contains only one element
            if node.next_node is None:
                if node.data.key == key:
                    return node.data.value

            # If the hashed address contains multiple elements
            while node.next_node:  # This will run until the second-last node.
                if node.data.key == key:
                    return node.data.value
                node = node.next_node
            # Checking last node of linked list
            if node.data.key == key:
                return node.data.value

        # Finally if key is not present in the hash table
        return None

    def print_table(self):
        print("{")
        for i, val in enumerate(self.hash_table):
            if val is not None:
                llist_string = ""
                node = val
                if node.next_node:
                    while node.next_node:
                        llist_string += (
                            str(node.data.key) + " : " +
                            str(node.data.value) + " --> "
                        )
                        node = node.next_node
                    llist_string += (
                        str(node.data.key) + " : " +
                        str(node.data.value) + " --> None"
                    )
                    print(f"    [{i}] {llist_string}")
                else:
                    print(f"    [{i}] {val.data.key} : {val.data.value}")
            else:
                print(f"    [{i}] {val}")
        print("}")


# ht = HashTable(4)

# ht.add_key_value("abc", "defgh")
# ht.add_key_value("abc", "2")
# ht.add_key_value("abc", "3")
# ht.print_table()
