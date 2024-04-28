from typing import Tuple
from games.maco.maco_piece_type import MacoPieceType

class MacoPiece:
    """
    This class represents a piece in the game Maco.

    Attributes:
        piece_type (MacoPieceType): The type of the piece.
        pos (Tuple[int, int]): The position of the piece on the game board.
    """

    def __init__(self, piece_type: 'MacoPieceType', pos: Tuple[int, int] = None) -> None:
        """
        The constructor for MacoPiece class.

        Parameters:
            piece_type (MacoPieceType): The type of the piece.
            pos (Tuple[int, int]): The position of the piece on the game board.
        """
        self.piece_type = piece_type
        self.pos = pos

    def clone(self) -> 'MacoPiece':
        """
        Clones the current piece.

        Returns:
            MacoPiece: A new piece with the same type and position as the current piece.
        """
        return MacoPiece(self.piece_type, self.pos)

    def copy_into(self, other: 'MacoPiece') -> None:
        """
        Copies the current piece's attributes into another piece.

        Parameters:
            other (MacoPiece): The piece to copy into.
        """
        other.piece_type = self.piece_type
        other.pos = self.pos

    def get_piece_type(self) -> 'MacoPieceType':
        """
        Gets the type of the piece.

        Returns:
            MacoPieceType: The type of the piece.
        """
        return self.piece_type

    def get_pos(self) -> Tuple[int, int]:
        """
        Gets the position of the piece.

        Returns:
            Tuple[int, int]: The position of the piece.
        """
        return self.pos

    def __str__(self) -> str:
        """
        Returns a string representation of the piece.

        Returns:
            str: A string representation of the piece.
        """
        return f"MacoPiece[{self.piece_type.name}, {self.pos}]"

    def __eq__(self, other: object) -> bool:
        """
        Checks if the current piece is equal to another piece.

        Parameters:
            other (object): The piece to compare with.

        Returns:
            bool: True if the pieces are equal, False otherwise.
        """
        if not isinstance(other, MacoPiece):
            return False
        return self.piece_type == other.piece_type and self.pos == other.pos

    def __hash__(self) -> int:
        """
        Returns a hash value for the piece.

        Returns:
            int: A hash value for the piece.
        """
        return hash((self.piece_type, self.pos))
