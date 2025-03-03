import pygame
import tkinter as tk
from tkinter import messagebox
import threading

# --- Constants ---
WIDTH, HEIGHT = 620, 435  # Window size
BOARD_SIZE = 600  # Board size
SQUARE_SIZE = BOARD_SIZE // 11  # Size of squares (8 rows and columns)

LIGHT_BROWN = (240, 217, 181)
DARK_BROWN = (181, 136, 99)
BACKGROUND_COLOR = (230, 230, 230)
BUTTON_COLOR = (255, 0, 0)  # Red button color
BUTTON_TEXT_COLOR = (255, 255, 255)  # Button text color

# --- Image Paths (Replace with your actual paths) ---
WHITE_ROOK_IMG_PATH = r"C:\Users\Admin\Desktop\white\r.png"
WHITE_KNIGHT_IMG_PATH = r"C:\Users\Admin\Desktop\white\n.png"
WHITE_BISHOP_IMG_PATH = r"C:\Users\Admin\Desktop\white\b.png"
WHITE_QUEEN_IMG_PATH = r"C:\Users\Admin\Desktop\white\q.png"
WHITE_KING_IMG_PATH = r"C:\Users\Admin\Desktop\white\k.png"
WHITE_PAWN_IMG_PATH = r"C:\Users\Admin\Desktop\white\p.png"
BLACK_ROOK_IMG_PATH = r"C:\Users\Admin\Desktop\Black\r (1).png"
BLACK_KNIGHT_IMG_PATH = r"C:\Users\Admin\Desktop\Black\n (1).png"
BLACK_BISHOP_IMG_PATH = r"C:\Users\Admin\Desktop\Black\b (1).png"
BLACK_QUEEN_IMG_PATH = r"C:\Users\Admin\Desktop\Black\q (1).png"
BLACK_KING_IMG_PATH = r"C:\Users\Admin\Desktop\Black\k (1).png"
BLACK_PAWN_IMG_PATH = r"C:\Users\Admin\Desktop\Black\p (1).png"

# --- Sound Path ---
MOVE_SOUND_PATH = r"C:\Users\Admin\Downloads\assets_sounds_capture.wav"  # Add sound path

# --- Helper Functions ---
def load_and_scale_image(path):
    image = pygame.image.load(path)
    return pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))

def draw_online_indicator(screen, current_player):
    radius = 5  # Small radius
    color = (255, 0, 0)  # Red color
    position = (WIDTH - 160, 15)

    # Draw the circle
    pygame.draw.circle(screen, color, position, radius)

    # Set up the font
    font = pygame.font.SysFont("Script", 18)
    online_text = font.render("Online", True, (0, 0, 0))  # "Online" text in black
    screen.blit(online_text, (WIDTH - 140, 9))  # Position the "Online" text

def render_scores(screen, scores):
    font = pygame.font.SysFont("Script", 23)
    white_score_text = font.render(f"White Score: {scores['white']}", True, (0, 0, 0))
    black_score_text = font.render(f"Black Score: {scores['black']}", True, (0, 0, 0))

    screen.blit(white_score_text, (WIDTH - 160, 50))
    screen.blit(black_score_text, (WIDTH - 160, 100))

