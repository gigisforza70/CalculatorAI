import re

with open('app/src/main/java/com/example/ui/UnitConverter.kt', 'r') as f:
    content = f.read()

# I will replace the incorrect CompositionLocalProvider wrapping in both places.

# Revert back first:
content = re.sub(r'androidx\.compose\.runtime\.CompositionLocalProvider\([\s\S]*?\{[\s\S]*?(androidx\.compose\.foundation\.text\.BasicTextField\([\s\S]*?readOnly = )false(,[\s\S]*?decorationBox = \{[\s\S]*?padding\(bottom = 8\.dp\)\n\s*\))[\s\S]*?\}\n(\s*\}\n\s*\}\n\s*\))',
    r'\1true\2\3', content)

# Okay, that might be hard. Let's just fix the braces.
