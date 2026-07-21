import re

with open('app/src/main/java/com/example/ui/UnitConverter.kt', 'r') as f:
    content = f.read()

# Replace InterceptPlatformTextInput with just BasicTextField
content = re.sub(r'androidx\.compose\.ui\.platform\.InterceptPlatformTextInput\(\s*interceptor = \{ _, _ -> kotlinx\.coroutines\.awaitCancellation\(\) \}\s*\)\s*\{\s*(androidx\.compose\.foundation\.text\.BasicTextField\([\s\S]*?cursorBrush = androidx\.compose\.ui\.graphics\.SolidColor\(primaryColor\)\s*\))\s*\}', r'\1', content)

# Change readOnly = false to readOnly = true
content = content.replace('readOnly = false', 'readOnly = true')

with open('app/src/main/java/com/example/ui/UnitConverter.kt', 'w') as f:
    f.write(content)
