from collections import defaultdict
from typing import TYPE_CHECKING, DefaultDict, Dict, List, Optional

from beagle.nodes.node import Node
from beagle.edges import Call

# mypy type hinting
if TYPE_CHECKING:
    from beagle.nodes import Process  # noqa: F401


class ApiCall(Node):
    __name__ = "API Call"
    __color__ = "#3CB371"

    thread_id: Optional[str]
    category: Optional[str]
    api: Optional[int]
    hashes: Optional[Dict[str, str]] = {}

    call: DefaultDict["ThreadProcess", Call]

    key_fields: List[str] = ["thread_id", "category", "api"]

    def __init__(
        self,
        thread_id: str = None,
        category: str = None,
        api: str = None,
    ) -> None:
        self.thread_id = thread_id
        self.category = category
        self.api = file_name

        # if full_path:
        #     self.full_path = full_path
        # elif category and file_name:
        #     if category[-1] == "\\":
        #         self.full_path = f"{category}{file_name}"
        #     else:
        #         self.full_path = f"{category}\\{file_name}"
        # else:
        #     # Fixes bug where we don't know the path of a process
        #     self.full_path = ""

        # self.extension = extension
        # self.hashes = hashes

        self.call = defaultdict(Call)

    # def set_extension(self) -> None:
    #     if self.full_path:
    #         self.extension = self.full_path.split(".")[-1]

    @property
    def edges(self) -> List[DefaultDict]:
        return [self.call]

    @property
    def _display(self) -> str:
        return self.file_name or super()._display
