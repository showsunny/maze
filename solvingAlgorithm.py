import pygame
import sys
import random
import time
import pickle
import copy
import networkx as nx
import matplotlib.pyplot as plt
import os
from datetime import datetime
import pandas as pd
import numpy as np




W = 30
ROWS = 24
COLS = 24
RED = (237,27,35)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 100, 0)
GRAY = (148,150,152)
CYAN = (0,174,239) 
DARK_RED = (100, 0, 0)
WHITE = (255, 255, 255)
GOLD = (190, 178, 124)
outlineThickness = 5
T = outlineThickness // 2
hW = W // 2
WIDTH, HEIGHT = W*COLS, W*ROWS
wallList = []
pygame.init()
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Maze Solver')

def load_data():    # read a maze from you file
    with open("./mazes/maze_artificial_24.dat", 'rb') as f:
        x = pickle.load(f)
    return x

def save_data(cells):    # save a maze as a .dat file
    with open("./mazes/maze_artificial_24.dat", 'wb') as f:
        pickle.dump(cells, f)




def returnCellIndex(row, col, cells):
    if row < 0 or col < 0 or row > ROWS-1 or col > COLS-1:
        return None
    else:
        return cells[row][col]
    
    
def returnCellIndex_LastPosition(row: int, col: int, lastPosition, cells):
    ### lastPosition是一个表示上一个cell的元组：(row, col)
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
    def __init__(self, row, col, lines, inPath, inMaze, highlited, arrows):
        self.row = row
        self.col = col
        self.lines = lines
        self.inPath = inPath
        self.inMaze = inMaze
        self.highlited = highlited
        self.arrows = arrows

    def draw(self):
        if self.inMaze:
            pygame.draw.rect(SCREEN, DARK_GREEN, pygame.Rect(self.col*W, self.row*W, W, W))

        if self.highlited:
            pygame.draw.rect(SCREEN, WHITE, pygame.Rect(self.col*W, self.row*W, W, W))

        if self.inPath:
            pygame.draw.rect(SCREEN, DARK_RED, pygame.Rect(self.col*W, self.row*W, W, W))

        if self.lines[0]:
            pygame.draw.line(SCREEN, GREEN, (self.col*W, self.row*W), (self.col*W+W+T, self.row*W), outlineThickness)
        if self.lines[1]:
            pygame.draw.line(SCREEN, GREEN, (self.col*W+W, self.row*W), (self.col*W+W, self.row*W+W+T), outlineThickness)
        if self.lines[2]:
            pygame.draw.line(SCREEN, GREEN, (self.col*W, self.row*W+W), (self.col*W+W+T, self.row*W+W), outlineThickness)
        if self.lines[3]:
            pygame.draw.line(SCREEN, GREEN, (self.col*W, self.row*W), (self.col*W, self.row*W+W+T), outlineThickness)

        if self.arrows[0]:  # 上
            pygame.draw.line(SCREEN, DARK_RED, (self.col*W+hW, self.row*W+hW), (self.col*W+hW, self.row*W), outlineThickness)

        if self.arrows[1]:  # 右
            pygame.draw.line(SCREEN, DARK_RED, (self.col*W+hW, self.row*W+hW), (self.col*W+hW+hW, self.row*W+hW), outlineThickness)

        if self.arrows[2]:  # 下
            pygame.draw.line(SCREEN, DARK_RED, (self.col*W+hW, self.row*W+hW), (self.col*W+hW, self.row*W+hW+hW), outlineThickness)

        if self.arrows[3]:  # 左
            pygame.draw.line(SCREEN, DARK_RED, (self.col*W+hW, self.row*W+hW), (self.col*W, self.row*W+hW), outlineThickness)
    
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

    def checkNextCells(self, lastPosition, cells):
        nearCells = []
        topCell = returnCellIndex(self.row-1, self.col, lastPosition)
        rightCell = returnCellIndex(self.row, self.col+1, lastPosition)
        bottomCell = returnCellIndex(self.row+1, self.col, lastPosition)
        leftCell = returnCellIndex(self.row, self.col-1, lastPosition)

        if topCell and not self.lines[0]:
            nearCells.append(topCell)

        if rightCell and not self.lines[1]:
            nearCells.append(rightCell)

        if bottomCell and not self.lines[2]:
            nearCells.append(bottomCell)
            
        if leftCell and not self.lines[3]:
            nearCells.append(leftCell)

        if len(nearCells) != 0:
            if len(nearCells) > 1:
                return random.choice(nearCells)
            else:
                return nearCells[0]
        else:
            return cells[lastPosition[0][lastPosition[1]]]
        
    def checkNextCell_DeadEnd(self, arr):
        nearCells = []

        topCell = returnCellIndex_DeadEndFillings(self.row-1, self.col, arr)
        rightCell = returnCellIndex_DeadEndFillings(self.row, self.col+1, arr)
        bottomCell = returnCellIndex_DeadEndFillings(self.row+1, self.col, arr)
        leftCell = returnCellIndex_DeadEndFillings(self.row, self.col-1, arr)


