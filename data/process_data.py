import glob
from model import Sequence
from gp import do_gp
from typing import List
from typing import TextIO

tolerance = 0.0000000001

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

def split_and_run_and_test(seq: List[int], terms: int, seed: int, f: TextIO):
    """
    takes the first <terms> terms of the sequence, runs the gp on it, and tests it on the terms after
    """
    train = seq[:terms]
    test = seq[terms:]
    result = do_gp(train, seed)
    toolbox = result[3]
    individual = result[2][0]
    log = result[1]
    func = toolbox.compile(expr=individual)
    print(log, file=f)
    print('{:15s} {:15s} {:15s} {:15s}'.format("Previous", "Expected", "Calculated", "Difference"), file=f)
    format_string = "{:14.2f} {:14.2f} {:14.2f} {:14.2f}"
    right = 1
    next_right = 1
    for i in range(len(test)-1):
        predicted = func(test[i])
        if abs(predicted-test[i+1]) > tolerance:
            if i == 0:
                next_right = 0
            right = 0
        print(format_string.format(test[i], test[i+1], predicted, predicted-test[i+1]), file=f)

    print("\n\n\n\n\n", file=f)
    return right, next_right



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
    min_len = 999
    for f in files:
        s = Sequence(f)
        if "easy" in s.tags:
            sequences.append(s)
        if len(s.first) < min_len:
            min_len = len(s.first)

    print(len(sequences))
    print(min_len)

def test_comparison():
    #seqid = "A000079"
    #seqid = "A033999"
    seqid = "A000045"
    file = split_and_run_and_test(Sequence(get_sequence_file(seqid)).first, 10)

def test_comparison_multiple_easy(output_loc: str):
    seed = 139
    output = open(output_loc, 'w')
    print("Seed: " + str(seed), file=output)
    files = get_sequence_files("A000")
    sequences = []
    for f in files:
        s = Sequence(f)
        if "easy" in s.tags:
            sequences.append(s)

    num_next_right = 0
    num_right = 0

    for s in sequences:
        print(s.seqid, file=output)
        result = split_and_run_and_test(s.first, 15, seed, output)
        num_right = num_right + result[0]
        num_next_right = num_next_right + result[1]


    print("Number of correct rest-of-sequence predictions: " + str(num_right), file=output)
    print("Number of correct next-term predictions: " + str(num_next_right), file=output)
    print("Total number of sequences:" + str(len(sequences)), file=output)
    print("Rest-of-sequence accuracy: " + str(num_right/len(sequences)), file=output)
    print("Next-term accuracy: " + str(num_next_right/len(sequences)), file=output)
    output.close()


if __name__ == "__main__":
    test_comparison_multiple_easy("8-26-24_test.txt")
    #test_comparison()
