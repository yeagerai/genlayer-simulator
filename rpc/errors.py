class InvalidAddressError(Exception):
    """Exception raised when the given address is not valid."""

    def __init__(
        self,
        address: str,
        message: str = "Incorrect address format. Please provide a valid address.",
    ):
        self.address = address
        self.message = message
        super().__init__(self.message)


class ItemNotFoundError(Exception):
    """Exception raised when a given item is not found."""

    def __init__(
        self,
        id,
        message: str = "Item not found.",
    ):
        self.id = id
        self.message = message
        super().__init__(self.message)
