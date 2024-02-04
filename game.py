import pygame
import sys
from piece import Piece, PieceType

CHESS_PIECE_IMAGE_DIR = "chess_piece_img/"


class ShogiGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 800))
        self.board = self.create_board()
        self.player1_captured_pieces = []
        self.player0_captured_pieces = []
        self.player1_turn = True
        self.last_clicked_button = None
        self.last_clicked_pos = None
        self.piece_images = {
            PieceType.EMPTY: pygame.image.load(CHESS_PIECE_IMAGE_DIR + "empty.png"),
            PieceType.PAWN: pygame.image.load(CHESS_PIECE_IMAGE_DIR + "pawn.png"),
            PieceType.LANCE: pygame.image.load(CHESS_PIECE_IMAGE_DIR + "lance.png"),
            PieceType.KNIGHT: pygame.image.load(CHESS_PIECE_IMAGE_DIR + "knight.png"),
            PieceType.SILVER: pygame.image.load(CHESS_PIECE_IMAGE_DIR + "silver_general.png"),
            PieceType.GOLD: pygame.image.load(CHESS_PIECE_IMAGE_DIR + "gold_general.png"),
            PieceType.BISHOP: pygame.image.load(CHESS_PIECE_IMAGE_DIR + "bishop.png"),
            PieceType.ROOK: pygame.image.load(CHESS_PIECE_IMAGE_DIR + "rook.png"),
            PieceType.KING: pygame.image.load(CHESS_PIECE_IMAGE_DIR + "reigning_king.png"),
            PieceType.PROMOTED_PAWN: pygame.image.load(CHESS_PIECE_IMAGE_DIR + "promoted_pawn.png"),
            PieceType.PROMOTED_LANCE: pygame.image.load(CHESS_PIECE_IMAGE_DIR + "promoted_lance.png"),
            PieceType.PROMOTED_KNIGHT: pygame.image.load(CHESS_PIECE_IMAGE_DIR + "promoted_knight.png"),
            PieceType.PROMOTED_SILVER: pygame.image.load(CHESS_PIECE_IMAGE_DIR + "promoted_silver_general.png"),
            PieceType.PROMOTED_BISHOP: pygame.image.load(CHESS_PIECE_IMAGE_DIR + "promoted_bishop.png"),
            PieceType.PROMOTED_ROOK: pygame.image.load(CHESS_PIECE_IMAGE_DIR + "promoted_rook.png")
        }

        self.move_vectors = {
            PieceType.EMPTY: [(0, 0)],
            PieceType.PAWN: [(0, 1)],
            PieceType.LANCE: [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8)],
            PieceType.KNIGHT: [(1, 2), (-1, 2)],
            PieceType.SILVER: [(0, 1), (1, 1), (-1, 1), (-1, -1), (1, -1)],
            PieceType.GOLD: [(0, 1), (1, 1), (-1, 1), (1, 0), (-1, 0)],
            PieceType.BISHOP: [(1, 1), (-1, -1), (-1, 1), (1, -1),
                               (2, 2), (-2, -2), (-2, 2), (2, -2),
                               (3, 3), (-3, -3), (-3, 3), (3, -3),
                               (4, 4), (-4, -4), (-4, 4), (4, -4),
                               (5, 5), (-5, -5), (-5, 5), (5, -5),
                               (6, 6), (-6, -6), (-6, 6), (6, -6),
                               (7, 7), (-7, -7), (-7, 7), (7, -7),
                               (8, 8), (-8, -8), (-8, 8), (8, -8)],
            PieceType.ROOK: [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0),
                             (-1, 0), (-2, 0), (-3, 0), (-4, 0), (-5, 0), (-6, 0), (-7, 0), (-8, 0),
                             (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8),
                             (0, -1), (0, -2), (0, -3), (0, -4), (0, -5), (0, -6), (0, -7), (0, -8)],
            PieceType.KING: [(1, 0), (1, 1), (1, -1), (0, 1), (0, -1), (-1, 0), (-1, 1), (-1, -1)],
            PieceType.PROMOTED_BISHOP: [(1, 1), (-1, -1), (-1, 1), (1, -1),
                                        (2, 2), (-2, -2), (-2, 2), (2, -2),
                                        (3, 3), (-3, -3), (-3, 3), (3, -3),
                                        (4, 4), (-4, -4), (-4, 4), (4, -4),
                                        (5, 5), (-5, -5), (-5, 5), (5, -5),
                                        (6, 6), (-6, -6), (-6, 6), (6, -6),
                                        (7, 7), (-7, -7), (-7, 7), (7, -7),
                                        (8, 8), (-8, -8), (-8, 8), (8, -8),
                                        (1, 0), (-1, 0), (0, -1), (0, 1)],
            PieceType.PROMOTED_ROOK: [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0),
                                      (-1, 0), (-2, 0), (-3, 0), (-4, 0), (-5, 0), (-6, 0), (-7, 0), (-8, 0),
                                      (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8),
                                      (0, -1), (0, -2), (0, -3), (0, -4), (0, -5), (0, -6), (0, -7), (0, -8),
                                      (-1, -1), (1, 1), (-1, 1), (1, -1)],
        }

    def create_board(self):
        board = [[Piece(PieceType.EMPTY, 0) for _ in range(9)] for _ in range(9)]
        for i in range(0, 9, 8):
            player = 0 if i == 0 else 1
            board[0][i] = Piece(PieceType.LANCE, player=player)
            board[1][i] = Piece(PieceType.KNIGHT, player=player)
            board[2][i] = Piece(PieceType.SILVER, player=player)
            board[3][i] = Piece(PieceType.GOLD, player=player)
            board[4][i] = Piece(PieceType.KING, player=player)
            board[5][i] = Piece(PieceType.GOLD, player=player)
            board[6][i] = Piece(PieceType.SILVER, player=player)
            board[7][i] = Piece(PieceType.KNIGHT, player=player)
            board[8][i] = Piece(PieceType.LANCE, player=player)
        for i in range(9):
            board[i][2] = Piece(PieceType.PAWN, player=0)
            board[i][6] = Piece(PieceType.PAWN, player=1)

        board[1][1] = Piece(PieceType.ROOK, player=0)
        board[7][7] = Piece(PieceType.ROOK, player=1)
        board[7][1] = Piece(PieceType.BISHOP, player=0)
        board[1][7] = Piece(PieceType.BISHOP, player=1)
        return board

    def draw_board(self):
        for i in range(9):
            for j in range(9):
                pygame.draw.rect(self.screen, (255, 255, 255), (i * 80, j * 80, 80, 80))
                pygame.draw.rect(self.screen, (0, 0, 0), (i * 80, j * 80, 80, 80), 1)
                image = self.piece_images[self.board[i][j].piece_type]
                image = pygame.transform.scale(image, (60, 60))
                self.screen.blit(image, (i * 80 + 10, j * 80 + 10))

    def is_valid_move(self, start, end, player):
        start_row, start_col = start
        end_row, end_col = end

        if start_row < 0 or start_row >= 9 or start_col < 0 or start_col >= 9:
            return False

        if end_row < 0 or end_row >= 9 or end_col < 0 or end_col >= 9:
            return False

        start_piece = self.board[start_row][start_col]
        move_vectors = None
        if 9 <= start_piece.piece_type <= 12:
            move_vectors = self.move_vectors[PieceType.GOLD]
        else:
            move_vectors = self.move_vectors[start_piece.piece_type]

        for row_move, col_move in move_vectors:
            if (end_row, end_col) == (start_row + row_move, start_col + (1 if player == 0 else -1) * col_move):
                return True

        return False

    # def display_captured_pieces(self, surface):
    #
    #     x = pygame.mouse.get_pos()[0]
    #     y = pygame.mouse.get_pos()[1]
    #     player_captured_pieces = self.player1_captured_pieces if self.player1_turn else self.player0_captured_pieces
    #
    #     box_width = 200
    #     box_height = 300
    #     box_x = x
    #     box_y = y - box_height - 10
    #
    #     pygame.draw.rect(surface, (255, 255, 255), pygame.Rect(box_x, box_y, box_width, box_height))
    #
    #     y = box_y + 20
    #
    #     # captured_pieces = player_captured_pieces
    #     # captured_pieces.sort(reverse=True)
    #
    #     x = box_x + 10
    #     for piece in player_captured_pieces:
    #         #for _ in range(count):
    #         image = self.piece_images[piece.piece_type]
    #         image = pygame.transform.scale(image, (60, 60))
    #         surface.blit(image, (x, y))
    #         x += 80
    #         # x = box_x + 10
    #         # y += 80

    def is_promotion_move(self, col, player, piece_type):
        if piece_type == PieceType.BISHOP or piece_type == PieceType.ROOK or piece_type == PieceType.SILVER \
                or piece_type == PieceType.KNIGHT or piece_type == PieceType.LANCE or piece_type == PieceType.PAWN:
            return (player == 0 and col >= 6) or (player == 1 and col <= 2)
        return False

    def promote_piece(self, piece_type):
        if piece_type == PieceType.ROOK:
            return PieceType.PROMOTED_ROOK
        elif piece_type == PieceType.BISHOP:
            return PieceType.PROMOTED_BISHOP
        elif piece_type == PieceType.SILVER:
            return PieceType.PROMOTED_SILVER
        elif piece_type == PieceType.KNIGHT:
            return PieceType.PROMOTED_KNIGHT
        elif piece_type == PieceType.LANCE:
            return PieceType.PROMOTED_LANCE
        elif piece_type == PieceType.PAWN:
            return PieceType.PROMOTED_PAWN
        else:
            return None

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x, y = pygame.mouse.get_pos()
                        i = x // 80
                        j = y // 80
                        if self.last_clicked_button is None:
                            self.last_clicked_button = self.board[i][j]
                            self.last_clicked_pos = (i, j)
                        else:
                            if self.is_valid_move(self.last_clicked_pos, (i, j),
                                                  self.player1_turn) and self.last_clicked_button.player == self.player1_turn:
                                prev_i, prev_j = self.last_clicked_pos
                                if self.player1_turn and self.last_clicked_button.piece_type is not PieceType.EMPTY:
                                    self.player1_captured_pieces.append(self.board[i][j])
                                elif not self.player1_turn and self.last_clicked_button.piece_type is not PieceType.EMPTY:
                                    self.player0_captured_pieces.append(self.board[i][j])
                                if self.is_promotion_move(j, self.player1_turn, self.last_clicked_button.piece_type):
                                    self.board[i][j] = Piece(self.promote_piece(self.last_clicked_button.piece_type), self.player1_turn)
                                else:
                                    self.board[i][j] = self.last_clicked_button
                                self.board[prev_i][prev_j] = Piece(PieceType.EMPTY, 0)
                                self.last_clicked_button = None
                                self.last_clicked_pos = None
                                self.player1_turn = not self.player1_turn
                            else:
                                self.last_clicked_button = None
                                self.last_clicked_pos = None
                self.screen.fill((255, 255, 255))
                self.draw_board()
                pygame.display.flip()
