import random
#didnt realize that lists could pop from the front too, so this import wouldn't be necessary if I did it again
import queue

def genMaze(dim, p):
  maze = []
  for x in range(dim):
    row = []
    for y in range(dim):
      #((row,col),isBlocked)
      #I put the coords in to make it more readable when printed but it wound up being more of a hassle later when I had to flip
      row.append([(x,y), random.random() < p])
    maze.append(row)

  #No need to waste time with trivially unsolvable mazes
  maze[0][0] = [(0,0), False]
  end = dim-1
  maze[end][end] = [(end,end),False]

  return maze

def draw(maze):
  blocked = "⬛"
  free = "⬜"
  grid = []
  for row in maze:
    tiles = ""
    for tile in row:
      tiles += blocked if tile[1] else free
    grid+=tiles
    print(tiles)
  return grid

def BD_BFS(maze):
  dim = len(maze)
  end = dim-1
  qStart = queue.Queue()
  qGoal = queue.Queue()
  qStart.put(maze[0][0])
  qGoal.put(maze[end][end])
  vis = visited(dim)

  while not qStart.empty() and not qGoal.empty():
    node = qStart.get()
    x = node[0][0]
    y = node[0][1]
    neighbors = getNeighbors(node, maze, vis, 0)
    for neighbor in neighbors:
      newX = neighbor[0]
      newY = neighbor[1]
      vis[newX][newY][0] = [x,y]
      if not vis[newX][newY][1] == None:
        return finalPath(maze, vis, [newX,newY])
      qStart.put(maze[newX][newY])
    
    node = qGoal.get()
    x = node[0][0]
    y = node[0][1]
    neighbors = getNeighbors(node, maze, vis, 1)
    for neighbor in neighbors:
      newX = neighbor[0]
      newY = neighbor[1]
      vis[newX][newY][1] = [x,y]
      if not vis[newX][newY][0] == None:
        return finalPath(maze, vis, [newX,newY])
      qGoal.put(maze[newX][newY])
  return "No solution"

def finalPath(maze, vis, coords):
  path = [coords]
  parentStart = vis[coords[0]][coords[1]][0]
  parentGoal = vis[coords[0]][coords[1]][1]

  while not parentStart == [None,None]: 
    path = [parentStart] + path
    parentStart = vis[parentStart[0]][parentStart[1]][0]
  while not parentGoal == [None,None]: 
    path.append(parentGoal)
    parentGoal = vis[parentGoal[0]][parentGoal[1]][1]
  return path

def getNeighbors(node, maze, vis, isGoalQueue):
  dim = len(maze)
  neighbors = []
  x = node[0][0]
  y = node[0][1]
  if x+1 < dim and vis[x+1][y][isGoalQueue] == None and not maze[x+1][y][1]:
    neighbors.append((x+1,y))
  if y+1 < dim and vis[x][y+1][isGoalQueue] == None and not maze[x][y+1][1]:
    neighbors.append((x,y+1))
  if y-1 >= 0 and vis[x][y-1][isGoalQueue] == None and not maze[x][y-1][1]:
    neighbors.append((x,y-1))
  if x-1 >= 0 and vis[x-1][y][isGoalQueue] == None and not maze[x-1][y][1]:
    neighbors.append((x-1,y))
  return neighbors

#helper fucntion to initisalize closed set
#Use parent in the seen to avoid sacrificing the square root on the time/space complexity
def visited(dim):
  ret = []
  for i in range(dim):
    ret.append(falses(dim))
  ret[0][0] = [[None, None], None]
  ret[dim-1][dim-1] = [None, [None, None]]
  return ret

#helper for the helper
def falses(dim):
  ret = []
  for i in range(dim):
    ret.append([None, None])
  return ret

def printSol(maze, solution):
  print(solution)
  if solution == "No solution":
    return
  dim = len(maze)

  blocked = "⬛"
  free = "⬜"
  start = "🔫"
  goal = "🏁"
  path = "🆒"

  for i in range(dim):
    row = ""
    for j in range(dim):
      if (i,j) == (0,0):
        row  += start
      elif (i,j) == (dim-1, dim-1):
        row += goal
      elif maze[i][j][1] == True:
        row += blocked
      elif [i,j] in solution:
        row += path
      else:
        row += free
    print(row)

