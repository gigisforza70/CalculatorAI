import re

with open('app/src/main/java/com/example/ui/UnitConverter.kt', 'r') as f:
    content = f.read()

# Replace updateValues signature and body
old_update = """    fun updateValues(input: String, isFirst: Boolean) {
        try {
            val v = input.replace(",", ".").toDoubleOrNull() ?: 0.0
            if (isFirst) {
                value1 = androidx.compose.ui.text.input.TextFieldValue(input, androidx.compose.ui.text.TextRange(input.length))
                val out2 = if (selectedCategory == UnitCategory.Temperature) {
                    convertTemp(v, unit1.name, unit2.name).toString().replace(".", ",")
                } else {
                    formatDouble((v * unit1.multiplierToStandard) / unit2.multiplierToStandard).replace(".", ",")
                }
                value2 = androidx.compose.ui.text.input.TextFieldValue(out2, androidx.compose.ui.text.TextRange(out2.length))
            } else {
                value2 = androidx.compose.ui.text.input.TextFieldValue(input, androidx.compose.ui.text.TextRange(input.length))
                val out1 = if (selectedCategory == UnitCategory.Temperature) {
                    convertTemp(v, unit2.name, unit1.name).toString().replace(".", ",")
                } else {
                    formatDouble((v * unit2.multiplierToStandard) / unit1.multiplierToStandard).replace(".", ",")
                }
                value1 = androidx.compose.ui.text.input.TextFieldValue(out1, androidx.compose.ui.text.TextRange(out1.length))
            }
        } catch(e: Exception) {}
    }"""

new_update = """    fun updateValues(inputField: androidx.compose.ui.text.input.TextFieldValue, isFirst: Boolean) {
        try {
            val input = inputField.text
            val v = input.replace(",", ".").toDoubleOrNull() ?: 0.0
            if (isFirst) {
                value1 = inputField
                val out2 = if (selectedCategory == UnitCategory.Temperature) {
                    convertTemp(v, unit1.name, unit2.name).toString().replace(".", ",")
                } else {
                    formatDouble((v * unit1.multiplierToStandard) / unit2.multiplierToStandard).replace(".", ",")
                }
                if (value2.text != out2) {
                    value2 = androidx.compose.ui.text.input.TextFieldValue(out2, androidx.compose.ui.text.TextRange(out2.length))
                }
            } else {
                value2 = inputField
                val out1 = if (selectedCategory == UnitCategory.Temperature) {
                    convertTemp(v, unit2.name, unit1.name).toString().replace(".", ",")
                } else {
                    formatDouble((v * unit2.multiplierToStandard) / unit1.multiplierToStandard).replace(".", ",")
                }
                if (value1.text != out1) {
                    value1 = androidx.compose.ui.text.input.TextFieldValue(out1, androidx.compose.ui.text.TextRange(out1.length))
                }
            }
        } catch(e: Exception) {}
    }"""
content = content.replace(old_update, new_update)

content = content.replace('updateValues("0", true)', 'updateValues(androidx.compose.ui.text.input.TextFieldValue("0", androidx.compose.ui.text.TextRange(1)), true)')

content = content.replace('onValue1Change = { updateValues(it.text, true) }', 'onValue1Change = { updateValues(it, true) }')
content = content.replace('onValue2Change = { updateValues(it.text, false) }', 'onValue2Change = { updateValues(it, false) }')

content = content.replace('onUnit1Change = { unit1 = it; expanded1 = false; updateValues(value1.text, true) }', 'onUnit1Change = { unit1 = it; expanded1 = false; updateValues(value1, true) }')
content = content.replace('onUnit2Change = { unit2 = it; expanded2 = false; updateValues(value2.text, false) }', 'onUnit2Change = { unit2 = it; expanded2 = false; updateValues(value2, false) }')

with open('app/src/main/java/com/example/ui/UnitConverter.kt', 'w') as f:
    f.write(content)
