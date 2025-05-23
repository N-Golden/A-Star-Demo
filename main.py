#%%
import pygame
from grid import Grid
from search_astar import a_star_algorithm

CELL_WIDTH = 30
ROWS = 20
COLS = 30

def draw(win, grid):
    grid.draw(win)
    pygame.display.update()

def get_clicked_pos(pos, width):
    x, y = pos
    col = x//width
    row = y//width
    return row, col

def main(win):
    start = None
    end = None
    run = True
    started = False
    algorithm_generator = None

    undo_stack = []  # Lưu lại các hành động để Undo

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue  # Không cho chỉnh sửa khi đang chạy thuật toán
            
            cell = None
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, CELL_WIDTH)
                cell = grid.grid[row][col]

                if event.button == 1:  # Click trái để thêm/xóa barrier
                    if cell.is_start() or cell.is_end():
                        continue
                    if not cell.is_barrier():
                        undo_stack.append((row, col, cell.color))
                        cell.make_barrier()
                    else:
                        undo_stack.append((row, col, cell.color))
                        cell.reset()

                elif event.button == 3:  # Click phải
                    if cell.is_start(): # Nếu click vào ô Start → xóa Start
                        undo_stack.append(('start', start))
                        start.reset()
                        start = None

                        for row in grid.grid: # Xóa các ô đã duyệt, open list, đường đi (reset tất cả trừ barrier, start, end)
                            for c in row:
                                if not (c.is_barrier() or c.is_end() or c.is_start()):
                                    c.reset()

                    elif cell.is_end(): # Nếu click vào ô End → xóa End
                        undo_stack.append(('end', end))
                        end.reset()
                        end = None
                        for row in grid.grid: # Xóa các ô đã duyệt, open list, đường đi
                            for c in row:
                                if not (c.is_barrier() or c.is_end() or c.is_start()):
                                    c.reset()

                    elif start is None and not cell.is_end() and not cell.is_barrier():  # Nếu chưa có Start và ô không phải End hoặc barrier → đặt Start
                        undo_stack.append(('start', start))
                        start = cell
                        start.make_start()

                    elif end is None and not cell.is_start() and not cell.is_barrier(): # Nếu chưa có End và ô không phải Start hoặc barrier → đặt End
                        undo_stack.append(('end', end))
                        end = cell
                        end.make_end()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_u:  # Undo
                    if undo_stack:
                        last = undo_stack.pop() # Lấy hành động cuối cùng ra khỏi stack
                        if last[0] == 'start':
                            if start:
                                start.reset() # Xóa trạng thái Start hiện tại
                            start = last[1] # Quay lại Start cũ (nếu có)
                            if start:
                                start.make_start() # Đánh dấu lại Start cũ
                        elif last[0] == 'end':
                            if end:
                                end.reset() # Xóa trạng thái End hiện tại
                            end = last[1] # Quay lại End cũ (nếu có)
                            if end:
                                end.make_end() # Đánh dấu lại End cũ
                        else:
                            r, c, prev_color = last # Lấy thông tin ô đã thay đổi
                            cell = grid.grid[r][c]
                            cell.color = prev_color # Quay về màu trước đó

                if event.key == pygame.K_c: # Nhấn C để xóa toàn bộ lưới, reset Start, End và undo_stack
                    for row in grid.grid:
                        for cell in row:
                            cell.reset()
                    start = None
                    end = None
                    undo_stack.clear()

                if event.key == pygame.K_SPACE and start and end: # Khi nhấn phím Space và đã có ô Start, End
                    grid.update_all_neighbors()
                    started = True  # Đánh dấu trạng thái là đã bắt đầu chạy thuật toán
                    algorithm_generator = a_star_algorithm(lambda: draw(win, grid), grid, start, end)  # Tạo generator chạy thuật toán A* với hàm vẽ lại giao diện
                        
        if started:
            try:
                done = next(algorithm_generator)
                if done:
                    started = False
            except StopIteration:
                started = False

        if cell !=  None :
            pygame.draw.rect(win, cell.color, (cell.x, cell.y, cell.width, cell.width))
            pygame.draw.rect(win, (128, 128, 128), (cell.x, cell.y, cell.width, cell.width), 1)
            pygame.display.update()

    pygame.quit()

def initWIN():
    pygame.init()
    WIN = pygame.display.set_mode((CELL_WIDTH*COLS, CELL_WIDTH*ROWS))
    WIN.fill((255, 0, 0))
    font = pygame.font.SysFont(None, 18)
    text = font.render("Left click: Add/Remove barrier | Right click: Set Start/End | U: Undo  | C: Clear all | Space: Run A*", True, (0, 0, 0))
    # WIN.blit(text, (10, CELL_WIDTH + 10))
    pygame.display.set_caption("Maze Solver with A*")
    return WIN

if __name__ == "__main__":
    WIN = initWIN()

    grid = Grid(ROWS, COLS, CELL_WIDTH)
    grid.draw(WIN)
    pygame.display.update()

    main(WIN)

# %%
