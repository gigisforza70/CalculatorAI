import re

with open('app/src/main/java/com/example/ui/UnitConverter.kt', 'r') as f:
    content = f.read()

replacement = """        } else if (action == ",") {
            if (!text.contains(",")) {
                text += ","
            }
        } else {
            val digitCount = text.count { it.isDigit() }
            if (digitCount < 15) {
                if (text == "0" && action != ",") {
                    text = action
                } else {
                    text += action
                }
            }
        }"""

content = re.sub(
    r'\} else if \(action == ","\) \{\s*if \(\!text\.contains\(","\)\) \{\s*text \+\= ","\s*\}\s*\} else \{\s*if \(text == "0" && action \!\= ","\) \{\s*text = action\s*\} else \{\s*text \+\= action\s*\}\s*\}',
    replacement,
    content
)

with open('app/src/main/java/com/example/ui/UnitConverter.kt', 'w') as f:
    f.write(content)
