import re

with open('app/src/main/java/com/example/ui/UnitConverter.kt', 'r') as f:
    content = f.read()

content = content.replace(
    '.androidx.compose.ui.focus.onFocusChanged',
    '.onFocusChanged'
)

# Add import if missing
if 'import androidx.compose.ui.focus.onFocusChanged' not in content:
    content = content.replace('import androidx.compose.ui.focus.FocusRequester', 'import androidx.compose.ui.focus.FocusRequester\nimport androidx.compose.ui.focus.onFocusChanged')

with open('app/src/main/java/com/example/ui/UnitConverter.kt', 'w') as f:
    f.write(content)

