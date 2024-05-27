class InvalidAddressError(Exception):
    """Exception raised when the given address is not valid."""

    def __init__(
        self,
        address,
        message="Incorrect address format. Please provide a valid address.",
    ):
        self.address = address
        self.message = message
        super().__init__(self.message)
