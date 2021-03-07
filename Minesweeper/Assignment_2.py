#!/usr/bin/env python
# coding: utf-8

# In[212]:



#mine_locs = [[1,2],[2,2]]
#rows = 8
#columns = 8

#on board we will represent mines by -1

board = []
mine_locs = [] #2d list
rows = 5
cols = 5
revealed_squares = [[3,4]]
count_safe_squares = []
count_mines = []
revealed_safe_squares = [[3,3],[2,3],[2,4]]
revealed_mine_sqaures = []


# In[213]:



def make_board(mine_locs, rows, columns):
    board = [[0 for i in range(0,rows)] for j in range(columns)]
    
    for mine in mine_locs:
        mine_x = mine[0]
        mine_y = mine[1]
        
        board[mine_x][mine_y] = -1
    return board


# In[214]:


board = make_board([[1,2],[1,3],[3,4]],5,5)


# In[215]:


board


# In[164]:



#selects the square that is safe if there are safe squares known
#or makes a random choice
def make_move():
    
    if len(revealed_safe_squares) > 0:
        safe_move = reveal_safe_squares.pop()
        reveal_square(safe_move[0],safe_move[1])
        revealed_squares.append([safe_move[0],safe_move[1]])
        
    # if there are no known safe blocks then we have to choose at random
    else :
        while 1:
            row = randint(0,rows-1)
            col = randint(0,cols-1)
            if [row,col] not in revealed_sqaures:
                reveal_sqaure(row,col)
                revealed_squares.append([safe_move[0],safe_move[1]])
                break
            
   


# In[165]:



#count the number of mines around for a given square
def countMines(row,col):
    count = 0
    row_range = range(row-1,row+2)
    col_range = range(col-1,col+2)
    
    for i in row_range:
        for j in col_range:
            if (0 <= i < rows and 0 <= j < cols and board[i][j] == -1 ):
                count = count + 1
    return count


# In[166]:


countMines(2,2)


# In[167]:


#not used. Maybe won't need it
def countSafeSquares(row,col): #count Safe neighbors
    count = 0
    row_range = range(row-1,row+2)
    col_range = range(col-1,col+2)
    
    for i in row_range:
        for j in col_range:
            if (0 <= i < rows and 0 <= j < cols and board[i][j] >= 1 and board[i][j] <= 8 and (i != row and j != col)):
                count = count + 1
    return count


# In[168]:


countSafeSquares(3,3)


# In[169]:




def revealedSafeNeighbors(row,col): #reveals number of safe squares around a square
    count = 0
    row_range = range(row-1,row+2)
    col_range = range(col-1,col+2)
    
    for i in row_range:
        for j in col_range:
            if (i == row and j == col):
                continue
            if (0 <= i < rows and 0 <= j < cols and [i,j] in revealed_safe_squares ):
                count = count + 1
    return count


# In[170]:


a = revealedSafeNeighbors(2,4)
a


# In[180]:


def countHiddenNeighbors(row,col):
    count = 0
    row_range = range(row-1,row+2)
    col_range = range(col-1,col+2)
    
    for i in row_range:
        for j in col_range:
            if (i == row and j == col):
                continue
            if (0 <= i < rows and 0 <= j < cols and [i,j] not in revealed_squares ):
                count = count + 1
    return count


# In[181]:


a = countHiddenNeighbors(2,4)
a


# In[216]:



def countRevealedMines(row,col):
    count = 0
    row_range = range(row-1,row+2)
    col_range = range(col-1,col+2)
    
    for i in row_range:
        for j in col_range:
            if (i == row and j == col):
                continue
            if (0 <= i < rows and 0 <= j < cols and [i,j] in revealed_squares and board[i][j]==-1):
                count = count + 1
    return count


# In[217]:


a = countRevealedMines(2,4)
a


# In[18]:



def showBoard():
    for i in range(row):
        for j in range(col):
            
            if board[i][j] == -1 and [i,j] not in revealed_squares: #mine there but we havent check the square
                print("❓")
            if board[i][j] == -1 and [i,j] in revealed_squares: #mine and we have checked the seuare
                print("💣")     
            if board[i][j] == 0 : #undiscovered squares
                print("❓")
            if board[i][j] == 1 : #1 to 8 are revealed squares 
                print("1️⃣")
            if board[i][j] == 2 :
                print("2️⃣")
            if board[i][j] == 3 :
                print("3️⃣")
            if board[i][j] == 4 :
                print("4️⃣")
            if board[i][j] == 5 :
                print("5️⃣")
            if board[i][j] == 6 :
                print("6️⃣")
            if board[i][j] == 7 :
                print("7️⃣")
            if board[i][j] == 8 :
                print("8️⃣")            


# In[19]:



def reveal_square(x,y):
    
    revealed_squares.append([x,y])
    
    if board[x][y] != -1 : #not a mine
        count = countMines(x,y)
        board[x][y] = count
        print("agent chose a safe sqaure")
        num_safe_sqaures = num_safe_mines + 1
        
    
    if board[x][y] == -1 : #we chose a mine
        count_mines = count_mines + 1
        print("Agent chose a mine")
        
    showBoard()


# In[22]:



def check_safe_Sqaures(): #finds a safe sqaure on the board
    for i in range(rows):
        for j in range(cols):
            clue = countMines(i,j)
            hn = countHiddenNeighbors(i,j)
            rm = countRevealedMines(i,j)
            if hn == clue - rm :#then all the adjacent unrevealed sqaures are mines
                row_range = range(i-1,i+2)
                col_range = range(j-1,j+2)
                
                for a in row_range :
                    for b in col_range :
                        if [a,b] not in revealed_squares :
                            revealed_squares.append([a,b])
                            revealed_mine_squares.append([a,b])
                            board[a][b] = -1
                            showBoard()
                            print("mines found")
            
            if ((8-clue) -  revealedSafeSquares(i,j)) == hn :
                #all the surrounding mines are safe
                row_range = range(i-1,i+2)
                col_range = range(j-1,j+2)
                
                for a in row_range :
                    for b in col_range :
                        if [a,b] not in revealed_squares :
                            revealed_safe_squares.append([a,b])
                            board[a][b] = countMines(a,b)
                            showBoard()
                            print("safe squares found")
                


# In[ ]:




