import csv
import re

def read_firms(filePath):
    with open(filePath, 'r') as f:
        reader = csv.reader(f)
        your_list = list(reader)
        flatten = lambda l: [item for sublist in l for item in sublist]
        firms = flatten(your_list)

        pattern = re.compile(r"\w+\b(?<!, Inc|, LLC)(?<! Ltd| LLC| Inc| INC)(?![^\(]*\))")
        firms = [" ".join(re.findall(pattern, firm)) for firm in firms]

    return firms
