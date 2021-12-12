""" Provides json (de)serializer for Artemis JSON objects.
"""

import json
import re
from datetime import datetime
from typing import Any, Dict, Optional, Union

DATE_REGEX = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d*)?Z"
DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


def dumps(obj: Any, *args, **kwargs) -> str:
    return json.dumps(obj, *args, default=_dumps_hook, **kwargs)


def loads(s: Union[str, bytes], *args, **kwargs) -> Any:
    return json.loads(s, *args, object_hook=_loads_object_hook, **kwargs)


def _dumps_hook(obj: Any) -> str:
    if isinstance(obj, (datetime)):
        return obj.strftime(DATE_FORMAT)
    raise TypeError(f"Type {type(obj)} not serializable")


def _loads_object_hook(dct: Dict[Any, Any]) -> Optional[Any]:
    for k, v in dct.items():
        if isinstance(v, str) and re.search(DATE_REGEX, v):
            try:
                dct[k] = deserialize_datetime(v)
            except ValueError:
                pass
    return dct


def deserialize_datetime(dt: str):
    # 2021-11-30T13:15:22Z
    # or 2021-11-30T13:15:22.82347923Z
    if "." in dt:
        dt = dt[0:dt.rindex(".")] + "Z"
    return datetime.strptime(dt, DATE_FORMAT)
