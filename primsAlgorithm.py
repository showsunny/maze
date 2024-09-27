import pygame
import sys
import random
import time


W = 30
ROWS = 24
COLS = 24

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 64, 0)
GRAY = (148,150,152)
CYAN = (0,174,239) 
WHITE = (255, 255, 255)
outlineThickness = 5
T = outlineThickness // 2
WIDTH, HEIGHT = W*COLS+T, W*ROWS+T
cells = []
wallList = []
pygame.init()
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))



def returnCellIndex(row, col):
    if row < 0 or col < 0 or row > ROWS-1 or col > COLS-1:
        return False
    else:
        return cells[row][col]
    
    
def returnCellIndex_LastPosition(row, col, lastPosition):
    if row < 0 or col < 0 or row > ROWS-1 or col > COLS-1:
        return False
    elif row == lastPosition[0] and col == lastPosition[1]:
        return False
    else:
        return cells[row][col]
    
    
def returnCellIndex_DeadEndFillings(row, col, arr):
    if row < 0 or col < 0 or row > ROWS-1 or col > COLS-1:
        return False
    else:
        return arr[row][col]


class Cell:
    def __init__(self, row, col, lines, visited, highlited):
        self.row = row
        self.col = col
        self.lines = lines
        self.visited = visited
        self.highlited = highlited
    def draw(self):
        #rect = pygame.Rect(100, 100, 200, 150)
        if self.visited:
            pygame.draw.rect(SCREEN, DARK_GREEN, pygame.Rect(self.row*W, self.col*W, W, W))
        if self.highlited:
            pygame.draw.rect(SCREEN, WHITE, pygame.Rect(self.row*W, self.col*W, W, W))
        if self.lines[0]:
            pygame.draw.line(SCREEN, GREEN, (self.col*W, self.row*W), (self.col*W+W+T, self.row*W), outlineThickness)
        if self.lines[1]:
            pygame.draw.line(SCREEN, GREEN, (self.col*W+W, self.row*W), (self.col*W+W, self.row*W+W+T), outlineThickness)
        if self.lines[2]:
            pygame.draw.line(SCREEN, GREEN, (self.col*W, self.row*W+W), (self.col*W+W+T, self.row*W+W), outlineThickness)
        if self.lines[3]:
            pygame.draw.line(SCREEN, GREEN, (self.col*W, self.row*W), (self.col*W, self.row*W+W+T), outlineThickness)
def updateCanvas():
    SCREEN.fill(BLACK)
    for i in range(ROWS):
        for j in range(COLS):
            cells[i][j].draw()
    pygame.display.update()
    pygame.time.delay(50)  # Adjust delay for animation speed    
def removeWalls(currentCell, nextCell):
    dx = currentCell.col - nextCell.col

    if dx == 1:
        currentCell.lines[3] = False
        nextCell.lines[1] = False
    elif dx == -1:
        currentCell.lines[1] = False
        nextCell.lines[3] = False

    dy = currentCell.row - nextCell.row
    
    if dy == 1:
        currentCell.lines[0] = False
        nextCell.lines[2] = False
    elif dy == -1:
        currentCell.lines[2] = False
        nextCell.lines[0] = False

def setUp():
    for i in range(ROWS):
        cells.append([])
        for j in range(COLS):
            cells[i].append(Cell(i,j, [True, True, True, True], False, False))
def main():
    
    setUp()

    firstCell = cells[0][0]
    firstCell.visited = True

    wallList.append([firstCell, 0])
    wallList.append([firstCell, 1])
    wallList.append([firstCell, 2])
    wallList.append([firstCell, 3])


    running = True
    while running:

        while len(wallList) > 0:
            randomWall = random.choice(wallList)

            if randomWall[1] == 1 and returnCellIndex(randomWall[0].row,randomWall[0].col+1):
                rowIndex = randomWall[0].row
                colIndex = randomWall[0].col
                dividingCell = cells[rowIndex] [colIndex+1]

                if randomWall[0].visited ^ dividingCell.visited:
                    removeWalls(randomWall[0], dividingCell)

                    if not(randomWall[0].visited):
                        randomWall[0].visited = True
                        print("There's somethings you're missing")
                    if not(dividingCell.visited):
                        dividingCell.visited = True
                        wallList.append([dividingCell, 0])
                        wallList.append([dividingCell, 1])
                        wallList.append([dividingCell, 2])

            if randomWall[1] == 2 and returnCellIndex(randomWall[0].row+1, randomWall[0].col):
                rowIndex = randomWall[0].row
                colIndex = randomWall[0].col
                dividingCell = cells[rowIndex+1][colIndex]

                if randomWall[0].visited ^ dividingCell.visited:
                    removeWalls(randomWall[0], dividingCell)

                    if not(randomWall[0].visited):
                        randomWall[0].visited = True
                        print("There's somethings you're missing")
                    if not(dividingCell.visited):
                        dividingCell.visited = True
                        wallList.append([dividingCell, 1])
                        wallList.append([dividingCell, 2])
                        wallList.append([dividingCell, 3])

            if randomWall[1] == 3 and returnCellIndex(randomWall[0].row, randomWall[0].col-1):
                rowIndex = randomWall[0].row
                colIndex = randomWall[0].col
                dividingCell = cells[rowIndex][colIndex-1]

                if randomWall[0].visited ^ dividingCell.visited:
                    removeWalls(randomWall[0], dividingCell)

                    if not(randomWall[0].visited):
                        randomWall[0].visited = True
                        print ("There's somethings you're missing")
                    if not(dividingCell.visited):
                        dividingCell.visited = True
                        wallList.append([dividingCell, 0])
                        wallList.append([dividingCell, 2])
                        wallList.append([dividingCell, 3])

            wallList.remove(randomWall)
            
            updateCanvas()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                pygame.display.flip()


if __name__ == '__main__':
    main()
