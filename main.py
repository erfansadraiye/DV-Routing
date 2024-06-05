class Link:
    links = {}

    def __init__(self, link_id, neighbor):
        self.id = link_id
        self.neighbor = neighbor
        Link.links[link_id] = self

    def remove(self):
        Link.links.pop(self.id)

    @staticmethod
    def get_link_by_id(link_id):
        if link_id in Link.links:
            return Link.links[link_id]
        else:
            return None


class Neighbor:
    all_neighbors = []

    def __init__(self, ip_address, subnet_mask_bits_number, distance_estimate, link_id):
        self.ip_address = ip_address
        self.subnet_mask_bits_number = subnet_mask_bits_number
        self.distance_estimate = distance_estimate
        self.link_id = link_id
        self.neighbors = []

    def identifier(self):
        return f'{self.ip_address}/{self.subnet_mask_bits_number}'

    def add_neighbor(self, neighbor):
        neighbor.distance_estimate += self.distance_estimate
        self.neighbors.append(neighbor)

    def is_ip_in_network(self, ip):
        subnet_ip, subnet_bit_number = self.ip_address, self.subnet_mask_bits_number
        split_ip = ip.split(".")
        split_subnet_ip = subnet_ip.split(".")
        ip_binary = "".join([format(int(x), '08b') for x in split_ip])
        subnet_ip_binary = "".join([format(int(x), '08b') for x in split_subnet_ip])
        subnet_mask = "1" * int(subnet_bit_number) + "0" * (32 - int(subnet_bit_number))
        network_address = "".join([str(int(ip_binary[i]) & int(subnet_mask[i])) for i in range(32)])
        return network_address == subnet_ip_binary

    @staticmethod
    def _check_and_add_to_all_neighbors(new_neighbor, all_neighbors):
        key = new_neighbor.identifier()
        if key in all_neighbors:
            exist_neighbor = all_neighbors[key]
            if new_neighbor.distance_estimate < exist_neighbor.distance_estimate:
                all_neighbors[key] = new_neighbor
        else:
            all_neighbors[new_neighbor.identifier()] = new_neighbor

    @staticmethod
    def update_distances():
        all_neighbors = {}
        for link_id, link in Link.links.items():
            Neighbor._check_and_add_to_all_neighbors(link.neighbor, all_neighbors)
            for neighbor in link.neighbor.neighbors:
                Neighbor._check_and_add_to_all_neighbors(neighbor, all_neighbors)
        all_neighbors = list(all_neighbors.values())
        all_neighbors.sort(key=lambda x: x.ip_address)
        Neighbor.all_neighbors = all_neighbors


def add_link(link_id, neighbor):
    Link(link_id, neighbor)
    Neighbor.update_distances()


def remove_link(link_id):
    link = Link.get_link_by_id(link_id)
    if link is None:
        print("DEBUG: Link doesn't exist for removing")
    else:
        link.remove()
        Neighbor.update_distances()


def update_link(link_id, neighbors):
    link = Link.get_link_by_id(link_id)
    if link is None:
        print("DEBUG: link doesn't exist for updating")
    link_neighbor = link.neighbor
    for n in neighbors:
        link_neighbor.add_neighbor(n)
    Neighbor.update_distances()


def print_states():
    for n in Neighbor.all_neighbors:
        print(f'{n.ip_address}/{n.subnet_mask_bits_number} {n.distance_estimate}')


def route(dest_ip):
    for neighbor in Neighbor.all_neighbors:
        if neighbor.is_ip_in_network(dest_ip):
            return neighbor.link_id
    return "No route found"


if __name__ == '__main__':
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
            neighbor = Neighbor(ip_address, subnet_mask_bits_number, distance_estimate, link_id)
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
                neighbors.append(Neighbor(ip_address, subnet_mask_bits_number, distance_estimate, link_id))
            update_link(link_id, neighbors)
        elif input_text.startswith("route"):
            _, dest_ip = input_text.split()
            print(route(dest_ip))
