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


class InsufficientFundsError(Exception):
    """Exception raised when a given account has insufficient funds."""

    def __init__(
        self,
        address: str,
        message: str = "Insufficient funds.",
    ):
        self.address = address
        self.message = message
        super().__init__(self.message)


class GenVMRPCErrorResponse(Exception):
    """Exception raised when calling the GenVM RPC server."""

    def __init__(
        self,
        data: dict,
        message: str = "Error calling the GenVM RPC server.",
    ):
        self.data = data
        self.message = message
        super().__init__(self.message)
