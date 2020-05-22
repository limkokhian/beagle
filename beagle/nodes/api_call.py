from collections import defaultdict
from typing import TYPE_CHECKING, DefaultDict, Dict, List, Optional

from beagle.nodes.node import Node
from beagle.edges import Call

# mypy type hinting
if TYPE_CHECKING:
    from beagle.nodes import ThreadProcess  # noqa: F401


class ApiCall(Node):
    __name__ = "APICall"
    __color__ = "#3CB371"

    thread_id: Optional[str]
    category: Optional[str]
    api_call: Optional[str]

    relation: DefaultDict["Call", Call]

    key_fields: List[str] = ["thread_id", "api_call"]
    
    def __init__(
        self,
        thread_id: str = None,
        category: str = None,
        api_call: str = None
    ) -> None:
        self.thread_id = str(thread_id)
        self.category = category
        self.api_call = api_call

        self.relation = defaultdict(Call)
        
    @property
    def edges(self) -> List[DefaultDict]:
        return [self.relation]

    @property
    def _display(self) -> str:
        return self.thread_id or super()._display
