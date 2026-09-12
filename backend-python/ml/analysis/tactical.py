import chess


PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 100
}


PIECE_NAMES = {
    chess.PAWN: "pawn",
    chess.KNIGHT: "knight",
    chess.BISHOP: "bishop",
    chess.ROOK: "rook",
    chess.QUEEN: "queen",
    chess.KING: "king"
}


# ==========================================================
# BASIC HELPERS
# ==========================================================

def piece_name(piece):
    if piece is None:
        return None

    return PIECE_NAMES.get(
        piece.piece_type,
        "piece"
    )


def piece_value(piece):
    if piece is None:
        return 0

    return PIECE_VALUES[piece.piece_type]


def square_name(square):
    return chess.square_name(square)


# ==========================================================
# TACTICAL CAPTURES
# ==========================================================

def find_tactical_captures(board, moves):

    results = []

    for move in moves:

        if not board.is_capture(move):
            continue

        attacker = board.piece_at(
            move.from_square
        )

        victim = board.piece_at(
            move.to_square
        )

        if attacker is None:
            continue

        # En passant
        if victim is None and board.is_en_passant(move):
            victim = chess.Piece(
                chess.PAWN,
                not attacker.color
            )

        if victim is None:
            continue

        attacker_value = piece_value(attacker)
        victim_value = piece_value(victim)

        # Keep your original definition:
        # captured value >= attacking piece value
        if victim_value >= attacker_value:

            results.append({

                "move": move.uci(),

                "from": square_name(
                    move.from_square
                ),

                "to": square_name(
                    move.to_square
                ),

                "attacker": piece_name(
                    attacker
                ),

                "attacker_value":
                    attacker_value,

                "victim": piece_name(
                    victim
                ),

                "victim_value":
                    victim_value,

                "material_gain":
                    victim_value - attacker_value,

                "side":
                    "white"
                    if attacker.color == chess.WHITE
                    else "black"
            })

    return results


# ==========================================================
# HANGING CAPTURES
# ==========================================================

def find_hanging_captures(board, moves):

    results = []

    for move in moves:

        if not board.is_capture(move):
            continue

        attacker = board.piece_at(
            move.from_square
        )

        victim = board.piece_at(
            move.to_square
        )

        if attacker is None:
            continue

        # En passant
        if victim is None and board.is_en_passant(move):
            victim = chess.Piece(
                chess.PAWN,
                not attacker.color
            )

        if victim is None:
            continue

        defenders = board.attackers(
            victim.color,
            move.to_square
        )

        if len(defenders) == 0:

            results.append({

                "move": move.uci(),

                "from": square_name(
                    move.from_square
                ),

                "to": square_name(
                    move.to_square
                ),

                "attacker": piece_name(
                    attacker
                ),

                "victim": piece_name(
                    victim
                ),

                "victim_value":
                    piece_value(victim),

                "side":
                    "white"
                    if attacker.color == chess.WHITE
                    else "black",

                "reason":
                    "captured_piece_is_undefended"
            })

    return results


# ==========================================================
# WINNING EXCHANGES
# ==========================================================

def find_winning_exchanges(board, moves):

    results = []

    for move in moves:

        if not board.is_capture(move):
            continue

        attacker = board.piece_at(
            move.from_square
        )

        victim = board.piece_at(
            move.to_square
        )

        if attacker is None or victim is None:
            continue

        attacker_value = piece_value(attacker)
        victim_value = piece_value(victim)

        if victim_value > attacker_value:

            results.append({

                "move": move.uci(),

                "from": square_name(
                    move.from_square
                ),

                "to": square_name(
                    move.to_square
                ),

                "attacker": piece_name(
                    attacker
                ),

                "attacker_value":
                    attacker_value,

                "victim": piece_name(
                    victim
                ),

                "victim_value":
                    victim_value,

                "material_gain":
                    victim_value - attacker_value,

                "side":
                    "white"
                    if attacker.color == chess.WHITE
                    else "black"
            })

    return results


# ==========================================================
# DISCOVERED CHECKS
# ==========================================================

