import re

with open('app/src/main/java/com/example/ui/UnitConverter.kt', 'r') as f:
    content = f.read()

content = content.replace('import androidx.compose.ui.focus.focusRequester', 'import androidx.compose.ui.focus.focusRequester\nimport androidx.compose.ui.focus.onFocusChanged')

with open('app/src/main/java/com/example/ui/UnitConverter.kt', 'w') as f:
    f.write(content)

