class NotFoundError(Exception):
    def __init__(self, resource: str, resource_id: str) -> None:
        self.resource = resource
        self.resource_id = resource_id
        super().__init__(f"{resource} not found: {resource_id}")


class ConcurrencyConflictError(Exception):
    pass
