# maze
python implementation of maze generation and solving algorithms

python代码实现迷宫生成与寻路算法(本项目的代码只能生成Perfect Maze：任意两点之间有且只有一条通路即不存在环路和隔离)

### 推荐环境：

`python==3.10.12`
`pygame==2.6.0`
`networkx==3.3`
`numpy==1.26.4`
`pandas==2.1.4`
`matplotlib==3.7.1`
## 目前只实现了3个生成算法和2个寻路算法
## 生成算法

每个生成算法单独写在一个python文件中直接运行即可(不能使用虚拟环境如jupyternotebook等因为用到了pygame的GUI)，生成算法的代码中的W = 30表示每个单元的边长，ROWS = 24，COLS = 24表示生成迷宫的行数和列数，可根据自己的需求修改，updateCanvas()中的pygame.time.delay(50)这里的50表示生成动画的延迟为50ms,由于Wilson算法寻路的随机回头现象导致前期寻路时间过于漫长所以设置为5ms
### 递归回溯器(recursiveBacktracker):
1. 选择现场的起点。
2. 随机选择该点处的一堵墙，并开辟一条通往相邻单元格的通道，但前提是相邻单元格尚未被访问过。这将成为新的当前单元格。
3. 如果所有相邻的单元格都已被访问，则返回到最后一个具有未雕刻墙壁的单元格并重复。
4. 当过程一直回到起点时，算法结束。
### prime算法:
从初始单元格开始（在本例中为左上角单元格 cells[0][0]）。
将初始单元格标记为已访问。
将初始单元格的所有墙壁添加到列表中。
    从列表中随机选择一面墙壁。
    如果墙壁另一侧的单元格尚未被访问：
        移除墙壁。
        将另一侧的单元格标记为已访问。
        将单元格的相邻墙壁添加到列表中。
    从列表中移除墙壁。

### wilson算法:
1. 随机选择任意顶点并将其添加到visited列表。
2. 选择任何尚未在visited中的顶点并执行随机游走，直到遇到位于visited中的顶点。
3. 移除相邻顶点之间的墙壁，将随机游走中接触到的顶点和边添加到visited。
4. 重复 2 和 3，直到所有顶点都添加到visited中。



### 求解算法
所有算法都在solvingAlgorithm.py，暂时只实现了Dijkstra和wallFollower，运行solvingAlgorithm.py即可生成寻路动画
