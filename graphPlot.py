from matplotlib import pyplot as plt
from matplotlib import animation

fig = plt.figure()
ax = plt.gca()
line, = ax.plot([], [], lw=2)
lines = []
dash_track_list = []
toggle = True
counter = 0
shortest_path_counter = 0
shortest_path_parent = None
figNum = 0


def init_lines():
    global dash_track_list, lines, toggle, counter, shortest_path_counter, shortest_path_parent
    toggle = True
    counter = 0
    shortest_path_counter = 0
    shortest_path_parent = None
    dash_track_list = []
    lines = [ax.plot([], [], lw=2, color='red', linestyle='solid')[0]]
    return lines


def append_dashed_lies(start_city_obj, expansion_obj_lst, nodes_list):
    global counter, lines
    aParent = expansion_obj_lst[counter]
    child_objs = []
    if aParent.root == start_city_obj.root:
        child_objs = get_child_objs(aParent, nodes_list)
        dash_track_list.append(aParent)
    else:
        child_objs = get_child_objs(aParent, nodes_list)
        for aAlreadyTraced in dash_track_list:
            if aAlreadyTraced in child_objs:
                child_objs.remove(aAlreadyTraced)
        dash_track_list.append(aParent)
    for aChild in child_objs:
        from_x = aParent.locationX
        to_x = aChild.locationX
        from_y = aParent.locationY
        to_y = aChild.locationY
        aline = ax.plot([from_x, to_x], [from_y, to_y], lw=2, color='red', linestyle='dashed')
        dash_track_list.append(aChild)
        lines.append(aline[0])


def append_solid_line(start_city_obj, expansion_obj_lst, nodes_list):
    global counter, lines
    child = expansion_obj_lst[counter]
    parent = child.parent
    from_x = parent.locationX
    to_x = child.locationX
    from_y = parent.locationY
    to_y = child.locationY
    aline = ax.plot([from_x, to_x], [from_y, to_y], lw=3, color='green', linestyle='solid')
    lines.append(aline[0])


def append_shortest_path_lines(start_city_obj, shortest_path_objs):
    global shortest_path_counter, lines, shortest_path_parent
    if shortest_path_counter >= len(shortest_path_objs):
        return
    else:
        child = shortest_path_objs[shortest_path_counter]
        shortest_path_counter += 1
        if child.root == start_city_obj.root:
            shortest_path_parent = child
        else:
            from_x = shortest_path_parent.locationX
            to_x = child.locationX
            from_y = shortest_path_parent.locationY
            to_y = child.locationY
            aline = ax.plot([from_x, to_x], [from_y, to_y], lw=3, color='yellow', linestyle='solid')
            lines.append(aline[0])
            shortest_path_parent = child


def animate(i, start_city_obj, expansion_obj_lst, shortest_path_objs, nodes_list):
    child_objs = None
    global dash_track_list, lines, counter, toggle
    if counter >= len(expansion_obj_lst):
        append_shortest_path_lines(start_city_obj, shortest_path_objs)
    else:
        if toggle:
            toggle = False
            append_dashed_lies(start_city_obj, expansion_obj_lst, nodes_list)
            counter += 1
        else:
            toggle = True
            append_solid_line(start_city_obj, expansion_obj_lst, nodes_list)

    return lines


def animate_graph(start_city_obj, end_city_obj, expansion_obj_lst, shortest_path_objs, nodes_list):

    global fig
    animation_obj = animation.FuncAnimation(fig, animate, init_func=init_lines,
                                            fargs=[start_city_obj, expansion_obj_lst,
                                                   shortest_path_objs, nodes_list],
                                            frames=60, interval=500, blit=True, repeat=False)
    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())
    # animation_obj.save('animation1.gif', writer='imagemagick', fps=1)
    plt.show()
    # plt.cla()
    # plt.clf()
    # plt.close(fig)


def draw_line(parent, child_objs, width, c, ls):
    for aChild in child_objs:
        xPoints = [parent.locationX, aChild.locationX]
        yPoints = [parent.locationY, aChild.locationY]
        plt.plot(xPoints, yPoints, linestyle=ls, linewidth=width, color=c)


def get_child_objs(parent, nodes_list):
    child_objs = []
    for aNode in nodes_list:
        if aNode.root in parent.neighbours:
            child_objs.append(aNode)
    return child_objs


def plot_main_graph(start_city_obj, end_city_obj, nodes_list, heuristic):
    x_points = []  # x points
    y_points = []  # y points
    for aNode in nodes_list:
        x_points.append(aNode.locationX)
        y_points.append(aNode.locationY)
    plt.scatter(x_points, y_points, s=50, edgecolors='none', c='green')
    plt.scatter(start_city_obj.locationX, start_city_obj.locationY, s=150, edgecolors='none', c='blue')
    plt.scatter(end_city_obj.locationX, end_city_obj.locationY, s=150, edgecolors='none', c='blue')
    for (xPoint, yPoint, aNode) in zip(x_points, y_points, nodes_list):
        label = ""
        if heuristic == '1':
            if start_city_obj.root == aNode.root or int(aNode.total_calc_dist) == 0:
                label = aNode.root
            else:
                label = aNode.root + " (" + str(int(aNode.total_calc_dist)) + ")"
        else:
            label = aNode.root + " (" + str(int(aNode.fewest_city_dist)) + ")"
        plt.annotate(label,
                     (xPoint, yPoint),
                     xytext=(xPoint + 8, yPoint + 8)
                     )


def draw_graph(start_city_obj, end_city_obj, expansion_obj_lst, heuristic, nodes_list):
    title = ""
    if heuristic == '1':
        title = "A star tracing - " + " straight line distance"
    else:
        title = "A star tracing - " + " fewest cities"
    plt.title(title)
    plt.xlabel("X  -> ")
    plt.ylabel("Y  -> ")
    plot_main_graph(start_city_obj, end_city_obj, nodes_list, heuristic)  # draw main graph first
    # draw all connections
    for aNode in nodes_list:
        child_objs = get_child_objs(aNode, nodes_list)
        for aChild in child_objs:
            draw_line(aNode, [aChild], 0.8, 'black', 'solid')

    shortest_path_objs = []  # the path will be in reverse order as it will be traced in revered order using parent
    # of each node
    cur_node = expansion_obj_lst[-1]
    while True:
        shortest_path_objs.append(cur_node)
        cur_node = cur_node.parent
        if cur_node.root == start_city_obj.root:
            shortest_path_objs.append(cur_node)
            break

    shortest_path_objs.reverse()
    animate_graph(start_city_obj, end_city_obj, expansion_obj_lst, shortest_path_objs, nodes_list)
