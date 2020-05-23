from typing import Optional, Tuple, Union

from beagle.common.logging import logger
from beagle.constants import EventTypes, FieldNames
from beagle.nodes import ThreadProcess, ApiCall
from beagle.transformers.base_transformer import Transformer

class CuckooApiTransformer(Transformer):
    name = "Cuckoo API"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        logger.info("Created Cuckoo API Transformer.")

    def transform(self, event: dict) -> Optional[Tuple]:

        event_type = event.get(FieldNames.EVENT_TYPE)

        if event_type == EventTypes.THREAD_LAUNCHED:
            return self.make_thread(event)
        else:
            return None

    def make_thread(self, event: dict) -> Tuple[ThreadProcess, ApiCall, ThreadProcess, ApiCall]:
        """Accepts a process with the `EventTypes.PROCESS_LAUNCHED` event_type.

        For example::

            {
                FieldNames.PARENT_PROCESS_IMAGE: "cmd.exe",
                FieldNames.PARENT_PROCESS_IMAGE_PATH: "\\",
                FieldNames.PARENT_PROCESS_ID: "2568",
                FieldNames.PARENT_COMMAND_LINE: '/K name.exe"',
                FieldNames.PROCESS_IMAGE: "find.exe",
                FieldNames.PROCESS_IMAGE_PATH: "\\",
                FieldNames.COMMAND_LINE: 'find /i "svhost.exe"',
                FieldNames.PROCESS_ID: "3144",
                FieldNames.EVENT_TYPE: EventTypes.PROCESS_LAUNCHED,
            }

        Parameters
        ----------
        event : dict
            [description]

        Returns
        -------
        Tuple[Process, File, Process, File]
            [description]
        """
        print(event)

        parent = ThreadProcess(
            thread_id=str(event[FieldNames.THREAD_ID])
        )

        # Create the file node.
        # TODO: Integrate into the ThreadProcess() init function?
        parent_thread = parent.get_api_node()
        parent_thread.relation[parent]

        child = ThreadProcess(
            api_call=event[FieldNames.API_CALL],
            category=event[FieldNames.CATEGORY],
            thread_id=str(event[FieldNames.THREAD_ID])
        )

        child_thread = child.get_api_node()
        child_thread.relation[child]

        print(parent_thread)
        print(child_thread)

        if FieldNames.TIMESTAMP in event:
            parent.threadlaunched[child].append(timestamp=int(event[FieldNames.TIMESTAMP]))
        else:
            parent.threadlaunched[child]

        return (parent, parent_thread, child, child_thread)