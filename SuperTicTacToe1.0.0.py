import sys
import math
import random
import copy
import time
import os
import pygame
from pygame.sprite import Sprite, Group
import base64

# 设置用来检测输赢的数组（常量）
DETECT_WINNER = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6]
]

# 翻选项号
NEXT = "iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsIAAA7CARUoSoAAAAEUSURBVGhD7dqxDcJAEERRQ0IVtIFonB4QhdADEehLRiRY2Hc7s4vln2A58tPdbsTucj8+hxW0H3//vg1SrdVAuob9fDqMT5+ut8f45K35RL4haOq9OsnVysDIZsSNkQ67EyPfWi5MM2TJdnJguk6kEqb7alXBhMxIBUzYsGdjwiCUiQmFUBYmHEIZGAmE3BgZhJwYKYRcGDmEHBgLhJZgWrJBaC6m5VSskLkf2HJ6NkjvVvqVBbIE0TpLcogDQVKIC0EyiBNBEogbQeGQDASFQrIQFAbJRFAIJBtB3ZAKCAof9qmUCLJA1AiSQxwIkkJcCOqGTH2sE0Gh/3xgg7kB70KvVhaCLFvL0Qap1gap1kogw/AC46FuEmBSaNAAAAAASUVORK5CYII="
LAST = "iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsIAAA7CARUoSoAAAAAhdEVYdENyZWF0aW9uIFRpbWUAMjAyMDowMzoyNiAxNDoyNTozMj1/Ov0AAAEISURBVGhD7doxDsIwEERRQ8MpuAbi4twBcRDuQAUayRXCUmzPzg6Rf5OUedp10uRwe57fZQcd6/XvWxC3FsStBZntejnVO07y78gvwP3xqnfjSSfSmgJjOjIIe5W+k0CiESgcokCgUIgKgcIgPQjbt5YageiQDASiQrIQiAbJRCAKJBuBpiEOCDQFcUGgYYgTAg1B3BCIcthbqRCoG7J1GkoE6oZsfcCe9WMUulpKzBCkZ21UmOGJuGGmVssJM31GXDCUw+6AoUBQNoYGQZkYKgRlYegQlIEJgSA1JgyClJhQCFJhwiGoBzOaBIKiMTIIisRIISgKI4egFmYGuX6qcWtB3NoJpJQPqG9o/J3iEK8AAAAASUVORK5CYII="

# 圈、叉图像
CIRCLE = 'iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAIAAAADnC86AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAFFSURBVFhH1c9RjsIwDAVA7n9ptrLHuyltSmgioZ0fi2f3RTyeX/IfHn4McDpg6FTrMJ9denOk6RYVHVdrBRMUnenufLpn1+HowHqvkx5YDPDBnl3jLNqTfsjHRdp4jRwW6S0qirTsfjsp0gmKijR0HxZNUxdE4e+HZZFOU1ekvYdFiygNot+HxSXDVZQWodHIZC3VQWI0MllLdZAYjUzWUh0kRiOTtVQHidHIZC3VQWI0MllLdZAYjUzWUh0kRiOTtVQHidHIZC3VQWI0MllLdZAYexmuorQIc2zEQbSI0iDqPbyRTlNXpO3DG8sgmqYuiEL34Y10gqIiDa/tTor0FhVFWk6qHRbph3xcpI33Dye7AT7Ys2ucNzo/sO5wdGC9d9XluwmKztz8EyNUdLxZJ03DfHZp6ChpveR0wAena33p4efzBz3L5NKgUjWiAAAAAElFTkSuQmCC'
CIRCLE_DARK = 'iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAIAAAADnC86AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAEFSURBVFhH7ZdBDoMwDARp35Xn8y8ayVEIjr3ZCJNemEs5YI/XpEh8juPY/sG3/C5nIvG+7+XKJ6VUrkZQYkbZwugH4lllC9ajZ3zHmsHlbmKzDIfwTGaVLe5b8KeGnNgQq0pe2TJsop9xiDWjCvs1XMRRVgG73VN90yqAJqe430Y4rcJOHBJX8FoV8YK4QhUZiQPjCmZD93A9zStexitexivOhL8+zYZFHP6a9Kgie9WBob1Wp3hB6FbhHq6Q0KDJRaxC33SrctVcJ45yY2vGXXUlt5jSk/ezXxJCP3jLVBX6WmQGx4BB0apxviG4HCWuzEZnJqbEAqPnlzQhjmX8d3qEbfsBHLSTUditGVYAAAAASUVORK5CYII='
CROSS = 'iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAIAAAADnC86AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAFHSURBVFhH1c7RcoMwDATA/P9Ppx68tFDORiRMM90XT6TTkcfzQz794cdeH95F6crQc9Dn71O3Ye5J+uodivasPAN9+xoVB7aesR64ynEi0J/GOJEoc5ZIbD/cWCYSBQ4SicXvRpFEYko0kViFOsFEYkAokdjIXeKJxIF1IrF3T5FFInEwXDROE4mFUSKRzHaNgqQYGDlZN2oucjx2nmiUlTmbKoUalQUOzlRzjeIp0YIL0Ub9gFDNf/iw+inRgmpUcYGDM6WcyjJnU+chZRc5HjtJqEmKgZHZWkEisTBKJJLhzmkisWGRSBzkhaNE4sA6kdi75+93QonExu+RYCIxJZpIrHa/RRKJAgeJxOLnh2UiUeYskfj+sHHSA1c5TgQ8A337GhUHtp6kr96haM/Kc9Dn71O3Ye7Z68O7KF0Z9ufvfejDz+cXTJEMnYcgfi0AAAAASUVORK5CYII='
CROSS_DARK = 'iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAIAAAADnC86AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAEeSURBVFhH5dhRDoIwEIRh9Fwcn3vhJNuIwHZ2dtvog/+LmtD9LDQx8bHv+/KLnu3167Udb9tmn611Xdu7GbnD/R1fLh2pN6p7q6fYZAh7xoM2Xx4crrIdLmwwOU0Fmyx5Q8eOZ9mKik63etwWVXR9xiO2riLncNXslIocGGXtrIp8GOl2QUVdGCl2TUXxzyIZTeIqYju2whH3lCUxjFK2eLEEI3Gc/hVVGIVDUzcmAc8tAYfHO3X+VVgcqtsSnNqKeHEMp1RLWRLAZATOMDnGoc1grl7e3ON2F1ZUq2b7sK5aBduBs6qVta9wTbVS9gkeUS3dPuBx1RLtBs9SLcV2DtdnBdUKFzK4rFp8eRceVC0yxIenqFZv1L/967MsL385q0ElMbTUAAAAAElFTkSuQmCC'
CIRCLE_NOW = 'iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsIAAA7CARUoSoAAAAEfSURBVFhH7ZgxEsMgDASdPCF9yvz/QSnT5wtJmDEejJF0koJMwTZ242M5wJ7x5fNjGZjreh0Wc4Pv+2O9w7i9nuudDrWgVqxGKwoLesVqUFFoD/5bLoFmig1yQWgLkgyXwwpSwdYNb5ksKdgKs4rVaLKbe7CnXKKVRbV7EOwtl0ElxVPcQy6DZO8EqZojqR3YBnu2l5HG2ARHaC9TupANRrSX4cYSD8nZTEEvU9DLFPQyBb2QgpGfPm6sTTDy0yZRurBLHNGiNMZOcIQWawfxkPRsEck+CLZa7CHZymyN3WywtyQqlxCXuCQFe0Qtz5v+LGSoWdd4cqC/W57WOJAJQkuMNqUBzYQaLPG2qZ2sWjCjFbWuglkwCtVrJp5l+QLPVJrVg/gzCAAAAABJRU5ErkJggg=='
CROSS_NOW = 'iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsIAAA7CARUoSoAAAAE2SURBVFhH7dgxDsIwDIXhwhHYGbn/gRjZuQJghCugTfLes4068C8gpDofaSMhdrdH04bbv14327yD1+Pp+cF7h8v59a623trdHVy7MLvRGsNbXIlEZkPPYAUSnQkfkkwkM2sGIgciA4nMeLd87GA1ksVZi1tchVRw1uozmI1UcVbzkGQhIzirCbSiyCjO6gItFZmBs4ZAi0Vm4Szq5xayMBKKs6Ad9JjBrdgZFNCKIJVraaClLKR+MQloMQtGdl0G/ioZyJzoyOmXgMqCKpIGRnZDuZYCRnAeOwMGIoPttCInlkFCQBTnZSKHQBbnZSG7QBXnZSCbwCjOiyJXgVk4L4JcALNxnor8AFbhPAU5A6txHotsHpLvMnAeMwsCZuI8dOYQWIHzkNldYCXOG63x/5c/1jTdAfhxrz2LhsaHAAAAAElFTkSuQmCC'

