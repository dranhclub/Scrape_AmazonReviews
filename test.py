import re
string = "Reviewed in the United States on August 14, 2017"

res = re.findall('(January|February|Match|April|May|June|July|August|October|September|November|December) \d*, \d*', string)
print(res)