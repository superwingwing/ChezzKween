"""
move_explanation.py  -  ChessQueen "coach" explanations and recommendations.

How it works
------------
Nothing here is a canned, per-piece script.  Every sentence is produced from a
FACT that was verified on the real board with python-chess:

  * static exchange evaluation (SEE)  -> free pieces, good/bad trades, hanging pieces
  * forks, pins, discovered attacks, checks, mate-in-one threats
  * king safety (pawn cover, pressure around the king, castling rights)
  * development, centre control, outposts, open files, passed pawns,
    pawn-structure damage, piece activity, endgame king activity
  * the engine's principal variation (material actually won / lost in the line)

Stockfish's numbers are only used for the QUALITY label, the evaluation
context, and "which move is best".  The reasons come from the board.

Player style
------------
  Aggressive -> recommends the attacking move (check, capture, fork, pin,
                threat, pressure on the king) when it is close in strength
                to the engine's best move.
  Positional -> recommends the improving move (development, centre, king
                safety, structure, outposts, open files, passed pawns).

To make the style choice really work, pass MultiPV lines through the
optional `candidates` argument of explain_move():

    candidates=[{"move": "e2e4", "evaluation": 0.31},
                {"move": "g1f3", "evaluation": 0.25}, ...]

(`evaluation` is in pawns from WHITE's point of view, like everywhere else
in this module.)  Without candidates the engine's best move is used.

Public API (unchanged names):
    calculate_move_quality, quality_verdict, explain_move,
    add_quality_to_result, add_consequence_analysis,
    build_personalized_recommendation, describe_move_idea,
    recommendation_text, convert_uci_to_san, convert_pv_to_san,
    get_captured_piece, format_square_list, format_piece_list,
    format_file_list
"""

import chess


# ==========================================================
# CONSTANTS
# ==========================================================

PIECE_NAMES = {
    chess.PAWN: "pawn",
    chess.KNIGHT: "knight",
    chess.BISHOP: "bishop",
    chess.ROOK: "rook",
    chess.QUEEN: "queen",
    chess.KING: "king",
}

PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0,
}

BAD_QUALITIES = ("inaccuracy", "mistake", "blunder")

ATTACK_TAGS = {
    "mate", "check", "capture_win", "fork", "pin", "threat",
    "mate_threat", "king_attack", "discovered", "promotion",
}
POSITIONAL_TAGS = {
    "development", "center", "castle", "king_safety", "structure",
    "open_file", "outpost", "passed_pawn", "activity", "trade", "defense",
}

CENTER_SQUARES = [chess.D4, chess.E4, chess.D5, chess.E5]
STYLE_TOLERANCE = 0.40  # pawns: how much weaker than the best a style pick may be


# ==========================================================
# SMALL HELPERS
# ==========================================================

def _join(items):
    items = [i for i in items if i]
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return f"{items[0]} and {items[1]}"
    return ", ".join(items[:-1]) + f", and {items[-1]}"


def format_square_list(squares):
    return _join(list(squares))


def format_piece_list(pieces):
    return _join(list(pieces))


def format_file_list(files):
    return _join(list(files))


def _lc(text):
    """Lower-case the first letter so a sentence can follow a lead-in."""
    return text[:1].lower() + text[1:] if text else text


def _color_name(color):
    return "White" if color == chess.WHITE else "Black"


def _points(n):
    n = int(round(n))
    return f"{n} point" if n == 1 else f"{n} points"


def _fmt_eval(value):
    if value is None:
        return "?"
    if abs(value) >= 50:
        return "mate-level"
    return f"{value:+.1f}"


def _mover_value(value, color):
    if value is None:
        return None
    return value if color == chess.WHITE else -value


def describe_eval(value):
    """Plain-English description of a White-perspective evaluation in pawns."""
    if value is None:
        return ""
    a = abs(value)
    side = "White" if value > 0 else "Black"
    if a < 0.3:
        return f"the position is roughly equal ({_fmt_eval(value)})"
    if a < 0.8:
        return f"{side} is slightly better ({_fmt_eval(value)})"
    if a < 1.8:
        return f"{side} is clearly better ({_fmt_eval(value)})"
    if a < 4:
        return f"{side} is much better ({_fmt_eval(value)})"
    return f"{side} is winning ({_fmt_eval(value)})"


def get_captured_piece(board, move):
    captured = board.piece_at(move.to_square)
    if captured:
        return captured
    if board.is_en_passant(move):
        sq = chess.square(chess.square_file(move.to_square),
                          chess.square_rank(move.from_square))
        return board.piece_at(sq)
    return None


def material(board, color):
    return sum(PIECE_VALUES[p.piece_type]
               for p in board.piece_map().values() if p.color == color)


def _with_turn(board, color):
    """Copy of the board with `color` to move (used for 'what if it were their turn')."""
    b = board.copy(stack=False)
    b.turn = color
    b.ep_square = None
    return b


def _rel_rank(square, color):
    r = chess.square_rank(square)
    return r if color == chess.WHITE else 7 - r


def _home_minor_squares(color):
    return ({chess.B1, chess.G1, chess.C1, chess.F1} if color == chess.WHITE
            else {chess.B8, chess.G8, chess.C8, chess.F8})


def _undeveloped(board, color):
    home = _home_minor_squares(color)
    n = 0
    for sq in home:
        p = board.piece_at(sq)
        if p and p.color == color and p.piece_type in (chess.KNIGHT, chess.BISHOP):
            n += 1
    return n


def _phase(board):
    npm = sum(PIECE_VALUES[p.piece_type] for p in board.piece_map().values()
              if p.piece_type not in (chess.PAWN, chess.KING))
    if npm <= 20:
        return "endgame"
    if board.fullmove_number <= 12 and (
            _undeveloped(board, chess.WHITE) + _undeveloped(board, chess.BLACK)) >= 2:
        return "opening"
    return "middlegame"


# ==========================================================
# MOVE QUALITY
# ==========================================================

def calculate_move_quality(before, after, evaluation_before, evaluation_after):
    """Quality label from the evaluation drop (pawns, White perspective)."""
    if after.is_checkmate():
        return "best"
    if evaluation_before is None or evaluation_after is None:
        return None

    if before.turn == chess.WHITE:
        change = evaluation_after - evaluation_before
    else:
        change = evaluation_before - evaluation_after
    loss = max(0, -change)

    if loss < 0.3:
        return "best"
    if loss < 0.7:
        return "good"
    if loss < 1.5:
        return "inaccuracy"
    if loss < 3:
        return "mistake"
    return "blunder"


_QUALITY_PHRASES = {
    "best": "a strong move",
    "good": "a good move",
    "inaccuracy": "an inaccuracy",
    "mistake": "a mistake",
    "blunder": "a blunder",
}


def quality_stem(played_move, quality):
    """'Qxc6 is a blunder' (no punctuation); '' when the quality is unknown."""
    phrase = _QUALITY_PHRASES.get(quality)
    return f"{played_move} is {phrase}" if phrase else ""


def quality_verdict(played_move, quality, swing=None):
    """Opening sentence, e.g. 'Qxc6 is a blunder.'  (`swing` kept for compatibility.)"""
    stem = quality_stem(played_move, quality)
    return f"{stem}." if stem else ""


# ==========================================================
# STATIC EXCHANGE EVALUATION
# ==========================================================

def _attacker_rank(board, move):
    p = board.piece_at(move.from_square)
    if p is None:
        return 100
    return 100 if p.piece_type == chess.KING else PIECE_VALUES[p.piece_type]


def _best_capture_gain(board, square, depth=0):
    """
    Material the side to move can win by starting a capture sequence on
    `square` (least valuable attacker first, legal moves only, may stop any time).
    """
    if depth > 10:
        return 0
    caps = [m for m in board.legal_moves
            if m.to_square == square and board.is_capture(m)]
    if not caps:
        return 0
    m = min(caps, key=lambda x: _attacker_rank(board, x))
    victim = get_captured_piece(board, m)
    if victim is None or victim.piece_type == chess.KING:
        return 0
    value = PIECE_VALUES[victim.piece_type]
    board.push(m)
    try:
        gain = value - _best_capture_gain(board, square, depth + 1)
    finally:
        board.pop()
    return max(0, gain)


def _best_capture_san(board, square):
    caps = [m for m in board.legal_moves
            if m.to_square == square and board.is_capture(m)]
    if not caps:
        return None
    m = min(caps, key=lambda x: _attacker_rank(board, x))
    return board.san(m)


def threatened_pieces(board, victim_color):
    """
    Pieces of `victim_color` that the opponent can win material from
    if the opponent were to move.  Returns [(square, piece, gain)].
    """
    b = _with_turn(board, not victim_color)
    if not b.is_valid():
        return []
    result = []
    for sq, p in b.piece_map().items():
        if p.color != victim_color or p.piece_type == chess.KING:
            continue
        if not b.is_attacked_by(not victim_color, sq):
            continue
        gain = _best_capture_gain(b.copy(stack=False), sq)
        if gain > 0:
            result.append((sq, p, gain))
    result.sort(key=lambda t: (-t[2], -PIECE_VALUES[t[1].piece_type]))
    return result


def _mate_in_one(board):
    b = board.copy(stack=False)
    for m in list(b.legal_moves):
        san = b.san(m)
        b.push(m)
        mate = b.is_checkmate()
        b.pop()
        if mate:
            return san
    return None


# ==========================================================
# STRUCTURE / KING / CENTRE HELPERS
# ==========================================================

def _is_passed(board, square, color):
    f = chess.square_file(square)
    r = chess.square_rank(square)
    ranks = range(r + 1, 8) if color == chess.WHITE else range(0, r)
    for ff in (f - 1, f, f + 1):
        if not 0 <= ff <= 7:
            continue
        for rr in ranks:
            p = board.piece_at(chess.square(ff, rr))
            if p and p.piece_type == chess.PAWN and p.color != color:
                return False
    return True


def _pawn_flaws(board, color):
    counts = [0] * 8
    for sq in board.pieces(chess.PAWN, color):
        counts[chess.square_file(sq)] += 1
    flaws = set()
    for f in range(8):
        if counts[f] >= 2:
            flaws.add(("doubled", chr(97 + f)))
        if counts[f] >= 1:
            left = counts[f - 1] if f > 0 else 0
            right = counts[f + 1] if f < 7 else 0
            if left == 0 and right == 0:
                flaws.add(("isolated", chr(97 + f)))
    return flaws


def _king_zone_pressure(board, king_color):
    ksq = board.king(king_color)
    if ksq is None:
        return 0
    zone = set(board.attacks(ksq)) | {ksq}
    return sum(len(board.attackers(not king_color, s)) for s in zone)


def _pawn_shield(board, color):
    ksq = board.king(color)
    if ksq is None or _rel_rank(ksq, color) != 0:
        return None
    kf = chess.square_file(ksq)
    if kf in (3, 4):          # king still in the middle: no shield concept
        return None
    step = 1 if color == chess.WHITE else -1
    kr = chess.square_rank(ksq)
    count = 0
    for f in (kf - 1, kf, kf + 1):
        if not 0 <= f <= 7:
            continue
        for rr in (kr + step, kr + 2 * step):
            if 0 <= rr <= 7:
                p = board.piece_at(chess.square(f, rr))
                if p and p.piece_type == chess.PAWN and p.color == color:
                    count += 1
                    break
    return count


def _center_influence(board, color):
    res = {}
    for sq in CENTER_SQUARES:
        n = len(board.attackers(color, sq))
        p = board.piece_at(sq)
        if p and p.color == color and p.piece_type == chess.PAWN:
            n += 1
        res[sq] = n
    return res


