#!/usr/bin/env python
# coding: utf-8

# In[1]:


correct_choice = []   #Mines Marked Correctly
wrong_choice = []     #Mines which had a Blast
global count_mines    #Total mines marked and had a blast till now
count_mines = 0


# In[2]:


import random
board = []
rows = 5                         
cols = 5
revealed_squares = []
count_safe_squares = []
revealed_safe_squares = []
revealed_mine_squares = []

#CREATE RANDOMLY 
#Input: Dimensions of 2D matrix and total number of Mines in it

def make_board(rows, columns, number_of_mines):                            
    board = [[0 for i in range(0,rows)] for j in range(0,columns)]
    x=0
    while(x!=number_of_mines):
        i = random.randint(0,rows-1)
        j = random.randint(0,columns-1)
        if(board[i][j]!=-1):
            board[i][j] = -1
            x = x+1
    return board


# In[3]:


board = make_board(5,5,15)
board


# In[4]:


#Visualization 
def showBoard():
    for i in range(rows):
        for j in range(cols):
            
            if board[i][j] == -1 and [i,j] not in revealed_squares: #Mines Present but Squares not Revealed
                print("❓", end = '')
            if board[i][j] == -1 and [i,j] in revealed_squares: #Mines Marked
                print("💣", end = '')     
            if board[i][j] == 0 : #Undiscovered squares
                print("❓", end = '')
            if board[i][j] == 1 : #Revealed Square with neighboring squares having 1 Mine
                print("1️⃣", end = '')
            if board[i][j] == 2 : #Revealed Square with neighboring squares having 2 Mines
                print("2️⃣", end = '')
            if board[i][j] == 3 : #Revealed Square with neighboring squares having 3 Mines
                print("3️⃣", end = '')
            if board[i][j] == 4 : #Revealed Square with neighboring squares having 4 Mines
                print("4️⃣", end = '')
            if board[i][j] == 5 : #Revealed Square with neighboring squares having 5 Mines
                print("5️⃣", end = '')
            if board[i][j] == 6 : #Revealed Square with neighboring squares having 6 Mines
                print("6️⃣", end = '')
            if board[i][j] == 7 : #Revealed Square with neighboring squares having 7 Mines
                print("7️⃣", end = '')
            if board[i][j] == 8 : #Revealed Square with neighboring squares having 8 Mines
                print("8️⃣", end = '')
            if board[i][j] == 9 : #Revealed Square which had a blast after selecting the square randomly
                print("💥", end = '')
        print("")


# In[5]:


#Count the number of mines around for a given square (to display the clue)
def countMines(row,col):
    count = 0
    row_range = range(row-1,row+2)       #for next and previous row
    col_range = range(col-1,col+2)       #for next and previous column
    
    for i in row_range:
        for j in col_range:
            if (i == row and j == col):  #exclude itself
                continue
            #Mines at -1(for unknown or marked Mines) and 9 (for Mines which were selected randomly and had a blast)
            if (0 <= i < rows and 0 <= j < cols and (board[i][j] == -1 or board[i][j] == 9)): 
                count = count + 1
    return count


# In[6]:


#Count Safe Neighbors(Neighbors without Mine)
def countSafeSquares(row,col): 
    count = 0
    row_range = range(row-1,row+2)
    col_range = range(col-1,col+2)
    
    for i in row_range:
        for j in col_range:
            if (i == row and j == col):
                continue
            if (0 <= i < rows and 0 <= j < cols and board[i][j] >= 1 and board[i][j] <= 8):
                count = count + 1
    return count


# In[7]:


#Count Revealed Safe Neighbors(Neighbors without Mine)
def revealedSafeNeighbors(row,col): 
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


# In[8]:


#Count Hidden Neighbors (It can be safe or Mine may be present in it)- Unrevealed Neighbors
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


#Count Total Revealed Mines in Neighboring Squares
def countRevealedMines(row,col):
    count = 0
    row_range = range(row-1,row+2)
    col_range = range(col-1,col+2)
    
    for i in row_range:
        for j in col_range:
            if (i == row and j == col):
                continue
            if (0 <= i < rows and 0 <= j < cols and [i,j] in revealed_mine_squares and (board[i][j]==-1 or board[i][j]==9)):
                count = count + 1
    return count


# In[10]:


#Gives the numbers of neighbors(mines and safe squares both), As square at the edge and corner does not have 8 neighbors
def neighbors_count(i,j): 
    count = 0
    a = max(j-1,0)
    b = min(j+2,cols)
    c = max(i-1,0)
    d = min(i+2,rows)
    
    row_range = range(c,d)
    col_range = range(a,b)
    
    for x in row_range:
        for y in col_range:
            if (x==i and y==j):
                continue
            count = count+1
    return count
                
    


# In[11]:


# Main Function
def make_move():
    global count_mines
    
    while True:
        if len(revealed_squares) == rows*cols:           #When all Squares are Revealed
         
            return
        
        row = random.randint(0,rows-1)                   #Random Selection of Square when knowledge is not sufficient
        col = random.randint(0,cols-1)
        
        #Append it to the revealed squares
        if [row,col] not in revealed_squares:             
            revealed_squares.append([row,col])
            #No Mine present at that square then count the neighboring mines and display the count
            if board[row][col]!=-1:
                if [row,col] not in revealed_safe_squares:
                    revealed_safe_squares.append([row,col])
                count = countMines(row,col)
                board[row][col] = count
                print("agent chose a safe square")
                showBoard()
                print(revealed_squares)                 #Print Revealed Squares soo far
                check_safe_Squares() 
                
            #Mine is present at the selected square - it Blasts (Agent Randomly selected a Mine)
            else:
                if [row,col] not in revealed_mine_squares:
                    revealed_mine_squares.append([row,col])
                if [row,col] not in wrong_choice:
                    wrong_choice.append([row,col])         #Add it to the Mines blasted ie. wrong_choice List
                count_mines = count_mines + 1
                board[row][col]=9
                print('agent randomly selected a mine')
                showBoard()
                print(revealed_squares)                    #Print Revealed Squares soo far
                check_safe_Squares()
            break
   


# In[12]:


# When Knowledge can be drawn for the information available. 
# Check for Safe Squares
def check_safe_Squares():  
    global count_mines
    # For all Revealed Safe Squares
    for c in revealed_safe_squares:
        i = c[0]
        j = c[1]
        clue = countMines(i,j) 
        Hidden_neighbors = countHiddenNeighbors(i,j)
        Revealed_Mines = countRevealedMines(i,j)
        
        #All the Hidden Neighbors are Mines
        if Hidden_neighbors == clue - Revealed_Mines :    # Hidden Remaining Mines = total Neighboring Mines - Revealed Mines
            row_range = range(i-1,i+2)
            col_range = range(j-1,j+2)
            
            # Hence Mark them as Mine  
            for a in row_range :
                for b in col_range :
                    if (a == i and b == j):
                        continue
                    if [a,b] not in revealed_squares and 0<=a<=rows-1 and 0<=b<=cols-1:
                        revealed_squares.append([a,b])
                        if [a,b] not in revealed_mine_squares:
                            revealed_mine_squares.append([a,b])
                        correct_choice.append([a,b])              #Add it to the correctly marked list
                        board[a][b] = -1
                        print("mines found")
                        showBoard()
                        print(revealed_squares)                   #Print Revealed Squares soo far
                        count_mines = count_mines + 1
                        check_safe_Squares()
        
        #All Surrounding squares are Safe
        if ((neighbors_count(i,j)-clue) -  revealedSafeNeighbors(i,j)) == Hidden_neighbors :  # Hidden safe Neighbors = Total Safe Neighbors - Revealed Safe Neighbors        
            row_range = range(i-1,i+2)
            col_range = range(j-1,j+2)
            
            # Hence mark them as Safe Revealed Squares 
            for a in row_range :
                for b in col_range :
                    if (a == i and b == j):
                        continue
                    if [a,b] not in revealed_squares and 0<=a<=rows-1 and 0<=b<=cols-1:
                        revealed_squares.append([a,b])
                        if [a,b] not in revealed_safe_squares:
                            revealed_safe_squares.append([a,b])   #Add them to the safe Revealed Squares
                        board[a][b] = countMines(a,b)
                        print("safe squares found")
                        showBoard()
                        print(revealed_squares)                   #Print Revealed Squares soo far
                        check_safe_Squares()
    make_move()                               #if no Knowledge can be drawn by information available
    


# In[13]:


make_move()


# In[14]:


print('Mines Marked Correctly:', end = '')   #Print Number of Mines marked Correctly and its location
print(len(correct_choice))
print(correct_choice)
print('Mines Blasted:', end = '')            #Print Number of Mines Blasted and its location
print(len(wrong_choice))
print(wrong_choice)
print('Total Mines:', end = '')              #Total Mines
print(count_mines)
    


# In[ ]:




