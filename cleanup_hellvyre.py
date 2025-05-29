import re

with open('HELLVYRE.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Remove all headers_useragents.append(...) and headers_referers.append(...) lines
code = re.sub(r"^\s*headers_useragents\.append\(.*\)\s*$", "", code, flags=re.MULTILINE)
code = re.sub(r"^\s*headers_referers\.append\(.*\)\s*$", "", code, flags=re.MULTILINE)

# Replace useragent_list() function
code = re.sub(
    r"def useragent_list\(\):.*?def ",
    "def useragent_list():\n    global headers_useragents\n    headers_useragents = []\n    with open('useragents.txt', 'r') as f:\n        headers_useragents = [line.strip() for line in f if line.strip()]\n\ndef ",
    code,
    flags=re.DOTALL
)

# Replace referer_list() function
code = re.sub(
    r"def referer_list\(\):.*?def ",
    "def referer_list():\n    global headers_referers\n    headers_referers = []\n    with open('referers.txt', 'r') as f:\n        headers_referers = [line.strip() for line in f if line.strip()]\n    headers_referers.append('http://' + host + '/')\n    return(headers_referers)\n\ndef ",
    code,
    flags=re.DOTALL
)

# Save the cleaned file
with open('HELLVYRE.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Cleanup complete! All header append lines removed and functions replaced.")
