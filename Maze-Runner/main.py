import random
import queue

def genMaze(dim, p):
  maze = []
  for x in range(dim):
    row = []
    for y in range(dim):
      #((row,col),isBlocked)
      row.append(((x,y), random.random() < p))
    maze.append(row)

  #No need to waste time with trivially unsolvable mazes
  maze[0][0] = ((0,0), False)
  end = dim-1
  maze[end][end] = ((end,end),False)

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
  if x-1 >= 0 and vis[x-1][y][isGoalQueue] == None and not maze[x-1][y][1]:
    neighbors.append((x-1,y))
  if y+1 < dim and vis[x][y+1][isGoalQueue] == None and not maze[x][y+1][1]:
    neighbors.append((x,y+1))
  if y-1 >= 0 and vis[x][y-1][isGoalQueue] == None and not maze[x][y-1][1]:
    neighbors.append((x,y-1))
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

maze = genMaze(1000, 0)
draw(maze)
print(BD_BFS(maze))