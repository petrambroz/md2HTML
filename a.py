import re

string = "[a](www)"

x= re.search(r"[\[][^()]*[]][(][^\[\])]*[)]", string)

print(x.span()[:])