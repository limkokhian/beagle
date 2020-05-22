from collections import defaultdict
from typing import DefaultDict, Dict, List, Optional

from beagle.nodes.domain import URI, Domain
from beagle.nodes.file import File
from beagle.nodes.api_call import ApiCall
from beagle.nodes.ip_address import IPAddress
from beagle.nodes.node import Node
from beagle.nodes.registry import RegistryKey

from beagle.edges import (
    #Launched,
    ThreadLaunched,
    Call,
)

class ThreadProcess(Node):
    __name__ = "ThreadLaunched"
    __color__ = "#FF0000"
    key_fields: List[str] = ["thread_id", "api_call", "category"]

    thread_id: Optional[int]
    api_call: Optional[str]
    category: Optional[str]

    # Process edges
    threadlaunched: DefaultDict["ThreadProcess", ThreadLaunched]  # List of launched processes

    # call edges
    call: DefaultDict[ApiCall, Call]

    def __init__(
        self,
        thread_id: str = None,
        api_call: str = None,
        category: str = None,
    ) -> None:
        self.thread_id = str(thread_id)
        self.api_call = api_call
        self.category = category

        # Edge dicts
        self.call = defaultdict(Call)
        self.threadlaunched = defaultdict(ThreadLaunched)

    def get_api_node(self) -> ApiCall:
        return ApiCall(
            thread_id=self.thread_id,
            api_call=self.api_call,
            category=self.category,
        )

    @property
    def edges(self) -> List[DefaultDict]:
        return [
            self.call
        ]

    @property
    def _display(self) -> str:
        return self.api_call or super()._display
