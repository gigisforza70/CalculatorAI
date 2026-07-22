import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# I will find the part to replace by matching from '        } else if (isLandscape) {' (at the end of my new block) up to '                        Modifier.fillMaxWidth(0.95f).height(buttonHeight)'

pattern = re.compile(r'        \} else if \(isLandscape\) \{[\s\S]*?                        Modifier\.fillMaxWidth\(0\.95f\)\.height\(buttonHeight\)')

replacement = """        } else if (isLandscape) {
            val landscapeScientific = listOf(
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
                if (showHistory) {
                    Box(modifier = Modifier.weight(3f).fillMaxHeight()) {
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
                    }
                } else {
                    Column(modifier = Modifier.weight(3f).fillMaxHeight(), verticalArrangement = Arrangement.SpaceEvenly) {
                        landscapeScientific.forEach { row ->
                            Row(modifier = Modifier.fillMaxWidth().weight(1f).padding(vertical = 2.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                                row.forEach { btn ->
                                    CalculatorButton(text = btn, onClick = { onAction(btn) }, isScientific = true, isDark = isDark, primaryColor = primaryColor, modifier = Modifier.weight(1f), isLandscape = true)
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
                                CalculatorButton(text = btn, onClick = { onAction(btn) }, isScientific = false, isDark = isDark, primaryColor = primaryColor, modifier = Modifier.weight(1f), isLandscape = true)
                            }
                        }
                    }
                }

                // Right side (Empty space to balance the left side)
                Box(modifier = Modifier.weight(3f).fillMaxHeight())
            }
        } else {
            // Standard portrait layout
            val portraitKeys = listOf(
                listOf("C", "( )", "%", "÷"),
                listOf("7", "8", "9", "×"),
                listOf("4", "5", "6", "-"),
                listOf("1", "2", "3", "+"),
                listOf("+/-", "0", ",", "=")
            )
            Box(modifier = Modifier.fillMaxWidth().weight(1.5f)) {
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
                } else {
                    Column(modifier = Modifier.fillMaxSize(), verticalArrangement = Arrangement.SpaceEvenly) {
                        portraitKeys.forEach { row ->
                            Row(modifier = Modifier.fillMaxWidth().weight(1f).padding(vertical = 4.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                                row.forEach { btn ->
                                    CalculatorButton(text = btn, onClick = { onAction(btn) }, isScientific = false, isDark = isDark, primaryColor = primaryColor, modifier = Modifier.weight(1f))
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun CalculatorButton(text: String, onClick: () -> Unit, isScientific: Boolean = false, isDark: Boolean = true, primaryColor: Color = Color(0xFF2196F3), modifier: Modifier = Modifier, isLandscape: Boolean = false, isTabletPortrait: Boolean = false) {
    val isRed = text == "C"
    val isOperator = text in listOf("÷", "×", "-", "+", "( )", "%")
    val isEqual = text == "="
    
    val bgColor = if (isEqual) primaryColor
        else if (isRed) (if (isDark) Color(0xFF3A2121) else Color(0xFFFFEAEA))
        else if (isOperator) (if (isDark) Color(0xFF2B2B2B) else Color(0xFFE0E0E0))
        else if (isScientific) (if (isDark) Color(0xFF1E1E1E) else Color(0xFFF0F0F0))
        else (if (isDark) Color(0xFF222222) else Color(0xFFF5F5F5))
        
    val textColor = if (isEqual) Color.White
        else if (isRed) Color(0xFFE57373)
        else if (isOperator) primaryColor
        else if (isDark) Color.White else Color.Black

    val buttonHeight = if (isTabletPortrait) 64.dp else if (isLandscape) 48.dp else if (isScientific) 52.dp else 76.dp
    val fontSize = if (isTabletPortrait) 24.sp else if (isLandscape) 20.sp else if (isScientific) 24.sp else 36.sp

    Box(
        modifier = modifier,
        contentAlignment = Alignment.Center
    ) {
        Box(
            modifier = Modifier
                .then(
                    if (isTabletPortrait) {
                        Modifier.fillMaxWidth(0.95f).height(buttonHeight)
                    } else if (isLandscape) {
                        Modifier.fillMaxWidth(0.95f).height(buttonHeight)"""

content = pattern.sub(replacement, content)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

