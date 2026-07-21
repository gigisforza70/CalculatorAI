import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Extract the isTabletLandscape block
start_idx = content.find('} else if (isTabletLandscape) {')
end_idx = content.find('} else if (isLandscape) {')

replacement = """} else if (isTabletLandscape) {
            val tabletPortraitKeys = listOf(
                listOf("sin", "cos", "tan", "^", "C", "( )", "%", "÷"),
                listOf("asn", "acs", "atn", "!", "7", "8", "9", "×"),
                listOf("snh", "csh", "tnh", "√", "4", "5", "6", "-"),
                listOf("ash", "ach", "ath", "π", "1", "2", "3", "+"),
                listOf("ln", "lg", "g", "e", "+/-", "0", ",", "=")
            )
            Row(modifier = Modifier.fillMaxWidth().horizontalScroll(rememberScrollState()).weight(1.5f), horizontalArrangement = Arrangement.Center) {
                if (showHistory) {
                    // Left side (History permanently shown) -> Now toggleable
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
                       
                    Spacer(modifier = Modifier.width(16.dp))
                    Box(modifier = Modifier.width(1.dp).fillMaxHeight().padding(vertical = 16.dp).background(if(isDark) Color(0xFF2B2B2B) else Color(0xFFE0E0E0)))
                    Spacer(modifier = Modifier.width(16.dp))
                } else {
                    Spacer(modifier = Modifier.weight(0.5f))
                    Spacer(modifier = Modifier.width(16.5.dp))
                }
                   
                // Right side (tablet portrait keys layout) -> Now Center side
                Column(modifier = Modifier.weight(2.5f).fillMaxHeight(), verticalArrangement = Arrangement.SpaceEvenly) {
                    tabletPortraitKeys.forEach { row ->
                        Row(
                            modifier = Modifier.fillMaxWidth().horizontalScroll(rememberScrollState()).weight(1f).padding(vertical = 4.dp),
                            horizontalArrangement = Arrangement.SpaceEvenly,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            row.forEach { btn ->
                                CalculatorButton(
                                    text = btn,
                                    onClick = { onAction(btn) },
                                    isScientific = true,
                                    isDark = isDark,
                                    primaryColor = primaryColor,
                                    modifier = Modifier.weight(1f).padding(horizontal = 4.dp),
                                    isLandscape = false,
                                    isTabletPortrait = true
                                )
                            }
                        }
                    }
                }

                if (!showHistory) {
                    Spacer(modifier = Modifier.width(16.5.dp))
                    Spacer(modifier = Modifier.weight(0.5f))
                }
            }
        """

new_content = content[:start_idx] + replacement + content[end_idx:]

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(new_content)
