from beagle.edges import Edge


class Call(Edge):
    __name__ = "Call"

    timestamp: int

    def __init__(self) -> None:
        super().__init__()
