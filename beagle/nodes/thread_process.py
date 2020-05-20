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

    host: Optional[str]
    user: Optional[str]
    thread_id: Optional[int]
    api_call: Optional[str]
    category: Optional[str]
    status: Optional[str]
    command_line: Optional[str]
    hashes: Optional[Dict[str, str]] = {}

    # Process edges
    threadlaunched: DefaultDict["ThreadProcess", ThreadLaunched]  # List of launched processes

    # call edges
    call: DefaultDict[ApiCall, Call]

    def __init__(
        self,
        thread_id: int = None,
        api_call: str = None,
        category: str = None,
    ) -> None:
        self.thread_id = thread_id
        self.api_call = api_call
        self.category = category

        # if process_path:
        #     self.process_path = process_path
        # elif process_image_path and process_image:
        #     if process_image_path[-1] == "\\":
        #         self.process_path = f"{process_image_path}{process_image}"
        #     else:
        #         self.process_path = f"{process_image_path}\\{process_image}"

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
            self.threadlaunched,
            self.call,
        ]

    @property
    def _display(self) -> str:
        return self.call or super()._display


# class SysMonProc(Process):
#     """A custom Process class which extends the regular one. Adds
#     the unique Sysmon process_guid identifier.
#     """

#     key_fields: List[str] = ["process_guid"]
#     process_guid: Optional[str]

#     def __init__(self, process_guid: str = None, *args, **kwargs) -> None:
#         self.process_guid = process_guid
#         super().__init__(*args, **kwargs)