def _is_outpost(board, square, color):
    if not 3 <= _rel_rank(square, color) <= 5:
        return False
    supported = any(
        (p := board.piece_at(s)) is not None and p.piece_type == chess.PAWN
        for s in board.attackers(color, square)
    )
    if not supported:
        return False
    f = chess.square_file(square)
    r = chess.square_rank(square)
    for ff in (f - 1, f + 1):
        if not 0 <= ff <= 7:
            continue
        for sq in board.pieces(chess.PAWN, not color):
            if chess.square_file(sq) == ff:
                rr = chess.square_rank(sq)
                if (color == chess.WHITE and rr > r) or (color == chess.BLACK and rr < r):
                    return False
    return True


def is_open_file(board, file_index):
    return not any(
        (p := board.piece_at(chess.square(file_index, r))) is not None
        and p.piece_type == chess.PAWN for r in range(8))


def is_semi_open_file(board, file_index, color):
    own = enemy = False
    for r in range(8):
        p = board.piece_at(chess.square(file_index, r))
        if p and p.piece_type == chess.PAWN:
            if p.color == color:
                own = True
            else:
                enemy = True
    return (not own) and enemy


def _attack_targets(after, to_sq, mover):
    """Enemy pieces the moved piece attacks that are loose or worth more than it."""
    piece = after.piece_at(to_sq)
    if piece is None:
        return []
    av = 100 if piece.piece_type == chess.KING else PIECE_VALUES[piece.piece_type]
    res = []
    for sq in after.attacks(to_sq):
        t = after.piece_at(sq)
        if not t or t.color == mover or t.piece_type == chess.KING:
            continue
        v = PIECE_VALUES[t.piece_type]
        defended = after.is_attacked_by(not mover, sq)
        if (not defended and v >= 1) or v > av:
            res.append((sq, t))
    return res


# ==========================================================
# CORE: ANALYSE ONE MOVE FROM THE BOARD
# ==========================================================

