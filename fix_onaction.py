import re

with open('app/src/main/java/com/example/ui/UnitConverter.kt', 'r') as f:
    content = f.read()

old_action = """    val onAction: (String) -> Unit = { action ->
        val currentVal = if (focus1) value1.text else value2.text
        when (action) {
            "C" -> updateValues("0", focus1)
            "backspace" -> {
                val newVal = if (currentVal.length > 1) currentVal.dropLast(1) else "0"
                updateValues(newVal, focus1)
            }
            "+/-" -> {
                if (currentVal.startsWith("-")) updateValues(currentVal.drop(1), focus1)
                else if (currentVal != "0") updateValues("-$currentVal", focus1)
            }
            else -> {
                val newVal = if (currentVal == "0" && action != ",") action else currentVal + action
                updateValues(newVal, focus1)
            }
        }
    }"""

new_action = """    val onAction: (String) -> Unit = { action ->
        val currentField = if (focus1) value1 else value2
        val text = currentField.text
        val sel = currentField.selection.start
        
        when (action) {
            "C" -> updateValues(androidx.compose.ui.text.input.TextFieldValue("0", androidx.compose.ui.text.TextRange(1)), focus1)
            "backspace" -> {
                if (text.isNotEmpty() && text != "0" && sel > 0) {
                    val newVal = text.substring(0, sel - 1) + text.substring(sel)
                    val finalVal = if (newVal.isEmpty() || newVal == "-") "0" else newVal
                    val newSel = if (newVal.isEmpty() || newVal == "-") 1 else sel - 1
                    updateValues(androidx.compose.ui.text.input.TextFieldValue(finalVal, androidx.compose.ui.text.TextRange(newSel)), focus1)
                }
            }
            "+/-" -> {
                if (text.startsWith("-")) {
                    val newVal = text.drop(1)
                    val newSel = maxOf(0, sel - 1)
                    updateValues(androidx.compose.ui.text.input.TextFieldValue(newVal, androidx.compose.ui.text.TextRange(newSel)), focus1)
                } else if (text != "0") {
                    val newVal = "-$text"
                    val newSel = sel + 1
                    updateValues(androidx.compose.ui.text.input.TextFieldValue(newVal, androidx.compose.ui.text.TextRange(newSel)), focus1)
                }
            }
            else -> {
                val newVal = if (text == "0" && action != ",") action else text.substring(0, sel) + action + text.substring(sel)
                val newSel = if (text == "0" && action != ",") action.length else sel + action.length
                updateValues(androidx.compose.ui.text.input.TextFieldValue(newVal, androidx.compose.ui.text.TextRange(newSel)), focus1)
            }
        }
    }"""

content = content.replace(old_action, new_action)

with open('app/src/main/java/com/example/ui/UnitConverter.kt', 'w') as f:
    f.write(content)
