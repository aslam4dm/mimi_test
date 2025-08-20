import re

# Match a JSON-like string value: colon -> optional spaces -> " ... " -> followed by , } or end
# The inner group consumes:
#   - escaped chars (\\.)
#   - any non-quote char ([^"])
#   - OR a quote that is NOT the closing one: "(?!\s*(?:,|}|$))
quote_in_value = re.compile(
    r'(:\s*)"(?P<val>(?:\\.|[^"]|"(?!\s*(?:,|}|$)))*)"\s*(?=,|}|$)'
)

def strip_inner_quotes(s: str) -> str:
    def repl(m):
        inner = m.group('val')
        # Remove escaped quotes \" (and the backslash), then any remaining raw quotes
        inner = re.sub(r'\\+"', '', inner)
        inner = inner.replace('"', '')
        return f'{m.group(1)}"{inner}"'
    return quote_in_value.sub(repl, s)

# Demo
s = '"Description": "some "bad" "messy" text", "Recommendation": "other "bad" text"'
print(strip_inner_quotes(s))



#remove desc and recommend 
import re

def remove_fields(s: str, fields) -> str:
    for field in fields:
        # Remove "field": <anything until next comma or brace>
        s = re.sub(rf'\s*"{field}"\s*:\s*.*?(?=,|}})', '', s, flags=re.DOTALL)

    # Remove leftover ",," or ", }"
    s = re.sub(r',\s*,+', ',', s)
    s = re.sub(r'{\s*,', '{', s)
    s = re.sub(r',\s*}', '}', s)

    return s.strip()

# Example
s = '''{ "id": 1, "desc": "some "bad" "text"", "rec: "even more "bad" "text"", "status": "ok" }'''

cleaned = remove_fields(s, ["desc", "recommend"])
print(cleaned)