# 变量的含义
"""
board_states中：0为空格，1为圈，2为叉；
grid_states中：0为未占领，1为圈占领的，2为叉占领的, 3为平；
game_turn中：0为圈的回合，1为叉的回合；
player中：1为圈，2为叉；
free中：True为可任意下，False为只能在指定格子下；
人机模式下：默认人为圈，电脑为叉。
"""


# 棋盘类
class Board(object):

    # 初始化棋盘，格子状态和打印用的棋盘
    def __init__(self):
        self.board_states = [[0 for _ in range(9)] for _ in range(9)]
        self.grid_states = [4 for _ in range(9)]
        self.free = True
        self.blocks = Group()
        self.grids = Group()
        self.win = 0
        self.lost = 0
        self.tie = 0

    # 在（x，y）处写入状态
    def set_board_states(self, x, y, value):
        self.board_states[x][y] = value

    # 读取棋盘（x，y）处状态
    def get_board_states(self, x, y):
        return self.board_states[x][y]

    def get_board(self):
        return self.board_states

    # 设置格子状态
    def set_grid_states(self, grid, value):
        self.grid_states[grid] = value

    # 获取第grid个格子状态
    def get_grid_states(self, grid):
        return self.grid_states[grid]

    def get_grid(self):
        return self.grid_states

    # 检测下一步是否受格子限制
    def get_next_grid(self, y):
        if self.grid_states[y] in (0, 4):
            self.free = False
            for i in range(9):
                if self.grid_states[i] == 4:
                    self.grid_states[i] = 0
            self.grid_states[y] = 4
        else:
            self.free = True
            for i in range(9):
                if self.grid_states[i] == 0:
                    self.grid_states[i] = 4
        return self.free

    def initialize_screen(self, screen):
        for i in range(9):
            new_grid = Grid(screen, i)
            self.grids.add(new_grid)
        for i in range(81):
            new_block = Block(screen, i)
            self.blocks.add(new_block)

    def update_grid(self):
        for i in range(9):
            self.grids.sprites()[i].state = self.grid_states[i]
            self.grids.sprites()[i].update_color()

    def update_blocks(self):
        for i in range(9):
            for j in range(9):
                self.blocks.sprites()[i * 9 + j].state = self.board_states[i][j]
                self.blocks.sprites()[i * 9 + j].update_state()

    def reset_current_blocks(self, x, y):
        for block in self.blocks.sprites():
            if block.x == x and block.y == y:
                block.current = True
            else:
                block.current = False


# 检测格子是否构成三连
def grid_is_over(grid, player, grid_states, grid2):
    for i in DETECT_WINNER:
        if grid[i[0]] == player and \
                grid[i[1]] == player and \
                grid[i[2]] == player:
            grid_states[grid2] = player


# 检测格子是否作和
def grid_is_tie(grid, grid_states, grid2):
    if grid_states[grid2] in (0, 4):
        if 0 not in grid:
            grid_states[grid2] = 3


# 检测游戏是否结束
def game_is_over(board):
    for j in (1, 2):
        for i in DETECT_WINNER:
            if board[i[0]] == j and \
                    board[i[1]] == j and \
                    board[i[2]] == j:
                return True
    return False


# 检测游戏是否作和
def game_is_tie(board):
    if 0 in board:
        return False
    elif 4 in board:
        return False
    else:
        return True


# 游戏类
class Game(object):

    def __init__(self):
        self.game_turn = 0
        self.x = 0
        self.y = 0

    # 更新游戏轮回
    def update_game_turn(self):
        self.game_turn = 1 - self.game_turn


# 节点状态类
class State(object):

    def __init__(self):
        self.available_choices = []
        self.current_x = 0
        self.current_y = 0
        self.should_place_grid = 9
        self.current_board = []
        self.current_grid = []
        self.current_state = 0

    # 设置当前棋盘
    def set_current_board(self, arr):
        self.current_board = copy.deepcopy(arr)

    def get_current_board(self):
        return copy.deepcopy(self.current_board)

    # 设置当前格子情况
    def set_current_grid(self, arr):
        self.current_grid = copy.deepcopy(arr)

    def get_current_grid(self):
        return copy.deepcopy(self.current_grid)

    # 设置下棋地方
    def set_place_placed(self, x, y, is_update_place=True):
        if is_update_place:
            self.current_board[x][y] = 2 - self.current_state
        self.current_x = x
        self.current_y = y

    def get_current_x_y(self):
        return [self.current_x, self.current_y]

    def set_current_state(self, state):
        self.current_state = state

    def update_current_state(self, state):
        self.current_state = 1 - state

    def set_should_place_grid(self):
        if self.current_grid[self.current_y] == 0:
            self.should_place_grid = self.current_y
        else:
            self.should_place_grid = 9

    # 获取可选择落子的地方
    def get_available_choices(self):
        self.available_choices = []
        if self.current_grid[self.current_y] == 0:
            for i in range(9):
                if self.current_board[self.should_place_grid][i] == 0:
                    self.available_choices.append([self.should_place_grid, i])
        else:
            for i in range(9):
                if self.current_grid[i] == 0:
                    for j in range(9):
                        if self.current_board[i][j] == 0:
                            self.available_choices.append([i, j])

    # 判断游戏是否结束
    def is_terminal(self):
        return game_is_over(self.current_grid) or \
               game_is_tie(self.current_grid)

    # 更新游戏棋盘状态
    def update_board_states(self, grid):
        grid_is_over(self.current_board[grid], 2 - self.current_state,
                     self.current_grid, grid)

        grid_is_tie(self.current_board[grid], self.current_grid, grid)

    # 使用随机选项获取下一个状态，并获取
    def get_next_state_with_random_choice(self):

        # 从可用选择序列中随机选择一个数
        random_choice = random.choice(self.available_choices)
        self.available_choices.remove(random_choice)

        next_state = State()

        # 更新当前棋盘状态
        next_state.set_current_board(self.current_board)
        next_state.update_current_state(self.current_state)
        next_state.set_place_placed(random_choice[0], random_choice[1])
        next_state.set_current_grid(self.current_grid)
        next_state.update_board_states(random_choice[0])

        next_state.set_should_place_grid()
        next_state.get_available_choices()

        return next_state


# 节点类
class Node(object):

    # 初始化父节点，子节点，访问次数和quality值
    def __init__(self):
        self.parent = None
        self.children = []

        self.visit_times = 0
        self.quality_value = 0.0
        self.winning_times = 0
        self.losing_times = 0
        self.state = None

    # 设置状态
    def set_state(self, state):
        self.state = state

    # 获取状态
    def get_state(self):
        return self.state

    # 获取父节点
    def get_parent(self):
        return self.parent

    # 设置父节点
    def set_parent(self, parent):
        self.parent = parent

    # 获取子节点树
    def get_children(self):
        return self.children

    # 获取访问次数
    def get_visit_times(self):
        return self.visit_times

    # 设置访问次数
    def set_visit_times(self, times):
        self.visit_times = times

    # 使访问次数+1
    def visit_times_add_one(self):
        self.visit_times += 1

    # 获取quality值
    def get_quality_value(self):
        return self.quality_value

    # 设置quality值
    def set_quality_value(self, value):
        self.quality_value = value

    # 使quality+n
    def quality_value_add_n(self, n):
        self.quality_value += n

    # 在子节点后添加一个新节点
    def add_child(self, sub_node):
        # 将新节点设置为父节点
        sub_node.set_parent(self)
        self.children.append(sub_node)


# 模拟运行
def simulation(board, grid, y, players, mode):
    player = players - 1
    random_choice = [0, y]
    while not game_is_over(grid):

        if game_is_tie(grid):
            return 0

        available_choices = []
        if grid[random_choice[1]] == 0:
            for i in range(9):
                if board[random_choice[1]][i] == 0:
                    available_choices.append([random_choice[1], i])
        else:
            for i in range(9):
                if grid[i] == 0:
                    for j in range(9):
                        if board[i][j] == 0:
                            available_choices.append([i, j])

        random_choice = random.choice(available_choices)
        board[random_choice[0]][random_choice[1]] = player + 1

        grid_is_over(
            board[random_choice[0]], player + 1, grid, random_choice[0]
        )
        grid_is_tie(board[random_choice[0]], grid, random_choice[0])

        player = 1 - player

    if player == players - 1:
        return 1 * mode
    else:
        return -1 * mode


# 选择及扩展函数
def tree_policy(node):
    while not node.get_state().is_terminal():
        if not node.get_state().available_choices:
            node = best_child(node, True)
        else:
            sub_node = expand(node)
            return sub_node

    return node


# 模拟函数
def default_policy(node, mode):
    # 获取游戏状态
    state = node.get_state()
    random_board = copy.deepcopy(state.current_board)
    random_grid = copy.deepcopy(state.current_grid)
    # 读出最后的价值
    player = state.current_state + 1
    if game_is_tie(random_grid):
        return 0
    elif game_is_over(random_grid):
        if mode == 1:
            node.quality_value_add_n(sys.maxsize)
        return 1 * mode
    else:
        final_state_reward = simulation(
            random_board, random_grid, state.current_y, player, mode
        )
        return final_state_reward


# 扩展新节点函数
def expand(node):
    # 随机获得一个新状态
    new_state = node.get_state().get_next_state_with_random_choice()
    sub_node = Node()
    # 设置新节点状态
    sub_node.set_state(new_state)
    node.add_child(sub_node)

    return sub_node


# 计算UCB值函数
def best_child(node, is_exploration):
    # 使用最小浮点值
    best_score = -sys.maxsize
    best_visit_times = -sys.maxsize
    best_sub_node = None
    c = 1.0

    # 遍历所有子节点以找到最佳节点
    if is_exploration:
        for sub_node in node.get_children():
            # UCB值 = quality / times + C * sqrt(2 * ln(total_times) / times)
            left = sub_node.get_quality_value() / sub_node.get_visit_times()
            right = c * math.log(
                node.get_visit_times()) / sub_node.get_visit_times()
            score = left + math.sqrt(right)
            if score > best_score:
                best_sub_node = sub_node
                best_score = score
    else:
        for sub_node in node.get_children():
            if sub_node.get_visit_times() > best_visit_times:
                best_sub_node = sub_node
                best_visit_times = sub_node.get_visit_times()

    # 返回最好节点
    return best_sub_node


# 回溯函数
def backup(node, reward):
    n_state = node.get_state().current_state
    while node is not None:
        node.visit_times_add_one()
        if node.get_state().current_state == n_state:
            node.quality_value_add_n(reward)
            if reward > 0:
                node.winning_times += 1
            elif reward < 0:
                node.losing_times += 1
        else:
            node.quality_value_add_n(-reward)
            if reward < 0:
                node.winning_times += 1
            elif reward > 0:
                node.losing_times += 1
        node = node.parent


# 蒙特卡洛树搜索算法函数
def monte_carlo_tree_search(node, times, mode):
    begin = time.time()
    while time.time() - begin < times:
        expand_node = tree_policy(node)
        reward = default_policy(expand_node, mode)
        backup(expand_node, reward)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    best_next_node = best_child(node, False)
    return best_next_node


def ai_reset(board, x, y, nodes, turn):
    init_node = None
    if nodes:
        for node in nodes:
            if node.get_state().current_x == x and \
                    node.get_state().current_y == y:
                init_node = node
                init_node.parent = None
    else:
        init_state = State()
        init_state.set_current_board(board.get_board())
        true_grid = [0 for _ in range(9)]
        for i in range(9):
            if board.grid_states[i] == 4:
                true_grid[i] = 0
            else:
                true_grid[i] = board.grid_states[i]
        init_state.set_current_grid(true_grid)
        init_state.current_state = turn
        init_state.set_place_placed(x, y, False)
        init_state.set_should_place_grid()
        init_state.get_available_choices()
        init_node = Node()
        init_node.set_state(init_state)

    return init_node


class Button(object):

    def __init__(self, screen, a):
        """初始化按钮属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.msg_image = None
        self.msg_image_rect = None

        # 设置按钮尺寸和其他属性
        self.text_color = (0, 0, 0)

        # 创建按钮对象
        if a == 1:
            self.width, self.height = 300, 70
            self.button_color = (0, 230, 0)
            self.rect = pygame.Rect(0, 0, self.width, self.height)
            self.rect.centerx = self.screen_rect.centerx
            self.rect.top = self.screen_rect.top + 150
            self.font = pygame.font.SysFont('kaiti', 45)
        elif a == 2:
            self.width, self.height = 200, 50
            self.button_color = (255, 255, 0)
            self.rect = pygame.Rect(0, 0, self.width, self.height)
            self.rect.centerx = self.screen_rect.centerx
            self.rect.bottom = self.screen_rect.bottom - 160
            self.font = pygame.font.SysFont('kaiti', 35)
        elif a == 3:
            self.width, self.height = 300, 70
            self.button_color = (0, 230, 0)
            self.rect = pygame.Rect(0, 0, self.width, self.height)
            self.rect.centerx = self.screen_rect.centerx
            self.rect.top = self.screen_rect.top + 250
            self.font = pygame.font.SysFont('kaiti', 45)
        elif a == 4:
            self.width, self.height = 300, 70
            self.button_color = (0, 230, 0)
            self.rect = pygame.Rect(0, 0, self.width, self.height)
            self.rect.centerx = self.screen_rect.centerx
            self.rect.top = self.screen_rect.top + 350
            self.font = pygame.font.SysFont('kaiti', 45)
        elif a == 5:
            self.width, self.height = 300, 70
            self.button_color = (0, 230, 0)
            self.rect = pygame.Rect(0, 0, self.width, self.height)
            self.rect.centerx = self.screen_rect.centerx
            self.rect.top = self.screen_rect.top + 450
            self.font = pygame.font.SysFont('kaiti', 45)

    def prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self, msg):
        self.prep_msg(msg)
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)


class Title(object):

    def __init__(self, screen):
        """初始化按钮属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.msg_image = None
        self.msg_image_rect = None
        self.msg_image2 = None
        self.msg_image_rect2 = None

        # 设置按钮尺寸和其他属性
        self.width, self.height = 200, 100
        self.text_color = (0, 0, 0)

        # 创建按钮对象
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx = self.screen_rect.centerx
        self.rect.top = self.screen_rect.top + 20
        self.font = pygame.font.SysFont('kaiti', 50)
        self.font2 = pygame.font.SysFont('kaiti', 25)

    def prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          None)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

        msg2 = "made by Xie Jiaye"
        self.msg_image2 = self.font2.render(msg2, True, (255, 0, 0),
                                            None)
        self.msg_image_rect2 = self.msg_image2.get_rect()
        self.msg_image_rect2.centerx = self.rect.centerx
        self.msg_image_rect2.top = self.msg_image_rect.bottom + 5

    def draw_button(self, msg):
        self.prep_msg(msg)
        self.screen.blit(self.msg_image, self.msg_image_rect)
        self.screen.blit(self.msg_image2, self.msg_image_rect2)


def draw_button(screen, title, play_button, setting_button, rule_button, exit_button):
    bg_color = (230, 230, 230)
    screen.fill(bg_color)
    play_button.draw_button("开始")
    setting_button.draw_button("设置")
    rule_button.draw_button("规则")
    exit_button.draw_button("退出")
    title.draw_button("超级井字棋")
    pygame.display.flip()


def draw_rate_bar(screen, rates, position, size, colors, labels):
    """绘制胜率条
    Args:
    - screen: pygame的屏幕对象
    - rates: 一个包含三个元素的列表，表示人胜率、平局率、AI胜率
    - position: 绘制条的位置（x, y）
    - size: 绘制条的尺寸（宽度，高度）
    - colors: 一个包含三种颜色的列表，对应于人、平局、AI
    """
    total_width = size[0]
    x_start = position[0]
    y_start = position[1]

    # 计算每部分的长度
    total_rates = sum(rates)
    if total_rates == 0:
        lengths = [0, 0, 0]
    else:
        lengths = [total_width * (rate / total_rates) for rate in rates]

    # 绘制每个部分
    for i, length in enumerate(lengths):
        pygame.draw.rect(screen, colors[i], (x_start, y_start, length, size[1]))
        x_start += length  # 更新下一个条形的起始位置

    # 绘制分割线和文本
    font = pygame.font.SysFont('kaiti', 18)
    x_start = position[0]
    for i, rate in enumerate(rates):
        pygame.draw.line(screen, (0, 0, 0), (x_start, y_start), (x_start, y_start + size[1]), 2)
        if lengths[i] > 60:
            text_surf = font.render(f'{rate}%', True, (0, 0, 0))
            screen.blit(text_surf, (x_start + 5, y_start + 5))
        x_start += lengths[i]
    pygame.draw.line(screen, (0, 0, 0), (x_start-1, y_start), (x_start-1, y_start + size[1]), 2)

    # 绘制左侧和右侧的标签
    left_label_surf = font.render(labels[0], True, (0, 0, 0))
    right_label_surf = font.render(labels[1], True, (0, 0, 0))
    screen.blit(left_label_surf, (position[0] - left_label_surf.get_width() - 10, y_start))
    screen.blit(right_label_surf, (position[0] + total_width + 10, y_start))


def update_screen(screen, bg_color, board, ending, is_ai=False, toggle_button=None, difficulty=-1):
    screen.fill(bg_color)

    for gird in board.grids.sprites():
        gird.draw()

    for block in board.blocks.sprites():
        block.draw()

    draw_tips(screen, "按ESC键返回主菜单")
    if is_ai:
        draw_small_title(screen, difficulty, ending)
        toggle_button.draw()  # 绘制开关按钮
        if toggle_button.on:
            draw_rate_bar(screen, [board.lost, board.tie, board.win], (50, 600), (500, 30),
                          [(255, 0, 0), (255, 255, 0), (0, 0, 255)], ["人", "AI"])
    pygame.display.flip()


def show_setting(screen, mode, difficulty, first_or_second, ending):
    screen_rect = screen.get_rect()
    # 统一设置字体和大小
    title_font = pygame.font.SysFont('kaiti', 40)
    normal_font = pygame.font.SysFont('kaiti', 30)

    # 设置mode标题栏文字：模式
    mode_title_image = title_font.render(
        "模式:", True, (255, 0, 0), None)
    mode_title_image_rect = mode_title_image.get_rect()
    mode_title_image_rect.left = screen_rect.left + 20
    mode_title_image_rect.top = screen_rect.top + 50

    # 设置difficulty标题栏文字：难度
    difficulty_title_image = title_font.render(
        "难度:", True, (255, 0, 0), None)
    difficulty_title_image_rect = difficulty_title_image.get_rect()
    difficulty_title_image_rect.left = screen_rect.left + 20
    difficulty_title_image_rect.top = screen_rect.top + 150

    # 设置先后手选择标题栏文字：先手选择
    first_or_second_title_image = title_font.render(
        "先后手选择:", True, (255, 0, 0), None)
    first_or_second_title_image_rect = first_or_second_title_image.get_rect()
    first_or_second_title_image_rect.left = screen_rect.left + 20
    first_or_second_title_image_rect.top = screen_rect.top + 250

    # 设置先后手选择标题栏文字：先手选择
    ending_title_image = title_font.render(
        "获胜目标:", True, (255, 0, 0), None)
    ending_title_image_rect = ending_title_image.get_rect()
    ending_title_image_rect.left = screen_rect.left + 20
    ending_title_image_rect.top = screen_rect.top + 350

    # 设置显示Mode选择情况的矩形大小及位置
    mode_rect_all = pygame.Rect(0, 0, 250, 50)
    mode_rect_middle = pygame.Rect(0, 0, 150, 50)
    mode_rect_all.centerx = screen_rect.centerx
    mode_rect_all.top = mode_title_image_rect.bottom
    mode_rect_middle.center = mode_rect_all.center

    # 设置显示Difficulty选择情况的矩形大小及位置
    difficulty_rect_all = pygame.Rect(0, 0, 250, 50)
    difficulty_rect_middle = pygame.Rect(0, 0, 150, 50)
    difficulty_rect_all.centerx = screen_rect.centerx
    difficulty_rect_all.top = difficulty_title_image_rect.bottom
    difficulty_rect_middle.center = difficulty_rect_all.center

    # 设置显示先后手选择情况的矩形大小及位置
    first_or_second_rect_all = pygame.Rect(0, 0, 250, 50)
    first_or_second_rect_middle = pygame.Rect(0, 0, 150, 50)
    first_or_second_rect_all.centerx = screen_rect.centerx
    first_or_second_rect_all.top = first_or_second_title_image_rect.bottom
    first_or_second_rect_middle.center = first_or_second_rect_all.center

    # 设置显示先后手选择情况的矩形大小及位置
    ending_rect_all = pygame.Rect(0, 0, 250, 50)
    ending_rect_middle = pygame.Rect(0, 0, 150, 50)
    ending_rect_all.centerx = screen_rect.centerx
    ending_rect_all.top = ending_title_image_rect.bottom
    ending_rect_middle.center = ending_rect_all.center

    # 载入上翻和下翻按钮的图片
    mode_next_png = NEXT_PNG
    mode_last_png = LAST_PNG
    difficulty_next_png = NEXT_PNG
    difficulty_last_png = LAST_PNG
    first_or_second_next_png = NEXT_PNG
    first_or_second_last_png = LAST_PNG
    ending_next_png = NEXT_PNG
    ending_last_png = LAST_PNG

    # 初始化mode载入图片的位置
    mode_next_png_rect = mode_next_png.get_rect()
    mode_last_png_rect = mode_last_png.get_rect()
    mode_next_png_rect.topright = mode_rect_all.topright
    mode_last_png_rect.topleft = mode_rect_all.topleft

    # 初始化difficulty载入图片的位置
    difficulty_next_png_rect = difficulty_next_png.get_rect()
    difficulty_last_png_rect = difficulty_last_png.get_rect()
    difficulty_next_png_rect.topright = difficulty_rect_all.topright
    difficulty_last_png_rect.topleft = difficulty_rect_all.topleft

    # 初始化先后手载入图片的位置
    first_or_second_next_png_rect = first_or_second_next_png.get_rect()
    first_or_second_last_png_rect = first_or_second_last_png.get_rect()
    first_or_second_next_png_rect.topright = first_or_second_rect_all.topright
    first_or_second_last_png_rect.topleft = first_or_second_rect_all.topleft

    # 初始化先后手载入图片的位置
    ending_next_png_rect = ending_next_png.get_rect()
    ending_last_png_rect = ending_last_png.get_rect()
    ending_next_png_rect.topright = ending_rect_all.topright
    ending_last_png_rect.topleft = ending_rect_all.topleft

    # 设置OK按钮样式及位置
    ok_rect = pygame.Rect(0, 0, 150, 50)
    ok_rect.bottom = screen_rect.bottom - 20
    ok_rect.right = screen_rect.right - 20
    text_color = (0, 0, 0)
    button_color = (15, 255, 240)

    # 初始化ok文字
    ok_msg_image = normal_font.render(
        "OK", True, text_color, (255, 255, 0))
    ok_msg_image_rect = ok_msg_image.get_rect()
    ok_msg_image_rect.center = ok_rect.center

    def reset_screen(draw_ai_settings):
        # 绘制屏幕
        screen.fill((230, 230, 230))

        # 绘制Mode栏
        if mode == 0:
            mode_msg_image = normal_font.render(
                "人机对战", True, text_color, None)
        else:
            mode_msg_image = normal_font.render(
                "人人对战", True, text_color, None)
        mode_msg_image_rect = mode_msg_image.get_rect()
        mode_msg_image_rect.center = mode_rect_middle.center

        screen.blit(mode_next_png, mode_next_png_rect)
        screen.blit(mode_last_png, mode_last_png_rect)
        screen.fill(button_color, mode_rect_middle)
        screen.blit(mode_msg_image, mode_msg_image_rect)
        screen.blit(mode_title_image, mode_title_image_rect)

        if draw_ai_settings:
            # 绘制Difficulty栏
            if difficulty == -1:
                difficulty_msg_image = normal_font.render(
                    "幼稚", True, text_color, None)
            elif difficulty == 0:
                difficulty_msg_image = normal_font.render(
                    "简单", True, text_color, None)
            elif difficulty == 1:
                difficulty_msg_image = normal_font.render(
                    "中等", True, text_color, None)
            else:
                difficulty_msg_image = normal_font.render(
                    "困难", True, text_color, None)
            difficulty_msg_image_rect = difficulty_msg_image.get_rect()
            difficulty_msg_image_rect.center = difficulty_rect_middle.center

            screen.blit(difficulty_next_png, difficulty_next_png_rect)
            screen.blit(difficulty_last_png, difficulty_last_png_rect)
            screen.fill(button_color, difficulty_rect_middle)
            screen.blit(difficulty_msg_image, difficulty_msg_image_rect)
            screen.blit(difficulty_title_image, difficulty_title_image_rect)

            # 绘制先后手栏
            if first_or_second == 0:
                first_or_second_msg_image = normal_font.render(
                    "人先手", True, text_color, None)
            else:
                first_or_second_msg_image = normal_font.render(
                    "电脑先手", True, text_color, None)
            first_or_second_msg_image_rect = first_or_second_msg_image.get_rect()
            first_or_second_msg_image_rect.center = first_or_second_rect_middle.center

            screen.blit(first_or_second_next_png, first_or_second_next_png_rect)
            screen.blit(first_or_second_last_png, first_or_second_last_png_rect)
            screen.fill(button_color, first_or_second_rect_middle)
            screen.blit(first_or_second_msg_image,
                        first_or_second_msg_image_rect)
            screen.blit(first_or_second_title_image,
                        first_or_second_title_image_rect)

            # 绘制最终获胜栏
            if ending == 1:
                ending_msg_image = normal_font.render(
                    "赢得对局", True, text_color, None)
            else:
                ending_msg_image = normal_font.render(
                    "输掉对局", True, text_color, None)
            ending_msg_image_rect = ending_msg_image.get_rect()
            ending_msg_image_rect.center = ending_rect_middle.center

            screen.blit(ending_next_png, ending_next_png_rect)
            screen.blit(ending_last_png, ending_last_png_rect)
            screen.fill(button_color, ending_rect_middle)
            screen.blit(ending_msg_image, ending_msg_image_rect)
            screen.blit(ending_title_image, ending_title_image_rect)

        # 绘制ok按钮
        screen.fill((255, 255, 0), ok_rect)
        screen.blit(ok_msg_image, ok_msg_image_rect)

        pygame.display.flip()

    reset_screen(True)

    loop = True
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:  # 检测鼠标事件
                if event.button == 1:  # 如果按下左键
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if mode_next_png_rect.collidepoint(mouse_x, mouse_y) or mode_last_png_rect.collidepoint(mouse_x, mouse_y):
                        mode = 1 - mode
                    elif difficulty_next_png_rect.collidepoint(mouse_x, mouse_y) and mode == 0:
                        difficulty += 1
                        if difficulty == 3:
                            difficulty = -1
                    elif difficulty_last_png_rect.collidepoint(mouse_x, mouse_y) and mode == 0:
                        difficulty -= 1
                        if difficulty == -2:
                            difficulty = 2
                    elif first_or_second_next_png_rect.collidepoint(mouse_x, mouse_y) or first_or_second_last_png_rect.collidepoint(mouse_x, mouse_y) and mode == 0:
                        first_or_second = 1 - first_or_second
                    elif ending_next_png_rect.collidepoint(mouse_x, mouse_y) or ending_last_png_rect.collidepoint(mouse_x, mouse_y) and mode == 0:
                        ending = -ending
                    elif ok_rect.collidepoint(mouse_x, mouse_y):
                        loop = False
                    # 判断是否显示AI对局设置
                    if mode == 0:
                        reset_screen(True)
                    elif mode == 1:
                        reset_screen(False)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP_ENTER:
                    loop = False

    return mode, difficulty, first_or_second, ending


def render_multiline_text(screen, text, pos, font, color=(0, 0, 0), max_width=None):
    x, y = pos
    current_line = ""
    max_width = max_width if max_width else screen.get_width() - 50  # 设置文本最大宽度

    for char in text:
        # 测试当前行加上新字符后的长度
        test_line = current_line + char
        if font.size(test_line)[0] > max_width or char == "n":
            # 如果超过最大宽度，则输出当前行，并开始新的一行
            rendered_line = font.render(current_line, True, color)
            screen.blit(rendered_line, (x, y))
            y += rendered_line.get_height()
            if char != "n":
                current_line = char
            else:
                current_line = ""
        else:
            current_line += char

    # 输出最后一行
    if current_line:
        rendered_line = font.render(current_line, True, color)
        screen.blit(rendered_line, (x, y))


def show_rules_screen(screen):
    running = True
    while running:
        screen.fill((255, 255, 255))
        title_font = pygame.font.SysFont('simhei', 32)
        font = pygame.font.SysFont('fangsong', 18)
        title_text = title_font.render('游戏规则', True, (0, 0, 0))
        back_button_text = font.render('返回', True, (0, 0, 0))

        title_text_rect = title_text.get_rect(center=(400 / 2, 40))
        back_button_rect = pygame.Rect(400 / 2 - 50, 600 - 60, 100, 50)

        screen.blit(title_text, title_text_rect)  # 显示标题

        # 游戏规则和操作方法的详细介绍
        detailed_text = "    超级井字棋由一个大的3x3的井字棋盘组成，其中每个单元格自身也是一个独立的3x3井字棋盘。游戏的主要目标是在大棋盘上形成标准的井字棋获胜模式——即三个相同的标记连成一直线，无论是水平、垂直还是对角线。玩家必须在小棋盘上赢得局部胜利，以便在大棋盘上占领该格，进而努力形成整个大棋盘上的连线。n    游戏开始时，第一位玩家可以在任意的81个格子中下棋。接下来，玩家在任一小格中的落子将会决定对方下一步落子的小格位置。例如，如果一方在某大格的第2小格下，另一方下一步就必须在第2个大格下。如果一方在某大格的第7小格下，另一方下一步就必须在第7个大格下。特别地，一旦任一小格由一方玩家胜出（形成三连线）或被填满，该小格便不再允许落子。若一方被指派到已完成的小格进行落子，他们可以自由选择在任何未完成的小格中落子。n    在对局中，格子边框的不同颜色代表格子的不同状态。红色代表○占领，蓝色代表×占领，黑色代表不可落子，绿色代表可以落子。n    为了让玩家获得更好的游戏体验，加入了与以赢得对局为目标相反的模式——即尽可能输掉对局。 "
        render_multiline_text(screen, detailed_text, (20, 60), font, max_width=screen.get_width() - 40)

        # 绘制返回按钮
        pygame.draw.rect(screen, (0, 0, 0), back_button_rect, width=2, border_radius=10)
        screen.blit(back_button_text, back_button_text.get_rect(center=back_button_rect.center))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button_rect.collidepoint(event.pos):
                    running = False
        pygame.time.Clock().tick(15)


def check_button(play_button, setting_button, rule_button, exit_button, screen, title, mode, difficulty, first_or_second, ending):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # 如果按下左键
                mouse_x, mouse_y = pygame.mouse.get_pos()  # 获取鼠标位置
                # 如果开始按钮被点击
                if play_button.rect.collidepoint(mouse_x, mouse_y):
                    return False, mode, difficulty, first_or_second, ending
                # 如果设置按钮被点击
                elif setting_button.rect.collidepoint(mouse_x, mouse_y):
                    mode, difficulty, first_or_second, ending = show_setting(screen, mode, difficulty, first_or_second, ending)
                    draw_button(screen, title, play_button, setting_button,
                                rule_button, exit_button)
                # 如果规则按钮被点击
                elif rule_button.rect.collidepoint(mouse_x, mouse_y):
                    show_rules_screen(screen)
                    draw_button(screen, title, play_button, setting_button,
                                rule_button, exit_button)
                elif exit_button.rect.collidepoint(mouse_x, mouse_y):
                    sys.exit()

    return True, mode, difficulty, first_or_second, ending


class Grid(Sprite):

    def __init__(self, screen, a):
        super().__init__()
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.width, self.height = 146, 146
        self.color = (0, 0, 0)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.state = 0

        self.set_place(a)
        self.update_color()

    # 设置位置
    def set_place(self, a):
        self.rect.left = 66 + 166 * (a % 3)
        self.rect.top = 70 + 166 * int(a / 3)

    def update_color(self):
        if self.state == 0 or self.state == 3:
            self.color = (0, 0, 0)
        elif self.state == 1:
            self.color = (255, 0, 0)
        elif self.state == 2:
            self.color = (0, 0, 255)
        else:
            self.color = (0, 255, 0)

    def draw(self):
        self.screen.fill(self.color, self.rect)


class Block(Sprite):

    def __init__(self, screen, a):
        super().__init__()
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.width, self.height = 40, 40
        self.button_color = (255, 255, 255)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.state = 0
        self.x = int(a / 9)
        self.y = a % 9
        self.lock = False

        self.img = None
        self.img_rect = None
        self.current = False

        self.set_place()

    def set_place(self):
        self.rect.left = 76 + 166 * (self.x % 3) + 43 * (self.y % 3)
        self.rect.top = 80 + 166 * int(self.x / 3) + 43 * int(self.y / 3)

    def get_state(self, mouse_x, mouse_y, board, player, click):
        if not self.lock:
            if self.rect.collidepoint(mouse_x, mouse_y):
                if click:
                    board[self.x][self.y] = player
                    self.lock = True
                    self.state = player
                else:
                    self.state = player + 2
            else:
                self.state = 0
            self.update_state()

            return self.x, self.y, self.lock
        else:
            return self.x, self.y, False

    def update_state(self):
        if self.state == 1:
            if self.current:
                self.img = CIRCLE_NOW_PNG
            else:
                self.img = CIRCLE_PNG
            self.lock = True
        elif self.state == 2:
            if self.current:
                self.img = CROSS_NOW_PNG
            else:
                self.img = CROSS_PNG
            self.lock = True
        elif self.state == 3:
            self.img = CIRCLE_DARK_PNG
        elif self.state == 4:
            self.img = CROSS_DARK_PNG

    def draw(self):
        self.screen.fill(self.button_color, self.rect)
        if self.state != 0:
            self.img_rect = self.img.get_rect()
            self.img_rect.center = self.rect.center
            self.screen.blit(self.img, self.img_rect)


class ToggleButton:
    """一个简单的开关按钮，用于控制是否显示某些元素"""
    def __init__(self, screen, position, size):
        self.screen = screen
        self.position = position
        self.size = size
        self.on = False  # 默认关闭状态
        self.rect = pygame.Rect(position[0], position[1], size[0], size[1])
        self.font = pygame.font.SysFont('kaiti', 20)
        self.label_on = self.font.render('隐藏胜率', True, (0, 0, 0))
        self.label_off = self.font.render('显示胜率', True, (0, 0, 0))

    def draw(self):
        """绘制开关按钮"""
        if self.on:
            pygame.draw.rect(self.screen, (0, 200, 0), self.rect)  # 绿色表示开启
            self.screen.blit(self.label_on, (self.position[0] + 5, self.position[1] + 5))
        else:
            pygame.draw.rect(self.screen, (200, 0, 0), self.rect)  # 红色表示关闭
            self.screen.blit(self.label_off, (self.position[0] + 5, self.position[1] + 5))

    def toggle(self):
        """切换开关状态"""
        self.on = not self.on

    def handle_event(self, event):
        """处理鼠标事件，切换开关状态"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.toggle()
                return True
        return False


# 将base64编码转换为图片
def get_pic(pic_code, pic_name):
    image = open(pic_name, 'wb')
    image.write(base64.b64decode(pic_code))
    image.close()


# 通过win32api获取系统屏幕的分辨率
def get_system_metrics():
    from win32api import GetSystemMetrics
    return GetSystemMetrics(0), GetSystemMetrics(1)


# 传入窗口大小(分辨率)计算出窗口居中的位置
def get_window_positions(width, height):
    system_metrics = get_system_metrics()
    window_x_position = (system_metrics[0] - width) // 2
    window_y_position = (system_metrics[1] - height) // 2
    return window_x_position, window_y_position


def man_input(board, human, screen=None, bg_color=None, ending=None, toggle_button=None, difficulty=-1):
    ok = False
    while not ok:
        for event in pygame.event.get():
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if toggle_button:
                if toggle_button.handle_event(event):
                    update_screen(screen, bg_color, board, ending, True, toggle_button, difficulty)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for block in board.blocks.sprites():
                        if board.grid_states[block.x] == 4:
                            x, y, ok = block.get_state(mouse_x, mouse_y, board.board_states, human.game_turn + 1, True)
                            if ok:
                                human.x, human.y = x, y
                                break
            if ok:
                break
            elif event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
            else:
                for block in board.blocks.sprites():
                    if board.grid_states[block.x] == 4:
                        block.get_state(mouse_x, mouse_y, board.board_states,
                                        human.game_turn + 1, False)
                    block.draw()
                    pygame.display.flip()
    return False


def update_board_state(board, human):
    grid_is_over(board.get_board()[human.x], human.game_turn + 1,
                 board.grid_states, human.x)
    grid_is_tie(board.get_board()[human.x], board.grid_states, human.x)
    board.reset_current_blocks(human.x, human.y)
    if not board.get_next_grid(human.y):
        human.x = human.y
    board.update_grid()
    board.update_blocks()
    human.update_game_turn()


def draw_msg(screen, msg):
    screen_rect = screen.get_rect()

    text_color = (255, 0, 0)
    font = pygame.font.SysFont('kaiti', 45)

    msg_image = font.render(
        msg, True, text_color, None)
    msg_image_rect = msg_image.get_rect()
    msg_image_rect.centerx = screen_rect.centerx
    msg_image_rect.bottom = screen_rect.bottom - 120

    screen.blit(msg_image, msg_image_rect)


def draw_tips(screen, msg, delete=False):
    screen_rect = screen.get_rect()

    text_color = (255, 0, 0)
    font = pygame.font.SysFont('kaiti', 24)

    msg_image = font.render(
        msg, True, text_color, None)
    msg_image_rect = msg_image.get_rect()
    msg_image_rect.left = screen_rect.left + 10
    msg_image_rect.bottom = screen_rect.bottom - 10

    if delete:
        screen.fill((230, 230, 230), msg_image_rect)
    else:
        screen.blit(msg_image, msg_image_rect)


def draw_small_title(screen, types, ending):
    screen_rect = screen.get_rect()

    text_color = (255, 0, 0)
    font = pygame.font.SysFont('kaiti', 24)

    # 初始化难度标题
    if types == -1:
        types_msg = "难度：幼稚"
    elif types == 0:
        types_msg = "难度：简单"
    elif types == 1:
        types_msg = "难度：中等"
    else:
        types_msg = "难度：困难"
    types_msg_image = font.render(
        types_msg, True, text_color, None)
    types_msg_image_rect = types_msg_image.get_rect()
    types_msg_image_rect.left = screen_rect.left + 10
    types_msg_image_rect.top = screen_rect.top + 5

    # 初始化获胜目标标题
    if ending == 1:
        ending_msg = "获胜目标：赢得对局"
    else:
        ending_msg = "获胜目标：输掉对局"
    ending_msg_image = font.render(
        ending_msg, True, text_color, None)
    ending_msg_image_rect = ending_msg_image.get_rect()
    ending_msg_image_rect.left = screen_rect.left + 10
    ending_msg_image_rect.top = screen_rect.top + 35

    screen.blit(types_msg_image, types_msg_image_rect)
    screen.blit(ending_msg_image, ending_msg_image_rect)


class Reset(object):

    def __init__(self, screen, a, msg):
        """初始化按钮属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.msg_image = None
        self.msg_image_rect = None

        # 设置按钮尺寸和其他属性
        self.text_color = (0, 0, 0)
        self.button_color = (0, 255, 0)
        self.width, self.height = 230, 60
        self.font = pygame.font.SysFont('kaiti', 40)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.bottom = self.screen_rect.bottom - 30

        # 创建按钮对象
        if a == 1:
            self.rect.left = self.screen_rect.left + 50
        elif a == 2:
            self.rect.right = self.screen_rect.right - 50

        # 设置按钮的框的属性
        self.frame_rect = pygame.Rect(0, 0, 240, 70)
        self.frame_rect.center = self.rect.center

        self.prep_msg(msg)

    def prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill((0, 0, 0), self.frame_rect)
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)


def load_image():
    get_pic(CIRCLE_NOW, 'circle_now')
    circle_now = pygame.image.load('circle_now')
    get_pic(CIRCLE, 'circle_png')
    circle_png = pygame.image.load('circle_png')
    get_pic(CROSS_NOW, 'cross_now')
    cross_now = pygame.image.load('cross_now')
    get_pic(CROSS, 'cross_png')
    cross_png = pygame.image.load('cross_png')
    get_pic(CIRCLE_DARK, 'circle_dark_png')
    circle_dark_png = pygame.image.load('circle_dark_png')
    get_pic(CROSS_DARK, 'cross_dark_png')
    cross_dark_png = pygame.image.load('cross_dark_png')
    get_pic(NEXT, "next_png")
    next_png = pygame.image.load("next_png")
    get_pic(LAST, "last_png")
    last_png = pygame.image.load("last_png")
    os.remove("next_png")
    os.remove("last_png")
    os.remove('cross_dark_png')
    os.remove('circle_dark_png')
    os.remove('cross_png')
    os.remove('cross_now')
    os.remove('circle_png')
    os.remove('circle_now')

    return circle_now, circle_png, cross_now, cross_png, circle_dark_png, cross_dark_png, next_png, last_png


def run_game():
    while True:
        pygame.init()
        mode, difficulty, first_or_second, ending = 0, -1, 0, 1
        pos_x, pos_y = get_window_positions(400, 600)
        os.environ["SDL_VIDEO_WINDOW_POS"] = "%d, %d" % (pos_x, pos_y)
        screen = pygame.display.set_mode((400, 600))
        pygame.display.set_caption("超级井字棋")

        bg_color = (230, 230, 230)
        screen.fill(bg_color)

        play_button = Button(screen, 1)
        setting_button = Button(screen, 3)
        rule_button = Button(screen, 4)
        exit_button = Button(screen, 5)
        title = Title(screen)
        draw_button(screen, title, play_button,
                    setting_button, rule_button, exit_button)

        pygame.display.flip()
        loop = True
        while loop:
            loop, mode, difficulty, first_or_second, ending = check_button(play_button, setting_button, rule_button, exit_button, screen, title, mode, difficulty, first_or_second, ending)

        width = 600
        length = 750
        pos_x, pos_y = get_window_positions(width, length)
        os.environ["SDL_VIDEO_WINDOW_POS"] = "%d, %d" % (pos_x, pos_y)
        screen = pygame.display.set_mode((width, length))

        reset = False
        while not reset:
            board = Board()
            board.initialize_screen(screen)
            board.update_grid()
            update_screen(screen, bg_color, board, ending)
            draw_tips(screen, "按ESC键返回主菜单")
            human = Game()

            if mode == 1:
                while not game_is_over(board.grid_states):
                    if game_is_tie(board.grid_states):
                        human.game_turn = 2
                        break
                    reset = man_input(board, human)
                    if reset:
                        break
                    update_board_state(board, human)
                    update_screen(screen, bg_color, board, ending)
            elif mode == 0:
                if difficulty == -1:
                    run_time = 0.5
                elif difficulty == 0:
                    run_time = 1
                elif difficulty == 1:
                    run_time = 2
                else:
                    run_time = 3
                draw_small_title(screen, difficulty, ending)
                toggle_button = ToggleButton(screen, (screen.get_width() - 110, 10), (100, 30))
                human.game_turn = first_or_second
                historical_x, historical_y = 0, 4
                children = []
                while not game_is_over(board.grid_states):
                    if game_is_tie(board.grid_states):
                        human.game_turn = 2
                        break
                    if human.game_turn == 0:
                        reset = man_input(board, human, screen, bg_color, ending, toggle_button, difficulty)
                        if reset:
                            break
                        historical_x = human.x
                        historical_y = human.y
                    elif human.game_turn == 1:
                        current_node = ai_reset(board, historical_x, historical_y, children, human.game_turn)
                        current_node = monte_carlo_tree_search(current_node, run_time, ending)
                        human.x = current_node.get_state().current_x
                        human.y = current_node.get_state().current_y
                        board.win = round(current_node.winning_times / current_node.visit_times * 100, 2)
                        board.lost = round(current_node.losing_times / current_node.visit_times * 100, 2)
                        if ending != 1:
                            board.win, board.lost = board.lost, board.win
                        board.tie = round(100 - board.win - board.lost, 2)
                        board.board_states[human.x][human.y] = human.game_turn + 1
                        board.update_blocks()
                        children = current_node.children
                    else:
                        break
                    update_board_state(board, human)
                    update_screen(screen, bg_color, board, ending, True, toggle_button, difficulty)
            if not reset:
                update_screen(screen, bg_color, board, ending, False, toggle_button, difficulty)
                draw_tips(screen, "按ESC键返回主菜单", True)
                if human.game_turn == 1:
                    draw_msg(screen, "圈赢了")
                elif human.game_turn == 0:
                    draw_msg(screen, "叉赢了")
                else:
                    draw_msg(screen, "平局")

                again_button = Reset(screen, 1, "再来一局")
                return_button = Reset(screen, 2, "返回主菜单")
                again_button.draw_button()
                return_button.draw_button()

                pygame.display.flip()

                loop = True
                while loop:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            sys.exit()
                        elif event.type == pygame.MOUSEBUTTONUP:
                            if event.button == 1:
                                mouse_pos = pygame.mouse.get_pos()
                                if again_button.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                                    loop = False
                                elif return_button.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                                    loop = False
                                    reset = True


if __name__ == '__main__':
    images = load_image()
    CIRCLE_NOW_PNG = images[0]
    CIRCLE_PNG = images[1]
    CROSS_NOW_PNG = images[2]
    CROSS_PNG = images[3]
    CIRCLE_DARK_PNG = images[4]
    CROSS_DARK_PNG = images[5]
    NEXT_PNG = images[6]
    LAST_PNG = images[7]
    run_game()
