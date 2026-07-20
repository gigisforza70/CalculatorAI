import re

with open('app/src/main/java/com/example/ui/UnitConverter.kt', 'r') as f:
    content = f.read()

# Replace Arrangement.Center with just placing them at the top with some padding, so they are higher up
content = content.replace(
    'Column(modifier = Modifier.weight(1f), verticalArrangement = Arrangement.Center) {',
    'Column(modifier = Modifier.weight(1f).padding(top = 32.dp), verticalArrangement = Arrangement.Top) {'
)

with open('app/src/main/java/com/example/ui/UnitConverter.kt', 'w') as f:
    f.write(content)
