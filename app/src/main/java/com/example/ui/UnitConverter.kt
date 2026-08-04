@file:OptIn(androidx.compose.ui.ExperimentalComposeUiApi::class)
package com.example.ui

import androidx.activity.compose.BackHandler
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
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.focus.onFocusChanged
import androidx.compose.ui.focus.FocusRequester
import java.text.DecimalFormat
import java.util.Locale

enum class UnitCategory { Length, Area, Temperature, Volume, Mass, Data }

data class UnitType(val name: String, val value: Double, val symbol: String)

val lengthUnits = listOf(UnitType("Nanometers", 1e-9, "nm"), UnitType("Micrometers", 1e-6, "μm"), UnitType("Millimeters", 0.001, "mm"), UnitType("Centimeters", 0.01, "cm"), UnitType("Decimeters", 0.1, "dm"), UnitType("Meters", 1.0, "m"), UnitType("Kilometers", 1000.0, "km"), UnitType("Inches", 0.0254, "in"), UnitType("Feet", 0.3048, "ft"), UnitType("Yards", 0.9144, "yd"), UnitType("Miles", 1609.344, "mi"), UnitType("Nautical miles", 1852.0, "NM"))
val areaUnits = listOf(UnitType("Square millimeters", 0.000001, "mm²"), UnitType("Square centimeters", 0.0001, "cm²"), UnitType("Square meters", 1.0, "m²"), UnitType("Hectares", 10000.0, "ha"), UnitType("Square kilometers", 1000000.0, "km²"), UnitType("Square inches", 0.00064516, "sq in"), UnitType("Square feet", 0.09290304, "sq ft"), UnitType("Square yards", 0.83612736, "sq yd"), UnitType("Acres", 4046.8564224, "ac"), UnitType("Square miles", 2589988.110336, "sq mi"))
val volumeUnits = listOf(UnitType("Milliliters", 0.001, "ml"), UnitType("Cubic centimeters", 0.001, "cm³"), UnitType("Liters", 1.0, "l"), UnitType("Cubic meters", 1000.0, "m³"), UnitType("Teaspoons (US)", 0.00492892, "tsp"), UnitType("Tablespoons (US)", 0.0147868, "tbsp"), UnitType("Fluid ounces (US)", 0.0295735, "fl oz"), UnitType("Cups (US)", 0.236588, "c"), UnitType("Pints (US)", 0.473176, "pt"), UnitType("Quarts (US)", 0.946353, "qt"), UnitType("Gallons (US)", 3.78541, "gal"), UnitType("Cubic inches", 0.0163871, "cu in"), UnitType("Cubic feet", 28.3168, "cu ft"))
val massUnits = listOf(UnitType("Micrograms", 1e-9, "μg"), UnitType("Milligrams", 1e-6, "mg"), UnitType("Grams", 0.001, "g"), UnitType("Kilograms", 1.0, "kg"), UnitType("Metric tonnes", 1000.0, "t"), UnitType("Ounces", 0.0283495, "oz"), UnitType("Pounds", 0.453592, "lb"), UnitType("Stones", 6.35029, "st"), UnitType("Short tons (US)", 907.185, "ton"), UnitType("Long tons (UK)", 1016.05, "ton"))
val dataUnits = listOf(UnitType("Bits", 0.125, "bit"), UnitType("Bytes", 1.0, "B"), UnitType("Kilobits", 128.0, "kb"), UnitType("Kilobytes", 1024.0, "KB"), UnitType("Megabits", 131072.0, "Mb"), UnitType("Megabytes", 1048576.0, "MB"), UnitType("Gigabits", 134217728.0, "Gb"), UnitType("Gigabytes", 1073741824.0, "GB"), UnitType("Terabits", 137438953472.0, "Tb"), UnitType("Terabytes", 1099511627776.0, "TB"), UnitType("Petabytes", 1125899906842624.0, "PB"))

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun UnitConverterScreen(modifier: Modifier = Modifier, onBack: () -> Unit, isDark: Boolean = true, primaryColor: Color = Color(0xFF2196F3)) {
    var selectedCategory by remember { mutableStateOf(UnitCategory.Length) }
    
    var unit1 by remember { mutableStateOf(lengthUnits[0]) }
    var unit2 by remember { mutableStateOf(lengthUnits[1]) }
    var unit3 by remember { mutableStateOf(lengthUnits[2]) }
    
    var value1 by remember { mutableStateOf(TextFieldValue("0", TextRange(1))) }
    var value2 by remember { mutableStateOf(TextFieldValue("0", TextRange(1))) }
    var value3 by remember { mutableStateOf(TextFieldValue("0", TextRange(1))) }
    
    var activeFieldIndex by remember { mutableStateOf(1) }
    var expanded1 by remember { mutableStateOf(false) }
    var expanded2 by remember { mutableStateOf(false) }
    var expanded3 by remember { mutableStateOf(false) }

    BackHandler(onBack = onBack)

    val currentUnitsList = remember(selectedCategory) {
        when(selectedCategory) {
            UnitCategory.Length -> lengthUnits
            UnitCategory.Area -> areaUnits
            UnitCategory.Volume -> volumeUnits
            UnitCategory.Mass -> massUnits
            UnitCategory.Data -> dataUnits
            UnitCategory.Temperature -> listOf(UnitType("Celsius", 1.0, "°C"), UnitType("Fahrenheit", 1.0, "°F"), UnitType("Kelvin", 1.0, "K"))
        }
    }

    LaunchedEffect(selectedCategory) {
        unit1 = currentUnitsList.getOrNull(0) ?: lengthUnits[0]
        unit2 = currentUnitsList.getOrNull(1) ?: unit1
        unit3 = currentUnitsList.getOrNull(2) ?: unit2
        updateAllValues(1, value1, unit1, unit2, unit3, selectedCategory) { v1, v2, v3 ->
            value1 = v1; value2 = v2; value3 = v3
        }
    }

    val triggerUpdate = { activeIdx: Int, fieldVal: TextFieldValue ->
        updateAllValues(activeIdx, fieldVal, unit1, unit2, unit3, selectedCategory) { v1, v2, v3 ->
            value1 = v1; value2 = v2; value3 = v3
        }
    }

    val onAction = { action: String ->
        val currentField = when(activeFieldIndex) {
            1 -> value1
            2 -> value2
            else -> value3
        }
        var newField = currentField

        when (action) {
            "C" -> {
                newField = TextFieldValue("0", TextRange(1))
            }
            "backspace" -> {
                if (currentField.text.isNotEmpty() && currentField.text != "0") {
                    newField = deleteConverterTextAtCursor(currentField)
                    if (newField.text.isEmpty() || newField.text == "-") {
                        newField = TextFieldValue("0", TextRange(1))
                    }
                }
            }
            "+/-" -> {
                var text = currentField.text
                if (text != "0") {
                    if (text.startsWith("-")) {
                        text = text.substring(1)
                        val newCursor = maxOf(0, currentField.selection.min - 1)
                        newField = TextFieldValue(text, TextRange(newCursor))
                    } else {
                        text = "-$text"
                        val newCursor = currentField.selection.min + 1
                        newField = TextFieldValue(text, TextRange(newCursor))
                    }
                }
            }
            "," -> {
                if (!currentField.text.contains(",")) {
                    newField = insertConverterTextAtCursor(currentField, ",")
                }
            }
            else -> {
                val digitCount = currentField.text.count { it.isDigit() }
                if (digitCount < 15) {
                    if (currentField.text == "0" && action != ",") {
                        newField = TextFieldValue(action, TextRange(1))
                    } else {
                        newField = insertConverterTextAtCursor(currentField, action)
                    }
                }
            }
        }
        triggerUpdate(activeFieldIndex, newField)
    }

    val bgColor = if(isDark) Color(0xFF141414) else Color(0xFFFBFBFB)
    val textColor = if(isDark) Color.White else Color.Black
    val secondaryTextColor = if(isDark) Color(0xFFA0A0A0) else Color(0xFF707070)
    
    val configuration = androidx.compose.ui.platform.LocalConfiguration.current
    val isLandscape = configuration.orientation == android.content.res.Configuration.ORIENTATION_LANDSCAPE
    val isTablet = configuration.smallestScreenWidthDp >= 600
    
    val focusRequester1 = remember { FocusRequester() }
    val focusRequester2 = remember { FocusRequester() }
    val focusRequester3 = remember { FocusRequester() }

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
            colors = TopAppBarDefaults.topAppBarColors(containerColor = bgColor),
            windowInsets = if (isLandscape && !isTablet) WindowInsets(0.dp) else TopAppBarDefaults.windowInsets
        )
        
        LazyRow(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 16.dp, vertical = 4.dp)
        ) {
            items(UnitCategory.entries) { category ->
                TextButton(onClick = { selectedCategory = category }) {
                    Text(
                        text = category.name,
                        fontSize = 18.sp,
                        color = if (selectedCategory == category) primaryColor else secondaryTextColor,
                        fontWeight = if (selectedCategory == category) FontWeight.Bold else FontWeight.Normal
                    )
                }
            }
        }
        
        if (isLandscape) {
            Row(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(horizontal = 24.dp, vertical = if (!isTablet) 2.dp else 12.dp),
                horizontalArrangement = Arrangement.spacedBy(32.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Column(
                    modifier = Modifier
                        .weight(1.1f)
                        .fillMaxHeight(),
                    verticalArrangement = Arrangement.SpaceEvenly
                ) {
                    UnitInputRow(
                        unit = unit1, active = activeFieldIndex == 1, value = value1, expanded = expanded1,
                        onExpandedChange = { expanded1 = it }, onUnitChange = { unit1 = it; expanded1 = false; triggerUpdate(1, value1) },
                        onValueChange = { triggerUpdate(1, it) }, onFocus = { activeFieldIndex = 1 },
                        currentUnitsList = currentUnitsList, primaryColor = primaryColor, secondaryTextColor = secondaryTextColor,
                        isDark = isDark, focusRequester = focusRequester1
                    )
                    HorizontalDivider(color = if (isDark) Color(0xFF2B2B2B) else Color(0xFFE0E0E0))
                    UnitInputRow(
                        unit = unit2, active = activeFieldIndex == 2, value = value2, expanded = expanded2,
                        onExpandedChange = { expanded2 = it }, onUnitChange = { unit2 = it; expanded2 = false; triggerUpdate(2, value2) },
                        onValueChange = { triggerUpdate(2, it) }, onFocus = { activeFieldIndex = 2 },
                        currentUnitsList = currentUnitsList, primaryColor = primaryColor, secondaryTextColor = secondaryTextColor,
                        isDark = isDark, focusRequester = focusRequester2
                    )
                    HorizontalDivider(color = if (isDark) Color(0xFF2B2B2B) else Color(0xFFE0E0E0))
                    UnitInputRow(
                        unit = unit3, active = activeFieldIndex == 3, value = value3, expanded = expanded3,
                        onExpandedChange = { expanded3 = it }, onUnitChange = { unit3 = it; expanded3 = false; triggerUpdate(3, value3) },
                        onValueChange = { triggerUpdate(3, it) }, onFocus = { activeFieldIndex = 3 },
                        currentUnitsList = currentUnitsList, primaryColor = primaryColor, secondaryTextColor = secondaryTextColor,
                        isDark = isDark, focusRequester = focusRequester3
                    )
                }
                
                Box(
                    modifier = Modifier
                        .weight(0.9f)
                        .fillMaxHeight(),
                    contentAlignment = Alignment.Center
                ) {
                    Keypad(
                        onAction = onAction,
                        activeFieldIndex = activeFieldIndex,
                        onFieldChange = { activeFieldIndex = it },
                        isDark = isDark,
                        primaryColor = primaryColor,
                        buttonSize = if (isTablet) 84.dp else 56.dp
                    )
                }
            }
        } else {
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(horizontal = 24.dp, vertical = 8.dp),
                verticalArrangement = Arrangement.SpaceBetween
            ) {
                Column(
                    modifier = Modifier.fillMaxWidth(),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    UnitInputRow(
                        unit = unit1, active = activeFieldIndex == 1, value = value1, expanded = expanded1,
                        onExpandedChange = { expanded1 = it }, onUnitChange = { unit1 = it; expanded1 = false; triggerUpdate(1, value1) },
                        onValueChange = { triggerUpdate(1, it) }, onFocus = { activeFieldIndex = 1 },
                        currentUnitsList = currentUnitsList, primaryColor = primaryColor, secondaryTextColor = secondaryTextColor,
                        isDark = isDark, focusRequester = focusRequester1
                    )
                    HorizontalDivider(color = if (isDark) Color(0xFF2B2B2B) else Color(0xFFE0E0E0))
                    UnitInputRow(
                        unit = unit2, active = activeFieldIndex == 2, value = value2, expanded = expanded2,
                        onExpandedChange = { expanded2 = it }, onUnitChange = { unit2 = it; expanded2 = false; triggerUpdate(2, value2) },
                        onValueChange = { triggerUpdate(2, it) }, onFocus = { activeFieldIndex = 2 },
                        currentUnitsList = currentUnitsList, primaryColor = primaryColor, secondaryTextColor = secondaryTextColor,
                        isDark = isDark, focusRequester = focusRequester2
                    )
                    HorizontalDivider(color = if (isDark) Color(0xFF2B2B2B) else Color(0xFFE0E0E0))
                    UnitInputRow(
                        unit = unit3, active = activeFieldIndex == 3, value = value3, expanded = expanded3,
                        onExpandedChange = { expanded3 = it }, onUnitChange = { unit3 = it; expanded3 = false; triggerUpdate(3, value3) },
                        onValueChange = { triggerUpdate(3, it) }, onFocus = { activeFieldIndex = 3 },
                        currentUnitsList = currentUnitsList, primaryColor = primaryColor, secondaryTextColor = secondaryTextColor,
                        isDark = isDark, focusRequester = focusRequester3
                    )
                }
                
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(bottom = 16.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Keypad(
                        onAction = onAction,
                        activeFieldIndex = activeFieldIndex,
                        onFieldChange = { activeFieldIndex = it },
                        isDark = isDark,
                        primaryColor = primaryColor,
                        buttonSize = if (isTablet) 96.dp else 72.dp
                    )
                }
            }
        }
    }
}

