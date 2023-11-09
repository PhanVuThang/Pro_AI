import pygame
import random
import time
from collections import deque

# Khởi tạo pygame
pygame.init()

# Kích thước ô vuông và kích thước mê cung
CELL_SIZE = 20
MAZE_WIDTH, MAZE_HEIGHT = 50, 25
MENU_WIDTH = 200

# Màu sắc
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)

# Tạo cửa sổ hiển thị
screen = pygame.display.set_mode(((MAZE_WIDTH * CELL_SIZE) + MENU_WIDTH, MAZE_HEIGHT * CELL_SIZE))
pygame.display.set_caption('Real-Time Maze Solver')

# Hàm để vẽ ô vuông
def draw_cell(x, y, color):
    pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))


# Định nghĩa các nút
button_generate = pygame.Rect((MAZE_WIDTH * CELL_SIZE) + 50, 50, 120, 60)
button_solve = pygame.Rect((MAZE_WIDTH * CELL_SIZE) + 50, 100, 100, 50)

# Hàm vẽ các nút
def draw_button(button, text):
    pygame.draw.rect(screen, GRAY, button)
    font = pygame.font.SysFont(None, 22)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=button.center)
    screen.blit(text_surface, text_rect)



# Vẽ menu
def draw_menu():
    screen.fill(WHITE, (MAZE_WIDTH * CELL_SIZE, 0, MENU_WIDTH, MAZE_HEIGHT * CELL_SIZE))
    draw_button(button_generate,'create a maze')
#    draw_button(button_solve, 'Solve BFS')
    pygame.display.flip()

maze_created = False

# Tạo mê cung ngẫu nhiên theo thời gian thực
def generate_maze(width, height):
    # Khởi tạo mê cung toàn bộ là đường đi
    maze = [[0 for _ in range(width)] for _ in range(height)]

    for y in range(height):
        for x in range(width):
            # Ngẫu nhiên chọn là tường (1) hoặc đường đi (0) dựa trên xác suất
            cell_type = 1 if random.random() < 0.17 else 0  # 20% cơ hội để tạo tường
            maze[y][x] = cell_type
            # Vẽ ô tương ứng
            color = WHITE if cell_type == 1 else BLACK
            draw_cell(x, y, color)
            pygame.display.flip()
            time.sleep(0.01)  # Thời gian ngừng ngắn để quan sát quá trình

    # Đảm bảo điểm bắt đầu và kết thúc là đường đi
    maze[0][0] = 0
    maze[-1][-1] = 0
    draw_cell(0, 0, RED)  # Vẽ điểm bắt đầu màu đỏ
    draw_cell(width - 1, height - 1, GREEN)  # Vẽ điểm kết thúc màu xanh
    pygame.display.flip()

    return maze

# Hàm để thực hiện một bước BFS
def bfs_step(maze, queue, prev, visited):
    if not queue:
        return True  # Trả về True nếu không còn gì để duyệt

    current = queue.popleft()
    x, y = current

    for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        next_x, next_y = x + direction[0], y + direction[1]
        if 0 <= next_x < len(maze[0]) and 0 <= next_y < len(maze) and maze[next_y][next_x] == 0 and (next_x, next_y) not in visited:
            queue.append((next_x, next_y))
            prev[(next_x, next_y)] = current
            visited.add((next_x, next_y))
            draw_cell(next_x, next_y, BLUE)
            pygame.display.flip()
            time.sleep(0.01)  # Thời gian ngừng ngắn để quan sát quá trình

    return False  # Trả về False nếu BFS vẫn đang diễn ra

def create_maze():
    maze = generate_maze(MAZE_WIDTH, MAZE_HEIGHT)
    maze_created = True  # Cập nhật biến khi mê cung được tạo
    start = (0, 0)
    end = (MAZE_WIDTH - 1, MAZE_HEIGHT - 1)
    queue = deque([start])
    prev = {start: None}
    visited = {start}
    solved = False
    draw_menu()

# Thêm nút và chức năng của nút vào main loop
def main():
    global MAZE_WIDTH, MAZE_HEIGHT, maze_created
    clock = pygame.time.Clock()
    maze = []
    start = (0, 0)
    end = (MAZE_WIDTH - 1, MAZE_HEIGHT - 1)

    queue = deque()
    prev = {}
    visited = set()

    running = True
    solved = False
    draw_menu()  # Vẽ menu ngay khi bắt đầu
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_generate.collidepoint(event.pos):
                    create_maze()
                elif button_solve.collidepoint(event.pos) and maze_created and not solved:
                    # Reset lại BFS mỗi khi nhấn nút
                    queue = deque([start])
                    prev = {start: None}
                    visited = {start}
                    solved = False

        # Tiến hành giải mê cung nếu đã được tạo và chưa giải
        if maze_created and not solved:
            # Gọi bfs_step liên tục trong khi có item trong hàng đợi
            if queue:
                bfs_step(maze, queue, prev, visited)
            else:
                # Khi hàng đợi rỗng và tìm ra giải pháp, vẽ lộ trình
                if not solved and end in visited:
                    current = end
                    while current != start:
                        current = prev[current]
                        x, y = current
                        draw_cell(x, y, YELLOW)
                        pygame.display.flip()
                        time.sleep(0.05)
                    solved = True
                else:
                    create_maze()

        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()