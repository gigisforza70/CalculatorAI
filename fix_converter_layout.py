import re

with open('app/src/main/java/com/example/ui/UnitConverter.kt', 'r') as f:
    content = f.read()

# Fix Keypad horizontal padding
content = content.replace(
    '.padding(horizontal = 4.dp, vertical = 2.dp),',
    '.padding(vertical = 2.dp),'
)

# Fix Input1 padding
content = content.replace(
    """    Column(modifier = Modifier
        .fillMaxWidth()
        .padding(24.dp)) {""",
    """    Column(modifier = Modifier
        .fillMaxWidth()
        .padding(vertical = 12.dp, horizontal = 24.dp)) {"""
)

# Apply to Input2 as well (it should match)
# The above replace will hit both if they are identical, let's make sure
content = content.replace(
    """        .padding(24.dp)) {""",
    """        .padding(vertical = 12.dp, horizontal = 24.dp)) {"""
)

with open('app/src/main/java/com/example/ui/UnitConverter.kt', 'w') as f:
    f.write(content)

