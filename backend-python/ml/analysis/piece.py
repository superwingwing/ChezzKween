# ==========================================
# piece.py
#
# Piece Analysis Module
#
# Thesis:
# Chess Playing Style Classification
#
# Responsible for
# • Piece Mobility
# • Piece Coordination
# • Hanging Pieces
#
# FINAL VERSION
# ==========================================

import chess


# ==========================================
# Piece Mobility
# ==========================================

def piece_mobility(
    board: chess.Board,
    square: chess.Square
):
    """
    Number of legal moves
    available for one piece.

    This is true mobility,
    not board mobility.
    """

    piece = board.piece_at(square)

    if piece is None:
        return 0

    total = 0

    for move in board.legal_moves:

        if move.from_square == square:

            total += 1

    return total


# ==========================================
# Average Mobility
# ==========================================

def average_mobility(
    board: chess.Board,
    color: chess.Color
):
    """
    Average mobility of all pieces.
    """

    total = 0
    pieces = 0

    for square, piece in board.piece_map().items():

        if piece.color != color:
            continue

        if piece.piece_type == chess.KING:
            continue

        total += piece_mobility(
            board,
            square
        )

        pieces += 1

    if pieces == 0:
        return 0

    return total / pieces


# ==========================================
# Piece Coordination
# ==========================================

def coordination_score(
    board: chess.Board,
    color: chess.Color
):
    """
    Counts friendly support.

    Every friendly piece defended
    by another friendly piece
    contributes to coordination.
    """

    score = 0

    for square, piece in board.piece_map().items():

        if piece.color != color:
            continue

        defenders = board.attackers(
            color,
            square
        )

        defenders = defenders - {square}

        if defenders:

            score += 1

    return score


# ==========================================
# Hanging Piece
# ==========================================

def is_hanging_piece(
    board: chess.Board,
    square: chess.Square
):
    """
    Hanging piece

    Attacked

    AND

    Not defended
    """

    piece = board.piece_at(square)

    if piece is None:
        return False

    enemy = not piece.color

    attacked = board.attackers(
        enemy,
        square
    )

    defended = board.attackers(
        piece.color,
        square
    )

    return (

        len(attacked) > 0

        and

        len(defended) == 0

    )


# ==========================================
# Count Hanging Pieces
# ==========================================

def hanging_pieces(
    board: chess.Board,
    color: chess.Color
):
    """
    Counts hanging pieces
    belonging to player.
    """

    total = 0

    for square, piece in board.piece_map().items():

        if piece.color != color:
            continue

        if is_hanging_piece(
            board,
            square
        ):

            total += 1

    return total


# ==========================================
# Protected Pieces
# ==========================================

def protected_pieces(
    board: chess.Board,
    color: chess.Color
):
    """
    Counts defended pieces.
    """

    total = 0

    for square, piece in board.piece_map().items():

        if piece.color != color:
            continue

        defenders = board.attackers(
            color,
            square
        )

        defenders = defenders - {square}

        if defenders:

            total += 1

    return total


# ==========================================
# Piece Activity
# ==========================================

def activity_score(
    board: chess.Board,
    color: chess.Color
):
    """
    Combines

    mobility

    +

    coordination

    into one metric.
    """

    mobility = average_mobility(
        board,
        color
    )

    coordination = coordination_score(
        board,
        color
    )

    return mobility + coordination


# ==========================================
# Testing
# ==========================================

if __name__ == "__main__":

    board = chess.Board()

    print(
        average_mobility(
            board,
            chess.WHITE
        )
    )

    print(
        coordination_score(
            board,
            chess.WHITE
        )
    )

    print(
        hanging_pieces(
            board,
            chess.WHITE
        )
    )

    # ==========================================
# Outpost Detection
# ==========================================

def is_outpost(
    board: chess.Board,
    square: chess.Square,
    color: chess.Color
):
    """
    Classical chess definition.

    An outpost is a square occupied by
    a knight or bishop that:

    1. Is protected by a friendly pawn.
    2. Cannot be attacked by an enemy pawn.
    3. Is located in enemy territory.
    """

    piece = board.piece_at(square)

    if piece is None:
        return False

    if piece.color != color:
        return False

    if piece.piece_type not in (
        chess.KNIGHT,
        chess.BISHOP
    ):
        return False

    file = chess.square_file(square)
    rank = chess.square_rank(square)

    # ----------------------------
    # Enemy territory
    # ----------------------------

    if color == chess.WHITE:

        if rank < 4:
            return False

    else:

        if rank > 3:
            return False

    # ----------------------------
    # Protected by friendly pawn
    # ----------------------------

    pawn_support = False

    if color == chess.WHITE:

        support_rank = rank - 1

    else:

        support_rank = rank + 1

    if 0 <= support_rank <= 7:

        for df in (-1, 1):

            f = file + df

            if 0 <= f <= 7:

                sq = chess.square(
                    f,
                    support_rank
                )

                p = board.piece_at(sq)

                if (
                    p is not None
                    and
                    p.color == color
                    and
                    p.piece_type == chess.PAWN
                ):

                    pawn_support = True

    if not pawn_support:
        return False

    # ----------------------------
    # Enemy pawn cannot attack
    # ----------------------------

    enemy = not color

    if color == chess.WHITE:

        attack_rank = rank + 1

    else:

        attack_rank = rank - 1

    if 0 <= attack_rank <= 7:

        for df in (-1, 1):

            f = file + df

            if 0 <= f <= 7:

                sq = chess.square(
                    f,
                    attack_rank
                )

                p = board.piece_at(sq)

                if (
                    p is not None
                    and
                    p.color == enemy
                    and
                    p.piece_type == chess.PAWN
                ):

                    return False

    return True


