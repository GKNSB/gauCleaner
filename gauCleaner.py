#!/usr/bin/env python
import bisect
from argparse import ArgumentParser, FileType
from urllib.parse import urlparse, urljoin, unquote, unquote_plus


def inSortedList(elem, sorted_list):
    i = bisect.bisect_left(sorted_list, elem)
    return i != len(sorted_list) and sorted_list[i] == elem


parser = ArgumentParser(prog="gauCleaner.py", description="I clean gau results")
parser.add_argument("gauResultsFile", help="Gau output file containing urls", type=str)
parser.add_argument("output", help="Output file location", type=str)
args = parser.parse_args()

counter = 0
LINE_UP = "\033[1A"
LINE_CLEAR = "\x1b[2K"

with open(args.gauResultsFile, "r") as infile:
    toOutput = []
    seenUrls = []

    for aline in infile:
        #aline = unquote(thisline.strip())
        parameterNames = []
        cleanUrl = urljoin(aline.strip(), urlparse(aline.strip()).path)
        parameters = urlparse(aline.strip()).query.split("&")

        if len(parameters) > 1 or parameters[0] != "":

            for parameter in parameters:
                parameterNames.append(parameter.split("=")[0])
            parameterNames.sort()

            seenAgain = False
            temp = "@".join(parameterNames)
            convertedUrl = f"{cleanUrl}@{temp}"

            if inSortedList(convertedUrl, seenUrls):
                seenAgain = True

            if not seenAgain:
                bisect.insort(seenUrls, convertedUrl)
                toOutput.append(aline.strip())

        counter += 1
        print(f"Lines checked: {counter} - Results: {len(toOutput)}")
        print(LINE_UP, end=LINE_CLEAR)

    print(f"Reduced initial urls from {counter} to {len(toOutput)}.")
    with open(args.output, "w") as outfile:
        for url in toOutput:
            outfile.write(f"{url}\n")
