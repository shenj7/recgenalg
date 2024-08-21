from dataclasses import dataclass
from typing import List

@dataclass
class Sequence:
    """
    Internal class for OEIS sequence data
    """
    seqid: str
    first: List[int]
    tags: List[str]

    def __init__(self, filename: str):
        f = open(filename, "r")
        beginnings = []
        for line in f:
            if line.startswith("%I"):
                self.seqid = line.split(" ")[1]
            if line.startswith("%S") or line.startswith("%T") or line.startswith("%U"):
                if line.endswith(",\n"):
                    beginnings = beginnings + [int(i) for i in line[11:-2].split(",")]
                else:
                    beginnings = beginnings + [int(i) for i in line[11:-1].split(",")]
            if line.startswith("%K"):
                self.tags = line[11:-1].split(",")

        self.first = beginnings

        f.close()

