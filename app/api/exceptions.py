class InternalServerError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__("Something went wrong, please contact our support.", *args)


class NotFoundElementError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__("Element not found - ", *args)


class BadRequestError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__("Bad request - ", *args)


class ForbiddenError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__("Forbidden - ", *args)
