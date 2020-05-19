from collections import defaultdict
from typing import TYPE_CHECKING, DefaultDict, Dict, List, Optional

from beagle.nodes.node import Node
from beagle.edges import Call

# mypy type hinting
if TYPE_CHECKING:
    from beagle.nodes import ThreadProcess  # noqa: F401


class ApiCall(Node):
    __name__ = "API Call"
    __color__ = "#3CB371"

    thread_id: Optional[str]
    category: Optional[str]
    call: Optional[str]

    relation: DefaultDict["Process", Call]

    key_fields: List[str] = ["thread_id", "call"]

    def __init__(
        self,
        thread_id: str = None,
        category: str = None,
        call: str = None
    ) -> None:
        self.thread_id = thread_id
        self.category = category
        self.call = call

        self.relation = defaultdict(Call)

    @property
    def edges(self) -> List[DefaultDict]:
        return [self.file_of, self.copied_to]

    @property
    def _display(self) -> str:
        return self.category or super()._display
