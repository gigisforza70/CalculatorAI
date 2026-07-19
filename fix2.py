content = open("app/src/main/java/com/example/MainActivity.kt").read()
import sys
lines = content.split('\n')
open_brackets = 0
for i, line in enumerate(lines):
    open_brackets += line.count('{') - line.count('}')
    print(f"Line {i+1} [lvl {open_brackets}]: {line}")
    if open_brackets < 0:
        print(f"FAILED AT LINE {i+1}")
        break
