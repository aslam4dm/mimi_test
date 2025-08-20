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
