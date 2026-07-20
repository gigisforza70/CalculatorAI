import re

with open('app/src/main/java/com/example/ui/UnitConverter.kt', 'r') as f:
    content = f.read()

# Fix keypad padding
content = content.replace(
    'modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp)',
    'modifier = Modifier.fillMaxWidth().padding(horizontal = 24.dp)'
)

with open('app/src/main/java/com/example/ui/UnitConverter.kt', 'w') as f:
    f.write(content)
