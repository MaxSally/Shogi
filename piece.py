from enum import IntEnum


class PieceType(IntEnum):
    EMPTY = 0
    PAWN = 1
    LANCE = 2
    KNIGHT = 3
    SILVER = 4
    GOLD = 5
    BISHOP = 6
    ROOK = 7
    KING = 8
    PROMOTED_PAWN = 9
    PROMOTED_LANCE = 10
    PROMOTED_KNIGHT = 11
    PROMOTED_SILVER = 12
    PROMOTED_BISHOP = 13
    PROMOTED_ROOK = 14


class Piece:
    def __init__(self, piece_type, player):
        self.piece_type = piece_type
        self.player = player

    def __str__(self):
        if self.piece_type == PieceType.EMPTY:
            return "  "
        elif self.player == 1:
            return self.piece_type.name[0] + " "
        else:
            return " " + self.piece_type.name[0]
