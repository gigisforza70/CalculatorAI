import re

with open('app/src/main/java/com/example/ui/UnitConverter.kt', 'r') as f:
    content = f.read()

# Add padding to Keypad so it matches CalculatorApp's width and bottom spacing
content = content.replace(
    'Column(verticalArrangement = Arrangement.Bottom, modifier = Modifier.fillMaxWidth()) {',
    'Column(verticalArrangement = Arrangement.Bottom, modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp)) {'
)

# Also CalculatorApp doesn't have Spacer(16.dp) at the bottom, but it has padding(16.dp) on the column.
# In UnitConverter, we currently have Spacer(modifier = Modifier.height(16.dp)) below Keypad.
# But if it overflows, it's pushed down.

# Wrap Inputs in a weight(1f) to prevent pushing keypad off-screen
old_layout = """        if (useRowLayout) {
            Row(modifier = Modifier.fillMaxSize()) {
                Column(modifier = Modifier.weight(1f).fillMaxHeight()) {
                    Input1(
                        unit1 = unit1,
                        focus1 = focus1,
                        value1 = value1,
                        expanded1 = expanded1,
                        onExpanded1Change = { expanded1 = it },
                        onUnit1Change = { unit1 = it; expanded1 = false; updateValues(value1, true) },
                        onValue1Change = { updateValues(it, true) },
                        onFocusChange = { focus1 = true },
                        currentUnitsList = currentUnitsList,
                        primaryColor = primaryColor,
                        secondaryTextColor = secondaryTextColor,
                        isDark = isDark,
                        focusRequester = focusRequester1
                    )
                    
                    HorizontalDivider(modifier = Modifier.fillMaxWidth(), color = if (isDark) Color(0xFF2B2B2B) else Color(0xFFE0E0E0))
                    
                    Input2(
                        unit2 = unit2,
                        focus1 = focus1,
                        value2 = value2,
                        expanded2 = expanded2,
                        onExpanded2Change = { expanded2 = it },
                        onUnit2Change = { unit2 = it; expanded2 = false; updateValues(value2, false) },
                        onValue2Change = { updateValues(it, false) },
                        onFocusChange = { focus1 = false },
                        currentUnitsList = currentUnitsList,
                        primaryColor = primaryColor,
                        secondaryTextColor = secondaryTextColor,
                        isDark = isDark,
                        focusRequester = focusRequester2
                    )
                }
                
                Box(modifier = Modifier.weight(1f).fillMaxHeight(), contentAlignment = Alignment.BottomCenter) {
                    Keypad(
                        onAction = onAction,
                        focus1 = focus1,
                        onFocusChange = { focus1 = it },
                        isDark = isDark,
                        primaryColor = primaryColor
                    )
                }
            }
        } else {
            Spacer(modifier = Modifier.weight(1f))
            
            Input1(
                unit1 = unit1,
                focus1 = focus1,
                value1 = value1,
                expanded1 = expanded1,
                onExpanded1Change = { expanded1 = it },
                onUnit1Change = { unit1 = it; expanded1 = false; updateValues(value1, true) },
                onValue1Change = { updateValues(it, true) },
                onFocusChange = { focus1 = true },
                currentUnitsList = currentUnitsList,
                primaryColor = primaryColor,
                secondaryTextColor = secondaryTextColor,
                isDark = isDark,
                focusRequester = focusRequester1
            )
            
            HorizontalDivider(modifier = Modifier.fillMaxWidth().padding(horizontal = 24.dp), color = if (isDark) Color(0xFF2B2B2B) else Color(0xFFE0E0E0))
            
            Input2(
                unit2 = unit2,
                focus1 = focus1,
                value2 = value2,
                expanded2 = expanded2,
                onExpanded2Change = { expanded2 = it },
                onUnit2Change = { unit2 = it; expanded2 = false; updateValues(value2, false) },
                onValue2Change = { updateValues(it, false) },
                onFocusChange = { focus1 = false },
                currentUnitsList = currentUnitsList,
                primaryColor = primaryColor,
                secondaryTextColor = secondaryTextColor,
                isDark = isDark,
                focusRequester = focusRequester2
            )
            
            Spacer(modifier = Modifier.weight(1f))
            
            Keypad(
                onAction = onAction,
                focus1 = focus1,
                onFocusChange = { focus1 = it },
                isDark = isDark,
                primaryColor = primaryColor
            )
            Spacer(modifier = Modifier.height(16.dp))
        }"""