def flip(maze):
  dim = len(maze)
  end = dim-1
  flipped = []
  for i in range(dim):
    row = []
    for j in range(dim):
      node = maze[i][end-j].copy()
      node[0] = (i, j)
      row.append(node)
    flipped.append(row)  
  return flipped

def genFireMaze(dim, p):
  maze = genMaze(dim, p)
  
  end = dim-1
  #Again, no need to bother with mazes trivially ineligible
  maze[end][0][1] = False
  maze[0][end][1] = False
  sol = BD_BFS(maze)
  while sol == "No solution" or BD_BFS(flip(maze)) == "No solution":
    maze = genMaze(dim, p)
    #Again, no need to bother with mazes trivially ineligible
    maze[end][0][1] = False
    maze[0][end][1] = False
    sol = BD_BFS(maze)

  for i in range(dim):
    for j in range(dim):
      maze[i][j].append(False)

  #Top right on fire to start
  maze[0][end][2] = True

  return (maze, sol)

def tryFireRun(maze, sol, q):
  while not sol == []:
    nxt = sol.pop(0)
    if maze[nxt[0]][nxt[1]][2]:
      return "Burnt to a crisp"
    propagateFlames(maze, q)
  return "A little toasty but still made it!"

def propagateFlames(maze, q):
  dim = len(maze)
  for i in range(dim):
    for j in range(dim):
      #Can only set on fire if not burning or blocked
      node = maze[i][j]
      if not (node[2] or node[1]):
        k = howManyBurningNeighbors(node, maze)
        p = 1 - (1-q)**k
        if random.random() < p:
          node[2] = True


def howManyBurningNeighbors(node, maze):
  dim = len(maze)
  #Use fake visited array to check all unblocked neighbors
  vis = [[[None]*2]*dim]*dim
  nbrs = getNeighbors(node, maze, vis, 0)

  burning = 0
  for nbr in nbrs:
    if maze[nbr[0]][nbr[1]][2]:
      burning += 1

  return burning

#DFS but considers who has the most burning neighbors when choosing a path
def fireDFS(maze, q):
  dim = len(maze)
  end = dim-1
  stack = [maze[0][0]]
  vis = visited(dim)
  #Lazily reusing something I made for BDBFS so I have to unmark the goal
  vis[end][end] = [None,None]

  while not stack == []:
    node = stack.pop()
    x = node[0][0]
    y = node[0][1]
    
    #No point in trying to go back to a space that's been set on fire since we last saw it
    if maze[x][y][2]:
        continue
    
    #Need to make sure we dont back track into a fire
    #Since we're doing DFS, we know we come from the same parent as where we just were, so only one place we need to hit on the path back
    #Except for the start node, of course, since there is no parent
    if (x,y) != (0,0):
        parent = vis[x][y][0]
        if maze[parent[0]][parent[1]][2]:
            #If we're at a dead end and can't go back, we must accept our fate
            return "Burnt to a crisp"
    neighbors = getNeighbors(node, maze, vis, 0)
    neighbors = minBurningNeighbors(neighbors, maze)
    while neighbors != []:
      #Want to pop from the end so the worst choices are towards the bottom of the stack
      neighbor = neighbors.pop()
      newX = neighbor[0]
      newY = neighbor[1]
      vis[newX][newY][0] = [x,y]

      #Cant go to a burning spot
      if maze[newX][newY][2]:
        continue
      if (newX,newY) == (end,end):
        return "A little toasty but still made it!"
      stack.append(maze[newX][newY])
    propagateFlames(maze,q)
  return "Burnt to a crisp"    

def minBurningNeighbors(neighbors, maze):
  #Zip list with burning neighbor counts
  withCounts = [(howManyBurningNeighbors(maze[nbr[0]][nbr[1]], maze), nbr) for nbr in neighbors]
  withCounts.sort(key = lambda x: x[0])
  #Sort by counts and unzip
  #Additionally, since sort() is stable we will still go: right, down, up, left if there is a tie 
  return [x[1] for x in withCounts]

flammabilities = [x/20 +.05 for x in range(20)]
print(flammabilities)

for f in flammabilities:
  c = 0
  for i in range(20):
    maze, sol = genFireMaze(100,.32)
    text = fireDFS(maze, f) #switched with tryFireRun() to try the other method
    print(text)
    if text == "A little toasty but still made it!":
      c = c + 1
  print("Informed search with flammability: " + str(f) + " resulted in " + str(c) + " successes out of 20 attempts")