# ==========================================
# Count Outposts
# ==========================================

def outposts(
    board: chess.Board,
    color: chess.Color
):

    total = 0

    for square, piece in board.piece_map().items():

        if piece.color != color:
            continue

        if is_outpost(
            board,
            square,
            color
        ):

            total += 1

    return total


# ==========================================
# Knight Outposts
# ==========================================

def knight_outposts(
    board: chess.Board,
    color: chess.Color
):

    total = 0

    for square in board.pieces(
        chess.KNIGHT,
        color
    ):

        if is_outpost(
            board,
            square,
            color
        ):

            total += 1

    return total


# ==========================================
# Bishop Outposts
# ==========================================

def bishop_outposts(
    board: chess.Board,
    color: chess.Color
):

    total = 0

    for square in board.pieces(
        chess.BISHOP,
        color
    ):

        if is_outpost(
            board,
            square,
            color
        ):

            total += 1

    return total


# ==========================================
# Strong Squares
# ==========================================

def strong_squares(
    board: chess.Board,
    color: chess.Color
):
    """
    Number of occupied outpost squares.

    Used as a positional feature.
    """

    return outposts(
        board,
        color
    )


# ==========================================
# Positional Piece Score
# ==========================================

def positional_piece_score(
    board: chess.Board,
    color: chess.Color
):
    """
    Overall positional score for pieces.

    Formula:
        Activity
      + Coordination
      + Outposts
    """

    score = 0

    score += activity_score(
        board,
        color
    )

    score += coordination_score(
        board,
        color
    )

    score += outposts(
        board,
        color
    ) * 2

    return score

    # ==========================================
# Queen Attack Participation
# ==========================================

def queen_attack_participation(
    board: chess.Board,
    color: chess.Color
):
    """
    Counts queen attacks
    inside enemy territory.

    Used as an aggressive feature.
    """

    total = 0

    queens = board.pieces(
        chess.QUEEN,
        color
    )

    for queen in queens:

        attacks = board.attacks(
            queen
        )

        for square in attacks:

            rank = chess.square_rank(square)

            if color == chess.WHITE:

                if rank >= 4:

                    total += 1

            else:

                if rank <= 3:

                    total += 1

    return total


# ==========================================
# Rook Attack Participation
# ==========================================

def rook_attack_participation(
    board: chess.Board,
    color: chess.Color
):
    """
    Counts rook attacks
    inside enemy territory.
    """

    total = 0

    rooks = board.pieces(
        chess.ROOK,
        color
    )

    for rook in rooks:

        attacks = board.attacks(
            rook
        )

        for square in attacks:

            rank = chess.square_rank(
                square
            )

            if color == chess.WHITE:

                if rank >= 4:

                    total += 1

            else:

                if rank <= 3:

                    total += 1

    return total


# ==========================================
# Attacking Piece Concentration
# ==========================================

def attacking_piece_concentration(
    board: chess.Board,
    color: chess.Color
):
    """
    Counts how many attacking pieces
    are concentrated around the
    enemy king.

    Radius:
        1 square
    """

    enemy = not color

    king = board.king(enemy)

    if king is None:

        return 0

    zone = set()

    file = chess.square_file(king)
    rank = chess.square_rank(king)

    for df in (-1, 0, 1):

        for dr in (-1, 0, 1):

            f = file + df
            r = rank + dr

            if 0 <= f <= 7 and 0 <= r <= 7:

                zone.add(
                    chess.square(f, r)
                )

    total = 0

    for square, piece in board.piece_map().items():

        if piece.color != color:
            continue

        if piece.piece_type == chess.PAWN:
            continue

        attacks = board.attacks(square)

        if any(
            target in zone
            for target in attacks
        ):

            total += 1

    return total


# ==========================================
# Aggressive Piece Score
# ==========================================

def aggressive_piece_score(
    board: chess.Board,
    color: chess.Color
):
    """
    Overall aggressive activity
    of heavy pieces.

    Used for playing style
    classification.
    """

    score = 0

    score += queen_attack_participation(
        board,
        color
    )

    score += rook_attack_participation(
        board,
        color
    )

    score += attacking_piece_concentration(
        board,
        color
    )

    return score