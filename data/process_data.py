import glob
from model import Sequence
from gp import do_gp

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
    do_gp(Sequence(get_sequence_file(seq2id)).first)

if __name__ == "__main__":
    test_gp()