def analyze_move(before, after, move):
    """
    Return {"positives": [(prio, text, tag)], "negatives": [(prio, text, tag)],
            "tags": set}.  Every item is verified on the board.
    """
    pos, neg = [], []
    mover = before.turn
    enemy = not mover
    ename = _color_name(enemy)
    piece = before.piece_at(move.from_square)
    result = {"positives": pos, "negatives": neg, "tags": set()}
    if piece is None:
        return result

    san = before.san(move)
    to_sq = move.to_square
    to_name = chess.square_name(to_sq)
    from_name = chess.square_name(move.from_square)
    pname = PIECE_NAMES[piece.piece_type]
    phase = _phase(before)
    handled_sq = None

    # ---------- game-ending outcomes ----------
    if after.is_checkmate():
        pos.append((100, "It is checkmate: the king has no escape, no block and no capture.", "mate"))
        result["tags"] = {"mate", "check"}
        return result
    if after.is_stalemate():
        neg.append((95, "It leaves the opponent without a legal move while not in check, which is stalemate and a draw.", "king_safety"))

    # ---------- promotion ----------
    if move.promotion:
        pos.append((95, f"It promotes the pawn to a {PIECE_NAMES[move.promotion]} on {to_name}, creating a brand-new piece.", "promotion"))

    # ---------- castling ----------
    if before.is_castling(move):
        side = "kingside" if chess.square_file(to_sq) > chess.square_file(move.from_square) else "queenside"
        pos.append((55, f"It castles {side}: the king gets behind its pawns and the rook joins the game.", "castle"))
    elif piece.piece_type == chess.KING and before.has_castling_rights(mover) \
            and not after.has_castling_rights(mover) and phase != "endgame":
        neg.append((50, "It gives up the right to castle, leaving the king in the centre.", "king_safety"))

    # ---------- captures ----------
    if before.is_capture(move):
        cap = get_captured_piece(before, move)
        if cap is not None:
            cap_name = PIECE_NAMES[cap.piece_type]
            cap_val = PIECE_VALUES[cap.piece_type]
            regain = _best_capture_gain(after.copy(stack=False), to_sq)
            net = cap_val - regain
            if regain == 0 and cap_val >= 1:
                prio = 90 if cap_val >= 3 else 60
                pos.append((prio, f"It wins a free {cap_name} on {to_name}: nothing can legally take the {pname} back.", "capture_win"))
            elif net > 0:
                pos.append((75, f"It captures the {cap_name} on {to_name}; even after the recapture you finish {_points(net)} ahead.", "capture_win"))
            elif net == 0:
                pos.append((40, f"It trades the {pname} for the {cap_name} on {to_name}.", "trade"))
                diff = material(after, mover) - material(after, enemy)
                if diff >= 3:
                    pos.append((35, "Trading pieces while ahead in material makes the advantage easier to convert.", "trade"))
            else:
                handled_sq = to_sq
                neg.append((90, f"It captures the {cap_name} on {to_name}, but after the recapture you lose {_points(-net)} in the exchange.", "capture_win"))

    # ---------- check / discovered check ----------
    if after.is_check():
        replies = list(after.legal_moves)
        discovered = to_sq not in after.checkers()
        if discovered:
            pos.append((70, "It uncovers a discovered check: another piece now attacks the king while the moved piece does something else.", "discovered"))
        else:
            txt = f"It gives check, so {ename} must deal with the king before anything else."
            if len(replies) == 1:
                txt = f"It gives check and {ename} has only one legal reply, which makes the move very forcing."
            pos.append((60, txt, "check"))

    # ---------- forks / new threats ----------
    targets = _attack_targets(after, to_sq, mover)
    moved_piece_sq_hanging = any(
        sq == to_sq for sq, _, _ in threatened_pieces(after, mover))
    fork_squares = set()
    check_by_moved = after.is_check() and to_sq in after.checkers()
    if len(targets) + (1 if check_by_moved else 0) >= 2:
        desc = [f"the {PIECE_NAMES[t.piece_type]} on {chess.square_name(s)}" for s, t in targets]
        if check_by_moved:
            desc.insert(0, "the king")
        txt = f"It forks {_join(desc[:3])} with the {PIECE_NAMES[after.piece_at(to_sq).piece_type]}: it cannot save everything."
        if moved_piece_sq_hanging:
            txt = f"It attacks {_join(desc[:3])} at once, although the {pname} itself can be captured, so check the sequence."
            pos.append((50, txt, "threat"))
        else:
            pos.append((82, txt, "fork"))
        fork_squares = {s for s, _ in targets}

    before_threats = {sq for sq, _, _ in threatened_pieces(before, enemy)}
    after_threats = threatened_pieces(after, enemy) if not after.is_check() else []
    shown = 0
    for sq, p, gain in after_threats:
        if sq in before_threats or sq in fork_squares or shown >= 1:
            continue
        sqn = chess.square_name(sq)
        pn = PIECE_NAMES[p.piece_type]
        if sq in after.attacks(to_sq):
            pos.append((70 if gain >= 3 else 45,
                        f"It attacks the {pn} on {sqn} and threatens to win it.", "threat"))
        else:
            pos.append((68 if gain >= 3 else 45,
                        f"It uncovers an attack on the {pn} on {sqn}, threatening to win it.", "discovered"))
        shown += 1

    # ---------- pins ----------
    for sq, p in after.piece_map().items():
        if p.color != enemy or p.piece_type in (chess.KING, chess.PAWN):
            continue
        if after.is_pinned(enemy, sq) and not before.is_pinned(enemy, sq):
            pos.append((65, f"It pins the {PIECE_NAMES[p.piece_type]} on {chess.square_name(sq)} to the king, so that piece cannot move freely.", "pin"))
            break

    # ---------- mate threats / mate allowed ----------
    if not after.is_check():
        flipped = _with_turn(after, mover)
        if flipped.is_valid():
            mate_san = _mate_in_one(flipped)
            if mate_san:
                pos.append((85, f"It threatens {mate_san}, which would be checkmate.", "mate_threat"))
    if not after.is_stalemate():
        enemy_mate = _mate_in_one(after)
        if enemy_mate:
            neg.append((100, f"It allows {enemy_mate}, which is checkmate.", "king_safety"))

    # ---------- hanging pieces ----------
    before_hanging = {sq for sq, _, _ in threatened_pieces(before, mover)}
    after_hanging = threatened_pieces(after, mover)
    after_hanging_sqs = {sq for sq, _, _ in after_hanging}
    for sq, p, gain in after_hanging[:2]:
        if sq == handled_sq:
            continue
        sqn = chess.square_name(sq)
        pn = PIECE_NAMES[p.piece_type]
        cap_san = _best_capture_san(after, sq)
        how = f" with {cap_san}" if cap_san else ""
        prio = 95 if gain >= 3 else 65
        if sq == to_sq:
            neg.append((prio, f"The {pn} on {sqn} can be captured{how}, winning about {_points(gain)} of material.", "capture_win"))
        elif sq in before_hanging:
            neg.append((prio, f"It does not deal with the threat to the {pn} on {sqn}, so {cap_san or 'a capture'} wins {_points(gain)}.", "defense"))
        else:
            neg.append((prio, f"It leaves the {pn} on {sqn} loose: the opponent can win {_points(gain)}{how}.", "defense"))
    rescued = [sq for sq in before_hanging if sq not in after_hanging_sqs
               and (before.piece_at(sq) is not None)]
    for sq in rescued[:1]:
        p = before.piece_at(sq)
        if p and not before.is_capture(move):
            moved_it = (sq == move.from_square)
            pos.append((60, f"It {'moves' if moved_it else 'protects'} the {PIECE_NAMES[p.piece_type]} {'out of danger' if moved_it else 'that was under threat on ' + chess.square_name(sq)}.", "defense"))

    # ---------- king safety ----------
    ek_b, ek_a = _king_zone_pressure(before, enemy), _king_zone_pressure(after, enemy)
    if ek_a - ek_b >= 2 and not after.is_check():
        pos.append((50, f"It increases the pressure around {ename}'s king.", "king_attack"))
    ok_b, ok_a = _king_zone_pressure(before, mover), _king_zone_pressure(after, mover)
    if ok_a - ok_b >= 2:
        neg.append((55, "It lets the opponent's pieces target the squares around your own king.", "king_safety"))
    sh_b, sh_a = _pawn_shield(before, mover), _pawn_shield(after, mover)
    if sh_b is not None and sh_a is not None and sh_a < sh_b and piece.piece_type == chess.PAWN:
        neg.append((50, "It breaks up the pawn cover in front of your king.", "king_safety"))

    # ---------- development / opening principles ----------
    if piece.piece_type in (chess.KNIGHT, chess.BISHOP) and \
            move.from_square in _home_minor_squares(mover) and to_sq not in _home_minor_squares(mover):
        pos.append((45, f"It develops the {pname} to {to_name}, bringing another piece into the game.", "development"))
    if phase == "opening" and piece.piece_type == chess.QUEEN and before.fullmove_number <= 8:
        attackers = [after.piece_at(s) for s in after.attackers(enemy, to_sq)]
        lesser = [a for a in attackers if a and PIECE_VALUES[a.piece_type] < 9 and a.piece_type != chess.KING]
        if lesser:
            neg.append((50, f"Bringing the queen out this early lets the opponent gain time by attacking it with a {PIECE_NAMES[lesser[0].piece_type]}.", "development"))

    # ---------- centre ----------
    if piece.piece_type == chess.PAWN and to_sq in CENTER_SQUARES:
        pos.append((50, f"It plants a pawn on {to_name}, taking space in the centre.", "center"))
    else:
        ci_b, ci_a = _center_influence(before, mover), _center_influence(after, mover)
        gained = [chess.square_name(s) for s in CENTER_SQUARES if ci_a[s] > ci_b[s]]
        if gained and piece.piece_type != chess.PAWN:
            pos.append((35, f"It increases the influence over the centre ({_join(gained)}).", "center"))

    # ---------- piece placement ----------
    if piece.piece_type == chess.ROOK and chess.square_file(to_sq) != chess.square_file(move.from_square):
        fi = chess.square_file(to_sq)
        fname = chr(97 + fi)
        if is_open_file(after, fi):
            pos.append((50, f"It places the rook on the open {fname}-file, where nothing blocks it.", "open_file"))
        elif is_semi_open_file(after, fi, mover):
            pos.append((40, f"It places the rook on the semi-open {fname}-file, pressuring the enemy pawn there.", "open_file"))
    if piece.piece_type == chess.ROOK and _rel_rank(to_sq, mover) == 6 and _rel_rank(move.from_square, mover) != 6:
        pos.append((45, "It puts the rook on the seventh rank, where it eyes enemy pawns and restricts the king.", "activity"))
    if piece.piece_type == chess.KNIGHT and _is_outpost(after, to_sq, mover) and not _is_outpost(before, move.from_square, mover):
        pos.append((55, f"It places the knight on {to_name}, a protected outpost the enemy pawns can never attack.", "outpost"))
    if piece.piece_type != chess.PAWN and piece.piece_type != chess.KING and not move.promotion:
        m_before = len(before.attacks(move.from_square))
        m_after = len(after.attacks(to_sq))
        if m_after - m_before >= 3:
            pos.append((30, f"The {pname} becomes more active: it now controls {m_after} squares instead of {m_before}.", "activity"))
        elif m_before - m_after >= 3 and not any(t == "capture_win" for _, _, t in pos):
            neg.append((30, f"It makes the {pname} more passive: it controls {m_after} squares instead of {m_before}.", "activity"))

    # ---------- pawns ----------
    if piece.piece_type == chess.PAWN and not move.promotion:
        if _is_passed(after, to_sq, mover) and not _is_passed(before, move.from_square, mover):
            pos.append((60, f"It creates a passed pawn on {to_name}: no enemy pawn can stop it by capturing.", "passed_pawn"))
        elif _is_passed(after, to_sq, mover) and _rel_rank(to_sq, mover) >= 5:
            steps = 7 - _rel_rank(to_sq, mover)
            pos.append((65, f"It pushes the passed pawn to {to_name}, only {steps} step{'s' if steps != 1 else ''} from promotion.", "passed_pawn"))
    new_flaws = _pawn_flaws(after, mover) - _pawn_flaws(before, mover)
    for kind, f in sorted(new_flaws)[:1]:
        neg.append((35, f"It creates {'doubled' if kind == 'doubled' else 'an isolated'} pawn{'s' if kind == 'doubled' else ''} on the {f}-file, a long-term weakness.", "structure"))
    enemy_flaws = _pawn_flaws(after, enemy) - _pawn_flaws(before, enemy)
    for kind, f in sorted(enemy_flaws)[:1]:
        pos.append((40, f"It damages {ename}'s pawn structure, leaving {'doubled' if kind == 'doubled' else 'an isolated'} pawn{'s' if kind == 'doubled' else ''} on the {f}-file.", "structure"))

    # ---------- endgame king ----------
    if piece.piece_type == chess.KING and not before.is_castling(move) and phase == "endgame":
        def center_dist(sq):
            return max(abs(chess.square_file(sq) - 3.5), abs(chess.square_rank(sq) - 3.5))
        if center_dist(to_sq) < center_dist(move.from_square):
            pos.append((35, "It centralises the king, which is a real asset in the endgame.", "activity"))

    # de-duplicate
    seen = set()
    for lst in (pos, neg):
        lst[:] = [x for x in lst if not (x[1] in seen or seen.add(x[1]))]
    result["tags"] = {t for _, _, t in pos}
    return result


