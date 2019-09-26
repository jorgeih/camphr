"""Module utils defines utility for ner labels.

This module can be called directly to generete "labels_**.py" from yml file.

Examples:
    $ python utils.py
"""
from pathlib import Path
from typing import IO, Dict, Iterable, List, Optional, Union

import yaml

__dir__ = Path(__file__).parent


def make_biluo_labels(entity_types: Iterable[str]) -> List[str]:
    """Make BILUO-style ner label from entity type list.

    Examples:
        >>> make_biluo_labels(["PERSON"])
        ["-", "O", "U-PERSON", "B-PERSON", ...]
    """
    labels = ["-", "O"]
    prefix = "BILU"
    for l in entity_types:
        for pref in prefix:
            labels.append(pref + "-" + l)
    return labels


def make_bio_labels(entity_types: Iterable[str]) -> List[str]:
    """Make BIO-style ner label from entity type list.

    Examples:
        >>> make_biluo_labels(["PERSON"])
        ["-", "O", "B-PERSON", "I-PERSON", ...]
    """
    labels = ["-", "O"]
    prefix = "BI"
    for l in entity_types:
        for pref in prefix:
            labels.append(pref + "-" + l)
    return labels


def yml_to_py(yml_path: Union[str, Path], py_path: Union[str, Path]):
    """Convert ymlfile that defines ner labels to python script."""
    yml_path = Path(yml_path)
    py_path = Path(py_path)
    with yml_path.open() as f, py_path.open("w") as fw:
        d = yaml.safe_load(f)
        keys = sorted(extract_keys(d))
        generate_py(fw, keys)


def extract_keys(d: Dict[str, Optional[Dict]]) -> List[str]:
    res = []
    for k, v in d.items():
        res.append(k)
        if isinstance(v, dict):
            res += extract_keys(v)
    return res


def generate_py(f: IO, keys: List[str]):
    for k in keys:
        f.write(f"{k} = '{k}'\n")
    f.write(f"\nALL_LABELS = [{' ,'.join(keys)}]\n")


PREFIX = "labels_"
if __name__ == "__main__":
    for y in __dir__.glob("*.yml"):
        p = __dir__ / (PREFIX + y.stem + ".py")
        yml_to_py(y, p)