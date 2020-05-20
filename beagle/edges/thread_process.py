# Process based nodes
from beagle.edges import Edge


class ThreadLaunched(Edge):
    __name__ = "ThreadLaunched"

    timestamp: int  # Array of process launch times

    def __init__(self) -> None:
        super().__init__()
