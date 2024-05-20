from typing import Tuple
from copy import deepcopy
from games import Action
from games.maco.maco_piece import MacoPiece

class MacoAction(Action):
    def __init__(self, piece: 'MacoPiece', pos: Tuple[int, int]):
        self.piece = piece
        self.pos = pos

    def clone(self) -> 'MacoAction':
        return MacoAction(self.piece.clone(), deepcopy(self.pos) if self.pos is not None else None)

    def copy_into(self, other: 'MacoAction') -> None:
        self.piece.copy_into(other.piece)
        other.pos = deepcopy(self.pos) if self.pos is not None else None

    def get_piece(self) -> 'MacoPiece':
        return self.piece

    def get_position(self) -> Tuple[int, int]:
        return self.pos

    def __str__(self) -> str:
        return f"Action[{self.piece}, {self.pos if self.pos is not None else ''}]"