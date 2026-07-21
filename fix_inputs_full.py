import re

with open('app/src/main/java/com/example/ui/UnitConverter.kt', 'r') as f:
    content = f.read()

start_idx = content.find('@OptIn(ExperimentalMaterial3Api::class, androidx.compose.ui.ExperimentalComposeUiApi::class)\n@Composable\nfun Input1(')
end_idx = content.find('@Composable\nfun Keypad(')

replacement = """@OptIn(ExperimentalMaterial3Api::class, androidx.compose.ui.ExperimentalComposeUiApi::class)
@Composable
fun Input1(
    unit1: UnitType,
    focus1: Boolean,
    value1: TextFieldValue,
    expanded1: Boolean,
    onExpanded1Change: (Boolean) -> Unit,
    onUnit1Change: (UnitType) -> Unit,
    onValue1Change: (TextFieldValue) -> Unit,
    onFocusChange: () -> Unit,
    currentUnitsList: List<UnitType>,
    primaryColor: Color,
    secondaryTextColor: Color,
    isDark: Boolean,
    focusRequester: androidx.compose.ui.focus.FocusRequester
) {
    Column(modifier = Modifier
        .fillMaxWidth()
        .padding(vertical = 12.dp, horizontal = 24.dp)) {
        ExposedDropdownMenuBox(
            expanded = expanded1,
            onExpandedChange = { onExpanded1Change(!expanded1) }
        ) {
            Row(modifier = Modifier.menuAnchor(androidx.compose.material3.MenuAnchorType.PrimaryEditable, true), verticalAlignment = Alignment.CenterVertically) {
                Text(
                    text = unit1.name,
                    color = if(focus1) primaryColor else secondaryTextColor,
                    fontSize = 16.sp
                )
                Spacer(modifier = Modifier.width(4.dp))
                Icon(
                    imageVector = Icons.Default.ArrowDropDown,
                    contentDescription = "Dropdown",
                    tint = if(focus1) primaryColor else secondaryTextColor
                )
            }
            ExposedDropdownMenu(
                expanded = expanded1,
                onDismissRequest = { onExpanded1Change(false) },
                modifier = Modifier.background(if(isDark) Color(0xFF2B2B2B) else Color(0xFFF0F0F0))
            ) {
                currentUnitsList.forEach { unit ->
                    DropdownMenuItem(
                        text = { Text(unit.name, color = if(isDark) Color.White else Color.Black) },
                        onClick = { onUnit1Change(unit) }
                    )
                }
            }
        }
        
        androidx.compose.foundation.text.BasicTextField(
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
        )
    }
}

@OptIn(ExperimentalMaterial3Api::class, androidx.compose.ui.ExperimentalComposeUiApi::class)
@Composable
fun Input2(
    unit2: UnitType,
    focus1: Boolean,
    value2: TextFieldValue,
    expanded2: Boolean,
    onExpanded2Change: (Boolean) -> Unit,
    onUnit2Change: (UnitType) -> Unit,
    onValue2Change: (TextFieldValue) -> Unit,
    onFocusChange: () -> Unit,
    currentUnitsList: List<UnitType>,
    primaryColor: Color,
    secondaryTextColor: Color,
    isDark: Boolean,
    focusRequester: androidx.compose.ui.focus.FocusRequester
) {
    Column(modifier = Modifier
        .fillMaxWidth()
        .padding(vertical = 12.dp, horizontal = 24.dp)) {
        ExposedDropdownMenuBox(
            expanded = expanded2,
            onExpandedChange = { onExpanded2Change(!expanded2) }
        ) {
            Row(modifier = Modifier.menuAnchor(androidx.compose.material3.MenuAnchorType.PrimaryEditable, true), verticalAlignment = Alignment.CenterVertically) {
                Text(
                    text = unit2.name,
                    color = if(!focus1) primaryColor else secondaryTextColor,
                    fontSize = 16.sp
                )
                Spacer(modifier = Modifier.width(4.dp))
                Icon(
                    imageVector = Icons.Default.ArrowDropDown,
                    contentDescription = "Dropdown",
                    tint = if(!focus1) primaryColor else secondaryTextColor
                )
            }
            ExposedDropdownMenu(
                expanded = expanded2,
                onDismissRequest = { onExpanded2Change(false) },
                modifier = Modifier.background(if(isDark) Color(0xFF2B2B2B) else Color(0xFFF0F0F0))
            ) {
                currentUnitsList.forEach { unit ->
                    DropdownMenuItem(
                        text = { Text(unit.name, color = if(isDark) Color.White else Color.Black) },
                        onClick = { onUnit2Change(unit) }
                    )
                }
            }
        }
        
        androidx.compose.foundation.text.BasicTextField(
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
        )
    }
}

"""

new_content = content[:start_idx] + replacement + content[end_idx:]

with open('app/src/main/java/com/example/ui/UnitConverter.kt', 'w') as f:
    f.write(new_content)

