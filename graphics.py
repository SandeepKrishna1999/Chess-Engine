import chess

board = chess.Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
square = "G1"
sq = chess.Square(7)
pm = board.piece_map()
print(pm.get(chess.sq))