new_layout = """        if (useRowLayout) {
            Row(modifier = Modifier.fillMaxSize()) {
                Column(modifier = Modifier.weight(1f).fillMaxHeight()) {
                    Input1(
                        unit1 = unit1,
                        focus1 = focus1,
                        value1 = value1,
                        expanded1 = expanded1,
                        onExpanded1Change = { expanded1 = it },
                        onUnit1Change = { unit1 = it; expanded1 = false; updateValues(value1, true) },
                        onValue1Change = { updateValues(it, true) },
                        onFocusChange = { focus1 = true },
                        currentUnitsList = currentUnitsList,
                        primaryColor = primaryColor,
                        secondaryTextColor = secondaryTextColor,
                        isDark = isDark,
                        focusRequester = focusRequester1
                    )
                    
                    HorizontalDivider(modifier = Modifier.fillMaxWidth(), color = if (isDark) Color(0xFF2B2B2B) else Color(0xFFE0E0E0))
                    
                    Input2(
                        unit2 = unit2,
                        focus1 = focus1,
                        value2 = value2,
                        expanded2 = expanded2,
                        onExpanded2Change = { expanded2 = it },
                        onUnit2Change = { unit2 = it; expanded2 = false; updateValues(value2, false) },
                        onValue2Change = { updateValues(it, false) },
                        onFocusChange = { focus1 = false },
                        currentUnitsList = currentUnitsList,
                        primaryColor = primaryColor,
                        secondaryTextColor = secondaryTextColor,
                        isDark = isDark,
                        focusRequester = focusRequester2
                    )
                }
                
                Box(modifier = Modifier.weight(1f).fillMaxHeight(), contentAlignment = Alignment.BottomCenter) {
                    Keypad(
                        onAction = onAction,
                        focus1 = focus1,
                        onFocusChange = { focus1 = it },
                        isDark = isDark,
                        primaryColor = primaryColor
                    )
                }
            }
        } else {
            Column(modifier = Modifier.weight(1f)) {
                Spacer(modifier = Modifier.weight(1f))
                
                Input1(
                    unit1 = unit1,
                    focus1 = focus1,
                    value1 = value1,
                    expanded1 = expanded1,
                    onExpanded1Change = { expanded1 = it },
                    onUnit1Change = { unit1 = it; expanded1 = false; updateValues(value1, true) },
                    onValue1Change = { updateValues(it, true) },
                    onFocusChange = { focus1 = true },
                    currentUnitsList = currentUnitsList,
                    primaryColor = primaryColor,
                    secondaryTextColor = secondaryTextColor,
                    isDark = isDark,
                    focusRequester = focusRequester1
                )
                
                HorizontalDivider(modifier = Modifier.fillMaxWidth().padding(horizontal = 24.dp), color = if (isDark) Color(0xFF2B2B2B) else Color(0xFFE0E0E0))
                
                Input2(
                    unit2 = unit2,
                    focus1 = focus1,
                    value2 = value2,
                    expanded2 = expanded2,
                    onExpanded2Change = { expanded2 = it },
                    onUnit2Change = { unit2 = it; expanded2 = false; updateValues(value2, false) },
                    onValue2Change = { updateValues(it, false) },
                    onFocusChange = { focus1 = false },
                    currentUnitsList = currentUnitsList,
                    primaryColor = primaryColor,
                    secondaryTextColor = secondaryTextColor,
                    isDark = isDark,
                    focusRequester = focusRequester2
                )
                
                Spacer(modifier = Modifier.weight(1f))
            }
            
            Keypad(
                onAction = onAction,
                focus1 = focus1,
                onFocusChange = { focus1 = it },
                isDark = isDark,
                primaryColor = primaryColor
            )
            Spacer(modifier = Modifier.height(16.dp))
        }"""

content = content.replace(old_layout, new_layout)

with open('app/src/main/java/com/example/ui/UnitConverter.kt', 'w') as f:
    f.write(content)

