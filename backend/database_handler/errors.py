class AccountNotFoundError(Exception):
    """Exception raised when a given account is not found."""

    def __init__(
        self,
        address: str,
        message: str = "Account not found.",
    ):
        self.address = address
        self.message = message
        super().__init__(self.message)
