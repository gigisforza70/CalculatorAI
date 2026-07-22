import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

pattern = r"Box\(modifier = Modifier\.fillMaxWidth\(\)\.weight\(1\.5f\)\) \{\n\s*if \(showHistory\) \{[\s\S]*?\} else \{\n\s*Column\(modifier = Modifier\.fillMaxSize\(\), verticalArrangement = Arrangement\.SpaceEvenly\) \{\n\s*if \(isScientific\) \{[\s\S]*?\} else \{[\s\S]*?portraitKeys\.forEach \{ row ->[\s\S]*?\}\n\s*\}\n\s*\}\n\s*\}\n\s*\}"

replacement = """Row(modifier = Modifier.fillMaxWidth().weight(1.5f)) {
                // Left side: History or Scientific or Digits
                Box(modifier = Modifier.weight(3f).fillMaxHeight()) {
                    if (showHistory) {
                        LazyColumn(
                            modifier = Modifier.fillMaxSize(),
                            contentPadding = PaddingValues(bottom = 64.dp)
                        ) {
                            items(history) { entry ->
                                Column(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .clickable {
                                            expression = androidx.compose.ui.text.input.TextFieldValue(entry.expression, androidx.compose.ui.text.TextRange(entry.expression.length))
                                            isResultCalculated = true
                                            showHistory = false
                                        }
                                        .padding(vertical = 12.dp, horizontal = 16.dp),
                                    horizontalAlignment = Alignment.End
                                ) {
                                    Text(text = formatExpression(entry.expression), color = if(isDark) Color(0xFFA0A0A0) else Color(0xFF707070), fontSize = 16.sp)
                                    Spacer(modifier = Modifier.height(4.dp))
                                    Text(text = "=" + formatExpression(entry.result), color = primaryColor, fontSize = 24.sp, fontWeight = FontWeight.Medium)
                                }
                            }
                        }
                        androidx.compose.material3.Button(
                            onClick = { viewModel.clearHistory() },
                            modifier = Modifier
                                .align(Alignment.BottomCenter)
                                .fillMaxWidth(0.7f)
                                .padding(bottom = 8.dp),
                            colors = androidx.compose.material3.ButtonDefaults.buttonColors(containerColor = if(isDark) Color(0xFF2B2B2B) else Color(0xFFE0E0E0)),
                            shape = CircleShape
                        ) {
                            Text("Clear history", color = if(isDark) Color.White else Color.Black, fontSize = 14.sp)
                        }
                    } else if (isScientific) {
                        val scientificLeftKeys = listOf(
                            listOf("sin", "cos", "tan"),
                            listOf("ln", "lg", "x^y"),
                            listOf("√x", "x²", "|x|"),
                            listOf("1/x", "π", "e"),
                            listOf("2nd", "deg", "x!")
                        )
                        Column(modifier = Modifier.fillMaxSize(), verticalArrangement = Arrangement.SpaceEvenly) {
                            scientificLeftKeys.forEach { row ->
                                Row(modifier = Modifier.fillMaxWidth().weight(1f).padding(vertical = 4.dp), horizontalArrangement = Arrangement.SpaceEvenly, verticalAlignment = Alignment.CenterVertically) {
                                    row.forEach { btn ->
                                        CalculatorButton(text = btn, onClick = { onAction(btn) }, isScientific = true, isDark = isDark, primaryColor = primaryColor, modifier = Modifier.weight(1f).padding(horizontal = 4.dp), isPortraitScientific = true)
                                    }
                                }
                            }
                        }
                    } else {
                        val standardLeftKeys = listOf(
                            listOf("C", "( )", "%"),
                            listOf("7", "8", "9"),
                            listOf("4", "5", "6"),
                            listOf("1", "2", "3"),
                            listOf("+/-", "0", ",")
                        )
                        Column(modifier = Modifier.fillMaxSize(), verticalArrangement = Arrangement.SpaceEvenly) {
                            standardLeftKeys.forEach { row ->
                                Row(modifier = Modifier.fillMaxWidth().weight(1f).padding(vertical = 4.dp), horizontalArrangement = Arrangement.SpaceEvenly, verticalAlignment = Alignment.CenterVertically) {
                                    row.forEach { btn ->
                                        CalculatorButton(text = btn, onClick = { onAction(btn) }, isScientific = false, isDark = isDark, primaryColor = primaryColor, modifier = Modifier.weight(1f).padding(horizontal = 4.dp))
                                    }
                                }
                            }
                        }
                    }
                }
                
                Spacer(modifier = Modifier.width(4.dp))
                
                // Right side: Operators
                Column(modifier = Modifier.weight(1f).fillMaxHeight(), verticalArrangement = Arrangement.SpaceEvenly) {
                    val operatorKeys = listOf("÷", "×", "-", "+", "=")
                    operatorKeys.forEach { btn ->
                        Row(modifier = Modifier.fillMaxWidth().weight(1f).padding(vertical = 4.dp), horizontalArrangement = Arrangement.SpaceEvenly, verticalAlignment = Alignment.CenterVertically) {
                            CalculatorButton(text = btn, onClick = { onAction(btn) }, isScientific = false, isDark = isDark, primaryColor = primaryColor, modifier = Modifier.weight(1f).padding(horizontal = 4.dp))
                        }
                    }
                }
            }"""

new_content = re.sub(pattern, replacement, content)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(new_content)
