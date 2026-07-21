import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

content = re.sub(r'@OptIn\(androidx\.compose\.ui\.ExperimentalComposeUiApi::class\)\s*androidx\.compose\.ui\.platform\.InterceptPlatformTextInput\(\s*interceptor = \{ _, _ ->\s*kotlinx\.coroutines\.awaitCancellation\(\)\s*\}\s*\)\s*\{\s*(androidx\.compose\.foundation\.text\.BasicTextField\([\s\S]*?cursorBrush = androidx\.compose\.ui\.graphics\.SolidColor\(primaryColor\)\s*\))\s*\}', r'\1', content)

content = content.replace('readOnly = false, // To prevent soft keyboard from popping up', 'readOnly = true, // To prevent soft keyboard from popping up')

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
