import re

with open('app/src/main/java/com/example/ui/UnitConverter.kt', 'r') as f:
    content = f.read()

# Replace the layout part from Column(modifier=Modifier.fillMaxSize().background(bgColor)) { ... }
# with a new adaptive layout.

# Find the start of the Column layout
start_idx = content.find('    Column(\n        modifier = Modifier\n            .fillMaxSize()')

if start_idx == -1:
    print("Could not find start of Column layout")
    exit(1)

pre_content = content[:start_idx]

new_layout = """
    val configuration = androidx.compose.ui.platform.LocalConfiguration.current
    val isLandscape = configuration.orientation == android.content.res.Configuration.ORIENTATION_LANDSCAPE
    val isTablet = configuration.screenWidthDp >= 600
    val useRowLayout = isLandscape || isTablet

    val focusRequester1 = remember { androidx.compose.ui.focus.FocusRequester() }
    val focusRequester2 = remember { androidx.compose.ui.focus.FocusRequester() }

    LaunchedEffect(focus1) {
        try {
            if (focus1) focusRequester1.requestFocus() else focusRequester2.requestFocus()
        } catch (e: Exception) {}
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(bgColor)
    ) {
        TopAppBar(
            title = { Text("Unit converter", color = textColor) },
            navigationIcon = {
                IconButton(onClick = onBack) {
                    Icon(Icons.AutoMirrored.Filled.ArrowBack, "Back", tint = textColor)
                }
            },
            colors = TopAppBarDefaults.topAppBarColors(containerColor = bgColor)
        )
        
        LazyRow(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 8.dp)
        ) {
            items(UnitCategory.values()) { category ->
                TextButton(onClick = { selectedCategory = category }) {
                    Text(
                        text = category.name,
                        color = if (selectedCategory == category) primaryColor else secondaryTextColor,
                        fontWeight = if (selectedCategory == category) FontWeight.Bold else FontWeight.Normal
                    )
                }
            }
        }
        
        if (useRowLayout) {
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
                    HorizontalDivider(color = if(isDark) Color(0xFF2B2B2B) else Color(0xFFE0E0E0), modifier = Modifier.padding(horizontal = 24.dp))
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
                Box(modifier = Modifier.weight(1f).fillMaxHeight().padding(bottom = 16.dp)) {
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
            HorizontalDivider(color = if(isDark) Color(0xFF2B2B2B) else Color(0xFFE0E0E0), modifier = Modifier.padding(horizontal = 24.dp))
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
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class, androidx.compose.ui.ExperimentalComposeUiApi::class)
@Composable
fun Input1(
    unit1: UnitType,
    focus1: Boolean,
    value1: String,
    expanded1: Boolean,
    onExpanded1Change: (Boolean) -> Unit,
    onUnit1Change: (UnitType) -> Unit,
    onValue1Change: (String) -> Unit,
    onFocusChange: () -> Unit,
    currentUnitsList: List<UnitType>,
    primaryColor: Color,
    secondaryTextColor: Color,
    isDark: Boolean,
    focusRequester: androidx.compose.ui.focus.FocusRequester
) {
    Column(modifier = Modifier
        .fillMaxWidth()
        .clickable { onFocusChange() }
        .padding(24.dp)) {
        ExposedDropdownMenuBox(
            expanded = expanded1,
            onExpandedChange = { onExpanded1Change(!expanded1) }
        ) {
            Row(modifier = Modifier.menuAnchor(MenuAnchorType.PrimaryEditable, true), verticalAlignment = Alignment.CenterVertically) {
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
        
        androidx.compose.ui.platform.InterceptPlatformTextInput(
            interceptor = { _, _ -> kotlinx.coroutines.awaitCancellation() }
        ) {
            androidx.compose.foundation.text.BasicTextField(
                value = value1,
                onValueChange = { newValue ->
                    if (newValue.matches(Regex("[0-9.,\\-]*"))) {
                        onValue1Change(newValue)
                    }
                },
                textStyle = androidx.compose.ui.text.TextStyle(
                    fontSize = 48.sp,
                    color = if(focus1) primaryColor else (if(isDark) Color(0xFFFBFBFB) else Color(0xFF141414))
                ),
                singleLine = true,
                readOnly = false,
                modifier = Modifier.fillMaxWidth().androidx.compose.ui.focus.focusRequester(focusRequester),
                cursorBrush = androidx.compose.ui.graphics.SolidColor(primaryColor)
            )
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class, androidx.compose.ui.ExperimentalComposeUiApi::class)
@Composable
fun Input2(
    unit2: UnitType,
    focus1: Boolean,
    value2: String,
    expanded2: Boolean,
    onExpanded2Change: (Boolean) -> Unit,
    onUnit2Change: (UnitType) -> Unit,
    onValue2Change: (String) -> Unit,
    onFocusChange: () -> Unit,
    currentUnitsList: List<UnitType>,
    primaryColor: Color,
    secondaryTextColor: Color,
    isDark: Boolean,
    focusRequester: androidx.compose.ui.focus.FocusRequester
) {
    Column(modifier = Modifier
        .fillMaxWidth()
        .clickable { onFocusChange() }
        .padding(24.dp)) {
        ExposedDropdownMenuBox(
            expanded = expanded2,
            onExpandedChange = { onExpanded2Change(!expanded2) }
        ) {
            Row(modifier = Modifier.menuAnchor(MenuAnchorType.PrimaryEditable, true), verticalAlignment = Alignment.CenterVertically) {
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
        
        androidx.compose.ui.platform.InterceptPlatformTextInput(
            interceptor = { _, _ -> kotlinx.coroutines.awaitCancellation() }
        ) {
            androidx.compose.foundation.text.BasicTextField(
                value = value2,
                onValueChange = { newValue ->
                    if (newValue.matches(Regex("[0-9.,\\-]*"))) {
                        onValue2Change(newValue)
                    }
                },
                textStyle = androidx.compose.ui.text.TextStyle(
                    fontSize = 48.sp,
                    color = if(!focus1) primaryColor else (if(isDark) Color(0xFFFBFBFB) else Color(0xFF141414))
                ),
                singleLine = true,
                readOnly = false,
                modifier = Modifier.fillMaxWidth().androidx.compose.ui.focus.focusRequester(focusRequester),
                cursorBrush = androidx.compose.ui.graphics.SolidColor(primaryColor)
            )
        }
    }
}

@Composable
fun Keypad(
    onAction: (String) -> Unit,
    focus1: Boolean,
    onFocusChange: (Boolean) -> Unit,
    isDark: Boolean,
    primaryColor: Color
) {
    val pad = listOf(
        listOf("7", "8", "9", "backspace"),
        listOf("4", "5", "6", "C"),
        listOf("1", "2", "3", "up"),
        listOf("+/-", "0", ",", "down")
    )
    Column(verticalArrangement = Arrangement.Bottom, modifier = Modifier.fillMaxSize()) {
        pad.forEach { row ->
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 4.dp, vertical = 2.dp),
                horizontalArrangement = Arrangement.SpaceEvenly
            ) {
                row.forEach { btn ->
                    Box(modifier = Modifier.weight(1f), contentAlignment = Alignment.Center) {
                        if (btn == "backspace") {
                            Box(
                                modifier = Modifier
                                    .size(84.dp)
                                    .clip(androidx.compose.foundation.shape.CircleShape)
                                    .background(if(isDark) Color(0xFF2B2B2B) else Color(0xFFE8E8E8))
                                    .clickable { onAction("backspace") },
                                contentAlignment = Alignment.Center
                            ) {
                                Icon(Icons.AutoMirrored.Filled.Backspace, "Backspace", tint = primaryColor)
                            }
                        } else if (btn == "up") {
                            Box(
                                modifier = Modifier
                                    .size(84.dp)
                                    .clip(androidx.compose.foundation.shape.CircleShape)
                                    .background(if(isDark) Color(0xFF2B2B2B) else Color(0xFFE8E8E8))
                                    .clickable { onFocusChange(true) },
                                contentAlignment = Alignment.Center
                            ) {
                                Icon(Icons.Default.ArrowUpward, "Up", tint = primaryColor)
                            }
                        } else if (btn == "down") {
                            Box(
                                modifier = Modifier
                                    .size(84.dp)
                                    .clip(androidx.compose.foundation.shape.CircleShape)
                                    .background(if(isDark) Color(0xFF2B2B2B) else Color(0xFFE8E8E8))
                                    .clickable { onFocusChange(false) },
                                contentAlignment = Alignment.Center
                            ) {
                                Icon(Icons.Default.ArrowDownward, "Down", tint = primaryColor)
                            }
                        } else {
                            com.example.CalculatorButton(
                                text = btn,
                                onClick = { onAction(btn) },
                                isDark = isDark,
                                primaryColor = primaryColor
                            )
                        }
                    }
                }
            }
        }
    }
}
"""

end_funcs = content.find('fun convertTemp(')

post_content = content[end_funcs:]

with open('app/src/main/java/com/example/ui/UnitConverter.kt', 'w') as f:
    f.write(pre_content + new_layout + post_content)
