from pip._vendor.distlib.compat import raw_input
from utils import *
from queue import Queue


def trace_straight_line(start_node, end_node, node_list):
    expansion_lst = []
    open_nodes = [start_node]
    while True:
        if len(open_nodes) == 0:
            break
        cur_obj = object()
        min_dist = -1
        for aNode in open_nodes:
            if min_dist == -1 or aNode.total_calc_dist < cur_obj.total_calc_dist:
                min_dist = aNode.straight_line_dist
                cur_obj = aNode

        remove_node_lst = []
        for aNode in open_nodes:
            if aNode.root != cur_obj.root:
                remove_node_lst.append(aNode)
        open_nodes = remove_node_lst

        expansion_lst.append(cur_obj)
        cur_neighbours_obj = []
        for aNode in node_list:
            if aNode.root in cur_obj.neighbours:
                cur_neighbours_obj.append(aNode)

        for aNeighbour in cur_neighbours_obj:
            parent_child_dist = calc_node_dist(cur_obj, aNeighbour)
            upto_dist = parent_child_dist + cur_obj.total_upto_dist
            calc_dist = upto_dist + aNeighbour.straight_line_dist
            if aNeighbour.total_calc_dist == 0 or calc_dist < aNeighbour.total_calc_dist:
                found = False
                for aExpendedNode in expansion_lst:
                    if aExpendedNode.root == aNeighbour.root:
                        found = True
                if found is False:
                    open_nodes.append(aNeighbour)
                    aNeighbour.total_upto_dist = upto_dist
                    aNeighbour.total_calc_dist = calc_dist
                    aNeighbour.parent = cur_obj

    final_exp_lst = []
    for anode in expansion_lst:
        final_exp_lst.append(anode)
        if anode.root == end_node.root:
            break
    return final_exp_lst


def trace_straight_line_with_steps(start_node, end_node, node_list):
    expansion_lst = []
    open_nodes = [start_node]
    print(">> At each step please press enter to continue. <<")
    while True:
        if len(open_nodes) == 0:
            break
        cur_obj = object()
        min_dist = -1
        for aNode in open_nodes:
            if min_dist == -1 or aNode.total_calc_dist < cur_obj.total_calc_dist:
                min_dist = aNode.straight_line_dist
                cur_obj = aNode
        if cur_obj.root == end_node.root:
            expansion_lst.append(cur_obj)
            break
        remove_node_lst = []
        for aNode in open_nodes:
            if aNode.root != cur_obj.root:
                remove_node_lst.append(aNode)
        open_nodes = remove_node_lst

        expansion_lst.append(cur_obj)
        cur_neighbours_obj = []
        for aNode in node_list:
            if aNode.root in cur_obj.neighbours:
                cur_neighbours_obj.append(aNode)

        for aNeighbour in cur_neighbours_obj:
            parent_child_dist = calc_node_dist(cur_obj, aNeighbour)
            upto_dist = parent_child_dist + cur_obj.total_upto_dist
            calc_dist = upto_dist + aNeighbour.straight_line_dist
            if aNeighbour.total_calc_dist == 0 or calc_dist < aNeighbour.total_calc_dist:
                found = False
                for aExpendedNode in expansion_lst:
                    if aExpendedNode.root == aNeighbour.root:
                        found = True
                if found is False:
                    open_nodes.append(aNeighbour)
                    aNeighbour.total_upto_dist = upto_dist
                    aNeighbour.total_calc_dist = calc_dist
                    aNeighbour.parent = cur_obj
        print("City selected: "+cur_obj.root)
        print("Possible cities to travel: ", end="")
        cities_to_travel = []
        for aNode in open_nodes:
            cities_to_travel.append(aNode.root)
        print(*cities_to_travel, sep=", ")
        print("Cities at the end of possible path: ", end="")
        cities_at_end = []
        for aNode in open_nodes:
            cities_at_end.append(aNode.root + "(" + str(aNode.total_calc_dist) + ")")
        print(*cities_at_end, sep=", ")
        print("********************************************************************************")
        enter_press = raw_input("")

    return expansion_lst


def trace_fewest_cities(start_node, end_node, node_list):
    expansion_lst = []
    expansion_queue = Queue()
    expansion_queue.put(start_node)
    print(">> At each step please press enter to continue. <<")
    level = 0
    while True:
        if expansion_queue.empty():
            break
        cur_obj = expansion_queue.get()
        if cur_obj.root == end_node.root:
            expansion_lst.append(cur_obj)
            break
        expansion_lst.append(cur_obj)
        for aNeighbour in cur_obj.neighbours:
            for aNode in node_list:
                if aNode.root == aNeighbour:
                    if aNode in expansion_lst:
                        break
                    expansion_queue_lst = list(expansion_queue.queue)
                    if aNode in expansion_queue_lst:
                        break
                    aNode.parent = cur_obj
                    expansion_queue.put(aNode)
                    break

    return expansion_lst


def trace_fewest_cities_with_steps(start_node, end_node, node_list):
    expansion_lst = []
    expansion_queue = Queue()
    expansion_queue.put(start_node)
    while True:
        if expansion_queue.empty():
            break
        cur_obj = expansion_queue.get()
        if cur_obj.root == end_node.root:
            expansion_lst.append(cur_obj)
            break
        expansion_lst.append(cur_obj)
        for aNeighbour in cur_obj.neighbours:
            for aNode in node_list:
                if aNode.root == aNeighbour:
                    if aNode in expansion_lst:
                        break
                    expansion_queue_lst = list(expansion_queue.queue)
                    if aNode in expansion_queue_lst:
                        break
                    aNode.parent = cur_obj
                    expansion_queue.put(aNode)
                    break

        print("City selected: " + cur_obj.root)
        print("Possible cities to travel: ", end="")
        cities_to_travel = []
        cities_at_end = []
        cities_to_travel_objs = list(expansion_queue.queue)
        for aNode in cities_to_travel_objs:
            cities_to_travel.append(aNode.root)
            cities_at_end.append(aNode.root + "(" + str(1) + ")")

        print(*cities_to_travel, sep=", ")
        print("Cities at the end of possible path: ", end="")
        print(*cities_at_end, sep=", ")
        print("********************************************************************************")
        enter_press = raw_input("")
    return expansion_lst