def updateCanvas(cells):
    SCREEN.fill(BLACK)
    for i in range(ROWS):
        for j in range(COLS):
            cells[i][j].draw()
    #if show:
    pygame.display.update()
    pygame.time.delay(50)

def addZeros(number, desired_length):
    number_str = str(number)
    zeros_to_add = max(0, desired_length - len(number_str))

    if number_str.startswith('-'):
        return '-' + '0' * zeros_to_add + number_str[1:]
    else:
        return  '0' * zeros_to_add + number_str


def checkWalls(direction, current):
    """
    检查当前方向的墙壁情况。
    返回一个元组 (forward, right)：
    - forward: 当前方向前方是否有墙壁。
    - right: 右转方向是否有墙壁。
    """
    # direction的顺序是[上, 右, 下, 左]
    forward = current.lines[direction.index(1)]  # 当前方向的前方
    right = current.lines[(direction.index(1) + 1) % 4]  # 当前方向的右转

    return forward, right

def moveForward(current, direction, cells):
    """
    根据当前的方向移动到下一个单元格。
    """
    row, col = current.row, current.col

    # 根据方向向上、右、下、左移动
    if direction[0] == 1:  # 向上
        next_cell = returnCellIndex(row - 1, col, cells)
    elif direction[1] == 1:  # 向右
        next_cell = returnCellIndex(row, col + 1, cells)
    elif direction[2] == 1:  # 向下
        next_cell = returnCellIndex(row + 1, col, cells)
    elif direction[3] == 1:  # 向左
        next_cell = returnCellIndex(row, col - 1, cells)

    return next_cell

def wallFollower(startCell, endCell, cells, show=True, saveVideo=False, saveData=False):
    """
        right hand side wall follower
    """
    done = False
    path = []
    visited = set()  # 使用集合记录访问过的单元格
    direction = [0, 0, 0, 1]  # 初始方向向左
    current = startCell
    current.highlited = True
    
    lastPosition = [current.row, current.col]

    current.inMaze = True  # 初始位置在迷宫中

    current_date_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    k = 0

    while not done:
        # 更新迷宫显示
        if show:
            updateCanvas(cells)

        # 检查当前方向是否能移动
        nextWalls = checkWalls(direction, current)

        if not nextWalls[1]:  # 右边无墙
            # 右转
            direction = direction[-1:] + direction[:-1]  # 右转
            next = moveForward(current, direction, cells)
            current.highlited = False
            current.inMaze = True  # 标记为已探索
            next.highlited = True
            current = next

            path.append(current)
        elif not nextWalls[0]:  # 前方无墙
            # 继续前进
            next = moveForward(current, direction, cells)
            current.highlited = False
            current.inMaze = True  # 标记为已探索
            next.highlited = True
            current = next
            path.append(current)
        else:
            # 左转
            direction = direction[1:] + direction[:1]  # 左转

        # 判断是否到达终点
        if current == endCell:
            done = True
            break

        if saveVideo:
            directory = f"./video.wallFollowers/{current_date_time}"
            if not os.path.exists(directory):
                os.makedirs(directory)
                pygame.image.save(SCREEN, f"{directory}/{addZeros({k, 8})}.png")
                k += 1
            else:
                pygame.image.save(SCREEN, f"{directory}/{addZeros({k, 8})}.png")
                k += 1

    # 从终点回溯标记路径
    traceBackPath(path, cells, show)



def traceBackPath(path, cells, show):
    for i in range(len(path) - 1):
        current = path[i]
        next_cell = path[i + 1]

        # 根据相对位置标记箭头方向
        if next_cell.row < current.row:  # Next cell is above
            cells[current.row][current.col].arrows[0] = True
        elif next_cell.row > current.row:  # Next cell is below
            cells[current.row][current.col].arrows[2] = True
        elif next_cell.col < current.col:  # Next cell is to the left
            cells[current.row][current.col].arrows[3] = True
        elif next_cell.col > current.col:  # Next cell is to the right
            cells[current.row][current.col].arrows[1] = True

        cells[current.row][current.col].inPath = True

    # 标记终点
    cells[path[-1].row][path[-1].col].inPath = True




