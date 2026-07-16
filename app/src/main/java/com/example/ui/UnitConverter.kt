package com.example.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.automirrored.filled.Backspace
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

val lengthUnits = listOf(UnitType("Millimeters", 0.001), UnitType("Centimeters", 0.01), UnitType("Meters", 1.0), UnitType("Kilometers", 1000.0), UnitType("Inches", 0.0254), UnitType("Feet", 0.3048), UnitType("Miles", 1609.34))
val areaUnits = listOf(UnitType("Acres", 4046.86), UnitType("Ares", 100.0), UnitType("Hectares", 10000.0), UnitType("Square centimeters", 0.0001), UnitType("Square feet", 0.092903), UnitType("Square inches", 0.00064516), UnitType("Square meters", 1.0))
val volumeUnits = listOf(UnitType("Gallons (US)", 3.78541), UnitType("Liters", 1.0), UnitType("Milliliters", 0.001), UnitType("Cubic centimeters", 0.001), UnitType("Cubic meters", 1000.0))
val massUnits = listOf(UnitType("Milligrams", 0.000001), UnitType("Grams", 0.001), UnitType("Kilograms", 1.0), UnitType("Ounces", 0.0283495), UnitType("Pounds", 0.453592))
val dataUnits = listOf(UnitType("Bytes", 1.0), UnitType("Kilobytes", 1024.0), UnitType("Megabytes", 1048576.0), UnitType("Gigabytes", 1073741824.0), UnitType("Terabytes", 1099511627776.0))

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun UnitConverterScreen(onBack: () -> Unit, isDark: Boolean = true, primaryColor: Color = Color(0xFF2196F3)) {
    var selectedCategory by remember { mutableStateOf(UnitCategory.Length) }
    
    var unit1 by remember { mutableStateOf(lengthUnits[2]) }
    var unit2 by remember { mutableStateOf(lengthUnits[1]) }
    
    var value1 by remember { mutableStateOf("1") }
    var value2 by remember { mutableStateOf("100") }
    
    var focus1 by remember { mutableStateOf(true) }

    fun updateValues(input: String, isFirst: Boolean) {
        try {
            val v = input.toDoubleOrNull() ?: 0.0
            if (isFirst) {
                value1 = input
                if (selectedCategory == UnitCategory.Temperature) {
                    value2 = convertTemp(v, unit1.name, unit2.name).toString()
                } else {
                    value2 = formatDouble((v * unit1.multiplierToStandard) / unit2.multiplierToStandard)
                }
            } else {
                value2 = input
                if (selectedCategory == UnitCategory.Temperature) {
                    value1 = convertTemp(v, unit2.name, unit1.name).toString()
                } else {
                    value1 = formatDouble((v * unit2.multiplierToStandard) / unit1.multiplierToStandard)
                }
            }
        } catch(e: Exception) {}
    }

    // Effect when category changes
    LaunchedEffect(selectedCategory) {
        val list = when(selectedCategory) {
            UnitCategory.Length -> lengthUnits
            UnitCategory.Area -> areaUnits
            UnitCategory.Volume -> volumeUnits
            UnitCategory.Mass -> massUnits
            UnitCategory.Data -> dataUnits
            UnitCategory.Temperature -> listOf(UnitType("Celsius", 1.0), UnitType("Fahrenheit", 1.0), UnitType("Kelvin", 1.0))
        }
        unit1 = list.first()
        unit2 = list.getOrNull(1) ?: list.first()
        value1 = "1"
        updateValues("1", true)
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
                val newVal = if (currentVal == "0" && action != ".") action else currentVal + action
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
            Text(text = unit1.name, color = if(focus1) primaryColor else secondaryTextColor, fontSize = 16.sp)
            Text(text = value1, color = if(focus1) primaryColor else (if(isDark) Color(0xFFFBFBFB) else Color(0xFF141414)), fontSize = 48.sp, maxLines = 1)
        }
        
        HorizontalDivider(color = if(isDark) Color(0xFF2B2B2B) else Color(0xFFE0E0E0), modifier = Modifier.padding(horizontal = 24.dp))
        
        // Input 2
        Column(modifier = Modifier
            .fillMaxWidth()
            .clickable { focus1 = false }
            .padding(24.dp)) {
            Text(text = unit2.name, color = if(!focus1) primaryColor else secondaryTextColor, fontSize = 16.sp)
            Text(text = value2, color = if(!focus1) primaryColor else (if(isDark) Color(0xFFFBFBFB) else Color(0xFF141414)), fontSize = 48.sp, maxLines = 1)
        }
        
        Spacer(modifier = Modifier.weight(1f))
        
        // Keypad
        val pad = listOf(
            listOf("C", "backspace"),
            listOf("7", "8", "9"),
            listOf("4", "5", "6"),
            listOf("1", "2", "3"),
            listOf("+/-", "0", ".")
        )

        pad.forEach { row ->
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 24.dp, vertical = 8.dp),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                row.forEach { btn ->
                    if (btn == "backspace") {
                        Box(
                            modifier = Modifier
                                .size(72.dp)
                                .clip(androidx.compose.foundation.shape.CircleShape)
                                .background(if(isDark) Color(0xFF2B2B2B) else Color(0xFFE0E0E0))
                                .clickable { onAction("backspace") },
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(Icons.AutoMirrored.Filled.Backspace, "Backspace", tint = primaryColor)
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
