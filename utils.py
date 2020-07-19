import math
import sys
from queue import Queue
sys.setrecursionlimit(10000)


def calc_node_dist(start_node, end_node):
    fromX = start_node.locationX
    fromY = start_node.locationY
    toX = end_node.locationX
    toY = end_node.locationY
    total_length = math.sqrt(math.pow((toX - fromX), 2) + math.pow((toY - fromY), 2))
    return total_length


def update_by_excluding(nodes_list, anexclude):
    new_node_list = []
    for aNode in nodes_list:
        if aNode.root == anexclude:
            continue
        newNeighbours = []
        for aNeighbour in aNode.neighbours:
            if aNeighbour != anexclude:
                newNeighbours.append(aNeighbour)
        aNode.neighbours = newNeighbours
        new_node_list.append(aNode)
    return new_node_list


def print_expansion_and_path(start_city_obj, end_city_obj, expansion_obj_lst, heuristic):
    success = True
    expansion_lst = []
    for anode in expansion_obj_lst:
        expansion_lst.append(anode.root)

    if end_city_obj.root not in expansion_lst:
        print("Path between "+ start_city_obj.root + " and " + end_city_obj.root + " not found.")
        success = False
        return
    print("Expansion order: ")
    print(*expansion_lst, sep=" -> ")

    path_objs = []  # the path will be in reverse order as it will be traced in revered order using parent of each node
    cur_node = expansion_obj_lst[-1]
    while True:
        path_objs.append(cur_node)
        cur_node = cur_node.parent
        if cur_node.root == start_city_obj.root:
            path_objs.append(cur_node)
            break

    path_objs.reverse()
    print("shortest path: ")
    path_lst = []
    for aObj in path_objs:
        path_lst.append(aObj.root)
    print(*path_lst, sep=" -> ")
    city1 = path_objs[0]
    city2 = object()
    total_dist = 0
    for aObj in path_objs:
        if aObj == city1:
            continue
        city2 = aObj
        if heuristic == '1':
            aDist = calc_node_dist(city1, city2)
            total_dist = total_dist + aDist
            print(city1.root + " to " + city2.root + " length: " + str(aDist))
        if heuristic == '2':
            total_dist += 1
            print(city1.root + " to " + city2.root + " length: " + str(1))
        city1 = city2
    print("Total path length: "+str(total_dist))
    return success


def recursive_update_fw_count(root_node, node_list, count):
    allNeighbours = root_node.neighbours
    allNeighboursObj = []
    count = count + 1
    for aNeighbour in allNeighbours:
        aNeighbourObj = object()
        for aNode in node_list:
            if aNode.root == aNeighbour:
                aNeighbourObj = aNode
                break
        if aNeighbourObj.fewest_city_dist == -1:
            allNeighboursObj.append(aNeighbourObj)
            aNeighbourObj.fewest_city_dist = count
    for aNeighbourObj in allNeighboursObj:
        recursive_update_fw_count(aNeighbourObj, node_list, count)


def update_node_fw_dist(start_obj, node_list):
    queue_objs = Queue()
    for aNode in node_list:
        if aNode.root == start_obj.root:
            aNode.fewest_city_dist = 0
            break
    queue_objs.put(start_obj)
    count = 0
    while True:
        if queue_objs.empty():
            break
        anObj = queue_objs.get()
        count = anObj.fewest_city_dist + 1
        for aNeighbour in anObj.neighbours:
            aNeighbourObj = object()
            for aNode in node_list:
                if aNode.root == aNeighbour:
                    aNeighbourObj = aNode
                    break
            if aNeighbourObj.fewest_city_dist == -1:
                aNeighbourObj.fewest_city_dist = count
                queue_objs.put(aNeighbourObj)
    return node_list


