import json
from typing import Dict, Generator
from urllib import parse

from beagle.common import split_path, split_reg_path
from beagle.common.logging import logger
from beagle.constants import EventTypes, FieldNames, HTTPMethods, Protocols
from beagle.datasources.base_datasource import DataSource
from beagle.transformers import CuckooApiTransformer


class CuckooAPIReport(DataSource):
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

    def metadata(self) -> dict:

        return {
            "machine": self.report["info"]["machine"]["name"],
            "package": self.report["info"]["package"],
            "score": self.report["info"]["score"],
            "report_id": self.report["info"]["id"],
            "name": self.report["target"].get("file", {"name": ""})["name"],
            "category": self.report["target"]["category"],
            "type": self.report["target"].get("file", {"type": ""})["type"],
        }

    def events(self) -> Generator[dict, None, None]:
        self.threads: Dict[int, dict] = self.identify_threads()
        yield from self.process_calls()

    def identify_threads(self) -> Dict[int, dict]:
        """The `generic` tab contains an array of processes. We can iterate over it to quickly generate
        `Process` entries for later. After grabbing all processes, we can walk the "processtree" entry
        to update them with the command lines.


        Returns
        -------
        None
        """

        threads = {}

        for process in self.behavior["processes"]:
            # for call in process["calls"]:
            threads[str(process["pid"])] = {
                FieldNames.THREAD_ID: str(process["pid"]),
                FieldNames.API_CALL: None,
                FieldNames.CATEGORY: None
                # FieldNames.API_CALL.append("unknown"),
            }

        return threads
    
    def process_calls(self) -> Generator[dict, None, None]:
        def process_single_calls(entry: dict) -> Generator[dict, None, None]:
            if "pid" in entry:
                current_threads = self.threads[str(entry["pid"])]
                self.threads[str(entry["pid"])] = current_threads.copy()
                children = entry.get("calls", [])

                # # If the parent pid is not in the processes, then we need to make an artifical node.
                if entry["pid"] not in self.threads and self.threads[str(entry["pid"])] == {}:
                    yield {
                        FieldNames.EVENT_TYPE: EventTypes.THREAD_LAUNCHED,
                        FieldNames.THREAD_ID: str(entry["pid"]),
                        child_proc[FieldNames.CATEGORY]: entry["category"] if "category" in entry else None,
                        child_proc[FieldNames.API_CALL]: entry["api"] if "api" in entry else None,
                        **current_threads,
                    }
            else:
                current_threads = self.threads[str(entry["tid"])]
                self.threads[str(entry["tid"])] = current_threads.copy()
                children = entry.get("calls", [])

                # # If the parent pid is not in the processes, then we need to make an artifical node.
                if entry["tid"] not in self.threads and self.threads[str(entry["tid"])] == {}:
                    yield {
                        FieldNames.EVENT_TYPE: EventTypes.THREAD_LAUNCHED,
                        FieldNames.THREAD_ID: str(entry["tid"]),
                        child_proc[FieldNames.CATEGORY]: entry["category"] if "category" in entry else None,
                        child_proc[FieldNames.API_CALL]: entry["api"] if "api" in entry else None,
                        **current_threads,
                    }

            if len(children) > 0:

                for child in children:
                    unknown_child_node = {
                        FieldNames.EVENT_TYPE: EventTypes.THREAD_LAUNCHED,
                        FieldNames.THREAD_ID: str(child["tid"]),
                        FieldNames.CATEGORY: str(child["category"]) if "category" in child else None,
                        FieldNames.API_CALL: str(child["api"]) if "api" in child else None,
                    }
                                
                    child_threads = self.threads[str(child["tid"])] if str(child["tid"]) in self.threads else unknown_child_node
                    child_threads[FieldNames.CATEGORY]= child["category"]
                    child_threads[FieldNames.API_CALL]= child["api"]
                    self.threads[str(child["tid"])] = child_threads.copy()

                    current_thread_as_parent = self._convert_thread_to_parent_fields(current_threads.copy())

                    yield {
                        FieldNames.EVENT_TYPE: EventTypes.THREAD_LAUNCHED,
                        FieldNames.TIMESTAMP: child["time"] if "time" in child else 0,
                        **current_thread_as_parent,
                        **child_threads,
                    }

                    yield from process_single_calls(child)

        for entry in self.behavior.get("processes", []):
            yield from process_single_calls(entry)