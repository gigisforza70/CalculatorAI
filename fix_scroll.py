import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Remove .horizontalScroll(rememberScrollState()) from Rows that have weights inside them
content = content.replace('.horizontalScroll(rememberScrollState())', '')

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
