import chess
import chess.pgn
import io
from engine.stockfish_engine import evaluate_position
from ml.coach.reason_detector import detect_reason
from ml.coach.explanation_engine import generate_explanation



def classify_move(loss):

    if loss < 0.20:
        return "Best"

    elif loss < 0.50:
        return "Excellent"

    elif loss < 1.00:
        return "Good"

    elif loss < 2.00:
        return "Inaccuracy"

    elif loss < 4.00:
        return "Mistake"

    return "Blunder"



def analyze_pgn(pgn_text):

    game = chess.pgn.read_game(
        io.StringIO(pgn_text)
    )

    if game is None:
        return {
            "error": "Invalid PGN"
        }


    board = game.board()

    evaluations = []

    move_number = 1


    for move in game.mainline_moves():


        ##################################################
        # POSITION BEFORE MOVE
        ##################################################

        board_before = board.copy()

        before = evaluate_position(
            board_before
        )


        evaluation_before = before["evaluation"]

        best_move = before["best_move"]

        pv_before = before["pv"]



        ##################################################
        # PLAYER MOVE
        ##################################################

        san = board.san(move)


        board.push(move)


        ##################################################
        # POSITION AFTER MOVE
        ##################################################

        board_after = board.copy()


        after = evaluate_position(
            board_after
        )


        evaluation_after = after["evaluation"]



        ##################################################
        # EVALUATION LOSS
        ##################################################

        # White move loses advantage
        if board.turn == chess.BLACK:

            loss = (
                evaluation_before -
                evaluation_after
            )


        # Black move loses advantage
        else:

            loss = (
                evaluation_after -
                evaluation_before
            )


        loss = max(
            0,
            round(loss, 2)
        )



        ##################################################
        # MOVE QUALITY
        ##################################################

        quality = classify_move(
            loss
        )



        ##################################################
        # FIND WHY THE MOVE CHANGED
        ##################################################

        reason = detect_reason(

            board_before,

            board_after,

            evaluation_before,

            evaluation_after

        )



        ##################################################
        # GENERATE EXPLANATION
        ##################################################

        explanation = generate_explanation(

            reason,

            san,

            best_move

        )



        ##################################################
        # SAVE RESULT
        ##################################################

        evaluations.append({

            "move_number":
                move_number,


            "move":
                san,


            "fen":
                board.fen(),


            "quality":
                quality,


            "evaluation_before":
                evaluation_before,


            "evaluation_after":
                evaluation_after,


            "evaluation_loss":
                loss,


            "best_move":
                best_move,


            "pv":
                pv_before,


            "reason":
                reason,


            "explanation":
                explanation["explanation"],


            "recommendation":
                explanation["recommendation"]

        })



        ##################################################
        # MOVE NUMBER
        ##################################################

        if board.turn == chess.WHITE:

            move_number += 1



    return {

        "evaluations":
            evaluations

    }