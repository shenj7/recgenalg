import glob
from dataclasses import dataclass
from typing import List

def get_sequence_files(prefix: str):
    """
    Get sequence files from repository

    output: list of filenames
    """
    if prefix == "all":
        seq_files = glob.glob("../oeisdata/seq/**/*.seq")
    else:
        seq_files = glob.glob(f"../oeisdata/seq/{prefix}/*.seq")
    return seq_files

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


def test_single():
    f = "../oeisdata/seq/A000/A000001.seq"
    seq = Sequence(f)
    print(seq.seqid)
    print(seq.first)
    print(seq.tags)

def test_multiple():
    files = get_sequence_files("A000")
    sequences = []
    for f in files:
        sequences.append(Sequence(f))

    print(sequences)



if __name__ == "__main__":
    test_multiple()
