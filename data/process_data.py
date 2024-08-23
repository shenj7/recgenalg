import glob
from model import Sequence
from gp import do_gp
from typing import List

def get_sequence_files(prefix: str):
    """
    Get sequence files from prefix

    output: list of filenames
    """
    if prefix == "all":
        seq_files = glob.glob("../oeisdata/seq/**/*.seq")
    else:
        seq_files = glob.glob(f"../oeisdata/seq/{prefix}/*.seq")
    return seq_files

def get_sequence_file(seqid: str):
    """
    Get sequence from id
    TODO: maybe dont need actually
    """
    print(f"../oeisdata/seq/{seqid[:4]}/{seqid[4:]}.seq")
    seq_file = glob.glob(f"../oeisdata/seq/{seqid[:4]}/{seqid}.seq")
    print(seq_file)
    return seq_file[0]

def split_sequence(seq: List[int], terms: int):
    """
    takes the first <terms> terms of the sequence and returns both halves
    """
    return seq[:terms], seq[terms:]

def split_and_run_and_test(seq: List[int], terms: int):
    """
    takes the first <terms> terms of the sequence, runs the gp on it, and tests it on the terms after
    """
    train = seq[:terms]
    test = seq[terms:]
    result = do_gp(train)
    toolbox = result[3]
    individual = result[2][0]
    func = toolbox.compile(expr=individual)
    print('{:15s} {:15s} {:15s} {:15s}'.format("Previous", "Expected", "Calculated", "Difference"))
    format_string = "{:15d} {:15d} {:15d} {:15d}"
    for i in range(len(test)-1):
        predicted = func(test[i])
        print(format_string.format(test[i], test[i+1], predicted, predicted-test[i+1]))



"""
Testing functions
"""
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

def test_gp():
    #seq1id = "A000079"
    seq2id = "A033999"
    result = do_gp(Sequence(get_sequence_file(seq2id)).first)
    print(result[2][1])

def test_multiple_easy():
    files = get_sequence_files("A000")
    sequences = []
    for f in files:
        s = Sequence(f)
        if "easy" in s.tags:
            sequences.append(s)

def test_comparison():
    seqid = "A000079"
    file = split_and_run_and_test(Sequence(get_sequence_file(seqid)).first, 10)

if __name__ == "__main__":
    test_comparison()
