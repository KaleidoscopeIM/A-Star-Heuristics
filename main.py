from nodeCls import *
from graphPlot import *
from astarTrace import *

file1 = open("./connections.txt", "r")
connections = file1.readlines()
file2 = open("./locations.txt", "r")
locations = file2.readlines()

print('#### Assignment 2 by Gautam Saini and Shilpi FNU ####')
nodes_list = []
open_nodes = []
path_list = []
available_nodes = []
for aLocation in locations:
    aLocationList = aLocation.split()
    if aLocationList[0] != 'END':
        anode = aLocationList[0]
        available_nodes.append(anode)
        aConnectionList = []
        for aConnection in connections:
            aConnectionList = aConnection.split()
            if aConnectionList[0] != 'END' and aConnectionList[0] == anode:
                break
        nodes_list.append(NodeCls(aConnectionList, aLocationList))

print('List of cities:')
print(*available_nodes, sep=' , ')

initial_Exists = False
start_city = ''
while initial_Exists is False:
    start_city = input("Enter starting city:: ")
    if start_city in available_nodes:
        initial_Exists = True
    else:
        print('City is not available in list. Enter city from list :: ')

finale_exists = False
end_city = ''
while finale_exists is False:
    end_city = input("Enter end city: ")
    if end_city in available_nodes:
        finale_exists = True
    else:
        print('City is not available in list. Enter city from list.')

if start_city == end_city:
    print("Start and end city are same. Try again.")
    sys.exit("Start city and end city cannot be same. Please Try again.")

start_city_obj = object()
end_city_obj = object()
for aObj in nodes_list:
    if aObj.root == end_city:
        end_city_obj = aObj
    if aObj.root == start_city:
        start_city_obj = aObj

exclude = input("Enter list of city separated by comma to exclude from search (eg A1,A2,..) or press enter to "
                "continue without excluding :: ")
exclude_nodes = exclude.split(',')
for aExclude in exclude_nodes:
    if aExclude == '':
        break
    elif aExclude not in available_nodes:
        sys.exit(aExclude + " city not available in available cities list. Try again.")
    elif aExclude == start_city_obj.root:
        sys.exit("Start city cannot be excluded from tracing. try again.")
    elif aExclude == end_city_obj.root:
        sys.exit("End city cannot be excluded from tracing. try again.")
    else:
        nodes_list = update_by_excluding(nodes_list, aExclude)

step_flat = False
while step_flat is False:
    step_option = input("step by step option or not (y/n) :: ")
    step_option = step_option.lower()
    if step_option not in ['y', 'n']:
        print("Please select the correct option 'y' or 'n' and try again.")
        continue
    else:
        step_flat = True
heuristic_flag = False
while heuristic_flag is False:
    heuristic = input("Which heuristic to use? \n1. straight line distance or 2. fewest cities (1,2)?:: ")
    if heuristic not in ['1', '2']:
        print("Please select the correct option 1 or 2 and try again.")
        continue
    else:
        heuristic_flag = True
print_success = False
if heuristic == '1' and step_option == 'n':
    for aObj in nodes_list:
        aObj.straight_line_dist = calc_node_dist(aObj, end_city_obj)
    expansion_obj_lst = trace_straight_line(start_city_obj, end_city_obj, nodes_list)
    print_success = print_expansion_and_path(start_city_obj, end_city_obj, expansion_obj_lst, heuristic)
if heuristic == '2' and step_option == 'n':
    nodes_list = update_node_fw_dist(start_city_obj, nodes_list)
    expansion_obj_lst = trace_fewest_cities(start_city_obj, end_city_obj, nodes_list)
    print_success = print_expansion_and_path(start_city_obj, end_city_obj, expansion_obj_lst, heuristic)
if heuristic == '1' and step_option == 'y':
    for aObj in nodes_list:
        aObj.straight_line_dist = calc_node_dist(aObj, end_city_obj)
    expansion_obj_lst = trace_straight_line_with_steps(start_city_obj, end_city_obj, nodes_list)
    print_success = print_expansion_and_path(start_city_obj, end_city_obj, expansion_obj_lst, heuristic)
if heuristic == '2' and step_option == 'y':
    nodes_list = update_node_fw_dist(start_city_obj, nodes_list)
    expansion_obj_lst = trace_fewest_cities_with_steps(start_city_obj, end_city_obj, nodes_list)
    print_success = print_expansion_and_path(start_city_obj, end_city_obj, expansion_obj_lst, heuristic)

if print_success:
    draw_graph_option = input("\nWould you like to visualize graph? (y,n)::")
    if draw_graph_option == 'y':
        draw_graph(start_city_obj, end_city_obj, expansion_obj_lst, heuristic, nodes_list)


