import pickle
import pygame
import sys
import random
import time


W = 30
ROWS = 24
COLS = 24
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 100, 13)
LIGHT_RED=(255, 170, 170)
GRAY = (148,150,152)
CYAN = (0,174,239)
RED = (237,27,35)
outlineThickness = 5
T = outlineThickness // 2
WIDTH, HEIGHT = W*COLS, W*ROWS
cells = []
pygame.init()
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))


def load_data():    # read a maze from you file
    with open("./mazes/xxxx.dat", 'rb') as f:
        x = pickle.load(f)
    return x

def save_data():    # save a maze as a .dat file
    with open("./mazes/xxxx.dat", 'wb') as f:
        pickle.dump(cells, f)


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
    def __init__(self, row: int, col: int, lines: list, visited: bool, highlited: bool):
        self.row = row
        self.col = col
        self.lines = lines
        self.visited = visited
        self.highlited = highlited

    def draw(self):
        if self.visited:
            pygame.draw.rect(SCREEN, DARK_GREEN, pygame.Rect(self.col*W, self.row*W, W, W))
        if self.highlited:
            pygame.draw.rect(SCREEN, WHITE, pygame.Rect(self.col*W, self.row*W, W, W))
        if self.lines[0]:
            pygame.draw.line(SCREEN, GREEN, (self.col * W, self.row * W), (self.col * W, self.row * W + W + T), outlineThickness)
        if self.lines[1]:
            pygame.draw.line(SCREEN, GREEN, (self.col * W, self.row * W + W), (self.col * W + W + T, self.row * W + W), outlineThickness)
        if self.lines[2]:
            pygame.draw.line(SCREEN, GREEN, (self.col * W + W, self.row * W), (self.col * W + W, self.row * W + W + T), outlineThickness)
        if self.lines[3]:
            pygame.draw.line(SCREEN, GREEN, (self.col * W, self.row * W), (self.col * W + W + T, self.row * W), outlineThickness)
        
    def checkNearCells(self, lastPosition):
        nearCells = []

        topCell = returnCellIndex_LastPosition(self.row-1, self.col, lastPosition)
        rightCell = returnCellIndex_LastPosition(self.row, self.col+1, lastPosition)
        bottomCell = returnCellIndex_LastPosition(self.row+1, self.col, lastPosition)
        leftCell = returnCellIndex_LastPosition(self.row, self.col-1, lastPosition)

        if self.row > 0:  # 顶部单元格
            if topCell!=False and not topCell.visited:
                nearCells.append(topCell)

        if self.col < ROWS-1:  # 右侧单元格
            if rightCell !=False and not rightCell.visited:
                nearCells.append(rightCell)

        if self.row < COLS-1:  # 底部单元格
            if bottomCell !=False and not bottomCell.visited:
                nearCells.append(bottomCell)
    
        if self.col > 0:  # 左侧单元格
            if leftCell !=False and not leftCell.visited:
                nearCells.append(leftCell)

        if len(nearCells) != 0:
            # 周围有多个未访问过的单元格则随机选择一个
            if len(nearCells) > 1:
                return random.choice(nearCells)
            else:
                return nearCells[0]
        else:
            # 周围没有未访问过的单元格
            return None
def updateCanvas():
    SCREEN.fill(BLACK)
    for i in range(ROWS):
        for j in range(COLS):
            cells[i][j].draw()
    pygame.display.update()
    pygame.time.delay(50)  # Adjust delay for animation speed
def removeWalls(currentCell, nextCell):
    dy = currentCell.row - nextCell.row
    dx = currentCell.col - nextCell.col
    if dx == 1:
        currentCell.lines[3] = False
        nextCell.lines[1] = False
    elif dx == -1:
        currentCell.lines[1] = False
        nextCell.lines[3] = False

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
    saveModel = False

    stack = []
    current = cells[random.randint(0, ROWS - 1)][random.randint(0, COLS - 1)]
    current.visited = True
    current.highlited = True


    running = True
    while running:
        
        next = current.checkNearCells((current.row, current.col)) # 检查未访问的相邻单元格
        if  next:
            next.visited = True             # 将下一个单元格标记为已访问
            next.highlited = True
            stack.append(current)
            
            removeWalls(current, next)
            current.highlited=False
            current  = next

        elif len(stack) > 0:
            current.highlited = False
            current = stack.pop(len(stack)-1)  # next为空相邻单元格都被访问过则回溯
            current.highlited = True
        else:
            updateCanvas()
            if saveModel == True:
                print("Maze is Finished")
                #save_data()
                saveModel = False
            #pygame.image.save(SCREEN, "./images/maze1.png")
        updateCanvas()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               running = False
            else:
                pygame.display.flip()

if __name__ == '__main__':
    main()


