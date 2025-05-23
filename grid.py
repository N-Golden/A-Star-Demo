import pygame

class Cell: #hinh vuong 
    # Khởi tạo ô với vị trí (row, col), kích thước ô và tổng số hàng
    def __init__(self, row, col, width, total_rows, total_cols):
        self.row = row  # vi tri hang, cot: 0,1,2,3
        self.col = col 
        self.x = col * width # qui ra toa do tren truc Oxy
        self.y = row * width
        self.color = (255, 255, 255)  # Trắng mặc định
        self.neighbors = []
        self.width = width # chieu dai 1 o
        self.total_rows = total_rows
        self.total_cols = total_cols

        self.parent = None  

    # Trả về vị trí của ô
    def get_pos(self):
        return self.row, self.col

    # Kiểm tra ô đã xét chưa (màu đỏ)
    def is_closed(self):
        return self.color == (255, 0, 0)

    # Kiểm tra ô đang mở (màu xanh lá)
    def is_open(self):
        return self.color == (0, 255, 0)

    # Kiểm tra ô là chướng ngại vật (màu đen)
    def is_barrier(self):
        return self.color == (0, 0, 0)

    # Kiểm tra ô là điểm bắt đầu (màu cam)
    def is_start(self):
        return self.color == (255, 165, 0)

    # Kiểm tra ô là điểm kết thúc (màu xanh ngọc)
    def is_end(self):
        return self.color == (64, 224, 208)

    # Đặt ô về lại trạng thái trống (trắng)
    def reset(self):
        self.color = (255, 255, 255)

    # Gán ô là điểm bắt đầu
    def make_start(self):
        self.color = (255, 165, 0)

    # Gán ô là đã xét (màu đỏ)
    def make_closed(self):
        self.color = (255, 0, 0)

    # Gán ô là đang xét (màu xanh lá)
    def make_open(self):
        self.color = (0, 255, 0)

    # Gán ô là chướng ngại vật (màu đen)
    def make_barrier(self):
        self.color = (0, 0, 0)

    # Gán ô là điểm kết thúc (màu xanh ngọc)
    def make_end(self):
        self.color = (64, 224, 208)

    # Gán ô là một phần của đường đi tìm được (màu tím)
    def make_path(self):
        self.color = (128, 0, 128)

    # Cập nhật danh sách các ô kề không bị chắn
    def update_neighbors(self, grid):
        self.neighbors = []
        # Kiểm tra ô bên dưới
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])
        # Kiểm tra ô bên trên
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])
        # Kiểm tra ô bên phải
        if self.col < self.total_cols - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])
        # Kiểm tra ô bên trái
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

class Grid:
    # Khởi tạo lưới gồm rows x cols ô, mỗi ô có kích thước width // rows
    def __init__(self, rows, cols, width):
        self.rows = rows
        self.cols = cols
        self.grid = []
        self.cell_width = width
        self.create_grid()

    # Tạo lưới gồm các ô Cell
    def create_grid(self):
        self.grid = []
        for i in range(self.rows):
            self.grid.append([])
            for j in range(self.cols):
                self.grid[i].append(Cell(i, j, self.cell_width, self.rows, self.cols))

    # draw gird into WIN
    def draw(self, win):
        for row in self.grid:
            for cell in row:
                pygame.draw.rect(win, cell.color, (cell.x, cell.y, cell.width, cell.width))
                pygame.draw.rect(win, (128, 128, 128), (cell.x, cell.y, cell.width, cell.width), 1)

    # Cập nhật neighbor (hàng xóm) cho tất cả các ô
    def update_all_neighbors(self):
        for row in self.grid:
            for cell in row:
                cell.update_neighbors(self.grid)