# ==========================================================
# ENGINE-PV MATERIAL STORY
# ==========================================================

def _normalise_move(board, candidate):
    if candidate is None:
        return None
    if isinstance(candidate, chess.Move):
        move = candidate
    else:
        raw = str(candidate).strip()
        try:
            move = chess.Move.from_uci(raw)
        except ValueError:
            try:
                move = board.parse_san(raw)
            except ValueError:
                return None
    return move if move in board.legal_moves else None


def _pv_moves(board, variation, limit=12):
    """Legal chess.Move list from a UCI/SAN/Move variation, stopping at first problem."""
    if not variation:
        return []
    if isinstance(variation, str):
        variation = variation.split()
    try:
        items = list(variation)
    except TypeError:
        return []
    temp = board.copy(stack=False)
    moves = []
    for item in items[:limit]:
        m = _normalise_move(temp, item)
        if m is None:
            break
        moves.append(m)
        temp.push(m)
    return moves


def _normalise_pv(board, variation):
    temp = board.copy(stack=False)
    out = []
    for m in _pv_moves(board, variation):
        out.append(temp.san(m))
        temp.push(m)
    return out


def _pv_story(after, moves, mover):
    """Follow the engine line after the played move and report the first capture sequence."""
    if not moves:
        return None
    board = after.copy(stack=False)
    start = material(board, mover) - material(board, not mover)
    sans, first, last = [], None, None
    for i, m in enumerate(moves[:10]):
        is_cap = board.is_capture(m)
        victim = get_captured_piece(board, m) if is_cap else None
        sq = m.to_square
        if board.is_en_passant(m):
            sq = chess.square(chess.square_file(m.to_square), chess.square_rank(m.from_square))
        capturer = board.turn
        sans.append(board.san(m))
        board.push(m)
        if is_cap:
            if first is None:
                first = {"capturer": capturer, "victim": victim, "square": sq, "san": sans[-1]}
            last = i
        elif first is not None:
            break
        if board.is_game_over():
            break
    if first is None or last is None:
        return None
    # material after the capture sequence
    b = after.copy(stack=False)
    for m in moves[:last + 1]:
        b.push(m)
    net = (material(b, mover) - material(b, not mover)) - start
    return {"line": sans[:last + 1], "net": net, "first": first}


def _story_sentence(story, mover):
    if not story:
        return None
    net, first, line = story["net"], story["first"], " ".join(story["line"])
    enemy = not mover
    victim = first["victim"]
    vname = PIECE_NAMES[victim.piece_type] if victim else "piece"
    sqn = chess.square_name(first["square"])
    if first["capturer"] == enemy and net <= -1:
        return (f"The engine's line ({line}) shows {_color_name(enemy)} winning your {vname} on {sqn} "
                f"and finishing {_points(-net)} ahead after the exchanges.")
    if first["capturer"] == mover and net >= 1:
        return f"The engine's line ({line}) shows you finishing {_points(net)} ahead after the exchanges."
    return None


