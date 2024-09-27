import pygame
import sys
import random
import time
#from models.utils import removeWalls

W = 30
ROWS = 24
COLS = 24
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 100, 0)
LIGHT_RED=(255, 170, 170)
GRAY = (148,150,152)
CYAN = (0,174,239)
RED = (237,27,35)
outlineThickness = 5
T = outlineThickness // 2
WIDTH, HEIGHT = W*COLS + T, W*ROWS + T
cells = []

pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))


def returnCellIndex(row, col):
    if row < 0 or col < 0 or row > ROWS - 1 or col > COLS - 1:
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
    
def returnCellIndex_DeadEndFillings(row, col, arr):
    if row < 0 or col < 0 or row > ROWS-1 or col > COLS-1:
        return False
    else:
        return arr[row][col]

class Cell:
    def __init__(self, row, col, lines, visited, highlited, inPath, inMaze):
        self.row = row
        self.col = col
        self.lines = lines
        self.visited = visited
        self.highlited = highlited
        self.inPath = inPath
        self.inMaze = inMaze


    def draw(self):
        if self.visited:
            pygame.draw.rect(SCREEN, DARK_GREEN, pygame.Rect(self.col*W, self.row*W, W, W))
        if self.highlited:
            pygame.draw.rect(SCREEN, WHITE, pygame.Rect(self.col*W, self.row*W, W, W))
        if self.inPath:
            pygame.draw.rect(SCREEN, GREEN, pygame.Rect(self.col*W, self.row*W, W, W))
        if self.lines[0]:
            #top
            pygame.draw.line(SCREEN, GREEN, (self.col*W, self.row*W), (self.col*W+W+T, self.row*W), outlineThickness)
        if self.lines[1]:
            #right
            pygame.draw.line(SCREEN, GREEN, (self.col*W+W, self.row*W), (self.col*W+W, self.row*W+W+T), outlineThickness)
        if self.lines[2]:
            #botttom
            pygame.draw.line(SCREEN, GREEN, (self.col*W, self.row*W+W), (self.col*W+W+T, self.row*W+W), outlineThickness)
        if self.lines[3]:
            #left
            pygame.draw.line(SCREEN, GREEN, (self.col*W, self.row*W), (self.col*W, self.row*W+W+T), outlineThickness)
        
    def checkNearCells(self, lastPosition):
        nearCells = []

        topCell = returnCellIndex_LastPosition(self.row-1, self.col, lastPosition)
        rightCell = returnCellIndex_LastPosition(self.row, self.col+1, lastPosition)
        bottomCell = returnCellIndex_LastPosition(self.row+1, self.col, lastPosition)
        leftCell = returnCellIndex_LastPosition(self.row, self.col-1, lastPosition)

        if self.row > 0:  # 顶部单元格
            if topCell!=False:
                nearCells.append(topCell)

        if self.col < ROWS-1:  # 右侧单元格
            if rightCell !=False:
                nearCells.append(rightCell)

        if self.row < COLS-1:  # 底部单元格
            if bottomCell !=False:
                nearCells.append(bottomCell)
    
        if self.col > 0:  # 左侧单元格
            if leftCell !=False:
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
    pygame.time.delay(5)  # Adjust delay for animation speed

def eraseWrongPath(path, collision_point):
    """擦除环路部分路径，从碰撞点开始删除"""
    # 找到重合点的位置
    collision_index = path.index(collision_point)
    
    # 从路径中删除重合点之后的所有单元格
    path_to_keep = path[:collision_index + 1]  # 保留到重合点的路径
    
    # 清除重合点之后的路径
    for cell in path[collision_index + 1:]:
        cell.inPath = False
        cell.highlited = False
    
    return path_to_keep  # 返回更新后的路径


def setUp():
    for i in range(ROWS):
        cells.append([])
        for j in range(COLS):
            cell = Cell(i, j, [True, True, True, True], False, False, False, False)
            cells[i].append(cell)



def checkDeadEnd(current):
    topCell = returnCellIndex(current.row - 1, current.col)
    rightCell = returnCellIndex(current.row, current.col + 1)
    bottomCell = returnCellIndex(current.row + 1, current.col)
    leftCell = returnCellIndex(current.row, current.col - 1)

    neighbors = [topCell, rightCell, bottomCell, leftCell]
    
    # 找到所有合法的邻居（未访问过的单元格）
    valid_neighbors = [cell for cell in neighbors if cell and not cell.inPath]

    # 如果没有未访问过的邻居，且四周都在路径中，则为死路
    if not valid_neighbors and all(cell and cell.inPath for cell in neighbors):
        return True
    return False

def randomWalk(startCell):
    current = startCell
    current.highlited = True

    path = [current]
    while not current.visited:
        walking = True
        while walking:
            
            walking = False

            

            # 检查附近的单元格并随机选择一个
            next = current.checkNearCells([current.row, current.col])
            if next:
                # 检查下一个单元格是否已经在路径中
                if next.inPath:
                    # 如果下一个单元格已经在路径中，触发擦除环路逻辑
                    path = eraseWrongPath(path, next)
                    current = path[-1]
                    current.highlited = True
                else:
                    # 否则继续前进
                    path.append(next)
                    current.highlited = False
                    current.inPath = True
                    current = next
                    current.highlited = True
                    updateCanvas()

                if next.inMaze:
                    walking = False
                    for i, cell in enumerate(path[:-1]):
                        nextCell = path[i + 1]
                        nextCell.visited = True
                        nextCell.inMaze = True
                        nextCell.highlited = False
                        nextCell.inPath = False
                        cell.visited = True
                        cell.inPath =False
                        cell.inMaze=True
                        cell.highlited = False
                        removeWalls(cell, nextCell)
                        updateCanvas()
                else:
                    walking = True
            else:
                # 如果没有下一个单元格，停止当前路径的生成
                walking = False
        




            
def setUp():
    for i in range(ROWS):
        cells.append([])
        for j in range(COLS):
            cell = Cell(i, j, [True, True, True, True], False, False, False, False)
            cells[i].append(cell)



def main():
    setUp()
    IN = cells[random.randint(0, COLS - 1)][random.randint(0, ROWS - 1)]
    IN.inMaze=True
    IN.visited = True


    running = True
    while running:
    
        not_in_maze_cells = [cell for row in cells for cell in row if not cell.inMaze]

        if not_in_maze_cells:
            startCell = random.choice(not_in_maze_cells)
        randomWalk(startCell)
        updateCanvas()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

if __name__ == '__main__':
    main()
