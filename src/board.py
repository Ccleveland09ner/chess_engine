from const import *
from square import *
from piece import *
from move import *

class Board:
    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        self.last_move = None
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')
    
    def move(self, piece, move):
        initial = move.initial
        final = move.final

        #console board move update
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        #move
        piece.moved = True

        #clear valid moves
        piece.clear_moves()

        #set last move
        self.last_move = move

    def valid_move(self, piece, move):
        return move in piece.moves

    def calc_moves(self, piece, row, col):
        # Calculate possible moves for a piece at a given position
        def pawn_moves():
            #steps
            steps = 1 if piece.moved else 2

            #vertical moves
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))
            for possible_move_row in range(start, end, piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].isempty():
                        #create initial and final move square
                        initial = Square(row, col)
                        final = Square(possible_move_row, col)
                        #create a new move
                        move = Move(initial, final)
                        piece.add_move(move)
                    #pawn has no possible moves
                    else:
                        break
                else:
                    break
            #diagonal move
            possible_move_row = row + piece.dir
            possible_move_cols = [col - 1, col + 1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                        #create initial and final move squares
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        #create a new move
                        move = Move(initial, final)
                        #append new move
                        piece.add_move(move)

        def knight_moves():
            possible_moves = [
                (row + 2, col + 1), (row + 2, col - 1),
                (row - 2, col + 1), (row - 2, col - 1),
                (row + 1, col + 2), (row + 1, col - 2),
                (row - 1, col + 2), (row - 1, col - 2)
            ]

            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col): 
                    square = self.squares[possible_move_row][possible_move_col]
                    if square.isempty_or_enemy(piece.color):
                        #create a squares of new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        #create new move
                        move = Move(initial, final)
                        #add new valid move
                        piece.add_move(move)
                
        def straightline_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr

                while True:
                    if Square.in_range(possible_move_row, possible_move_col):
                        square = self.squares[possible_move_row][possible_move_col]
                        
                        #create squares of the possible new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)

                        #create a possible new move
                        move = Move(initial, final)

                        #if empty continue looping
                        if square.isempty():
                            #append new move
                            piece.add_move(move)
                            break

                        if square.has_enemy_piece(piece.color):
                            #append new move
                            piece.add_move(move)
                            break
                        if square.has_team_piece(piece.color):
                            break
                    #not in range
                    else:
                        break

                    #incrementing the increments    
                    possible_move_row = possible_move_row + row_incr
                    possible_move_col = possible_move_col + col_incr

        def king_moves():
            # TODO: ADD QUEEN AND KING CASTLING
            adjs = [
                (row - 1, col + 0),
                (row - 1, col + 1),
                (row + 0, col + 1),
                (row + 1, col + 1),
                (row + 1, col + 0),
                (row + 1, col - 1),
                (row + 0, col - 1),
                (row - 1, col - 1)
            ]
            for possible_move in adjs:
                possible_move_row, possible_move_col = possible_move
                if Square.in_range(possible_move_row, possible_move_col):
                    #create square of the new move
                    initial = Square(row, col)
                    final = Square(possible_move_row, possible_move_col)

                    #create new move
                    move =Move(initial, final)

                    #append new valid move
                    piece.add_move(move)            

        if isinstance(piece, Pawn): pawn_moves()

        elif isinstance(piece, Knight): knight_moves()

        elif isinstance(piece, Bishop):
            straightline_moves([
                (-1, 1), (-1, -1),
                (1, 1), (1, -1)
            ])

        elif isinstance(piece, Rook):
            straightline_moves([
                (-1, 0), (0, 1),
                (1, 0), (0, -1)
            ])

        elif isinstance(piece, Queen):
            straightline_moves([
                (-1, 0), (0, 1),
                (1, 0), (0, -1),
                (-1, 1), (-1, -1),
                (1, 1), (1, -1)
            ])

        elif isinstance(piece, King): king_moves()

    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        row_pawn, row_other = (6,7) if color == 'white' else (1,0)

        #pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        #knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        #bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        #rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        #queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        #king
        self.squares[row_other][4] = Square(row_other, 4, King(color)) 
