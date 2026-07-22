import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# I will replace the entire 'if (isTabletPortrait)' and 'else if (isTabletLandscape)' blocks.

new_logic = """        if (isTabletPortrait) {
            val scientificKeys = listOf(
                listOf("sin", "cos", "tan", "^"),
                listOf("asn", "acs", "atn", "!"),
                listOf("snh", "csh", "tnh", "√"),
                listOf("ash", "ach", "ath", "π"),
                listOf("ln", "lg", "g", "e")
            )
            val standardKeys = listOf(
                listOf("C", "( )", "%", "÷"),
                listOf("7", "8", "9", "×"),
                listOf("4", "5", "6", "-"),
                listOf("1", "2", "3", "+"),
                listOf("+/-", "0", ",", "=")
            )
            Row(modifier = Modifier.fillMaxWidth().weight(1.5f), horizontalArrangement = Arrangement.SpaceBetween) {
                // Left side: History OR Scientific Keys
                if (showHistory) {
                    Box(modifier = Modifier.weight(1f).fillMaxHeight()) {
                        if (history.isEmpty()) {
                            Text(
                                "Qui vedrai la cronologia\\ndei calcoli.",
                                textAlign = TextAlign.Center,
                                color = if(isDark) Color(0xFFA0A0A0) else Color(0xFF707070),
                                modifier = Modifier.align(Alignment.Center)
                            )
                        } else {
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
                        }
                    }
                } else {
                    Column(modifier = Modifier.weight(1f).fillMaxHeight(), verticalArrangement = Arrangement.SpaceEvenly) {
                        scientificKeys.forEach { row ->
                            Row(modifier = Modifier.fillMaxWidth().weight(1f).padding(vertical = 4.dp), horizontalArrangement = Arrangement.SpaceEvenly, verticalAlignment = Alignment.CenterVertically) {
                                row.forEach { btn ->
                                    CalculatorButton(text = btn, onClick = { onAction(btn) }, isScientific = true, isDark = isDark, primaryColor = primaryColor, modifier = Modifier.weight(1f).padding(horizontal = 4.dp), isTabletPortrait = true)
                                }
                            }
                        }
                    }
                }
                
                // Divider if history is shown (optional, but looks good)
                if (showHistory) {
                    Spacer(modifier = Modifier.width(8.dp))
                    Box(modifier = Modifier.width(1.dp).fillMaxHeight().padding(vertical = 16.dp).background(if(isDark) Color(0xFF2B2B2B) else Color(0xFFE0E0E0)))
                    Spacer(modifier = Modifier.width(8.dp))
                }
                
                // Right side: Standard Keys
                Column(modifier = Modifier.weight(1f).fillMaxHeight(), verticalArrangement = Arrangement.SpaceEvenly) {
                    standardKeys.forEach { row ->
                        Row(modifier = Modifier.fillMaxWidth().weight(1f).padding(vertical = 4.dp), horizontalArrangement = Arrangement.SpaceEvenly, verticalAlignment = Alignment.CenterVertically) {
                            row.forEach { btn ->
                                val isNumOrOp = btn in listOf("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", ",", "+/-", "+", "-", "×", "÷", "=", "C", "%", "( )")
                                CalculatorButton(text = btn, onClick = { onAction(btn) }, isScientific = !isNumOrOp, isDark = isDark, primaryColor = primaryColor, modifier = Modifier.weight(1f).padding(horizontal = 4.dp), isTabletPortrait = true)
                            }
                        }
                    }
                }
            }
        } else if (isTabletLandscape) {"""

# Find the block starting with "if (isTabletPortrait) {" and ending before "else if (isLandscape) {"
# Let's use regex to replace it
pattern = re.compile(r'if \(isTabletPortrait\) \{.*?\} else if \(isLandscape\) \{', re.DOTALL)

# The replacement should also include the tablet landscape layout (which we'll restore as the old isTabletPortrait layout)
tablet_landscape_layout = """            val landscapeScientific = listOf(
                listOf("2nd", "deg", "sin"),
                listOf("cos", "tan", "x^y"),
                listOf("lg", "ln", "x²"),
                listOf("|x|", "√x", "x!"),
                listOf("1/x", "π", "e")
            )
            val landscapeStandard = listOf(
                listOf("C", "( )", "%", "÷"),
                listOf("7", "8", "9", "×"),
                listOf("4", "5", "6", "-"),
                listOf("1", "2", "3", "+"),
                listOf("+/-", "0", ",", "=")
            )
            Row(modifier = Modifier.fillMaxWidth().weight(1.5f), horizontalArrangement = Arrangement.SpaceBetween) {
                // Left side (Scientific or History)
                Box(modifier = Modifier.weight(3f).fillMaxHeight()) {
                    if (showHistory) {
                        if (history.isEmpty()) {
                            Text(
                                "Qui vedrai la cronologia\\ndei calcoli.",
                                textAlign = TextAlign.Center,
                                color = if(isDark) Color(0xFFA0A0A0) else Color(0xFF707070),
                                modifier = Modifier.align(Alignment.Center)
                            )
                        } else {
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
                        }
                    } else {
                        Column(modifier = Modifier.fillMaxSize(), verticalArrangement = Arrangement.SpaceEvenly) {
                            landscapeScientific.forEach { row ->
                                Row(modifier = Modifier.fillMaxWidth().weight(1f).padding(vertical = 2.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                                    row.forEach { btn ->
                                        CalculatorButton(text = btn, onClick = { onAction(btn) }, isScientific = true, isDark = isDark, primaryColor = primaryColor, modifier = Modifier.weight(1f), isLandscape = true)
                                    }
                                }
                            }
                        }
                    }
                }
                    
                Spacer(modifier = Modifier.width(8.dp))
                Box(modifier = Modifier.width(1.dp).fillMaxHeight().padding(vertical = 16.dp).background(if(isDark && !showHistory) Color(0xFF2B2B2B) else if (!isDark && !showHistory) Color(0xFFE0E0E0) else Color.Transparent))
                Spacer(modifier = Modifier.width(8.dp))

                // Center side (Standard Keypad)
                Column(modifier = Modifier.weight(4f).fillMaxHeight(), verticalArrangement = Arrangement.SpaceEvenly) {
                    landscapeStandard.forEach { row ->
                        Row(modifier = Modifier.fillMaxWidth().weight(1f).padding(vertical = 2.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                            row.forEach { btn ->
                                val isNumOrOp = btn in listOf("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", ",", "+/-", "+", "-", "×", "÷", "=", "C", "%", "( )")
                                CalculatorButton(text = btn, onClick = { onAction(btn) }, isScientific = !isNumOrOp, isDark = isDark, primaryColor = primaryColor, modifier = Modifier.weight(1f), isLandscape = true)
                            }
                        }
                    }
                }

                // Right side (Empty space to balance the left side)
                Box(modifier = Modifier.weight(3f).fillMaxHeight())
            }
        } else if (isLandscape) {"""

new_content = pattern.sub(new_logic + tablet_landscape_layout, content)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(new_content)
