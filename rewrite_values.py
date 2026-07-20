import re

with open('app/src/main/java/com/example/ui/UnitConverter.kt', 'r') as f:
    content = f.read()

content = content.replace(
    'var value1 by remember { mutableStateOf("0") }',
    'var value1 by remember { mutableStateOf(androidx.compose.ui.text.input.TextFieldValue("0", androidx.compose.ui.text.TextRange(1))) }'
)
content = content.replace(
    'var value2 by remember { mutableStateOf("0") }',
    'var value2 by remember { mutableStateOf(androidx.compose.ui.text.input.TextFieldValue("0", androidx.compose.ui.text.TextRange(1))) }'
)

update_values_old = """    fun updateValues(input: String, isFirst: Boolean) {
        try {
            val v = input.replace(",", ".").toDoubleOrNull() ?: 0.0
            if (isFirst) {
                value1 = input
                if (selectedCategory == UnitCategory.Temperature) {
                    value2 = convertTemp(v, unit1.name, unit2.name).toString().replace(".", ",")
                } else {
                    value2 = formatDouble((v * unit1.multiplierToStandard) / unit2.multiplierToStandard).replace(".", ",")
                }
            } else {
                value2 = input
                if (selectedCategory == UnitCategory.Temperature) {
                    value1 = convertTemp(v, unit2.name, unit1.name).toString().replace(".", ",")
                } else {
                    value1 = formatDouble((v * unit2.multiplierToStandard) / unit1.multiplierToStandard).replace(".", ",")
                }
            }
        } catch(e: Exception) {}
    }"""

update_values_new = """    fun updateValues(input: String, isFirst: Boolean) {
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

content = content.replace(update_values_old, update_values_new)

effect_old = """    LaunchedEffect(selectedCategory) {
        unit1 = currentUnitsList.first()
        unit2 = currentUnitsList.getOrNull(1) ?: currentUnitsList.first()
        value1 = "0"
        updateValues("0", true)
    }"""

effect_new = """    LaunchedEffect(selectedCategory) {
        unit1 = currentUnitsList.first()
        unit2 = currentUnitsList.getOrNull(1) ?: currentUnitsList.first()
        value1 = androidx.compose.ui.text.input.TextFieldValue("0", androidx.compose.ui.text.TextRange(1))
        updateValues("0", true)
    }"""

content = content.replace(effect_old, effect_new)

action_old = """    val onAction: (String) -> Unit = { action ->
        val currentVal = if (focus1) value1 else value2"""

action_new = """    val onAction: (String) -> Unit = { action ->
        val currentVal = if (focus1) value1.text else value2.text"""

content = content.replace(action_old, action_new)

content = content.replace('value1: String,', 'value1: androidx.compose.ui.text.input.TextFieldValue,')
content = content.replace('value2: String,', 'value2: androidx.compose.ui.text.input.TextFieldValue,')
content = content.replace('onValue1Change: (String) -> Unit,', 'onValue1Change: (androidx.compose.ui.text.input.TextFieldValue) -> Unit,')
content = content.replace('onValue2Change: (String) -> Unit,', 'onValue2Change: (androidx.compose.ui.text.input.TextFieldValue) -> Unit,')


content = content.replace(
"""                onValueChange = { newValue ->
                    if (newValue.matches(Regex("[0-9.,-]*"))) {
                        onValue1Change(newValue)
                    }
                },""",
"""                onValueChange = { newValue ->
                    if (newValue.text.matches(Regex("[0-9.,-]*"))) {
                        onValue1Change(newValue)
                    }
                },""")

content = content.replace(
"""                onValueChange = { newValue ->
                    if (newValue.matches(Regex("[0-9.,-]*"))) {
                        onValue2Change(newValue)
                    }
                },""",
"""                onValueChange = { newValue ->
                    if (newValue.text.matches(Regex("[0-9.,-]*"))) {
                        onValue2Change(newValue)
                    }
                },""")

content = content.replace(
    'updateValues(value1, true)',
    'updateValues(value1.text, true)'
)
content = content.replace(
    'updateValues(value2, false)',
    'updateValues(value2.text, false)'
)
content = content.replace(
    'updateValues(it, true)',
    'updateValues(it.text, true)'
)
content = content.replace(
    'updateValues(it, false)',
    'updateValues(it.text, false)'
)

with open('app/src/main/java/com/example/ui/UnitConverter.kt', 'w') as f:
    f.write(content)

