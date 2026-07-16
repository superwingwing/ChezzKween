import chess


class MoveAnalyzer:

    def __init__(self, board):

        self.board = board.copy()

    def analyze(
        self,
        played_move,
        engine_result_before,
        engine_result_after
    ):

        analysis = {}

        # ===========================
        # Basic
        # ===========================

        analysis["played_move"] = played_move.uci()

        analysis["best_move"] = (
            engine_result_before["best_move"]
        )

        analysis["eval_before"] = (
            engine_result_before["evaluation"]
        )

        analysis["eval_after"] = (
            engine_result_after["evaluation"]
        )

        analysis["evaluation_loss"] = abs(

            analysis["eval_before"]

            -

            analysis["eval_after"]

        )

        # ===========================
        # Move Type
        # ===========================

        analysis["capture"] = self.board.is_capture(
            played_move
        )

        analysis["castle"] = self.board.is_castling(
            played_move
        )

        analysis["en_passant"] = (
            self.board.is_en_passant(
                played_move
            )
        )

        analysis["promotion"] = (
            played_move.promotion is not None
        )

        analysis["check"] = (
            self.board.gives_check(
                played_move
            )
        )

        # ===========================
        # Piece
        # ===========================

        piece = self.board.piece_at(
            played_move.from_square
        )

        if piece:

            analysis["piece"] = chess.piece_name(
                piece.piece_type
            )

            analysis["piece_type"] = (
                piece.piece_type
            )

        else:

            analysis["piece"] = None

            analysis["piece_type"] = None

        return analysis