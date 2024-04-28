from typing import List, Tuple
from collections import defaultdict
from games.maco.maco_piece import MacoPiece, MacoPieceType

class MacoPieceCollection:
    def __init__(self):
        self.pieces: List['MacoPiece'] = []

    def clone(self) -> 'MacoPieceCollection':
        new_collection = MacoPieceCollection()
        for piece in self.pieces:
            new_collection.add_piece(piece.clone())
        return new_collection

    def add_piece(self, piece: 'MacoPiece') -> None:
        self.pieces.append(piece)

    def add_pieces(self, pieces: List['MacoPiece']) -> None:
        self.pieces.extend(pieces)

    def remove_piece(self, piece: 'MacoPiece') -> None:
        if piece in self.pieces:
            self.pieces.remove(piece)

    def remove_pieces_in_position(self, pos: Tuple[int, int]) -> None:
        self.pieces = [piece for piece in self.pieces if piece.get_pos() != pos]

    def get_pieces(self) -> List['MacoPiece']:
        return self.pieces

    def get_regular_pieces(self) -> List['MacoPiece']:
        return [piece for piece in self.pieces if piece.get_piece_type() == MacoPieceType.REGULAR]

    def get_explode_pieces(self) -> List['MacoPiece']:
        return [piece for piece in self.pieces if piece.get_piece_type() == MacoPieceType.EXPLODE]

    def get_block_pieces(self) -> List['MacoPiece']:
        return [piece for piece in self.pieces if piece.get_piece_type() == MacoPieceType.BLOCK]

    def get_piece_in_position(self, pos: Tuple[int, int]) -> 'MacoPiece':
        pieces = [piece for piece in self.pieces if piece.get_pos() == pos]
        return pieces[0] if pieces else None

    def get_regular_positions(self) -> List[Tuple[int, int]]:
        return [piece.get_pos() for piece in self.pieces if piece.get_piece_type() == MacoPieceType.REGULAR]

    def get_explode_positions(self) -> List[Tuple[int, int]]:
        return [piece.get_pos() for piece in self.pieces if piece.get_piece_type() == MacoPieceType.EXPLODE]

    def get_block_positions(self) -> List[Tuple[int, int]]:
        return [piece.get_pos() for piece in self.pieces if piece.get_piece_type() == MacoPieceType.BLOCK]

    def __str__(self) -> str:
        return f"Regular: {self.get_regular_positions()}, Explode: {self.get_explode_positions()}, Block: {self.get_block_positions()}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MacoPieceCollection):
            return False
        return self.pieces == other.pieces

    def __hash__(self) -> int:
        piece_dict = defaultdict(int)
        for piece in self.pieces:
            piece_dict[piece] += 1
        hashed = "".join([str(piece.__hash__()) + str(piece_dict[piece]) for piece in piece_dict])
        return hash(hashed)
