package com.example.ui

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

enum class UnitCategory { Length, Area, Temperature, Volume, Mass, Data }

data class UnitType(val name: String, val multiplierToStandard: Double) // For temperature it's more complex, but we'll simplify or special-case

val lengthUnits = listOf(UnitType("Nanometers", 1e-9), UnitType("Micrometers", 1e-6), UnitType("Millimeters", 0.001), UnitType("Centimeters", 0.01), UnitType("Decimeters", 0.1), UnitType("Meters", 1.0), UnitType("Kilometers", 1000.0), UnitType("Inches", 0.0254), UnitType("Feet", 0.3048), UnitType("Yards", 0.9144), UnitType("Miles", 1609.344), UnitType("Nautical miles", 1852.0))
val areaUnits = listOf(UnitType("Square millimeters", 0.000001), UnitType("Square centimeters", 0.0001), UnitType("Square meters", 1.0), UnitType("Hectares", 10000.0), UnitType("Square kilometers", 1000000.0), UnitType("Square inches", 0.00064516), UnitType("Square feet", 0.09290304), UnitType("Square yards", 0.83612736), UnitType("Acres", 4046.8564224), UnitType("Square miles", 2589988.110336))
val volumeUnits = listOf(UnitType("Milliliters", 0.001), UnitType("Cubic centimeters", 0.001), UnitType("Liters", 1.0), UnitType("Cubic meters", 1000.0), UnitType("Teaspoons (US)", 0.00492892), UnitType("Tablespoons (US)", 0.0147868), UnitType("Fluid ounces (US)", 0.0295735), UnitType("Cups (US)", 0.236588), UnitType("Pints (US)", 0.473176), UnitType("Quarts (US)", 0.946353), UnitType("Gallons (US)", 3.78541), UnitType("Cubic inches", 0.0163871), UnitType("Cubic feet", 28.3168))
val massUnits = listOf(UnitType("Micrograms", 1e-9), UnitType("Milligrams", 1e-6), UnitType("Grams", 0.001), UnitType("Kilograms", 1.0), UnitType("Metric tonnes", 1000.0), UnitType("Ounces", 0.0283495), UnitType("Pounds", 0.453592), UnitType("Stones", 6.35029), UnitType("Short tons (US)", 907.185), UnitType("Long tons (UK)", 1016.05))
val dataUnits = listOf(UnitType("Bits", 0.125), UnitType("Bytes", 1.0), UnitType("Kilobits", 128.0), UnitType("Kilobytes", 1024.0), UnitType("Megabits", 131072.0), UnitType("Megabytes", 1048576.0), UnitType("Gigabits", 134217728.0), UnitType("Gigabytes", 1073741824.0), UnitType("Terabits", 137438953472.0), UnitType("Terabytes", 1099511627776.0), UnitType("Petabytes", 1125899906842624.0))

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun UnitConverterScreen(onBack: () -> Unit, isDark: Boolean = true, primaryColor: Color = Color(0xFF2196F3)) {
    var selectedCategory by remember { mutableStateOf(UnitCategory.Length) }
    
    var unit1 by remember { mutableStateOf(lengthUnits[5]) }
    var unit2 by remember { mutableStateOf(lengthUnits[3]) }
    
    var value1 by remember { mutableStateOf("0") }
    var value2 by remember { mutableStateOf("0") }
    
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

    fun updateValues(input: String, isFirst: Boolean) {
        try {
            val v = input.replace(",", ".").toDoubleOrNull() ?: 0.0
            if (isFirst) {
                value1 = input
                if (selectedCategory == UnitCategory.Temperature) {
                    value2 = convertTemp(v, unit1.name, unit2.name).toString().replace(".", ",")
                } else {
                    value2 = formatDouble((v * unit1.multiplierToStandard) / unit2.multiplierToStandard).replace(".", ",")
                }
            } else {
                value2 = input
                if (selectedCategory == UnitCategory.Temperature) {
                    value1 = convertTemp(v, unit2.name, unit1.name).toString().replace(".", ",")
                } else {
                    value1 = formatDouble((v * unit2.multiplierToStandard) / unit1.multiplierToStandard).replace(".", ",")
                }
            }
        } catch(e: Exception) {}
    }

    // Effect when category changes
    LaunchedEffect(selectedCategory) {
        unit1 = currentUnitsList.first()
        unit2 = currentUnitsList.getOrNull(1) ?: currentUnitsList.first()
        value1 = "0"
        updateValues("0", true)
    }

    val onAction: (String) -> Unit = { action ->
        val currentVal = if (focus1) value1 else value2
        when (action) {
            "C" -> updateValues("0", focus1)
            "backspace" -> {
                val newVal = if (currentVal.length > 1) currentVal.dropLast(1) else "0"
                updateValues(newVal, focus1)
            }
            "+/-" -> {
                if (currentVal.startsWith("-")) updateValues(currentVal.drop(1), focus1)
                else if (currentVal != "0") updateValues("-$currentVal", focus1)
            }
            else -> {
                val newVal = if (currentVal == "0" && action != ",") action else currentVal + action
                updateValues(newVal, focus1)
            }
        }
    }

    val bgColor = if(isDark) Color(0xFF141414) else Color(0xFFFBFBFB)
    val textColor = if(isDark) Color.White else Color.Black
    val secondaryTextColor = if(isDark) Color(0xFFA0A0A0) else Color(0xFF707070)

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
        
        Spacer(modifier = Modifier.weight(1f))
        
        // Input 1
        Column(modifier = Modifier
            .fillMaxWidth()
            .clickable { focus1 = true }
            .padding(24.dp)) {
            ExposedDropdownMenuBox(
                expanded = expanded1,
                onExpandedChange = { expanded1 = !expanded1 }
            ) {
                Row(modifier = Modifier.menuAnchor(), verticalAlignment = Alignment.CenterVertically) {
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
                    onDismissRequest = { expanded1 = false },
                    modifier = Modifier.background(if(isDark) Color(0xFF2B2B2B) else Color(0xFFF0F0F0))
                ) {
                    currentUnitsList.forEach { unit ->
                        DropdownMenuItem(
                            text = { Text(unit.name, color = if(isDark) Color.White else Color.Black) },
                            onClick = {
                                unit1 = unit
                                expanded1 = false
                                updateValues(value1, true)
                            }
                        )
                    }
                }
            }
            Text(text = value1, color = if(focus1) primaryColor else (if(isDark) Color(0xFFFBFBFB) else Color(0xFF141414)), fontSize = 48.sp, maxLines = 1)
        }
        
        HorizontalDivider(color = if(isDark) Color(0xFF2B2B2B) else Color(0xFFE0E0E0), modifier = Modifier.padding(horizontal = 24.dp))
        
        // Input 2
        Column(modifier = Modifier
            .fillMaxWidth()
            .clickable { focus1 = false }
            .padding(24.dp)) {
            ExposedDropdownMenuBox(
                expanded = expanded2,
                onExpandedChange = { expanded2 = !expanded2 }
            ) {
                Row(modifier = Modifier.menuAnchor(), verticalAlignment = Alignment.CenterVertically) {
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
                    onDismissRequest = { expanded2 = false },
                    modifier = Modifier.background(if(isDark) Color(0xFF2B2B2B) else Color(0xFFF0F0F0))
                ) {
                    currentUnitsList.forEach { unit ->
                        DropdownMenuItem(
                            text = { Text(unit.name, color = if(isDark) Color.White else Color.Black) },
                            onClick = {
                                unit2 = unit
                                expanded2 = false
                                updateValues(value2, false)
                            }
                        )
                    }
                }
            }
            Text(text = value2, color = if(!focus1) primaryColor else (if(isDark) Color(0xFFFBFBFB) else Color(0xFF141414)), fontSize = 48.sp, maxLines = 1)
        }
        
        Spacer(modifier = Modifier.weight(1f))
        
        // Keypad
        val pad = listOf(
            listOf("7", "8", "9", "backspace"),
            listOf("4", "5", "6", "C"),
            listOf("1", "2", "3", "up"),
            listOf("+/-", "0", ",", "down")
        )

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
                                    .clickable { focus1 = true },
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
                                    .clickable { focus1 = false },
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
        Spacer(modifier = Modifier.height(16.dp))
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
