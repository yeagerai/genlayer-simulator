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


class AccountAlreadyExists(Exception):
    """Exception raised when someone wants to create an account with an address that already exists."""

    def __init__(
        self,
        address: str,
        message: str = "Account already exists.",
    ):
        self.address = address
        self.message = message
        super().__init__(self.message)


class ValidatorNotFound(Exception):
    """Exception raised when someone wants to get, update, or remove a validator that doesn't exist."""

    def __init__(
        self,
        address: str,
        message: str = "Validator doesn't exist.",
    ):
        self.address = address
        self.message = message
        super().__init__(self.message)


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


class InvalidInputError(Exception):
    """Exception raised when the given input is not valid."""

    def __init__(
        self,
        input_name: str,
        input_value: str,
        message: str = "Incorrect input",
    ):
        self.input_name = input_name
        self.input_value = input_value
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
