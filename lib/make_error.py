def make_error(status_code: int, message: str) -> tuple[dict[str, str], int]:
    """Create a standardized error response.

    Args:
        status_code (int): The HTTP status code for the error.
        message (str): A descriptive error message.

    Returns:
        tuple[dict[str, str], int]: A tuple containing the error message dictionary and the status code.
    """
    return {"error": message}, status_code
