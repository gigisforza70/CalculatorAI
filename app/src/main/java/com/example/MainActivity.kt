@file:OptIn(androidx.compose.ui.ExperimentalComposeUiApi::class)
package com.example

import android.os.Bundle
import androidx.compose.ui.focus.focusRequester
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.Backspace
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.ui.theme.MyApplicationTheme
import java.text.DecimalFormat

import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.viewmodel.CalculatorViewModel
import com.example.ui.UnitConverterScreen
import androidx.compose.material.icons.filled.History
import androidx.compose.material.icons.filled.Straighten
import androidx.compose.material.icons.filled.Science
import androidx.compose.material.icons.filled.Calculate
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.compose.material3.TextButton
import android.content.res.Configuration
import androidx.activity.compose.BackHandler
import androidx.compose.ui.platform.LocalConfiguration

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material.icons.filled.BrightnessAuto
import androidx.compose.material.icons.filled.LightMode
import androidx.compose.material.icons.filled.DarkMode
import androidx.compose.animation.Crossfade
import androidx.compose.animation.core.tween

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            var themeMode by remember { mutableStateOf("auto") }
            val isDark = when(themeMode) {
                "light" -> false
                "dark" -> true
                else -> isSystemInDarkTheme()
            }
            val primaryColor = Color(0xFF2196F3)
            val bgColor = if (isDark) Color(0xFF141414) else Color(0xFFFBFBFB)

            MyApplicationTheme(darkTheme = isDark) {
                Scaffold(
                    modifier = Modifier.fillMaxSize(),
                    containerColor = bgColor
                ) { innerPadding ->
                    CalculatorApp(
                        modifier = Modifier.padding(innerPadding),
                        isDark = isDark,
                        primaryColor = primaryColor,
                        themeMode = themeMode,
                        onThemeToggle = {
                            themeMode = when(themeMode) {
                                "auto" -> "light"
                                "light" -> "dark"
                                else -> "auto"
                            }
                        }
                    )
                }
            }
        }
    }
}

@Composable
fun CalculatorApp(
    modifier: Modifier = Modifier, 
    viewModel: CalculatorViewModel = viewModel(),
    isDark: Boolean = true,
    primaryColor: Color = Color(0xFF2196F3),
    themeMode: String = "auto",
    onThemeToggle: () -> Unit = {},
    isFloating: Boolean = false
) {
    val configuration = LocalConfiguration.current
    val isLandscape = configuration.orientation == Configuration.ORIENTATION_LANDSCAPE
    val isTablet = configuration.screenWidthDp >= 600
    val isTabletPortrait = isTablet && !isLandscape
    val isTabletLandscape = isTablet && isLandscape

    var screen by remember { mutableStateOf("calculator") }
    if (screen == "converter") {
        UnitConverterScreen(modifier = modifier, 
            onBack = { screen = "calculator" },
            isDark = isDark,
            primaryColor = primaryColor
        )
        return
    }

    val history by viewModel.history.collectAsStateWithLifecycle()
    var showHistory by remember { mutableStateOf(false) }
    var isScientific by remember { mutableStateOf(false) }

    BackHandler(enabled = showHistory) { showHistory = false }
    var isResultCalculated by remember { mutableStateOf(false) }

    var expression by remember { mutableStateOf(androidx.compose.ui.text.input.TextFieldValue("")) }
    var resultPreview by remember { mutableStateOf("") }

    // Evaluate whenever expression changes
    LaunchedEffect(expression) {
        if (expression.text.isEmpty()) {
            resultPreview = ""
        } else {
            try {
                val evalResult = evaluate(expression.text.replace(",", ".").replace("×", "*").replace("÷", "/"))
                val df = DecimalFormat("#.########")
                val resultStr = df.format(evalResult).replace(".", ",")
                resultPreview = formatExpression(resultStr)
            } catch (e: Exception) {
                // Ignore errors during typing
                resultPreview = ""
            }
        }
    }

    val onAction: (String) -> Unit = { action ->
        if (isResultCalculated) {
            isResultCalculated = false
            if (action !in listOf("+", "-", "×", "÷", "%", "x^y", "x²", "x!", "1/x", "√x", "^", "=", "backspace")) {
                expression = androidx.compose.ui.text.input.TextFieldValue("")
            }
        }
        
        when (action) {
            "C" -> {
                expression = androidx.compose.ui.text.input.TextFieldValue("")
                resultPreview = ""
            }
            "=" -> {
                if (resultPreview.isNotEmpty()) {
                    val finalResult = resultPreview.replace(".", "")
                    viewModel.addHistory(expression.text, finalResult)
                    expression = androidx.compose.ui.text.input.TextFieldValue(finalResult, androidx.compose.ui.text.TextRange(finalResult.length))
                    resultPreview = ""
                    isResultCalculated = true
                }
            }
            "( )" -> {
                val openParenCount = expression.text.count { it == '(' }
                val closeParenCount = expression.text.count { it == ')' }
                expression = insertAtCursor(expression, if (openParenCount > closeParenCount) ")" else "(")
            }
            "+/-" -> {
                if (expression.text.isEmpty() || expression.text.last() in listOf('+', '-', '×', '÷', '(')) {
                    expression = insertAtCursor(expression, "(-")
                } else if (expression.text.last() == ')') {
                    expression = insertAtCursor(expression, "×(-")
                } else {
                    var i = expression.text.lastIndex
                    while (i >= 0 && (expression.text[i].isDigit() || expression.text[i] == '.' || expression.text[i] == ',')) {
                        i--
                    }
                    if (i >= 1 && expression.text[i] == '-' && expression.text[i-1] == '(') {
                        // It was "(-", let's remove it
                        expression = androidx.compose.ui.text.input.TextFieldValue(expression.text.substring(0, i - 1) + expression.text.substring(i + 1), androidx.compose.ui.text.TextRange(i - 1))
                    } else {
                        // Insert "(-"
                        expression = androidx.compose.ui.text.input.TextFieldValue(expression.text.substring(0, i + 1) + "(-" + expression.text.substring(i + 1), androidx.compose.ui.text.TextRange(i + 3))
                    }
                }
            }
            "sin", "cos", "tan", "lg", "ln", "√", "abs" -> {
                val funcName = if (action == "lg") "log" else action
                expression = insertAtCursor(expression, "$funcName(")
            }
            "x^y" -> expression = insertAtCursor(expression, "^")
            "x²" -> expression = insertAtCursor(expression, "^2")
            "|x|" -> expression = insertAtCursor(expression, "abs(")
            "x!" -> expression = insertAtCursor(expression, "!")
            "1/x" -> expression = insertAtCursor(expression, "1/(")
            "√x" -> expression = insertAtCursor(expression, "√(")
            "2nd", "deg" -> { /* No-op for now or basic toggle */ }
            "backspace" -> {
                if (expression.text.isNotEmpty()) {
                    expression = deleteAtCursor(expression)
                }
            }
            "0", "1", "2", "3", "4", "5", "6", "7", "8", "9" -> {
                val parts = expression.text.split(Regex("[+\\-×÷()\\^!√]"))
                val lastPart = parts.last()
                val digitCount = lastPart.count { it.isDigit() }
                if (digitCount < 15) {
                    expression = insertAtCursor(expression, action)
                }
            }
            "," -> {
                val parts = expression.text.split(Regex("[+\\-×÷()\\^!√]"))
                val lastPart = parts.last()
                if (!lastPart.contains(",")) {
                    expression = insertAtCursor(expression, action)
                }
            }
            else -> {
                expression = insertAtCursor(expression, action)
            }
        }
    }

    Column(
        modifier = modifier
            .fillMaxSize()
            .padding(
                start = if (isLandscape) 48.dp else 24.dp,
                end = if (isLandscape) 48.dp else 24.dp,
                top = if (isLandscape) 8.dp else 16.dp,
                bottom = if (isLandscape) 8.dp else 4.dp
            ),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Column(modifier = Modifier.widthIn(max = if (isLandscape) 800.dp else androidx.compose.ui.unit.Dp.Unspecified).fillMaxHeight()) {
            // Display area
            Column(
                modifier = Modifier
                    .weight(1f)
                    .fillMaxWidth()
                    .padding(top = 24.dp),
                horizontalAlignment = Alignment.End
            ) {
                val focusRequester = remember { androidx.compose.ui.focus.FocusRequester() }
                LaunchedEffect(Unit) {
                    try { focusRequester.requestFocus() } catch (e: Exception) {}
                }
                
                androidx.compose.ui.platform.InterceptPlatformTextInput(
                    interceptor = { _, _ -> kotlinx.coroutines.awaitCancellation() }
                ) {
                androidx.compose.foundation.text.BasicTextField(
                    value = expression,
                    onValueChange = { newValue ->
                        if (isResultCalculated) {
                            isResultCalculated = false
                            // If the new value starts with the old result, it means they appended.
                            // But since they want it to clear on typing a number, we should just let it happen or clear.
                            // Actually, if they typed a new character, it's hard to tell if it's an operator or number.
                            // Let's clear if they typed a number? But we can't easily intercept every key.
                            // If we just clear the whole expression except the new char:
                            val oldText = expression.text
                            val newText = newValue.text
                            if (newText.length > oldText.length) {
                                val addedChar = newText.substring(oldText.length)
                                if (addedChar.matches(Regex("[0-9.,]"))) {
                                    expression = androidx.compose.ui.text.input.TextFieldValue(addedChar, androidx.compose.ui.text.TextRange(addedChar.length))
                                    return@BasicTextField
                                }
                            }
                        }
                        expression = newValue
                    },
                    textStyle = androidx.compose.ui.text.TextStyle(
                        fontSize = if (isLandscape) {
                            when {
                                expression.text.length > 25 -> 16.sp
                                expression.text.length > 15 -> 20.sp
                                else -> 32.sp
                            }
                        } else {
                            when {
                                expression.text.length > 25 -> 20.sp
                                expression.text.length > 15 -> 28.sp
                                expression.text.length > 10 -> 36.sp
                                else -> 48.sp
                            }
                        },
                        fontWeight = FontWeight.Light,
                        color = if (isDark) Color(0xFFFBFBFB) else Color(0xFF141414),
                        textAlign = TextAlign.End
                    ),
                    singleLine = true,
                    readOnly = false, // To prevent soft keyboard from popping up
                    visualTransformation = com.example.ui.ExpressionVisualTransformation(),
                    modifier = Modifier.fillMaxWidth().focusRequester(focusRequester),
                    cursorBrush = androidx.compose.ui.graphics.SolidColor(primaryColor)
                )
                }

                
                Spacer(modifier = Modifier.weight(1f))
                
                Text(
                    text = resultPreview,
                    fontSize = if (isLandscape) 24.sp else 32.sp,
                    fontWeight = FontWeight.Medium,
                    color = if (isDark) Color(0xFFA0A0A0) else Color(0xFF707070),
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
            }

        Spacer(modifier = Modifier.height(16.dp))

        // Toolbar row
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                IconButton(onClick = { showHistory = !showHistory }) {
                    Icon(imageVector = Icons.Default.History, contentDescription = "History", tint = if (showHistory) primaryColor else (if(isDark) Color(0xFFA0A0A0) else Color(0xFF707070)))
                }
                IconButton(onClick = { screen = "converter" }) {
                    Icon(imageVector = Icons.Default.Straighten, contentDescription = "Unit Converter", tint = if(isDark) Color(0xFFA0A0A0) else Color(0xFF707070))
                }
                if (!isLandscape && !isTabletPortrait) {
                    IconButton(onClick = { isScientific = !isScientific }) {
                        Icon(imageVector = Icons.Default.Calculate, contentDescription = "Scientific", tint = if (isScientific) primaryColor else (if(isDark) Color(0xFFA0A0A0) else Color(0xFF707070)))
                    }
                }
                IconButton(onClick = onThemeToggle) {
                    Crossfade(targetState = themeMode, animationSpec = tween(500), label = "theme") { mode ->
                        val icon = when(mode) {
                            "auto" -> Icons.Default.BrightnessAuto
                            "light" -> Icons.Default.LightMode
                            else -> Icons.Default.DarkMode
                        }
                        Icon(imageVector = icon, contentDescription = "Theme", tint = if(isDark) Color(0xFFA0A0A0) else Color(0xFF707070))
                    }
                }
                if (!isFloating) {
                    val context = androidx.compose.ui.platform.LocalContext.current
                    IconButton(onClick = {
                        if (!android.provider.Settings.canDrawOverlays(context)) {
                            val intent = android.content.Intent(
                                android.provider.Settings.ACTION_MANAGE_OVERLAY_PERMISSION,
                                android.net.Uri.parse("package:${context.packageName}")
                            )
                            context.startActivity(intent)
                        } else {
                            val intent = android.content.Intent(context, com.example.FloatingCalculatorService::class.java)
                            context.startService(intent)
                            
                            // Exit app when starting floating window
                            if (context is android.app.Activity) {
                                context.finish()
                            }
                        }
                    }) {
                        Icon(painter = androidx.compose.ui.res.painterResource(R.drawable.ic_float_window), contentDescription = "Floating Window", tint = if(isDark) Color(0xFFA0A0A0) else Color(0xFF707070))
                    }
                }
            }
            IconButton(onClick = { onAction("backspace") }) {
                Icon(
                    imageVector = Icons.AutoMirrored.Filled.Backspace,
                    contentDescription = "Backspace",
                    tint = primaryColor
                )
            }
        }

        Spacer(modifier = Modifier.height(8.dp))
        Box(modifier = Modifier.fillMaxWidth().height(1.dp).background(if(isDark) Color(0xFF2B2B2B) else Color(0xFFE0E0E0)))
        Spacer(modifier = Modifier.height(8.dp))

        // Keypad
                if (isTabletPortrait) {
            val scientificKeys = listOf(
                listOf("sin", "cos", "tan", "^"),
                listOf("asn", "acs", "atn", "!"),
                listOf("snh", "csh", "tnh", "√"),
                listOf("ash", "ach", "ath", "π"),
                listOf("ln", "lg", "g", "e")
            )
            val standardKeys = listOf(
                listOf("C", "( )", "%", "÷"),
                listOf("7", "8", "9", "×"),
                listOf("4", "5", "6", "-"),
                listOf("1", "2", "3", "+"),
                listOf("+/-", "0", ",", "=")
            )
            Row(modifier = Modifier.fillMaxWidth().weight(1.5f), horizontalArrangement = Arrangement.SpaceBetween) {
                // Left side: History OR Scientific Keys
                if (showHistory) {
                    Box(modifier = Modifier.weight(1f).fillMaxHeight()) {
                        if (history.isEmpty()) {
                            Text(
                                "Qui vedrai la cronologia\ndei calcoli.",
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
                } else {
                    Column(modifier = Modifier.weight(1f).fillMaxHeight(), verticalArrangement = Arrangement.SpaceEvenly) {
                        scientificKeys.forEach { row ->
                            Row(modifier = Modifier.fillMaxWidth().weight(1f).padding(vertical = 4.dp), horizontalArrangement = Arrangement.SpaceEvenly, verticalAlignment = Alignment.CenterVertically) {
                                row.forEach { btn ->
                                    CalculatorButton(text = btn, onClick = { onAction(btn) }, isScientific = true, isDark = isDark, primaryColor = primaryColor, modifier = Modifier.weight(1f).padding(horizontal = 4.dp), isTabletPortrait = true)
                                }
                            }
                        }
                    }
                }
                
                // Divider if history is shown (optional, but looks good)
                if (showHistory) {
                    Spacer(modifier = Modifier.width(8.dp))
                    Box(modifier = Modifier.width(1.dp).fillMaxHeight().padding(vertical = 16.dp).background(if(isDark) Color(0xFF2B2B2B) else Color(0xFFE0E0E0)))
                    Spacer(modifier = Modifier.width(8.dp))
                }
                
                // Right side: Standard Keys
                Column(modifier = Modifier.weight(1f).fillMaxHeight(), verticalArrangement = Arrangement.SpaceEvenly) {
                    standardKeys.forEach { row ->
                        Row(modifier = Modifier.fillMaxWidth().weight(1f).padding(vertical = 4.dp), horizontalArrangement = Arrangement.SpaceEvenly, verticalAlignment = Alignment.CenterVertically) {
                            row.forEach { btn ->
                                val isNumOrOp = btn in listOf("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", ",", "+/-", "+", "-", "×", "÷", "=", "C", "%", "( )")
                                CalculatorButton(text = btn, onClick = { onAction(btn) }, isScientific = !isNumOrOp, isDark = isDark, primaryColor = primaryColor, modifier = Modifier.weight(1f).padding(horizontal = 4.dp), isTabletPortrait = true)
                            }
                        }
                    }
                }
            }
        } else if (isTabletLandscape) {            val landscapeScientific = listOf(
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
                Box(modifier = Modifier.weight(3f).fillMaxHeight()) {
                    if (showHistory) {
                        if (history.isEmpty()) {
                            Text(
                                "Qui vedrai la cronologia\ndei calcoli.",
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
                    } else {
                        Column(modifier = Modifier.fillMaxSize(), verticalArrangement = Arrangement.SpaceEvenly) {
                            landscapeScientific.forEach { row ->
                                Row(modifier = Modifier.fillMaxWidth().weight(1f).padding(vertical = 2.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                                    row.forEach { btn ->
                                        CalculatorButton(text = btn, onClick = { onAction(btn) }, isScientific = true, isDark = isDark, primaryColor = primaryColor, modifier = Modifier.weight(1f), isLandscape = true)
                                    }
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
                                val isNumOrOp = btn in listOf("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", ",", "+/-", "+", "-", "×", "÷", "=", "C", "%", "( )")
                                CalculatorButton(text = btn, onClick = { onAction(btn) }, isScientific = !isNumOrOp, isDark = isDark, primaryColor = primaryColor, modifier = Modifier.weight(1f), isLandscape = true)
                            }
                        }
                    }
                }

                // Right side (Empty space to balance the left side)
                Box(modifier = Modifier.weight(3f).fillMaxHeight())
            }
        } else if (isLandscape) {
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
            val portraitScientificKeys = listOf(
                listOf("sin", "cos", "tan", "lg", "ln"),
                listOf("x^y", "x²", "√x", "1/x", "|x|"),
                listOf("C", "( )", "%", "÷", "x!"),
                listOf("7", "8", "9", "×", "π"),
                listOf("4", "5", "6", "-", "e"),
                listOf("1", "2", "3", "+", "2nd"),
                listOf("+/-", "0", ",", "=", "deg")
            )
            Row(modifier = Modifier.fillMaxWidth().weight(1.5f)) {
                // Left side: History or Scientific or Digits
                Box(modifier = Modifier.weight(3f).fillMaxHeight()) {
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
                    } else if (isScientific) {
                        val scientificLeftKeys = listOf(
                            listOf("sin", "cos", "tan"),
                            listOf("ln", "lg", "x^y"),
                            listOf("√x", "x²", "|x|"),
                            listOf("1/x", "π", "e"),
                            listOf("2nd", "deg", "x!")
                        )
                        Column(modifier = Modifier.fillMaxSize(), verticalArrangement = Arrangement.SpaceEvenly) {
                            scientificLeftKeys.forEach { row ->
                                Row(modifier = Modifier.fillMaxWidth().weight(1f).padding(vertical = 4.dp), horizontalArrangement = Arrangement.SpaceEvenly, verticalAlignment = Alignment.CenterVertically) {
                                    row.forEach { btn ->
                                        CalculatorButton(text = btn, onClick = { onAction(btn) }, isScientific = true, isDark = isDark, primaryColor = primaryColor, modifier = Modifier.weight(1f).padding(horizontal = 4.dp), isPortraitScientific = true)
                                    }
                                }
                            }
                        }
                    } else {
                        val standardLeftKeys = listOf(
                            listOf("C", "( )", "%"),
                            listOf("7", "8", "9"),
                            listOf("4", "5", "6"),
                            listOf("1", "2", "3"),
                            listOf("+/-", "0", ",")
                        )
                        Column(modifier = Modifier.fillMaxSize(), verticalArrangement = Arrangement.SpaceEvenly) {
                            standardLeftKeys.forEach { row ->
                                Row(modifier = Modifier.fillMaxWidth().weight(1f).padding(vertical = 4.dp), horizontalArrangement = Arrangement.SpaceEvenly, verticalAlignment = Alignment.CenterVertically) {
                                    row.forEach { btn ->
                                        CalculatorButton(text = btn, onClick = { onAction(btn) }, isScientific = false, isDark = isDark, primaryColor = primaryColor, modifier = Modifier.weight(1f).padding(horizontal = 4.dp))
                                    }
                                }
                            }
                        }
                    }
                }
                
                Spacer(modifier = Modifier.width(4.dp))
                
                // Right side: Operators
                Column(modifier = Modifier.weight(1f).fillMaxHeight(), verticalArrangement = Arrangement.SpaceEvenly) {
                    val operatorKeys = listOf("÷", "×", "-", "+", "=")
                    operatorKeys.forEach { btn ->
                        Row(modifier = Modifier.fillMaxWidth().weight(1f).padding(vertical = 4.dp), horizontalArrangement = Arrangement.SpaceEvenly, verticalAlignment = Alignment.CenterVertically) {
                            CalculatorButton(text = btn, onClick = { onAction(btn) }, isScientific = false, isDark = isDark, primaryColor = primaryColor, modifier = Modifier.weight(1f).padding(horizontal = 4.dp))
                        }
                    }
                }
            }
                }
            }
        }
    }

@Composable
fun CalculatorButton(text: String, onClick: () -> Unit, isScientific: Boolean = false, isDark: Boolean = true, primaryColor: Color = Color(0xFF2196F3), modifier: Modifier = Modifier, isLandscape: Boolean = false, isTabletPortrait: Boolean = false, isPortraitScientific: Boolean = false) {
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

    val buttonHeight = if (isTabletPortrait) 64.dp else if (isLandscape) 48.dp else if (isPortraitScientific) 52.dp else if (isScientific) 52.dp else 76.dp
    val fontSize = if (isTabletPortrait) 24.sp else if (isLandscape) 20.sp else if (isPortraitScientific) 22.sp else if (isScientific) 24.sp else 36.sp

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
                        Modifier.fillMaxWidth(0.95f).height(buttonHeight)
                    } else {
                        Modifier.size(buttonHeight)
                    }
                )
                .clip(androidx.compose.foundation.shape.RoundedCornerShape(percent = 50))
                .background(bgColor)
                .clickable(onClick = onClick),
            contentAlignment = Alignment.Center
        ) {
            Text(
                text = text,
                fontSize = fontSize,
                fontWeight = if (isOperator || isEqual) FontWeight.Medium else FontWeight.Normal,
                color = textColor
            )
        }
    }
}

fun formatExpression(expr: String): String {
    val regex = Regex("([0-9]+(,[0-9]*)?)")
    return expr.replace(regex) { matchResult ->
        val numStr = matchResult.value
        val parts = numStr.split(',')
        val integerPart = parts[0]
        val formattedInteger = if (integerPart.isNotEmpty() && integerPart != "-") {
            try {
                val reversed = integerPart.reversed()
                val chunked = reversed.chunked(3)
                chunked.joinToString(".").reversed()
            } catch (e: Exception) {
                integerPart
            }
        } else integerPart
        
        if (parts.size > 1) {
            "$formattedInteger,${parts[1]}"
        } else if (numStr.endsWith(",")) {
            "$formattedInteger,"
        } else {
            formattedInteger
        }
    }
}

fun evaluate(expr: String): Double {
    return object : Any() {
        var pos = -1
        var ch = 0

        fun nextChar() {
            ch = if (++pos < expr.length) expr[pos].code else -1
        }

        fun eat(charToEat: Int): Boolean {
            while (ch == ' '.code) nextChar()
            if (ch == charToEat) {
                nextChar()
                return true
            }
            return false
        }

        fun parse(): Double {
            nextChar()
            val x = parseExpression()
            if (pos < expr.length) throw RuntimeException("Unexpected: " + ch.toChar())
            return x
        }

        fun parseExpression(): Double {
            var x = parseTerm()
            while (true) {
                if (eat('+'.code)) x += parseTerm()
                else if (eat('-'.code)) x -= parseTerm()
                else return x
            }
        }

        fun parseTerm(): Double {
            var x = parseFactor()
            while (true) {
                if (eat('*'.code)) x *= parseFactor()
                else if (eat('/'.code)) x /= parseFactor()
                else return x
            }
        }

        fun parseFactor(): Double {
            if (eat('+'.code)) return parseFactor()
            if (eat('-'.code)) return -parseFactor()

            var x: Double
            val startPos = pos
            if (eat('('.code)) {
                x = parseExpression()
                eat(')'.code)
            } else if (ch >= 'a'.code && ch <= 'z'.code || ch == '√'.code || ch == 'π'.code) {
                while (ch >= 'a'.code && ch <= 'z'.code || ch == '√'.code || ch == 'π'.code) nextChar()
                val func = expr.substring(startPos, pos)
                if (func == ",") {
                    x = Math.PI
                } else if (func == ",") {
                    x = Math.E
                } else {
                    x = parseFactor()
                    x = when (func) {
                        "sin" -> Math.sin(Math.toRadians(x))
                        "cos" -> Math.cos(Math.toRadians(x))
                        "tan" -> Math.tan(Math.toRadians(x))
                        "log" -> Math.log10(x)
                        "ln" -> Math.log(x)
                        "abs" -> Math.abs(x)
                        "," -> Math.sqrt(x)
                        else -> throw RuntimeException("Unknown function: $func")
                    }
                }
            } else if (ch >= '0'.code && ch <= '9'.code || ch == '.'.code) {
                while (ch >= '0'.code && ch <= '9'.code || ch == '.'.code) nextChar()
                x = expr.substring(startPos, pos).toDouble()
            } else {
                throw RuntimeException("Unexpected: " + ch.toChar())
            }

            if (eat('^'.code)) x = Math.pow(x, parseFactor())
            if (eat('%'.code)) x /= 100.0
            if (eat('!'.code)) {
                var fact = 1.0
                for (i in 1..x.toInt()) fact *= i
                x = fact
            }

            return x
        }
    }.parse()
}
