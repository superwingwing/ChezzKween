import chess


class PositionAnalyzer:

    def __init__(self):
        pass

    def analyze(
        self,
        board_before: chess.Board,
        played_move: chess.Move,
        best_move: str,
        eval_before: float,
        eval_after: float
    ):

        facts = {}

        # ===========================
        # Basic Information
        # ===========================

        facts["played_move"] = played_move.uci()
        facts["best_move"] = best_move

        facts["evaluation_before"] = eval_before
        facts["evaluation_after"] = eval_after

        facts["evaluation_loss"] = round(
            abs(eval_before - eval_after),
            2
        )

        # ===========================
        # Piece Played
        # ===========================

        piece = board_before.piece_at(
            played_move.from_square
        )

        if piece:

            facts["piece"] = chess.piece_name(
                piece.piece_type
            )

            facts["piece_type"] = piece.piece_type

            facts["color"] = (
                "white"
                if piece.color
                else "black"
            )

        else:

            facts["piece"] = None
            facts["piece_type"] = None
            facts["color"] = None

        # ===========================
        # Move Properties
        # ===========================

        facts["is_capture"] = board_before.is_capture(
            played_move
        )

        facts["is_castle"] = board_before.is_castling(
            played_move
        )

        facts["is_en_passant"] = (
            board_before.is_en_passant(
                played_move
            )
        )

        facts["is_promotion"] = (
            played_move.promotion is not None
        )

        facts["gives_check"] = (
            board_before.gives_check(
                played_move
            )
        )

        # ===========================
        # Squares
        # ===========================

        facts["from_square"] = chess.square_name(
            played_move.from_square
        )

        facts["to_square"] = chess.square_name(
            played_move.to_square
        )

        return facts