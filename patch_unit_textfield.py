import re

with open('app/src/main/java/com/example/ui/UnitConverter.kt', 'r') as f:
    content = f.read()

pattern = r"(androidx\.compose\.foundation\.text\.BasicTextField\([\s\S]*?readOnly\s*=\s*)true(,\s*visualTransformation = ExpressionVisualTransformation\(\),[\s\S]*?decorationBox = \{ innerTextField ->[\s\S]*?innerTextField\(\)[\s\S]*?\}[\s\S]*?\n\s*\))"

def repl(m):
    return "androidx.compose.runtime.CompositionLocalProvider(\n            androidx.compose.ui.platform.LocalTextInputService provides null\n        ) {\n        " + m.group(1) + "false" + m.group(2) + "\n        }"

new_content = re.sub(pattern, repl, content)

with open('app/src/main/java/com/example/ui/UnitConverter.kt', 'w') as f:
    f.write(new_content)
