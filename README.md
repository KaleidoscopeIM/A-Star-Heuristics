The project aims to search cities(nodes) from a given graph with multiple option such as lowest cost or straight line.

Program has multiple stages and at each stage it will ask for an input.

If there is no path between given start and end city or the graph is disconnected graph, then it will show that there is no path available between two given nodes.

**Step to setup script:**

Connection and location file should be in same folder with the code. Connection file represents edges and location file represent nodes with x,y locations.

1. Sample connection.txt and location.txt provided are already available.
2. Please replace/edit those if want to test for any other connection and location file.
3. Open the command prompt and go to the location where code is placed.
4. Execute the program by running at command  python main.py
5. Provide the initial node and final node when prompted. Inputs are case sensitive, please make sure to select it from the provided list.
6. f the program doesn&#39;t execute with the command then please main sure that environment variable contains the python path.

**Steps to while ecexuting script:**

1. Enter list of cities: A list of cities will be shown on the screen
2. Enter starting city: enter a start city from the list
3. Enter end city: enter a city from the given list
4. Enter list of city separated by comma to exclude from search (eg A1,A2,..) or press enter to skip
5. step by step option or not (y/n)
6. Which heuristic to use - Enter 1 for straight line distance or 2 for fewest cities
7. Would you like to visualize graph?
8. After step 7 the program will exit. Please execute the main.py again to check other options available in the program.

Alternatively,

open the folder in pyCharm ( File --\&gt; Open --\&gt; Folder path). Set the path for the python.exe and then right click on main.py and select Run &#39;main&#39;
