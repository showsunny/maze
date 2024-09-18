# maze
python implementation of maze generation and solving algorithms

python代码实现迷宫生成与寻路算法(本项目的代码只能生成Perfect Maze：任意两点之间有且只有一条通路即不存在环路和隔离限制)

### 推荐环境：

`python==3.10.12`
`pygame==2.6.0`
`networkx==3.3`
## 目前只实现了3个生成算法和一个寻路算法
### 生成算法

每个生成算法直接运行即可(必须是python环境，不能使用虚拟环境如jupyternotebook等因为用到了pygame的GUI)，生成算法的代码中的W = 30表示每个单元的边长，ROWS = 24，COLS = 24表示生成迷宫的行数和列数，可根据自己的需求修改 

updateCanvas()中的pygame.time.delay(50)这里的50表示生成动画的延迟为50ms,由于Wilson算法寻路的随机回头现象导致前期寻路时间过于漫长所以设置为5ms

### 求解算法
所有算法都在solvingAlgorithm.py，暂时只实现了Dijkstra算法，运行solvingAlgorithm.py即可生成寻路动画
