import re

with open('app/src/main/java/com/example/ui/UnitConverter.kt', 'r') as f:
    content = f.read()

# Fix Input1
replacement1 = """        androidx.compose.foundation.text.BasicTextField(
                value = value1,
                onValueChange = { newValue ->
                    if (newValue.text.matches(Regex("[0-9.,-]*")) && newValue.text.count { it.isDigit() } <= 15) {
                        onValue1Change(newValue)
                    }
                },
                textStyle = androidx.compose.ui.text.TextStyle(
                    fontSize = 48.sp,
                    color = if(focus1) primaryColor else (if(isDark) Color(0xFFFBFBFB) else Color(0xFF141414))
                ),
                singleLine = true,
                readOnly = true,
                visualTransformation = ExpressionVisualTransformation(),
                modifier = Modifier.fillMaxWidth().focusRequester(focusRequester).onFocusChanged { if (it.isFocused) onFocusChange() },
                cursorBrush = androidx.compose.ui.graphics.SolidColor(primaryColor),
                decorationBox = { innerTextField ->
                    Row(verticalAlignment = Alignment.Bottom) {
                        Box(modifier = Modifier.weight(1f, fill = false)) {
                            innerTextField()
                        }
                        Spacer(modifier = Modifier.width(8.dp))
                        Text(
                            text = unit1.symbol,
                            fontSize = 24.sp,
                            color = if(focus1) primaryColor else (if(isDark) Color(0xFFA0A0A0) else Color(0xFF707070)),
                            modifier = Modifier.padding(bottom = 8.dp)
                        )
                    }
                }
            )"""

content = re.sub(
    r'androidx\.compose\.foundation\.text\.BasicTextField\([\s\S]*?cursorBrush = androidx\.compose\.ui\.graphics\.SolidColor\(primaryColor\)\s*\)',
    replacement1,
    content,
    count=1
)

# Fix Input2
replacement2 = """        androidx.compose.foundation.text.BasicTextField(
                value = value2,
                onValueChange = { newValue ->
                    if (newValue.text.matches(Regex("[0-9.,-]*")) && newValue.text.count { it.isDigit() } <= 15) {
                        onValue2Change(newValue)
                    }
                },
                textStyle = androidx.compose.ui.text.TextStyle(
                    fontSize = 48.sp,
                    color = if(!focus1) primaryColor else (if(isDark) Color(0xFFFBFBFB) else Color(0xFF141414))
                ),
                singleLine = true,
                readOnly = true,
                visualTransformation = ExpressionVisualTransformation(),
                modifier = Modifier.fillMaxWidth().focusRequester(focusRequester).onFocusChanged { if (it.isFocused) onFocusChange() },
                cursorBrush = androidx.compose.ui.graphics.SolidColor(primaryColor),
                decorationBox = { innerTextField ->
                    Row(verticalAlignment = Alignment.Bottom) {
                        Box(modifier = Modifier.weight(1f, fill = false)) {
                            innerTextField()
                        }
                        Spacer(modifier = Modifier.width(8.dp))
                        Text(
                            text = unit2.symbol,
                            fontSize = 24.sp,
                            color = if(!focus1) primaryColor else (if(isDark) Color(0xFFA0A0A0) else Color(0xFF707070)),
                            modifier = Modifier.padding(bottom = 8.dp)
                        )
                    }
                }
            )"""

content = re.sub(
    r'androidx\.compose\.foundation\.text\.BasicTextField\([\s\S]*?cursorBrush = androidx\.compose\.ui\.graphics\.SolidColor\(primaryColor\)\s*\)',
    replacement2,
    content,
    count=1 # It will find the second one because the first one has decorationBox now, but regex might match the first one again if it matches. Wait, regex doesn't match decorationBox because it ends at cursorBrush. 
)

with open('app/src/main/java/com/example/ui/UnitConverter.kt', 'w') as f:
    f.write(content)