def _story_reason(story, mover, bad):
    """(sentence, points) describing the engine line, or None if it proves nothing."""
    if not story:
        return None
    net, first = story["net"], story["first"]
    line = " ".join(story["line"])
    enemy = not mover
    victim = first["victim"]
    vname = PIECE_NAMES[victim.piece_type] if victim else "piece"
    sqn = chess.square_name(first["square"])
    if bad and first["capturer"] == enemy and net <= -1:
        return (f"In the engine's line ({line}), {_color_name(enemy)} wins your {vname} "
                f"on {sqn} and you end up {_points(-net)} down.", -net)
    if not bad and first["capturer"] == mover and net >= 1:
        return (f"In the engine's line ({line}), you win the opponent's {vname} "
                f"on {sqn} and come out {_points(net)} ahead.", net)
    return None


# ==========================================================
# ANALYSIS-PAYLOAD READERS
# ==========================================================

def _analysis_value(analysis):
    if not isinstance(analysis, dict):
        return None
    for key in ("evaluation", "eval", "score", "score_cp", "centipawns"):
        value = analysis.get(key)
        if isinstance(value, dict):
            value = value.get("value", value.get("score"))
        try:
            number = float(value)
        except (TypeError, ValueError):
            continue
        if number != number or abs(number) == float("inf"):
            continue
        if key in ("score_cp", "centipawns"):
            number /= 100.0
        return number
    return None


def _analysis_variation(analysis):
    if not isinstance(analysis, dict):
        return None
    for key in ("pv", "principal_variation", "variation", "line", "moves"):
        value = analysis.get(key)
        if value:
            return value
    return None


def _style_name(player_style):
    if player_style is None:
        return None
    if isinstance(player_style, dict):
        try:
            a = float(player_style.get("Aggressive", 50.0))
            p = float(player_style.get("Positional", 50.0))
        except (TypeError, ValueError):
            return None
        return "aggressive" if a >= p else "positional"
    s = str(player_style).strip().lower()
    return s if s in ("aggressive", "positional") else None


def _parse_candidates(before, candidates):
    """[(Move, white_eval_or_None)] from a MultiPV-style list."""
    out = []
    if not candidates:
        return out
    for c in candidates:
        ev, mv = None, None
        if isinstance(c, dict):
            ev = _analysis_value(c)
            raw = c.get("move") or c.get("best_move") or c.get("uci")
            if raw is None:
                pv = _analysis_variation(c)
                if pv:
                    raw = pv.split()[0] if isinstance(pv, str) else list(pv)[0]
            mv = _normalise_move(before, raw)
        else:
            mv = _normalise_move(before, c)
        if mv is not None and all(mv != m for m, _ in out):
            out.append((mv, ev))
    return out


def _style_score(analysis, style):
    wanted = ATTACK_TAGS if style == "aggressive" else POSITIONAL_TAGS
    score = sum(p for p, _, t in analysis["positives"] if t in wanted)
    score -= sum(p for p, _, _ in analysis["negatives"]) * 0.5
    return score


def _pick_style_move(before, best_obj, best_ev, candidates, style):
    """Return (move, analysis, is_style_pick)."""
    def run(m):
        a = before.copy(stack=False)
        a.push(m)
        return analyze_move(before, a, m)

    best_analysis = run(best_obj)
    if not style or not candidates:
        return best_obj, best_analysis, False

    color = before.turn
    pool = list(candidates)
    if all(best_obj != m for m, _ in pool):
        pool.append((best_obj, best_ev))
    evs = [_mover_value(e, color) for _, e in pool if e is not None]
    best_mover = _mover_value(best_ev, color)
    top = max(evs) if evs else best_mover
    chosen, chosen_an, chosen_score = best_obj, best_analysis, _style_score(best_analysis, style)
    for m, e in pool:
        if m == best_obj:
            continue
        mv_e = _mover_value(e, color)
        if mv_e is None or top is None or top - mv_e > STYLE_TOLERANCE:
            continue
        an = run(m)
        score = _style_score(an, style)
        if score > chosen_score + 10:
            chosen, chosen_an, chosen_score = m, an, score
    return chosen, chosen_an, chosen != best_obj


# ==========================================================
# EXPLANATION TEXT
# ==========================================================

def _sorted_texts(items):
    return [t for _, t, _ in sorted(items, key=lambda x: -x[0])]


MIN_BAD_REASON_PRIORITY = 50   # weaker findings are not good enough to justify a bad label


def _quality_reasons(before, move_obj, quality, analysis, best_obj, best_analysis,
                     story, ev_before, ev_after):
    """
    The justification for the quality label, as full sentences.
      * inaccuracy / mistake / blunder -> exactly ONE reason: the most decisive
        verified problem (mate allowed, piece lost, bad trade, engine line that
        loses material).  If the board shows none, fall back to what the engine's
        move would have done, then to the evaluation drop.
      * good / best -> up to TWO reasons: the strongest verified positives.
    """
    mover = before.turn
    pos = sorted(analysis["positives"], key=lambda x: -x[0])
    neg = sorted(analysis["negatives"], key=lambda x: -x[0])

    if quality in BAD_QUALITIES:
        options = []
        if best_obj is not None and best_obj != move_obj and best_analysis \
                and "mate" in best_analysis["tags"]:
            options.append((120, f"It misses a forced checkmate with {before.san(best_obj)}."))
        options.extend((p, t) for p, t, _ in neg if p >= MIN_BAD_REASON_PRIORITY)
        lost = _story_reason(story, mover, bad=True)
        if lost:
            text, points = lost
            options.append((97 if points >= 3 else 70, text))
        if options:
            return [max(options, key=lambda o: o[0])[1]]

        # nothing concrete on the board: say what the better move did instead
        if best_obj is not None and best_obj != move_obj and best_analysis:
            best_san = before.san(best_obj)
            for _, text, _ in sorted(best_analysis["positives"], key=lambda x: -x[0]):
                if text.startswith("It "):
                    return [f"It overlooks {best_san}, which {text[3:].rstrip('.')}."]
        if ev_before is not None and ev_after is not None:
            return [f"The evaluation falls from {_fmt_eval(ev_before)} to {_fmt_eval(ev_after)}, "
                    f"and {describe_eval(ev_after)}."]
        if best_obj is not None and best_obj != move_obj:
            return [f"It overlooks {before.san(best_obj)}, which the engine rates clearly higher."]
        return ["The engine rates the resulting position clearly worse than its alternatives."]

    options = [(p, t) for p, t, _ in pos]
    if not options:
        won = _story_reason(story, mover, bad=False)
        if won:
            options.append((80, won[0]))
    if options:
        return [t for _, t in sorted(options, key=lambda o: -o[0])[:2]]
    return ["It maintains the position healthy"]


