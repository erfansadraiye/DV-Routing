def get_or_create_link_by_id(link_id):
    exist_link = get_link_by_id(link_id)
    if exist_link is None:
        return Link(link_id)
    else:
        return exist_link


def get_link_by_id(link_id):
    if link_id in Link.links:
        return Link.links[link_id]
    else:
        return None


def is_ip_in_network(ip, subnet_ip, subnet_bit_number):
    # return ipaddress.ip_address(ip) in ipaddress.ip_network(f'{subnet_ip}/{subnet_bit_number}')
    split_ip = ip.split(".")
    split_subnet_ip = subnet_ip.split(".")
    ip_binary = "".join([format(int(x), '08b') for x in split_ip])
    subnet_ip_binary = "".join([format(int(x), '08b') for x in split_subnet_ip])
    subnet_mask = "1" * int(subnet_bit_number) + "0" * (32 - int(subnet_bit_number))
    network_address = "".join([str(int(ip_binary[i]) & int(subnet_mask[i])) for i in range(32)])
    return network_address == subnet_ip_binary

class Link:
    links = {}

    def __init__(self, link_id):
        self.id = link_id
        self.neighbors = []
        Link.links[link_id] = self

    def get_neighbor(self, neighbor):
        return self.neighbors[self.neighbors.index(neighbor)]

    def has_neighbor(self, neighbor):
        return neighbor in self.neighbors

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def remove(self):
        Link.links.pop(self.id)


class Neighbor:
    def __init__(self, ip_address, subnet_mask_bits_number, distance_estimate):
        self.ip_address = ip_address
        self.subnet_mask_bits_number = subnet_mask_bits_number
        self.distance_estimate = distance_estimate

    def __eq__(self, other):
        return self.ip_address == other.ip_address and self.subnet_mask_bits_number == other.subnet_mask_bits_number


def add_link(link_id, neighbor):
    link = get_or_create_link_by_id(link_id)
    link.add_neighbor(neighbor)


def remove_link(link_id):
    link = get_link_by_id(link_id)
    if link is None:
        print("DEBUG: Link doesn't exist for removing")
    else:
        link.remove()


def update_link(link_id, neighbors):
    link = get_link_by_id(link_id)
    if link is None:
        print("DEBUG: link doesn't exist for updating")
    nearest_neighbor_dist = sorted(link.neighbors, key=lambda x: x.distance_estimate)[0].distance_estimate
    for n in neighbors:
        if link.has_neighbor(n):
            link_neighbor = link.get_neighbor(n)
            link_neighbor.distance_estimate = min(n.distance_estimate + nearest_neighbor_dist,
                                                  link_neighbor.distance_estimate)
        else:
            n.distance_estimate = nearest_neighbor_dist + n.distance_estimate
            link.add_neighbor(n)


def print_states():
    links = Link.links
    neighbors = []
    for link_id, link in links.items():
        neighbors.extend(link.neighbors)
    neighbors.sort(key=lambda x: x.ip_address)
    for x in neighbors:
        print(f'{x.ip_address}/{x.subnet_mask_bits_number} {x.distance_estimate}')


def route(dest_ip):
    for link_id, link in Link.links.items():
        for n in link.neighbors:
            if is_ip_in_network(dest_ip, n.ip_address, n.subnet_mask_bits_number):
                return str(link_id)
    return "No route found"


import sys

if __name__ == '__main__':
    sys.stdin = open('input.txt', 'r')
    while True:
        input_text = input()
        if input_text == "exit":
            break
        elif input_text == "print":
            print_states()
        elif input_text.startswith("add link"):
            _, _, link_id, ip_and_num, distance_estimate = input_text.split()
            distance_estimate = int(distance_estimate)
            ip_address, subnet_mask_bits_number = ip_and_num.split("/")
            neighbor = Neighbor(ip_address, subnet_mask_bits_number, distance_estimate)
            add_link(link_id, neighbor)
        elif input_text.startswith("remove link"):
            _, _, link_id = input_text.split()
            remove_link(link_id)
        elif input_text.startswith("update"):
            _, link_id, distance_vector_length = input_text.split()
            distance_vector_length = int(distance_vector_length)
            neighbors = []
            for i in range(distance_vector_length):
                input_text = input()
                ip_and_num, distance_estimate = input_text.split()
                distance_estimate = int(distance_estimate)
                ip_address, subnet_mask_bits_number = ip_and_num.split("/")
                neighbors.append(Neighbor(ip_address, subnet_mask_bits_number, distance_estimate))
            update_link(link_id, neighbors)
        elif input_text.startswith("route"):
            _, dest_ip = input_text.split()
            print(route(dest_ip))
