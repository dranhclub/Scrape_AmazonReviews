import re

string = "Reviewed in the United States on January 9, 2017"

res = re.findall("on (.*)", string)
print(res[0])