import re

with open('app/src/main/java/com/example/ui/UnitConverter.kt', 'r') as f:
    content = f.read()

# Remove .clickable from Column
content = content.replace(
"""    Column(modifier = Modifier
        .fillMaxWidth()
        .clickable { onFocusChange() }
        .padding(24.dp)) {""",
"""    Column(modifier = Modifier
        .fillMaxWidth()
        .padding(24.dp)) {"""
)

# Add onFocusChanged to BasicTextField
content = content.replace(
    '.focusRequester(focusRequester),',
    '.focusRequester(focusRequester).androidx.compose.ui.focus.onFocusChanged { if (it.isFocused) onFocusChange() },'
)

with open('app/src/main/java/com/example/ui/UnitConverter.kt', 'w') as f:
    f.write(content)