def _compose_explanation(before, move_obj, san, quality, analysis, best_obj,
                         best_analysis, story, ev_before, ev_after, swing):
    """'<move> is a <quality>: <why>'  and nothing else."""
    reasons = _quality_reasons(before, move_obj, quality, analysis, best_obj,
                               best_analysis, story, ev_before, ev_after)
    reasons = [r.strip() if r.strip().endswith(".") else r.strip() + "." for r in reasons if r]
    stem = quality_stem(san, quality)
    if not stem:
        return " ".join(reasons)
    if not reasons:
        return stem + "."
    return f"{stem}: {_lc(reasons[0])}" + "".join(" " + r for r in reasons[1:])


# ==========================================================
# RECOMMENDATION TEXT
# ==========================================================

def _style_line(style, analysis, san, bad):
    tags = analysis["tags"]
    attack = tags & ATTACK_TAGS
    positional = tags & POSITIONAL_TAGS
    if style == "aggressive":
        if attack:
            return f"This suits your aggressive style: {san} keeps the initiative and puts concrete pressure on the opponent."
        return (f"You like to attack, but here the engine does not support a forcing continuation, "
                f"so improve your position with {san} first and attack once it is ready.")
    if style == "positional":
        if positional:
            return f"This suits your positional style: {san} improves your position without taking unnecessary risks."
        if attack:
            return f"A forcing move is justified here because {san} gains something concrete; calculate it carefully."
    return ""


def _build_recommendation(before, move_obj, quality, best_obj, best_ev, best_pv_san,
                          candidates, style):
    color = before.turn
    if best_obj is None:
        return None if quality not in BAD_QUALITIES else "Stockfish did not provide a replacement move."

    chosen, analysis, style_pick = _pick_style_move(before, best_obj, best_ev, candidates, style)
    san = before.san(chosen)
    best_san = before.san(best_obj)
    ideas = _sorted_texts(analysis["positives"])[:2]
    idea_text = " ".join(ideas)

    if chosen == move_obj:
        text = f"Stockfish agrees with {san}."
        if idea_text:
            text += " " + idea_text
        if best_pv_san:
            text += f" The engine expects {', '.join(best_pv_san[:3])} to follow."
        return text

    if quality in BAD_QUALITIES:
        text = f"Prefer {san} instead."
        if idea_text:
            text += " " + idea_text
        if style_pick:
            text += f" It is only slightly behind Stockfish's {best_san} but matches your style better."
        elif chosen != best_obj:
            pass
        style_text = _style_line(style, analysis, san, True)
        if style_text:
            text += " " + style_text
        if best_pv_san and not style_pick:
            text += f" The lines starts {', '.join(best_pv_san[:4])}."
        return text.strip()

    # good / best-but-not-identical: only a light pointer
    text = f"Stockfish's top choice is {best_san}"
    text += f": {_lc(ideas[0])}" if ideas else "."
    if style and chosen != move_obj:
        style_text = _style_line(style, analysis, san, False)
        if style_text and quality == "good":
            text += " " + style_text
    return text.strip()


def build_personalized_recommendation(before, best_move, player_style, candidates=None,
                                      best_eval=None):
    """Style-aware recommendation for inaccuracies, mistakes and blunders."""
    if before is None or not best_move or not player_style:
        return None
    style = _style_name(player_style)
    if style is None:
        return None
    best_obj = _normalise_move(before, best_move)
    if best_obj is None:
        return None
    return _build_recommendation(before, None, "mistake", best_obj, best_eval, None,
                                 _parse_candidates(before, candidates), style)


def describe_move_idea(before, after, best_move_san):
    """Short idea behind a move, built from the board (compat helper)."""
    try:
        move = before.parse_san(best_move_san)
    except ValueError:
        return ""
    b = before.copy(stack=False)
    b.push(move)
    texts = _sorted_texts(analyze_move(before, b, move)["positives"])
    if not texts:
        return ""
    t = texts[0]
    return _lc(t[3:] if t.startswith("It ") else t).rstrip(".")


def recommendation_text(before, after, played_move, best_move_san):
    if not best_move_san:
        return "Stockfish did not provide a replacement move."
    idea = describe_move_idea(before, after, best_move_san)
    if played_move == best_move_san:
        return f"Stockfish recommends {best_move_san}" + (f": it {idea}." if idea else ".")
    return f"Stockfish recommends {best_move_san} instead of {played_move}" + (f": it {idea}." if idea else ".")


# ==========================================================
# MAIN ENTRY POINT
# ==========================================================

