from collections import defaultdict
from typing import DefaultDict, Dict, List, Optional

from beagle.nodes.domain import URI, Domain
from beagle.nodes.file import File
from beagle.nodes.api_call import ApiCall
from beagle.nodes.ip_address import IPAddress
from beagle.nodes.node import Node
from beagle.nodes.registry import RegistryKey

from beagle.edges import (
    ConnectedTo,
    DNSQueryFor,
    HTTPRequestTo,
    Wrote,
    Accessed,
    Launched,
    Loaded,
    Deleted,
    Copied,
    Call,
    ChangedValue,
    CreatedKey,
    ReadKey,
    DeletedValue,
    DeletedKey,
)

class ThreadProcess(Node):
    __name__ = "ThreadProcess"
    __color__ = "#FF0000"
    key_fields: List[str] = ["thread_id", "api", "category"]

    host: Optional[str]
    user: Optional[str]
    thread_id: Optional[int]
    api: Optional[str]
    category: Optional[str]
    status: Optional[str]
    command_line: Optional[str]
    hashes: Optional[Dict[str, str]] = {}

    # Process edges
    launched: DefaultDict["ThreadProcess", Launched]  # List of launched processes

    # call edges
    call: DefaultDict[ApiCall, Call]

    def __init__(
        self,
        thread_id: int = None,
        api: str = None,
        category: str = None,
    ) -> None:
        self.thread_id = thread_id
        self.api = api
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
        self.launched = defaultdict(Launched)
        self.connected_to = defaultdict(ConnectedTo)
        self.http_request_to = defaultdict(HTTPRequestTo)
        self.dns_query_for = defaultdict(DNSQueryFor)
        self.changed_value = defaultdict(ChangedValue)
        self.created_key = defaultdict(CreatedKey)
        self.deleted_value = defaultdict(DeletedValue)
        self.read_key = defaultdict(ReadKey)
        self.deleted_key = defaultdict(DeletedKey)

    def get_api_node(self) -> ApiCall:
        return ApiCall(
            thread_id=self.thread_id,
            api=self.api,
            category=self.category,
        )

    @property
    def edges(self) -> List[DefaultDict]:
        return [
            self.launched,
            self.call,
        ]

    @property
    def _display(self) -> str:
        return self.process_image or super()._display


# class SysMonProc(Process):
#     """A custom Process class which extends the regular one. Adds
#     the unique Sysmon process_guid identifier.
#     """

#     key_fields: List[str] = ["process_guid"]
#     process_guid: Optional[str]

#     def __init__(self, process_guid: str = None, *args, **kwargs) -> None:
#         self.process_guid = process_guid
#         super().__init__(*args, **kwargs)
