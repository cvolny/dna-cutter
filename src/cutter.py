"""
DNA cutter algorithm
"""


import argparse
import os
import sys
import typing as t


VERSION = 1.0


"""
def find_segments(
    infile: t.IO,
    outfile: t.IO = sys.stdout,
    chunksize: int = 1024,
) -> None:
    while chunk := infile.read(chunksize):
        pass"
"""


class CutterT(t.NamedTuple):
    seq: str
    split_at: int


def parse_cutter_file(
    cutter_file: t.IO,
    sep: str = "|",
) -> list[CutterT]:
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
    buffer = ""
    n = 0
    while n < 100:
        data = infile.read(chunksize).replace("\n", "")
        if not data and not buffer:
            break
        consider = buffer + data
        buffer = cut_sequence_at_cutters(consider, cutters, outfile)
        if consider == buffer:
            print(consider, file=outfile)
            break


def main():
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

    cutters = []
    with open(args.cutter_filename, "r", encoding="utf-8") as cutter_file:
        cutters = parse_cutter_file(cutter_file)

    parse_dna_file(sys.stdin, cutters)


if __name__ == "__main__":
    main()
