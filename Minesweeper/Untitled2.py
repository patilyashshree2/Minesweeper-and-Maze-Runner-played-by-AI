#!/usr/bin/env python
# coding: utf-8

# In[20]:



correct_choice = []
wrong_choice = [] 
revealed_squares = []
count_safe_squares = []
count_mines = []
revealed_safe_squares = []
revealed_mine_sqaures = []
count_mines


# In[42]:


import random
board = []
rows = 6
cols = 6
revealed_squares = []
count_safe_squares = []
revealed_safe_squares = []
revealed_mine_squares = []

global count_mines
count_mines = 0
def make_board(rows, columns, number_of_mines):                            #CREATE RANDOMLY
    board = [[0 for i in range(0,rows)] for j in range(0,columns)]
    x=0
    while(x!=number_of_mines):
        i = random.randint(0,rows-1)
        j = random.randint(0,columns-1)
        if(board[i][j]!=-1):
            board[i][j] = -1
            x = x+1
    return board


# In[43]:


board = make_board(6,6,12)
board


# In[44]:


count_mines


# In[61]:


def make_move():
    
    if len(revealed_safe_squares) > 0:
        safe_move = revealed_safe_squares.pop()
        reveal_square(safe_move[0],safe_move[1])
        revealed_squares.append([safe_move[0],safe_move[1]])
        showBoard()
    # if there are no known safe blocks then we have to choose at random
    else :
        while 1:
            row = random.randint(0,rows-1)
            col = random.randint(0,cols-1)
            if [row,col] not in revealed_squares:
                #reveal_square(row,col)
                revealed_squares.append([row,col])
                if board[row][col]!=-1:
                    board[row][col]= countMines(row,col)
                    showBoard()
                else:
                    
                    print(count_mines)
                    showBoard()
                break
            


# In[62]:


make_move()
    
    


# In[60]:



#count the number of mines around for a given square
def countMines(row,col):
    count = 0
    row_range = range(row-1,row+2)
    col_range = range(col-1,col+2)
    
    for i in row_range:
        
        for j in col_range:
            if (i == row and j == col):
                continue
            if (0 <= i < rows and 0 <= j < cols and board[i][j] == -1 ):
                count = count + 1
    return count


# In[15]:



def reveal_square(x,y):

    revealed_squares.append([x,y])
    
    if board[x][y] != -1 : #not a mine
        count = countMines(x,y)
        board[x][y] = count
        print("agent chose a safe sqaure")
        
        #num_safe_squares = num_safe_mines + 1
        
    
    if board[x][y] == -1 : #we chose a mine
        #count_mines = count_mines + 1
        print("Agent chose a mine")
        


# In[13]:



def showBoard():
    for i in range(rows):
        for j in range(cols):
            
            if board[i][j] == -1 and [i,j] not in revealed_squares: #mine there but we havent check the square
                print("❓", end = '')
            if board[i][j] == -1 and [i,j] in revealed_squares: #mine and we have checked the seuare
                print("💣", end = '')     
            if board[i][j] == 0 : #undiscovered squares
                print("❓", end = '')
            if board[i][j] == 1 : #1 to 8 are revealed squares 
                print("1️⃣", end = '')
            if board[i][j] == 2 :
                print("2️⃣", end = '')
            if board[i][j] == 3 :
                print("3️⃣", end = '')
            if board[i][j] == 4 :
                print("4️⃣", end = '')
            if board[i][j] == 5 :
                print("5️⃣", end = '')
            if board[i][j] == 6 :
                print("6️⃣", end = '')
            if board[i][j] == 7 :
                print("7️⃣", end = '')
            if board[i][j] == 8 :
                print("8️⃣", end = '')            
        print("")


# In[ ]:





# In[12]:


#not used. Maybe won't need it
def countSafeSquares(row,col): #count Safe neighbors
    count = 0
    row_range = range(row-1,row+2)
    col_range = range(col-1,col+2)
    
    for i in row_range:
        for j in col_range:
            if (i == row and j == col):
                continue
            if (0 <= i < rows and 0 <= j < cols and board[i][j] >= 1 and board[i][j] <= 8 and (i != row and j != col)):
                count = count + 1
    return count


# In[11]:


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


# In[10]:


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


# In[9]:



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


# In[7]:



def check_safe_Squares(): #finds a safe square on the board 
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
            
            if ((8-clue) -  revealedSafeNeighbors(i,j)) == hn :
                #all the surrounding mines are safe
                
                
                row_range = range(i-1,i+2)
                col_range = range(j-1,j+2)
                
                for a in row_range :
                    for b in col_range :
                        if [a,b] not in revealed_squares and 0<=a<=rows-1 and 0<=b<=cols-1:
                            revealed_safe_squares.append([a,b])
                            print(a,b)
                            board[a][b] = countMines(a,b)
                            showBoard()
                            print("safe squares found")
                


# In[ ]:




