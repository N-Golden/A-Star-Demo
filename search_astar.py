
import pygame
import math
from queue import PriorityQueue

def h(p1, p2):
    # Heuristic Manhattan
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt(pow(x1-x2, 2) + pow(y1-y2, 2))

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()
        yield False  # yield để chạy từng bước

def a_star_algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue() # queue cell will check
    close_set = set() # cell already checked
    open_set.put((0, count, start))

    g_score = {cell: float("inf") for row in grid.grid for cell in row}
    g_score[start] = 0

    f_score = {cell: float("inf") for row in grid.grid for cell in row}
    f_score[start] = h(start.get_pos(), end.get_pos())



    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        # choose item check
        current = open_set.get()[2]
        close_set.add(current)

        #end : from node end -> path
        if current == end:
            for cell in close_set:
                cell.make_closed()
            while current.parent != start:
                path = current.parent
                path.make_path()
                current = current.parent
            start.make_start()
            end.make_end()
            draw()
            yield True
            return
        
        #neighbor of item check
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1
            if temp_g_score < g_score[neighbor]:
                if neighbor not in close_set:
                    neighbor.make_open()
                    neighbor.parent = current
                    g_score[neighbor] = temp_g_score
                    
                    # push open[]
                    f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                    count +=1
                    open_set.put((f_score[neighbor], count, neighbor))

        yield False

    yield True
