import json
from typing import Dict, Generator
from urllib import parse

from beagle.common.logging import logger
from beagle.constants import EventTypes, FieldNames
from beagle.datasources.base_datasource import DataSource
from beagle.transformers import CuckooApiTransformer


class CuckooApiReport(DataSource):
    """Yields events from a cuckoo sandbox report.

    Cuckoo now provides a nice summary for each process under the "generic" summary tab::

        {
            "behavior": {
                "generic": [
                    {
                        'process_path': 'C:\\Users\\Administrator\\AppData\\Local\\Temp\\It6QworVAgY.exe',
                        'process_name': 'It6QworVAgY.exe',
                        'pid': 2548,
                        'ppid': 2460,
                        'summary': {
                            "directory_created" : [...],
                            "dll_loaded" : [...],
                            "file_opened" : [...],
                            "regkey_opened" : [...],
                            "file_moved" : [...],
                            "file_deleted" : [...],
                            "file_exists" : [...],
                            "mutex" : [...],
                            "file_failed" : [...],
                            "guid" : [...],
                            "file_read" : [...],
                            "regkey_re" : [...]
                            ...
                        },

                    }
                ]
            }
        }

    Using this, we can crawl and extract out all activity for a specific process.

    Notes
    ---------
    This is based on the output of the following reporting module:
    https://github.com/cuckoosandbox/cuckoo/blob/master/cuckoo/processing/platform/windows.py



    Parameters
    ----------
    cuckoo_report : str
        The file path to the cuckoo sandbox report.
    """

    name = "Cuckoo API Report"
    category = "Cuckoo API"  # The category this will output to.

    # The events object yields both the API calls and the prettified version.
    transformers = [CuckooApiTransformer]

    def __init__(self, cuckoo_report: str) -> None:
        self.report = json.load(open(cuckoo_report, "r"))
        self.behavior = self.report["behavior"]
        self.threads: Dict[int, dict] = {}
        logger.info("Set up Cuckoo Sandbox")

    

    # def events(self) -> Generator[dict, None, None]:

    #     self.threads: Dict[int, dict] = self.identify_threads()
    #     yield from self.process_calls() 


    # def identify_threads(self) -> Dict[int, dict]:
    #     """The `generic` tab contains an array of processes. We can iterate over it to quickly generate
    #     `Process` entries for later. After grabbing all processes, we can walk the "processtree" entry
    #     to update them with the command lines.


    #     Returns
    #     -------
    #     None
    #     """

    #     threads = {}

    #     #Added by Ali Suwanda 19052020
    #     # for process2 in self.processes2:
    #     #     for call in process2["calls"]:
    #     #         threads[int(call["tid"])] = {
    #     #              FieldNames.THREAD_ID: int(call["tid"]),
    #     #              #FieldNames.CATEGORY: call["category"],
    #     #              #FieldNames.API_CALL.append("unknown"),
    #     #         }

    #     #Commented by Ali Suwanda 19052020
    #     for process in self.behavior["processes"]:
    #        for call in process["calls"]:
    #             threads[int(call["tid"])] = {
    #                 FieldNames.THREAD_ID: int(process["tid"]),
    #                 FieldNames.CATEGORY: "unknown",
    #                 # FieldNames.API_CALL.append("unknown"),
    #             }

        
    #     return threads

    # def process_calls(self) -> Generator[dict, None, None]:
    #     def process_single_calls(entry: dict) -> Generator[dict, None, None]:

    #         #print(self.threads)
            
    #         current_thread = self.threads[int(entry["tid"])] 
    #         #current_proc = self.threads[int(entry["tid"])] comment by Ali Suwanda 20052020
    #         #if int(entry["tid"]) in self.threads {
    #         #         FieldNames.EVENT_TYPE: EventTypes.THREAD_LAUNCHED,
    #         #         FieldNames.THREAD_ID: entry["tid"],
    #         #         FieldNames.CATEGORY: entry["category"] if "category" in entry else "",
    #         #         FieldNames.API_CALL: entry["api"] if "api" in entry else ""
    #         #}
    #         self.threads[int(entry["tid"])] = current_thread.copy()

    #         children = entry.get("calls", [])

    #         #print(children)
    #         # # If the parent pid is not in the processes, then we need to make an artifical node.
    #         if entry["tid"] not in self.threads: #and self.threads[int(entry["tid"])] == {}:
    #             # print({
    #             #     FieldNames.EVENT_TYPE: EventTypes.THREAD_LAUNCHED,
    #             #     FieldNames.THREAD_ID: entry["tid"],
    #             #     child_proc[FieldNames.CATEGORY]: child["category"] if "category" in child else "",
    #             #     child_proc[FieldNames.API_CALL]: child["api"] if "api" in child else "",
    #             #     **current_threads,
    #             # })
    #             yield {
    #                 FieldNames.EVENT_TYPE: EventTypes.THREAD_LAUNCHED,
    #                 FieldNames.THREAD_ID: entry["tid"],
    #                 current_thread[FieldNames.CATEGORY]: child["category"] if "category" in child else "",
    #                 current_thread[FieldNames.API_CALL]: child["api"] if "api" in child else "",
    #                 **current_thread,
    #             }

    #         if len(children) > 0:

    #             for child in children:

    #                 current_thread = self.threads[int(entry["tid"])]
    #                 current_thread[FieldNames.CATEGORY]= child["category"],
    #                 current_thread[FieldNames.API_CALL]= child["api"],
    #                 self.threads[int(entry["tid"])] = current_thread.copy()

    #                 current_thread_as_parent = self._convert_thread_to_parent_fields(current_thread.copy())

    #                 # print({
    #                 #     FieldNames.EVENT_TYPE: EventTypes.THREAD_LAUNCHED,
    #                 #     FieldNames.TIMESTAMP: child["time"],
    #                 #     **current_as_parent,
    #                 #     **child_proc,
    #                 # })

    #                 yield {
    #                     FieldNames.EVENT_TYPE: EventTypes.THREAD_LAUNCHED,
    #                     FieldNames.TIMESTAMP: child["time"] if "time" in child else "unknown",
    #                     **current_thread_as_parent,
    #                     **current_thread,
    #                 }

    #                 yield from process_single_calls(child)

    #     for entry in self.behavior.get("processes", []):
    #         yield from process_single_calls(entry)