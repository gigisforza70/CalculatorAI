import re

with open('app/src/main/java/com/example/ui/UnitConverter.kt', 'r') as f:
    content = f.read()

# Reconstruct everything
new_code = """package com.example.ui

import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.focus.onFocusChanged
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.automirrored.filled.Backspace
import androidx.compose.material.icons.filled.ArrowDownward
import androidx.compose.material.icons.filled.ArrowDropDown
import androidx.compose.material.icons.filled.ArrowUpward
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.draw.clip
import androidx.compose.ui.text.input.TextFieldValue
import androidx.compose.ui.text.TextRange

enum class UnitCategory { Length, Area, Temperature, Volume, Mass, Data }

data class UnitType(val name: String, val value: Double)

val lengthUnits = listOf(UnitType("Nanometers", 1e-9), UnitType("Micrometers", 1e-6), UnitType("Millimeters", 0.001), UnitType("Centimeters", 0.01), UnitType("Decimeters", 0.1), UnitType("Meters", 1.0), UnitType("Kilometers", 1000.0), UnitType("Inches", 0.0254), UnitType("Feet", 0.3048), UnitType("Yards", 0.9144), UnitType("Miles", 1609.344), UnitType("Nautical miles", 1852.0))
val areaUnits = listOf(UnitType("Square millimeters", 0.000001), UnitType("Square centimeters", 0.0001), UnitType("Square meters", 1.0), UnitType("Hectares", 10000.0), UnitType("Square kilometers", 1000000.0), UnitType("Square inches", 0.00064516), UnitType("Square feet", 0.09290304), UnitType("Square yards", 0.83612736), UnitType("Acres", 4046.8564224), UnitType("Square miles", 2589988.110336))
val volumeUnits = listOf(UnitType("Milliliters", 0.001), UnitType("Cubic centimeters", 0.001), UnitType("Liters", 1.0), UnitType("Cubic meters", 1000.0), UnitType("Teaspoons (US)", 0.00492892), UnitType("Tablespoons (US)", 0.0147868), UnitType("Fluid ounces (US)", 0.0295735), UnitType("Cups (US)", 0.236588), UnitType("Pints (US)", 0.473176), UnitType("Quarts (US)", 0.946353), UnitType("Gallons (US)", 3.78541), UnitType("Cubic inches", 0.0163871), UnitType("Cubic feet", 28.3168))
val massUnits = listOf(UnitType("Micrograms", 1e-9), UnitType("Milligrams", 1e-6), UnitType("Grams", 0.001), UnitType("Kilograms", 1.0), UnitType("Metric tonnes", 1000.0), UnitType("Ounces", 0.0283495), UnitType("Pounds", 0.453592), UnitType("Stones", 6.35029), UnitType("Short tons (US)", 907.185), UnitType("Long tons (UK)", 1016.05))
val dataUnits = listOf(UnitType("Bits", 0.125), UnitType("Bytes", 1.0), UnitType("Kilobits", 128.0), UnitType("Kilobytes", 1024.0), UnitType("Megabits", 131072.0), UnitType("Megabytes", 1048576.0), UnitType("Gigabits", 134217728.0), UnitType("Gigabytes", 1073741824.0), UnitType("Terabits", 137438953472.0), UnitType("Terabytes", 1099511627776.0), UnitType("Petabytes", 1125899906842624.0))

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun UnitConverterScreen(modifier: Modifier = Modifier, onBack: () -> Unit, isDark: Boolean = true, primaryColor: Color = Color(0xFF2196F3)) {
    var selectedCategory by remember { mutableStateOf(UnitCategory.Length) }
    
    var unit1 by remember { mutableStateOf(lengthUnits[5]) }
    var unit2 by remember { mutableStateOf(lengthUnits[3]) }
    
    var value1 by remember { mutableStateOf(TextFieldValue("0", TextRange(1))) }
    var value2 by remember { mutableStateOf(TextFieldValue("0", TextRange(1))) }
    
    var focus1 by remember { mutableStateOf(true) }
    var expanded1 by remember { mutableStateOf(false) }
    var expanded2 by remember { mutableStateOf(false) }

    val currentUnitsList = remember(selectedCategory) {
        when(selectedCategory) {
            UnitCategory.Length -> lengthUnits
            UnitCategory.Area -> areaUnits
            UnitCategory.Volume -> volumeUnits
            UnitCategory.Mass -> massUnits
            UnitCategory.Data -> dataUnits
            UnitCategory.Temperature -> listOf(UnitType("Celsius", 1.0), UnitType("Fahrenheit", 1.0), UnitType("Kelvin", 1.0))
        }
    }

    LaunchedEffect(selectedCategory) {
        unit1 = currentUnitsList[0]
        if (currentUnitsList.size > 1) {
            unit2 = currentUnitsList[1]
        } else {
            unit2 = currentUnitsList[0]
        }
        updateValuesInternal(value1, true, unit1, unit2, selectedCategory) { v1, v2 ->
            value1 = v1
            value2 = v2
        }
    }

    val updateValues = { inputField: TextFieldValue, isFirst: Boolean ->
        updateValuesInternal(inputField, isFirst, unit1, unit2, selectedCategory) { v1, v2 ->
            value1 = v1
            value2 = v2
        }
    }

    val onAction = { action: String ->
        val currentField = if (focus1) value1 else value2
        var text = currentField.text
        if (action == "C") {
            text = "0"
        } else if (action == "backspace") {
            if (text.isNotEmpty()) {
                text = text.dropLast(1)
            }
            if (text.isEmpty() || text == "-") {
                text = "0"
            }
        } else if (action == "+/-") {
            if (text != "0") {
                if (text.startsWith("-")) {
                    text = text.substring(1)
                } else {
                    text = "-" + text
                }
            }
        } else if (action == ",") {
            if (!text.contains(",")) {
                text += ","
            }
        } else {
            if (text == "0" && action != ",") {
                text = action
            } else {
                text += action
            }
        }
        val newField = TextFieldValue(text, TextRange(text.length))
        updateValues(newField, focus1)
    }

    val bgColor = if(isDark) Color(0xFF141414) else Color(0xFFFBFBFB)
    val textColor = if(isDark) Color.White else Color.Black
    val secondaryTextColor = if(isDark) Color(0xFFA0A0A0) else Color(0xFF707070)
    
    val configuration = androidx.compose.ui.platform.LocalConfiguration.current
    val isLandscape = configuration.orientation == android.content.res.Configuration.ORIENTATION_LANDSCAPE
    val isTablet = configuration.screenWidthDp >= 600
    val useRowLayout = isLandscape || isTablet
    
    val focusRequester1 = remember { androidx.compose.ui.focus.FocusRequester() }
    val focusRequester2 = remember { androidx.compose.ui.focus.FocusRequester() }

    Column(
        modifier = modifier
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
            Column(modifier = Modifier.weight(1f).padding(top = 16.dp), verticalArrangement = Arrangement.Top) {
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
            }
            
            Keypad(
                onAction = onAction,
                focus1 = focus1,
                onFocusChange = { focus1 = it },
                isDark = isDark,
                primaryColor = primaryColor
            )
            // Added 32.dp padding here so it aligns above the navigation bar
            Spacer(modifier = Modifier.height(32.dp))
        }
    }
}

fun updateValuesInternal(
    inputField: TextFieldValue,
    isFirst: Boolean,
    unit1: UnitType,
    unit2: UnitType,
    selectedCategory: UnitCategory,
    onResult: (TextFieldValue, TextFieldValue) -> Unit
) {
    try {
        val input = inputField.text
        val v = input.replace(",", ".").toDoubleOrNull() ?: 0.0
        if (isFirst) {
            val out2 = if (selectedCategory == UnitCategory.Temperature) {
                convertTemp(v, unit1.name, unit2.name).toString().replace(".", ",")
            } else {
                formatDouble((v * unit1.value) / unit2.value).replace(".", ",")
            }
            onResult(inputField, TextFieldValue(out2, TextRange(out2.length)))
        } else {
            val out1 = if (selectedCategory == UnitCategory.Temperature) {
                convertTemp(v, unit2.name, unit1.name).toString().replace(".", ",")
            } else {
                formatDouble((v * unit2.value) / unit1.value).replace(".", ",")
            }
            onResult(TextFieldValue(out1, TextRange(out1.length)), inputField)
        }
    } catch(e: Exception) {
    }
}

@OptIn(ExperimentalMaterial3Api::class, androidx.compose.ui.ExperimentalComposeUiApi::class)
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
                    if (newValue.text.matches(Regex("[0-9.,-]*"))) {
                        onValue1Change(newValue)
                    }
                },
                textStyle = androidx.compose.ui.text.TextStyle(
                    fontSize = 48.sp,
                    color = if(focus1) primaryColor else (if(isDark) Color(0xFFFBFBFB) else Color(0xFF141414))
                ),
                singleLine = true,
                readOnly = false,
                modifier = Modifier.fillMaxWidth().focusRequester(focusRequester).onFocusChanged { if (it.isFocused) onFocusChange() },
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
                    if (newValue.text.matches(Regex("[0-9.,-]*"))) {
                        onValue2Change(newValue)
                    }
                },
                textStyle = androidx.compose.ui.text.TextStyle(
                    fontSize = 48.sp,
                    color = if(!focus1) primaryColor else (if(isDark) Color(0xFFFBFBFB) else Color(0xFF141414))
                ),
                singleLine = true,
                readOnly = false,
                modifier = Modifier.fillMaxWidth().focusRequester(focusRequester).onFocusChanged { if (it.isFocused) onFocusChange() },
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
    val configuration = androidx.compose.ui.platform.LocalConfiguration.current
    val isLandscape = configuration.orientation == android.content.res.Configuration.ORIENTATION_LANDSCAPE
    val isTablet = configuration.screenWidthDp >= 600
    val isTabletPortrait = isTablet && !isLandscape
    val buttonHeight = if (isTabletPortrait) 64.dp else if (isLandscape) 48.dp else 76.dp

    val pad = listOf(
        listOf("7", "8", "9", "backspace"),
        listOf("4", "5", "6", "C"),
        listOf("1", "2", "3", "up"),
        listOf("+/-", "0", ",", "down")
    )
    Column(verticalArrangement = Arrangement.Bottom, modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp)) {
        pad.forEach { row ->
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 2.dp),
                horizontalArrangement = Arrangement.SpaceEvenly
            ) {
                row.forEach { btn ->
                    Box(modifier = Modifier.weight(1f), contentAlignment = Alignment.Center) {
                        if (btn == "backspace") {
                            Box(
                                modifier = Modifier
                                    .size(buttonHeight)
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
                                    .size(buttonHeight)
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
                                    .size(buttonHeight)
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
                                primaryColor = primaryColor,
                                isLandscape = isLandscape,
                                isTabletPortrait = isTabletPortrait
                            )
                        }
                    }
                }
            }
        }
    }
}
fun convertTemp(value: Double, from: String, to: String): Double {
    if (from == to) return value
    val c = when(from) {
        "Fahrenheit" -> (value - 32) * 5/9
        "Kelvin" -> value - 273.15
        else -> value // Celsius
    }
    return when(to) {
        "Fahrenheit" -> c * 9/5 + 32
        "Kelvin" -> c + 273.15
        else -> c
    }
}

fun formatDouble(d: Double): String {
    val df = java.text.DecimalFormat("#.########")
    return df.format(d)
}
"""

with open('app/src/main/java/com/example/ui/UnitConverter.kt', 'w') as f:
    f.write(new_code)
