"""
DNA cutter algorithm
"""


import argparse
import sys
import typing as t


VERSION = 1.0


class CutterT(t.NamedTuple):
    """
    A tuple representation of a DNA cutter.
        seq: the sequence to cut along.
        split_at: the position of the seq to cut at.
    """
    seq: str
    split_at: int


def parse_cutter_file(
    cutter_file: t.IO,
    sep: str = "|",
) -> list[CutterT]:
    """
    Parses a cutter control file into a list of CutterT.

    Sequences are defined in the format A|GTC AG|TC when sep=|.
    """
    cutter_strs: list[str] = cutter_file.readlines()
    return [
        CutterT(
            seq=cutter_str.replace(sep, "").strip(),
            split_at=cutter_str.find(sep),
        )
        for cutter_str in cutter_strs
    ]


def cut_sequence_at_cutters(
    data: str,
    cutters: t.Sequence[CutterT],
    outfile: t.IO,
) -> str:
    """
    A naive search and splitter based on the provided Cutters.
        writes the cut sequence (from data) to outfile.

    TODO: consider bisecting files with pointers that move outward,
        then sorting the resultset by splitloc to reorder results.
    """
    lowest_splitloc = len(data)
    lowest_cutter = None
    for cutter in cutters:
        if (findloc := data.find(cutter.seq)) != -1:
            splitloc = findloc + cutter.split_at
            if splitloc < lowest_splitloc:
                lowest_splitloc = splitloc
                lowest_cutter = cutter
    if lowest_cutter:
        print(
            #lowest_splitloc,
            data[:lowest_splitloc],
            #lowest_cutter.seq,
            file=outfile,
        )
        return data[lowest_splitloc:]
    return data


def parse_dna_file(
    infile: t.IO,
    cutters: t.Sequence[CutterT],
    chunksize: int = 1024,
    outfile: t.IO = sys.stdout,
) -> None:
    """
    loop over chunks of infile (by chunksize) and using
        cut_sequence_at_cutters to search for the provided
        cut point that's cloests while yielding the rest to
        be put into the buffer for the next chunk.

        when no data is left in infile, we will attempt cuts
        against the rest of buffer until no cuts are possible
        and we print the results as the tail sequence.
    """
    buffer = ""
    while True:
        data = infile.read(chunksize).replace("\n", "")
        if not data and not buffer:
            break
        consider = buffer + data
        buffer = cut_sequence_at_cutters(consider, cutters, outfile)
        if consider == buffer:
            print(consider, file=outfile)
            break


def main():
    """
    use argparse to make a comand line interface for this module.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "cutter_filename",
        help=(
            "The file of cutter sequences in form AA|GG where | is where the "
            "split will occur.",
        )
    )
    parser.add_argument(
        "--cutter-separator",
        action="store_const",
        const="|",
    )
    parser.add_argument(
        "--encoding",
        action="store_const",
        const="utf-8",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=("{prog} " + str(VERSION)),
    )
    args = parser.parse_args()

    # parse cutter rules from cutter_filename to cutters
    cutters = []
    with open(args.cutter_filename, "r", encoding=args.encoding) as cutter_file:
        cutters = parse_cutter_file(
            cutter_file,
            sep=args.cutter_separator,
        )

    # parse dna stream into sequences based cutter rules parsed earlier
    parse_dna_file(sys.stdin, cutters)


if __name__ == "__main__":
    main()
