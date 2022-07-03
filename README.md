## gauCleaner
Perform a cleanup on gau results. Clean-up gau output file from duplicates. Helper script that only keeps valid results based on unique combinations of urls and parameters.
For instance:

```
usage: gauCleaner.py [-h] gauResultsFile output

I clean gau results

positional arguments:
  gauResultsFile  Gau output file containing urls
  output          Output file location

optional arguments:
  -h, --help      show this help message and exit
```