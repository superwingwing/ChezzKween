import chess


class FactGenerator:

    def __init__(self):
        pass

    # ============================================
    # Count Developed Minor Pieces
    # ============================================

    def count_minor_piece_development(
        self,
        board: chess.Board,
        color: bool
    ):

        developed = 0

        if color == chess.WHITE:

            knight_start = [
                chess.B1,
                chess.G1
            ]

            bishop_start = [
                chess.C1,
                chess.F1
            ]

        else:

            knight_start = [
                chess.B8,
                chess.G8
            ]

            bishop_start = [
                chess.C8,
                chess.F8
            ]

        # Knights

        for sq in knight_start:

            piece = board.piece_at(sq)

            if piece is None:

                developed += 1

        # Bishops

        for sq in bishop_start:

            piece = board.piece_at(sq)

            if piece is None:

                developed += 1

        return developed

    # ============================================
    # Has Castled?
    # ============================================

    def has_castled(
        self,
        board,
        color
    ):

        if color == chess.WHITE:

            king = board.king(
                chess.WHITE
            )

            return king in [
                chess.G1,
                chess.C1
            ]

        king = board.king(
            chess.BLACK
        )

        return king in [
            chess.G8,
            chess.C8
        ]

    # ============================================
    # Phase
    # ============================================

    def game_phase(
        self,
        board
    ):

        pieces = len(
            board.piece_map()
        )

        if pieces > 26:

            return "opening"

        elif pieces > 12:

            return "middlegame"

        return "endgame"

    # ============================================
    # Material Balance
    # ============================================

    def material_balance(
        self,
        board
    ):

        values = {

            chess.PAWN:1,

            chess.KNIGHT:3,

            chess.BISHOP:3,

            chess.ROOK:5,

            chess.QUEEN:9

        }

        white = 0

        black = 0

        for piece in board.piece_map().values():

            value = values.get(
                piece.piece_type,
                0
            )

            if piece.color:

                white += value

            else:

                black += value

        return white - black

    # ============================================
    # Generate Facts
    # ============================================

    def generate(

        self,

        board_before,

        board_after,

        move,

        analysis

    ):

        color = not board_after.turn

        facts = analysis.copy()

        phase = self.game_phase(
            board_after
        )

        facts["opening"] = (
            phase == "opening"
        )

        facts["middlegame"] = (
            phase == "middlegame"
        )

        facts["endgame"] = (
            phase == "endgame"
        )

        facts[
            "minor_pieces_developed"
        ] = self.count_minor_piece_development(
            board_after,
            color
        )

        facts[
            "white_castled"
        ] = self.has_castled(
            board_after,
            chess.WHITE
        )

        facts[
            "black_castled"
        ] = self.has_castled(
            board_after,
            chess.BLACK
        )

        facts[
            "material_balance"
        ] = self.material_balance(
            board_after
        )

        facts[
            "move_number"
        ] = board_after.fullmove_number

        return facts