fun updateAllValues(
    changedIndex: Int,
    fieldVal: TextFieldValue,
    u1: UnitType,
    u2: UnitType,
    u3: UnitType,
    category: UnitCategory,
    onResult: (TextFieldValue, TextFieldValue, TextFieldValue) -> Unit
) {
    try {
        val textVal = fieldVal.text
        val baseVal = textVal.replace(",", ".").toDoubleOrNull() ?: 0.0
        
        val standardVal = when (changedIndex) {
            1 -> if (category == UnitCategory.Temperature) tempToBase(baseVal, u1.name) else baseVal * u1.value
            2 -> if (category == UnitCategory.Temperature) tempToBase(baseVal, u2.name) else baseVal * u2.value
            else -> if (category == UnitCategory.Temperature) tempToBase(baseVal, u3.name) else baseVal * u3.value
        }

        val out1 = if (category == UnitCategory.Temperature) baseToTemp(standardVal, u1.name) else standardVal / u1.value
        val out2 = if (category == UnitCategory.Temperature) baseToTemp(standardVal, u2.name) else standardVal / u2.value
        val out3 = if (category == UnitCategory.Temperature) baseToTemp(standardVal, u3.name) else standardVal / u3.value

        val f1 = if (changedIndex == 1) textVal else formatDouble(out1).replace(".", ",")
        val f2 = if (changedIndex == 2) textVal else formatDouble(out2).replace(".", ",")
        val f3 = if (changedIndex == 3) textVal else formatDouble(out3).replace(".", ",")

        onResult(
            if (changedIndex == 1) fieldVal else TextFieldValue(f1, TextRange(f1.length)),
            if (changedIndex == 2) fieldVal else TextFieldValue(f2, TextRange(f2.length)),
            if (changedIndex == 3) fieldVal else TextFieldValue(f3, TextRange(f3.length))
        )
    } catch (_: Exception) {}
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun UnitInputRow(
    unit: UnitType,
    active: Boolean,
    value: TextFieldValue,
    expanded: Boolean,
    onExpandedChange: (Boolean) -> Unit,
    onUnitChange: (UnitType) -> Unit,
    onValueChange: (TextFieldValue) -> Unit,
    onFocus: () -> Unit,
    currentUnitsList: List<UnitType>,
    primaryColor: Color,
    secondaryTextColor: Color,
    isDark: Boolean,
    focusRequester: FocusRequester
) {
    Column(modifier = Modifier
        .fillMaxWidth()
        .padding(vertical = 4.dp)) {
        ExposedDropdownMenuBox(
            expanded = expanded,
            onExpandedChange = { onExpandedChange(!expanded) }
        ) {
            Row(modifier = Modifier.menuAnchor(MenuAnchorType.PrimaryEditable, true), verticalAlignment = Alignment.CenterVertically) {
                Text(
                    text = unit.name,
                    color = if(active) primaryColor else secondaryTextColor,
                    fontSize = 18.sp,
                    fontWeight = FontWeight.Medium
                )
                Spacer(modifier = Modifier.width(6.dp))
                Icon(
                    imageVector = Icons.Default.ArrowDropDown,
                    contentDescription = "Dropdown",
                    tint = if(active) primaryColor else secondaryTextColor,
                    modifier = Modifier.size(24.dp)
                )
            }
            ExposedDropdownMenu(
                expanded = expanded,
                onDismissRequest = { onExpandedChange(false) },
                modifier = Modifier.background(if(isDark) Color(0xFF2B2B2B) else Color(0xFFF0F0F0))
            ) {
                currentUnitsList.forEach { u ->
                    DropdownMenuItem(
                        text = { Text(u.name, fontSize = 18.sp, color = if(isDark) Color.White else Color.Black) },
                        onClick = { onUnitChange(u) }
                    )
                }
            }
        }
        
        androidx.compose.ui.platform.InterceptPlatformTextInput(
            interceptor = { _, _ -> kotlinx.coroutines.awaitCancellation() }
        ) {
            androidx.compose.foundation.text.BasicTextField(
                value = value,
                onValueChange = { newValue ->
                    if (newValue.text.matches(Regex("[0-9.,-]*")) && newValue.text.count { it.isDigit() } <= 15) {
                        onValueChange(newValue)
                    }
                },
                textStyle = androidx.compose.ui.text.TextStyle(
                    fontSize = 38.sp,
                    fontWeight = FontWeight.Light,
                    color = if(active) primaryColor else (if(isDark) Color(0xFFFBFBFB) else Color(0xFF141414))
                ),
                singleLine = true,
                visualTransformation = ExpressionVisualTransformation(),
                modifier = Modifier
                    .fillMaxWidth()
                    .focusRequester(focusRequester)
                    .onFocusChanged { if (it.isFocused) onFocus() },
                cursorBrush = androidx.compose.ui.graphics.SolidColor(primaryColor),
                decorationBox = { innerTextField ->
                    Row(verticalAlignment = Alignment.Bottom) {
                        Box(modifier = Modifier.weight(1f, fill = false)) {
                            innerTextField()
                        }
                        Spacer(modifier = Modifier.width(12.dp))
                        Text(
                            text = unit.symbol,
                            fontSize = 22.sp,
                            color = if(active) primaryColor else (if(isDark) Color(0xFFA0A0A0) else Color(0xFF707070)),
                            modifier = Modifier.padding(bottom = 4.dp)
                        )
                    }
                }
            )
        }
    }
}

@Composable
fun Keypad(
    onAction: (String) -> Unit,
    activeFieldIndex: Int,
    onFieldChange: (Int) -> Unit,
    isDark: Boolean,
    primaryColor: Color,
    buttonSize: androidx.compose.ui.unit.Dp
) {
    val pad = listOf(
        listOf("7", "8", "9", "backspace"),
        listOf("4", "5", "6", "C"),
        listOf("1", "2", "3", "up"),
        listOf("+/-", "0", ",", "down")
    )
    Column(
        verticalArrangement = Arrangement.spacedBy(10.dp),
        modifier = Modifier.width(buttonSize * 4 + 30.dp)
    ) {
        pad.forEach { row ->
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(10.dp, Alignment.CenterHorizontally)
            ) {
                row.forEach { btn ->
                    Box(
                        modifier = Modifier
                            .size(buttonSize),
                        contentAlignment = Alignment.Center
                    ) {
                        when (btn) {
                            "backspace" -> {
                                Box(
                                    modifier = Modifier
                                        .fillMaxSize()
                                        .clip(androidx.compose.foundation.shape.CircleShape)
                                        .background(if(isDark) Color(0xFF2B2B2B) else Color(0xFFE8E8E8))
                                        .clickable { onAction("backspace") },
                                    contentAlignment = Alignment.Center
                                ) {
                                    Icon(Icons.AutoMirrored.Filled.Backspace, "Backspace", tint = primaryColor, modifier = Modifier.size(buttonSize * 0.42f))
                                }
                            }
                            "up" -> {
                                Box(
                                    modifier = Modifier
                                        .fillMaxSize()
                                        .clip(androidx.compose.foundation.shape.CircleShape)
                                        .background(if(isDark) Color(0xFF2B2B2B) else Color(0xFFE8E8E8))
                                        .clickable { 
                                            val next = if (activeFieldIndex > 1) activeFieldIndex - 1 else 3
                                            onFieldChange(next)
                                        },
                                    contentAlignment = Alignment.Center
                                ) {
                                    Icon(Icons.Default.ArrowUpward, "Up", tint = primaryColor, modifier = Modifier.size(buttonSize * 0.42f))
                                }
                            }
                            "down" -> {
                                Box(
                                    modifier = Modifier
                                        .fillMaxSize()
                                        .clip(androidx.compose.foundation.shape.CircleShape)
                                        .background(if(isDark) Color(0xFF2B2B2B) else Color(0xFFE8E8E8))
                                        .clickable { 
                                            val next = if (activeFieldIndex < 3) activeFieldIndex + 1 else 1
                                            onFieldChange(next)
                                        },
                                    contentAlignment = Alignment.Center
                                ) {
                                    Icon(Icons.Default.ArrowDownward, "Down", tint = primaryColor, modifier = Modifier.size(buttonSize * 0.42f))
                                }
                            }
                            else -> {
                                val isNumberOrDot = btn.matches(Regex("[0-9,]+")) || btn == "+/-"
                                val btnBg = if (!isNumberOrDot) (if(isDark) Color(0xFF2B2B2B) else Color(0xFFE8E8E8)) else (if(isDark) Color(0xFF222222) else Color(0xFFE8E8E8))
                                Box(
                                    modifier = Modifier
                                        .fillMaxSize()
                                        .clip(androidx.compose.foundation.shape.CircleShape)
                                        .background(btnBg)
                                        .clickable { onAction(btn) },
                                    contentAlignment = Alignment.Center
                                ) {
                                    Text(
                                        text = btn,
                                        fontSize = 36.sp,
                                        fontFamily = if (isNumberOrDot && btn != "+/-") androidx.compose.ui.text.font.FontFamily.SansSerif else null,
                                        fontWeight = FontWeight.Medium,
                                        color = if (btn == "C") Color(0xFFE57373) else (if(isDark) Color.White else Color.Black)
                                    )
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

fun tempToBase(v: Double, unit: String): Double {
    return when(unit) {
        "Fahrenheit" -> (v - 32) * 5/9
        "Kelvin" -> v - 273.15
        else -> v
    }
}

fun baseToTemp(c: Double, unit: String): Double {
    return when(unit) {
        "Fahrenheit" -> c * 9/5 + 32
        "Kelvin" -> c + 273.15
        else -> c
    }
}

fun formatDouble(d: Double): String {
    val df = DecimalFormat("#.########", java.text.DecimalFormatSymbols(Locale.US))
    return df.format(d)
}

private fun insertConverterTextAtCursor(tfv: TextFieldValue, textToInsert: String): TextFieldValue {
    val selection = tfv.selection
    val newText = tfv.text.substring(0, selection.min) + textToInsert + tfv.text.substring(selection.max)
    val newCursorPos = selection.min + textToInsert.length
    return TextFieldValue(text = newText, selection = TextRange(newCursorPos))
}

private fun deleteConverterTextAtCursor(tfv: TextFieldValue): TextFieldValue {
    val selection = tfv.selection
    if (selection.min != selection.max) {
        val newText = tfv.text.substring(0, selection.min) + tfv.text.substring(selection.max)
        return TextFieldValue(text = newText, selection = TextRange(selection.min))
    } else if (selection.min > 0) {
        val newText = tfv.text.substring(0, selection.min - 1) + tfv.text.substring(selection.min)
        return TextFieldValue(text = newText, selection = TextRange(selection.min - 1))
    }
    return tfv
}
