class NodeCls:
    def __init__(self, connection_lst, location_lst):
        self.root = connection_lst[0]
        self.connections = -1
        self.neighbours = []
        self.straight_line_dist = -1
        self.fewest_city_dist = -1
        self.total_upto_dist = 0
        self.total_calc_dist = 0
        self.parent = object()
        self.locationX = int(location_lst[1])
        self.locationY = int(location_lst[2])

        if len(connection_lst) != 1:
            self.connections = int(connection_lst[1])
        else:
            self.connections = 0

        i = 0
        while i < len(connection_lst):
            if i == 0 or i == 1:
                i = i + 1
                continue
            self.neighbours.append(connection_lst[i])
            i = i + 1

    def get_node_root(self):
        return self.root