def render_surrender_buttons(screen, surrender_callback, current_player):
    button_width, button_height = 140, 50
    font = pygame.font.SysFont("Script", 21)

    # Coordinates for surrender buttons in the empty space on the right
    white_surrender_pos = (WIDTH - 170, (HEIGHT // 2) - button_height - 10)  # Above
    black_surrender_pos = (WIDTH - 170, (HEIGHT // 2) + 10)  # Below

    # Draw a shadow for the white surrender button
    pygame.draw.rect(screen, (50, 50, 50),
                     (white_surrender_pos[0] + 5, white_surrender_pos[1] + 5, button_width, button_height), border_radius=10)

    # Draw the white surrender button
    pygame.draw.rect(screen, BUTTON_COLOR,
                     (white_surrender_pos[0], white_surrender_pos[1], button_width, button_height), border_radius=10)
    white_surrender_text = font.render('Surrender (White)', True, BUTTON_TEXT_COLOR)
    screen.blit(white_surrender_text, (white_surrender_pos[0] + 10, white_surrender_pos[1] + 10))

    # Draw a shadow for the black surrender button
    pygame.draw.rect(screen, (50, 50, 50),
                     (black_surrender_pos[0] + 5, black_surrender_pos[1] + 5, button_width, button_height), border_radius=10)

    # Draw the black surrender button
    pygame.draw.rect(screen, BUTTON_COLOR,
                     (black_surrender_pos[0], black_surrender_pos[1], button_width, button_height), border_radius=10)
    black_surrender_text = font.render('Surrender (Black)', True, BUTTON_TEXT_COLOR)
    screen.blit(black_surrender_text, (black_surrender_pos[0] + 10, black_surrender_pos[1] + 10))

    # Check for clicks on the surrender buttons
    mouse_position = pygame.mouse.get_pos()
    mouse_buttons = pygame.mouse.get_pressed()
    if mouse_buttons[0]:  # Left mouse button
        if (white_surrender_pos[0] <= mouse_position[0] <= white_surrender_pos[0] + button_width and
                white_surrender_pos[1] <= mouse_position[1] <= white_surrender_pos[1] + button_height):
            surrender_callback('w')  # White surrenders
        elif (black_surrender_pos[0] <= mouse_position[0] <= black_surrender_pos[0] + button_width and
              black_surrender_pos[1] <= mouse_position[1] <= black_surrender_pos[1] + button_height):
            surrender_callback('b')  # Black surrenders

    # Show current player text below buttons
    current_player_text = "Current Player: " + ("White" if current_player == "white" else "Black")
    current_player_rendered = font.render(current_player_text, True, (0, 0, 0))
    # Position it below the buttons
    screen.blit(current_player_rendered, (white_surrender_pos[0], black_surrender_pos[1] + 95))

# --- Initialize Pygame ---
pygame.init()
pygame.mixer.init()  # Initialize the sound module

# --- Load Sounds ---
move_sound = pygame.mixer.Sound(MOVE_SOUND_PATH)  # Load move sound

# --- Load and Scale Images ---
piece_images = {
    "wR": load_and_scale_image(WHITE_ROOK_IMG_PATH),
    "wN": load_and_scale_image(WHITE_KNIGHT_IMG_PATH),
    "wB": load_and_scale_image(WHITE_BISHOP_IMG_PATH),
    "wQ": load_and_scale_image(WHITE_QUEEN_IMG_PATH),
    "wK": load_and_scale_image(WHITE_KING_IMG_PATH),
    "wP": load_and_scale_image(WHITE_PAWN_IMG_PATH),
    "bR": load_and_scale_image(BLACK_ROOK_IMG_PATH),
    "bN": load_and_scale_image(BLACK_KNIGHT_IMG_PATH),
    "bB": load_and_scale_image(BLACK_BISHOP_IMG_PATH),
    "bQ": load_and_scale_image(BLACK_QUEEN_IMG_PATH),
    "bK": load_and_scale_image(BLACK_KING_IMG_PATH),
    "bP": load_and_scale_image(BLACK_PAWN_IMG_PATH)
}

# --- Piece values ---
piece_values = {
    "wP": 1, "wR": 5, "wN": 3, "wB": 3, "wQ": 9, "wK": 0,
    "bP": 1, "bR": 5, "bN": 3, "bB": 3, "bQ": 9, "bK": 0
}

def create_board():
    return [
        ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
        ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
        ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
    ]

def is_valid_move(board, start_row, start_col, end_row, end_col, current_player):
    if (start_row, start_col) == (end_row, end_col):
        return False
    piece = board[start_row][start_col]
    # Check if the piece belongs to the current player
    if (current_player == "white" and piece and piece.startswith("w")) or \
            (current_player == "black" and piece and piece.startswith("b")):
        return True
    return False

def implement_move(board, start_row, start_col, end_row, end_col, scores):
    piece_taken = board[end_row][end_col]
    if piece_taken:
        # Increase player's score based on the piece's value
        if piece_taken.startswith("w"):
            scores['black'] += piece_values[piece_taken]
        else:
            scores['white'] += piece_values[piece_taken]

    board[end_row][end_col] = board[start_row][start_col]
    board[start_row][start_col] = None
    move_sound.play()  # Play sound on move

def check_for_winner(board):
    white_king_alive = any("wK" in row for row in board)
    black_king_alive = any("bK" in row for row in board)

    if not white_king_alive:
        return 'black'
    elif not black_king_alive:
        return 'white'
    return None

def draw_board(screen, x_offset):
    for row in range(8):
        for col in range(8):
            x = col * SQUARE_SIZE + x_offset
            y = row * SQUARE_SIZE
            color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
            pygame.draw.rect(screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces(screen, board, x_offset):
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece:
                x = col * SQUARE_SIZE + x_offset
                y = row * SQUARE_SIZE
                screen.blit(piece_images[piece], (x, y))

def chess_game(board, surrender_callback):
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess play online")

    running = True
    selected_piece = None
    current_player = "white"  # Player starts with white
    winner = None

    # Variables for scores
    scores = {'white': 0, 'black': 0}

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    x, y = event.pos
                    clicked_col = x // SQUARE_SIZE
                    clicked_row = y // SQUARE_SIZE

                    if 0 <= clicked_col < 8 and 0 <= clicked_row < 8:  # Check for proper click
                        if selected_piece is None:  # If there is nothing selected to move
                            if board[clicked_row][clicked_col] is not None:  # Is there a piece on the square?
                                if (current_player == "white" and board[clicked_row][clicked_col].startswith("w")) or \
                                        (current_player == "black" and board[clicked_row][clicked_col].startswith("b")):
                                    selected_piece = (clicked_row, clicked_col)  # Set the click
                        else:  # Otherwise, there is a piece selected
                            start_row, start_col = selected_piece  # Set the start location
                            end_row, end_col = clicked_row, clicked_col  # Set the end location
                            if is_valid_move(board, start_row, start_col, end_row, end_col,
                                             current_player):  # Valid move?
                                implement_move(board, start_row, start_col, end_row, end_col, scores)  # Move the piece
                                selected_piece = None  # Deselect after move
                                current_player = "black" if current_player == "white" else "white"  # Change player

                                # Check for winner after each move
                                winner = check_for_winner(board)
                                if winner:
                                    messagebox.showinfo("Game Over", f"{winner.capitalize()} Wins!")
                                    running = False  # End the loop on win

                            else:
                                print("Invalid move!")
                                selected_piece = None  # Deselect

        # Drawing
        screen.fill(BACKGROUND_COLOR)
        draw_board(screen, 0)  # Draw left board
        draw_board(screen, BOARD_SIZE + 20)  # Draw right board with space in between
        draw_pieces(screen, board, 0)  # Draw left pieces

        # Draw online indicator
        draw_online_indicator(screen, current_player)

        render_scores(screen, scores)

        # Draw surrender buttons outside the boards
        render_surrender_buttons(screen, surrender_callback, current_player)

        pygame.display.flip()

    pygame.quit()

# --- GUI Class ---
class ChessGUI:
    def __init__(self, master):
        self.master = master
        master.title("Online Chess")
        master.configure(bg="#ADD8E6")

        self.server_address = tk.StringVar()
        self.server_address.set(" you api")

        self.font = ("Arial", 12)
        self.button_font = ("Arial", 12, "bold")
        self.label_color = "#000080"
        self.button_color = "#FF0000"  # Red button color
        self.button_active_color = "#FFFF00"

        self.server_label = tk.Label(master, text="Server Address:", font=self.font, bg="#ADD8E6", fg=self.label_color)
        self.server_entry = tk.Entry(master, textvariable=self.server_address, width=50, font=self.font)

        self.connect_button = tk.Button(master, text="Connect", command=self.connect_to_server,
                                         font=self.button_font, bg=self.button_color,
                                         activebackground=self.button_active_color)
        self.create_room_button = tk.Button(master, text="Create Room", command=self.create_room,
                                             font=self.button_font, bg=self.button_color,
                                             activebackground=self.button_active_color,
                                             state=tk.DISABLED)
        self.exit_button = tk.Button(master, text="Exit", command=self.exit_game, font=self.button_font,
                                     bg=self.button_color, activebackground=self.button_active_color)

        self.server_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.server_entry.grid(row=0, column=1, padx=10, pady=10, sticky="e")
        self.connect_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.create_room_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.exit_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    def connect_to_server(self):
        server_address = self.server_address.get()
        if not server_address:
            messagebox.showerror("Error", "Please enter a server address.")
            return
        messagebox.showinfo("Success", f"Connected to server: {server_address}")
        self.connect_button.config(state=tk.DISABLED)
        self.create_room_button.config(state=tk.NORMAL)

    def create_room(self):
        messagebox.showinfo("Success", "Room created.")
        threading.Thread(target=self.start_chess_game).start()

    def exit_game(self):
        if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
            self.master.destroy()
            pygame.quit()

    def start_chess_game(self):
        board = create_board()
        chess_game(board, self.declare_winner)

    def declare_winner(self, color):
        if color == 'w':
            winner_message = "Black Wins! White surrendered."
        else:
            winner_message = "White Wins! Black surrendered."
        messagebox.showinfo("Game Over", winner_message)
        pygame.quit()  # Here we close the game

# --- Main ---
if __name__ == "__main__":
    root = tk.Tk()
    my_gui = ChessGUI(root)

    # Start the Tkinter main loop
    root.mainloop()