def dijkstra(startCell, endCell, cells, show=True, saveVideo=False, saveData=False):


    G = nx.Graph()
    nodes = []
    for i in range(ROWS):
        for j in range(COLS):
            nodes.append((i, j))

    for i in range(ROWS):
        for j in range(COLS):
            # Check top neighbor (i-1, j)
            if cells[i][j].lines[0] == False and returnCellIndex(i-1, j, cells) is not None:  
                G.add_edge((i, j), (i-1, j), weight=1)
        
            # Check right neighbor (i, j+1)
            if cells[i][j].lines[1] == False and returnCellIndex(i, j+1, cells) is not None:  
                G.add_edge((i, j), (i, j+1), weight=1)
        
            # Check bottom neighbor (i+1, j)
            if cells[i][j].lines[2] == False and returnCellIndex(i+1, j, cells) is not None:  
                G.add_edge((i, j), (i+1, j), weight=1)
        
            # Check left neighbor (i, j-1)
            if cells[i][j].lines[3] == False and returnCellIndex(i, j-1, cells) is not None:  
                G.add_edge((i, j), (i, j-1), weight=1)

    start = (startCell.row, startCell.col)
    end = (endCell.row, endCell.col)

    explored_cells = []
    def explore_cell(node):
        cells[node[0]][node[1]].inMaze = True

    distances = {node: float('inf') for node in G.nodes}
    distances[start] = 0

    previous = {node: None for node in G.nodes}

    unvisited_nodes = list(G.nodes)

    data = []
    bestPosition = [startCell.row, startCell.col]

    current_date_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    k = 0
    print("started Algorithm",current_date_time)
    while unvisited_nodes:
        unvisited_nodes.sort(key=lambda node: distances[node])

        current_node = unvisited_nodes.pop(0)
        #print(current_node)

        if current_node == end:
            cells[end[0]][end[1]].inMaze = True
            break

        for neighbor in G.neighbors(current_node):
            tentative_distance = distances[current_node] + G[current_node][neighbor]['weight']

            if tentative_distance < distances[neighbor]:
                distances[neighbor] = tentative_distance
                previous[neighbor] = current_node
        explore_cell(current_node)
        if save_data:
            if k % 2 == 0:
                if (current_node[0]+current_node[1]) > bestPosition[0]+bestPosition[1]:
                    bestPosition = [current_node[0], current_node[1]]

                data.append([k, bestPosition[0], bestPosition[1], bestPosition[0]+bestPosition[1]])
        if show:
                updateCanvas(cells)

                if saveVideo:
                    directory = f"./video.deadEndFillings/{current_date_time}"

                    if not os.path.exists(directory):
                        os.makedirs(directory)
                        pygame.image.save(SCREEN, f"{directory}/{addZeros({k, 8})}.png")
                        k += 1
                    else:
                        pygame.image.save(SCREEN, f"{directory}/{addZeros({k, 8})}.png")
                        k += 1
    complete_date_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    print("done",complete_date_time)
    path = []
    current = end
    while previous[current]:
        path.insert(0, current)
        current = previous[current]

    # Add the start cell to the path
    path.insert(0, start)
    if end not in path:
        path.append(end)
    # Highlight the path using arrows
    for i in range(len(path) - 1):
        current = path[i]
        next_cell = path[i + 1]
        
        if next_cell[0] < current[0]:  # Next cell is above
            cells[current[0]][current[1]].arrows[0] = True  # Arrow pointing up
        elif next_cell[0] > current[0]:  # Next cell is below
            cells[current[0]][current[1]].arrows[2] = True  # Arrow pointing down
        elif next_cell[1] < current[1]:  # Next cell is to the left
            cells[current[0]][current[1]].arrows[3] = True  # Arrow pointing left
        elif next_cell[1] > current[1]:  # Next cell is to the right
            cells[current[0]][current[1]].arrows[1] = True  # Arrow pointing right

        # Highlight the current cell as part of the path
        cells[current[0]][current[1]].inPath = True
        # Optionally update the canvas after each arrow is placed
        if show:
            updateCanvas(cells)
    cells[end[0]][end[1]].inPath = True
    if show:
        updateCanvas(cells)

    # Optionally save data for the path
    if saveData:
        with open(f"./data/dijkstra_{current_date_time}.dat", 'wb') as f:
            pickle.dump(data, f)

def main():
    cells = load_data()
    running = True
    startCell = cells[23][23]
    endCell = cells[0][23]
    startCell.visited = True



    running = True
    while running:
        if endCell.inPath != True:
            dijkstra(startCell, endCell,cells, show=True)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               running = False
            else:
                pygame.display.flip()

if __name__ == '__main__':
    main()
