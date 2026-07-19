content = open("app/src/main/java/com/example/MainActivity.kt").read()
# Let's count { and }
import sys
lines = content.split('\n')
open_brackets = 0
for i, line in enumerate(lines):
    open_brackets += line.count('{') - line.count('}')
    if open_brackets < 0:
        print(f"Line {i+1} has unmatched closing bracket: {line}")