def find_discovered_checks(board, moves):

    results = []

    for move in moves:

        if not board.is_legal(move):
            continue

        mover = board.piece_at(
            move.from_square
        )

        if mover is None:
            continue

        enemy = not mover.color

        # Check attackers BEFORE move
        enemy_king = board.king(enemy)

        if enemy_king is None:
            continue

        before_attackers = set(
            board.attackers(
                mover.color,
                enemy_king
            )
        )

        temp = board.copy()
        temp.push(move)

        if not temp.is_check():
            continue

        king = temp.king(enemy)

        if king is None:
            continue

        after_attackers = set(
            temp.attackers(
                mover.color,
                king
            )
        )

        # A discovered check should reveal another attacker.
        if len(after_attackers) >= 2:

            results.append({

                "move": move.uci(),

                "from": square_name(
                    move.from_square
                ),

                "to": square_name(
                    move.to_square
                ),

                "moving_piece":
                    piece_name(mover),

                "side":
                    "white"
                    if mover.color == chess.WHITE
                    else "black",

                "king_square":
                    square_name(king),

                "attackers_after":
                    [
                        square_name(s)
                        for s in after_attackers
                    ],

                "meaning":
                    "moving_piece_reveals_another_attack_on_the_king"
            })

    return results


# ==========================================================
# DOUBLE CHECKS
# ==========================================================

def find_double_checks(board, moves):
    results = []
    for move in moves:
        if not board.is_legal(move):
            continue
        mover = board.piece_at(
            move.from_square
        )
        if mover is None:
            continue
        enemy = not mover.color
        temp = board.copy()
        temp.push(move)
        if not temp.is_check():
            continue
        king = temp.king(enemy)
        if king is None:
            continue
        attackers = temp.attackers(
            mover.color,
            king
        )

        if len(attackers) >= 2:
            results.append({
                "move": move.uci(),
                "from": square_name(
                    move.from_square
                ),
                "to": square_name(
                    move.to_square
                ),
                "moving_piece":
                    piece_name(mover),

                "side":
                    "white"
                    if mover.color == chess.WHITE
                    else "black",
                "king_square":
                    square_name(king),

                "attackers":
                    [
                        square_name(s)
                        for s in attackers
                    ],

                "meaning":
                    "the_king_is_attacked_by_two_pieces_or_lines"
            })

    return results


# ==========================================================
# MATERIAL WINNING COMBINATIONS
# ==========================================================

def find_material_winning_combinations(
    board,
    moves
):

    results = []

    for move in moves:

        if not board.is_capture(move):
            continue

        attacker = board.piece_at(
            move.from_square
        )

        victim = board.piece_at(
            move.to_square
        )

        if attacker is None or victim is None:
            continue

        attacker_value = piece_value(attacker)
        victim_value = piece_value(victim)

        gain = (
            victim_value
            -
            attacker_value
        )

        if gain >= 3:

            results.append({

                "move": move.uci(),

                "from": square_name(
                    move.from_square
                ),

                "to": square_name(
                    move.to_square
                ),

                "attacker":
                    piece_name(attacker),

                "attacker_value":
                    attacker_value,

                "victim":
                    piece_name(victim),

                "victim_value":
                    victim_value,

                "material_gain":
                    gain,

                "side":
                    "white"
                    if attacker.color == chess.WHITE
                    else "black"
            })

    return results


# ==========================================================
# TACTICAL SUMMARY
# ==========================================================

def tactical_summary(board, moves):

    tactical_captures = find_tactical_captures(
        board,
        moves
    )

    hanging_captures = find_hanging_captures(
        board,
        moves
    )

    winning_exchanges = find_winning_exchanges(
        board,
        moves
    )

    discovered_checks = find_discovered_checks(
        board,
        moves
    )

    double_checks = find_double_checks(
        board,
        moves
    )

    material_combinations = (
        find_material_winning_combinations(
            board,
            moves
        )
    )

    return {

        # ==================================================
        # EXISTING COUNTS
        # Keep these so your other code still works.
        # ==================================================

        "tactical_captures":
            len(tactical_captures),

        "hanging_captures":
            len(hanging_captures),

        "winning_exchanges":
            len(winning_exchanges),

        "discovered_checks":
            len(discovered_checks),

        "double_checks":
            len(double_checks),

        "material_winning_combinations":
            len(material_combinations),

        # ==================================================
        # NEW DETAILED INFORMATION
        # ==================================================

        "tactical_capture_moves":
            tactical_captures,

        "hanging_capture_moves":
            hanging_captures,

        "winning_exchange_moves":
            winning_exchanges,

        "discovered_check_moves":
            discovered_checks,

        "double_check_moves":
            double_checks,

        "material_winning_moves":
            material_combinations
    }


# ==========================================================
# COACHING TACTICAL ANALYSIS
# ==========================================================

def analyze_tactical(board, moves):

    summary = tactical_summary(
        board,
        moves
    )

    # Only numeric features should be included
    # in the tactical score.
    score = (
        summary["tactical_captures"]
        +
        summary["hanging_captures"]
        +
        summary["winning_exchanges"]
        +
        summary["discovered_checks"]
        +
        summary["double_checks"]
        +
        summary["material_winning_combinations"]
    )

    return {

        **summary,

        "score":
            score

    }