def explain_move(
    before,
    after,
    move,
    played_move,
    best_move=None,
    pv=None,
    evaluation_before=None,
    evaluation_after=None,
    quality=None,
    player_style=None,
    played_analysis=None,
    best_move_analysis=None,
    opponent_pv=None,
    candidates=None,
    **kwargs,
):
    """
    Explain one move like a coach.

    Returns {"explanation": str, "recommendation": str|None, "consequences": [str]}

    Evaluations are in pawns from White's point of view.
      pv           : engine line starting at `before` (best line)
      opponent_pv  : engine line starting at `after` (opponent's reply first)
      candidates   : optional MultiPV list [{"move": uci, "evaluation": pawns}, ...]
    """
    if before is None or not hasattr(before, "legal_moves"):
        return {"explanation": f"Unable to analyze {played_move}: the starting position is unavailable.",
                "recommendation": None, "consequences": []}

    move_obj = _normalise_move(before, move)
    if move_obj is None:
        return {"explanation": f"Unable to verify {played_move}: it is not a legal move in the supplied position.",
                "recommendation": None, "consequences": []}

    verified_after = before.copy(stack=False)
    verified_after.push(move_obj)
    san = before.san(move_obj)
    mover = before.turn

    # evaluations (reuse what analysis_service already computed)
    if evaluation_before is None:
        evaluation_before = _analysis_value(played_analysis)
    if evaluation_after is None:
        evaluation_after = _analysis_value(best_move_analysis)
    if evaluation_after is None and isinstance(played_analysis, dict):
        for key in ("evaluation_after", "after_evaluation", "eval_after"):
            if key in played_analysis:
                evaluation_after = _analysis_value({"evaluation": played_analysis[key]})
                if evaluation_after is not None:
                    break

    # engine best move
    if best_move is None and isinstance(best_move_analysis, dict):
        best_move = best_move_analysis.get("best_move") or best_move_analysis.get("move")
        if best_move is None:
            bpv = _analysis_variation(best_move_analysis)
            if bpv:
                best_move = bpv.split()[0] if isinstance(bpv, str) else list(bpv)[0]
    best_obj = _normalise_move(before, best_move)

    if quality is None:
        quality = calculate_move_quality(before, verified_after, evaluation_before, evaluation_after)
    quality = str(quality).strip().lower() if quality else None

    swing = None
    if evaluation_before is not None and evaluation_after is not None:
        swing = max(0.0, -(_mover_value(evaluation_after, mover) - _mover_value(evaluation_before, mover)))

    # facts
    analysis = analyze_move(before, verified_after, move_obj)
    best_analysis = None
    best_ev = None
    if best_obj is not None:
        ba = before.copy(stack=False)
        ba.push(best_obj)
        best_analysis = analyze_move(before, ba, best_obj)
        best_ev = _analysis_value(best_move_analysis)
        if best_ev is None and best_obj == move_obj:
            best_ev = evaluation_after
        if best_ev is None and candidates:
            for m, e in _parse_candidates(before, candidates):
                if m == best_obj and e is not None:
                    best_ev = e

    # engine lines
    best_line = _analysis_variation(best_move_analysis) or pv
    best_pv_san = _normalise_pv(before, best_line)
    post_line = opponent_pv or _analysis_variation(played_analysis)
    post_moves = _pv_moves(verified_after, post_line)
    if not post_moves and pv:
        full = _pv_moves(before, pv)
        if full and full[0] == move_obj:
            post_moves = full[1:]
    story = _pv_story(verified_after, post_moves, mover)

    explanation = _compose_explanation(
        before, move_obj, san, quality, analysis, best_obj, best_analysis,
        story, evaluation_before, evaluation_after, swing)

    style = _style_name(player_style)
    recommendation = None
    if quality in BAD_QUALITIES or (best_obj is not None and best_obj != move_obj and quality == "good"):
        recommendation = _build_recommendation(
            before, move_obj, quality, best_obj, best_ev, best_pv_san,
            _parse_candidates(before, candidates), style)
    elif quality == "best" and best_obj == move_obj:
        recommendation = _build_recommendation(
            before, move_obj, quality, best_obj, best_ev, best_pv_san, None, None)

    # The explanation already carries the single justification, so there is no
    # separate list of side effects (keeps the UI from repeating itself).
    return {
        "explanation": explanation,
        "recommendation": recommendation,
        "consequences": [],
    }


# ==========================================================
# COMPATIBILITY WRAPPERS
# ==========================================================

def add_consequence_analysis(result, before, after, move, played_move, best_move=None,
                             evaluation_before=None, evaluation_after=None, pv=None,
                             quality=None):
    """explain_move() already includes consequences; this only fills the list."""
    if "consequences" not in result:
        a = analyze_move(before, after, move)
        result["consequences"] = _sorted_texts(a["negatives"])[:3]
    return result


def add_quality_to_result(result, played_move, quality, before=None, best_move=None,
                          player_style=None, after=None, move=None,
                          evaluation_before=None, evaluation_after=None, pv=None):
    """Prepend the verdict if missing and set a style-aware recommendation."""
    verdict = quality_verdict(played_move, quality)
    explanation = result.get("explanation", "")
    if verdict and not explanation.startswith(verdict.split(":")[0].split(".")[0]):
        result["explanation"] = f"{verdict} {explanation}".strip()
    if quality in BAD_QUALITIES and not result.get("recommendation"):
        result["recommendation"] = build_personalized_recommendation(
            before=before, best_move=best_move, player_style=player_style)
    elif quality not in BAD_QUALITIES and "recommendation" not in result:
        result["recommendation"] = None
    return add_consequence_analysis(result, before, after, move, played_move, best_move,
                                    evaluation_before, evaluation_after, pv, quality) \
        if before is not None and after is not None and move is not None else result


# ==========================================================
# UCI -> SAN
# ==========================================================

def convert_uci_to_san(board, uci_move):
    if not uci_move:
        return None
    try:
        move = chess.Move.from_uci(uci_move)
        if move not in board.legal_moves:
            return uci_move
        return board.san(move)
    except Exception:
        return uci_move


def convert_pv_to_san(board, pv):
    if not pv:
        return []
    result = []
    temp = board.copy()
    for uci_move in pv:
        try:
            move = chess.Move.from_uci(uci_move)
            if move not in temp.legal_moves:
                result.append(uci_move)
                break
            result.append(temp.san(move))
            temp.push(move)
        except Exception:
            result.append(uci_move)
            break
    return result