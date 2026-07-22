import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

target = """        } else {
            // Standard portrait layout
            val portraitKeys = listOf(
                listOf("C", "( )", "%", "÷"),
                listOf("7", "8", "9", "×"),
                listOf("4", "5", "6", "-"),
                listOf("1", "2", "3", "+"),
                listOf("+/-", "0", ",", "=")
            )"""

replacement = """        } else {
            // Standard portrait layout
            val portraitKeys = listOf(
                listOf("C", "( )", "%", "÷"),
                listOf("7", "8", "9", "×"),
                listOf("4", "5", "6", "-"),
                listOf("1", "2", "3", "+"),
                listOf("+/-", "0", ",", "=")
            )
            val portraitScientificKeys = listOf(
                listOf("sin", "cos", "tan", "lg", "ln"),
                listOf("x^y", "x²", "√x", "1/x", "|x|"),
                listOf("C", "( )", "%", "÷", "x!"),
                listOf("7", "8", "9", "×", "π"),
                listOf("4", "5", "6", "-", "e"),
                listOf("1", "2", "3", "+", "2nd"),
                listOf("+/-", "0", ",", "=", "deg")
            )"""

content = content.replace(target, replacement)

target2 = """                } else {
                    Column(modifier = Modifier.fillMaxSize(), verticalArrangement = Arrangement.SpaceEvenly) {
                        portraitKeys.forEach { row ->
                            Row(modifier = Modifier.fillMaxWidth().weight(1f).padding(vertical = 4.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                                row.forEach { btn ->
                                    CalculatorButton(text = btn, onClick = { onAction(btn) }, isScientific = false, isDark = isDark, primaryColor = primaryColor, modifier = Modifier.weight(1f))
                                }
                            }
                        }
                    }
                }"""

replacement2 = """                } else {
                    Column(modifier = Modifier.fillMaxSize(), verticalArrangement = Arrangement.SpaceEvenly) {
                        if (isScientific) {
                            portraitScientificKeys.forEach { row ->
                                Row(modifier = Modifier.fillMaxWidth().weight(1f).padding(vertical = 2.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                                    row.forEach { btn ->
                                        val isNumOrOp = btn in listOf("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", ",", "+/-", "+", "-", "×", "÷", "=", "C", "%", "( )")
                                        CalculatorButton(text = btn, onClick = { onAction(btn) }, isScientific = !isNumOrOp, isDark = isDark, primaryColor = primaryColor, modifier = Modifier.weight(1f).padding(horizontal = 2.dp))
                                    }
                                }
                            }
                        } else {
                            portraitKeys.forEach { row ->
                                Row(modifier = Modifier.fillMaxWidth().weight(1f).padding(vertical = 4.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                                    row.forEach { btn ->
                                        CalculatorButton(text = btn, onClick = { onAction(btn) }, isScientific = false, isDark = isDark, primaryColor = primaryColor, modifier = Modifier.weight(1f))
                                    }
                                }
                            }
                        }
                    }
                }"""

content = content.replace(target2, replacement2)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
