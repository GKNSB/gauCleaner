#!/usr/bin/env python3

import random
import string
import os, sys
import sqlite3
from argparse import ArgumentParser, FileType
from urllib.parse import urlparse, urljoin, unquote, unquote_plus


parser = ArgumentParser(prog="gauCleanerSQLite.py", description="I clean gau results")
parser.add_argument("gauResultsFile", help="Gau output file containing urls", type=str)
parser.add_argument("output", help="Output file location", type=str)
args = parser.parse_args()
databaseName = "".join(random.choices(string.ascii_lowercase, k=16))
databaseLocation = f"{sys.path[0]}/{databaseName}.sqlite"

connection= sqlite3.connect(databaseLocation)
cursor= connection.cursor()
create_table = 'CREATE TABLE FilteredURLs (FullURL text, FilteringURL text NOT NULL, PRIMARY KEY(FilteringURL))'
cursor.execute(create_table)

myInput = args.gauResultsFile
myOutput = args.output
counter = 0
counterOut = 0

with open(myInput, "r") as infile:
    toOutput = []
    cursor= connection.cursor()

    for aline in infile:
        #aline = unquote(thisline.strip())
        parameterNames = []
        cleanUrl = urljoin(aline.strip(), urlparse(aline.strip()).path)
        parameters = urlparse(aline.strip()).query.split("&")

        if len(parameters) > 1 or parameters[0] != "":

            for parameter in parameters:
                parameterNames.append(parameter.split("=")[0])
            parameterNames.sort()

            temp = "@".join(parameterNames)
            convertedUrl = f"{cleanUrl}@{temp}"

            try:
                cursor.execute("INSERT INTO FilteredURLs VALUES (?, ?)", (aline.strip(), convertedUrl))
                counterOut += 1

            except sqlite3.IntegrityError as integrityError:
                if "UNIQUE constraint failed" in str(integrityError):
                    pass
                
                else:
                    print(integrityError)

        counter += 1

    connection.commit()

    with open(myOutput, "w") as outfile:
        selectq = "SELECT FullURL from FilteredURLs"
        cursor.execute(selectq)
        recordNumber = 100000

        while recordNumber == 100000:
            records = cursor.fetchmany(100000)
            recordNumber = len(records)
            
            for record in records:
                outfile.write(f"{record[0]}\n")

    print(f"Reduced initial urls from {counter} to {counterOut}.")

    connection.close()
    os.remove(databaseLocation)