package com.example

import android.os.Bundle
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
    onThemeToggle: () -> Unit = {}
) {
    val configuration = LocalConfiguration.current
    val isLandscape = configuration.orientation == Configuration.ORIENTATION_LANDSCAPE

    var screen by remember { mutableStateOf("calculator") }
    if (screen == "converter") {
        UnitConverterScreen(
            onBack = { screen = "calculator" },
            isDark = isDark,
            primaryColor = primaryColor
        )
        return
    }

    val history by viewModel.history.collectAsStateWithLifecycle()
    var showHistory by remember { mutableStateOf(false) }
    var isScientific by remember { mutableStateOf(false) }

    var expression by remember { mutableStateOf("") }
    var resultPreview by remember { mutableStateOf("") }

    // Evaluate whenever expression changes
    LaunchedEffect(expression) {
        if (expression.isEmpty()) {
            resultPreview = ""
        } else {
            try {
                val evalResult = evaluate(expression.replace("×", "*").replace("÷", "/"))
                val df = DecimalFormat("#.########")
                resultPreview = df.format(evalResult)
            } catch (e: Exception) {
                // Ignore errors during typing
                resultPreview = ""
            }
        }
    }

    val onAction: (String) -> Unit = { action ->
        when (action) {
            "C" -> {
                expression = ""
                resultPreview = ""
            }
            "=" -> {
                if (resultPreview.isNotEmpty()) {
                    viewModel.addHistory(expression, resultPreview)
                    expression = resultPreview
                    resultPreview = ""
                }
            }
            "( )" -> {
                val openParenCount = expression.count { it == '(' }
                val closeParenCount = expression.count { it == ')' }
                expression += if (openParenCount > closeParenCount) ")" else "("
            }
            "+/-" -> {
                if (expression.isEmpty() || expression.last() in listOf('+', '-', '×', '÷', '(')) {
                    expression += "(-"
                } else if (expression.last() == ')') {
                    expression += "×(-"
                } else {
                    var i = expression.lastIndex
                    while (i >= 0 && (expression[i].isDigit() || expression[i] == '.')) {
                        i--
                    }
                    if (i >= 1 && expression[i] == '-' && expression[i-1] == '(') {
                        // It was "(-", let's remove it
                        expression = expression.substring(0, i - 1) + expression.substring(i + 1)
                    } else {
                        // Insert "(-"
                        expression = expression.substring(0, i + 1) + "(-" + expression.substring(i + 1)
                    }
                }
            }
            "sin", "cos", "tan", "lg", "ln", "√", "abs" -> {
                val funcName = if (action == "lg") "log" else action
                expression += "$funcName("
            }
            "x^y" -> expression += "^"
            "x²" -> expression += "^2"
            "|x|" -> expression += "abs("
            "x!" -> expression += "!"
            "1/x" -> expression += "1/("
            "√x" -> expression += "√("
            "2nd", "deg" -> { /* No-op for now or basic toggle */ }
            "backspace" -> {
                if (expression.isNotEmpty()) {
                    expression = expression.dropLast(1)
                }
            }
            else -> {
                expression += action
            }
        }
    }

    Column(
        modifier = modifier
            .fillMaxSize()
            .padding(horizontal = if (isLandscape) 48.dp else 24.dp, vertical = if (isLandscape) 8.dp else 16.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Column(modifier = Modifier.widthIn(max = if (isLandscape) 800.dp else androidx.compose.ui.unit.Dp.Unspecified).fillMaxHeight()) {
            // Display area
            Column(
            modifier = Modifier
                .weight(1f)
                .fillMaxWidth(),
            verticalArrangement = Arrangement.Bottom,
            horizontalAlignment = Alignment.End
        ) {
            val scrollState = rememberScrollState()
            
            LaunchedEffect(expression.length) {
                scrollState.animateScrollTo(scrollState.maxValue)
            }
            
            Text(
                text = expression,
                fontSize = if (expression.length > 15) 40.sp else 64.sp,
                fontWeight = FontWeight.Light,
                color = if (isDark) Color(0xFFFBFBFB) else Color(0xFF141414),
                maxLines = 1,
                modifier = Modifier.horizontalScroll(scrollState),
                textAlign = TextAlign.End
            )
            Spacer(modifier = Modifier.height(16.dp))
            Text(
                text = resultPreview,
                fontSize = 32.sp,
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
                if (!isLandscape) {
                    IconButton(onClick = { isScientific = !isScientific }) {
                        Icon(imageVector = Icons.Default.Science, contentDescription = "Scientific", tint = if (isScientific) primaryColor else (if(isDark) Color(0xFFA0A0A0) else Color(0xFF707070)))
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

        // Keypad
        if (showHistory) {
            Row(modifier = Modifier.fillMaxWidth().height(440.dp)) {
                Box(modifier = Modifier.weight(1f).fillMaxHeight()) {
                    LazyColumn(
                        modifier = Modifier.fillMaxSize(),
                        contentPadding = PaddingValues(bottom = 64.dp)
                    ) {
                        items(history) { entry ->
                            Column(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .clickable {
                                        expression = entry.expression
                                        showHistory = false
                                    }
                                    .padding(vertical = 12.dp, horizontal = 16.dp),
                                horizontalAlignment = Alignment.End
                            ) {
                                Text(text = entry.expression, color = if(isDark) Color(0xFFA0A0A0) else Color(0xFF707070), fontSize = 24.sp)
                                Spacer(modifier = Modifier.height(4.dp))
                                Text(text = "=" + entry.result, color = primaryColor, fontSize = 32.sp, fontWeight = FontWeight.Medium)
                            }
                        }
                    }
                    androidx.compose.material3.Button(
                        onClick = { viewModel.clearHistory() },
                        modifier = Modifier
                            .align(Alignment.BottomCenter)
                            .padding(bottom = 16.dp),
                        colors = androidx.compose.material3.ButtonDefaults.buttonColors(containerColor = if(isDark) Color(0xFF2B2B2B) else Color(0xFFE0E0E0)),
                        shape = CircleShape
                    ) {
                        Text("Clear history", color = if(isDark) Color.White else Color.Black, fontSize = 16.sp)
                    }
                }
                
                Box(modifier = Modifier.width(1.dp).fillMaxHeight().padding(vertical = 8.dp).background(if(isDark) Color(0xFF2B2B2B) else Color(0xFFE0E0E0)))
                
                Column(
                    modifier = Modifier.width(88.dp).fillMaxHeight(),
                    verticalArrangement = Arrangement.SpaceEvenly,
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    val ops = listOf("÷", "×", "-", "+", "=")
                    ops.forEach { btn ->
                        CalculatorButton(
                            text = btn,
                            onClick = { onAction(btn) },
                            isScientific = false,
                            isDark = isDark,
                            primaryColor = primaryColor
                        )
                    }
                }
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
                listOf("+/-", "0", ".", "=")
            )
            Row(modifier = Modifier.fillMaxWidth().weight(1f), horizontalArrangement = Arrangement.SpaceBetween) {
                // Left side
                Column(modifier = Modifier.weight(0.45f).fillMaxHeight(), verticalArrangement = Arrangement.SpaceEvenly) {
                    landscapeScientific.forEach { row ->
                        Row(modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                            row.forEach { btn ->
                                CalculatorButton(text = btn, onClick = { onAction(btn) }, isScientific = true, isDark = isDark, primaryColor = primaryColor)
                            }
                        }
                    }
                }
                Spacer(modifier = Modifier.width(16.dp))
                // Right side
                Column(modifier = Modifier.weight(0.55f).fillMaxHeight(), verticalArrangement = Arrangement.SpaceEvenly) {
                    landscapeStandard.forEach { row ->
                        Row(modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                            row.forEach { btn ->
                                CalculatorButton(text = btn, onClick = { onAction(btn) }, isScientific = true, isDark = isDark, primaryColor = primaryColor)
                            }
                        }
                    }
                }
            }
        } else {
            val standardButtons = listOf(
                listOf("C", "( )", "%", "÷"),
                listOf("7", "8", "9", "×"),
                listOf("4", "5", "6", "-"),
                listOf("1", "2", "3", "+"),
                listOf("+/-", "0", ".", "=")
            )
            
            val scientificButtons = listOf(
                listOf("2nd", "deg", "sin", "cos", "tan"),
                listOf("x^y", "lg", "ln", "x²", "|x|"),
                listOf("√x", "C", "( )", "%", "÷"),
                listOf("x!", "7", "8", "9", "×"),
                listOf("1/x", "4", "5", "6", "-"),
                listOf("π", "1", "2", "3", "+"),
                listOf("switch", "e", "0", ".", "=")
            )
    
            val buttons = if (isScientific) scientificButtons else standardButtons
    
            buttons.forEach { row ->
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = if (isScientific) 2.dp else 8.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    row.forEach { btn ->
                        if (btn == "backspace") {
                            IconButton(onClick = { onAction("backspace") }, modifier = Modifier.size(if (isScientific) 56.dp else 72.dp)) {
                                Icon(Icons.AutoMirrored.Filled.Backspace, "Backspace", tint = primaryColor)
                            }
                        } else if (btn == "switch") {
                            Box(
                                modifier = Modifier
                                    .size(if (isScientific) 56.dp else 72.dp)
                                    .clip(CircleShape)
                                    .background(if(isDark) Color(0xFF212121) else Color(0xFFE8E8E8))
                                    .clickable { isScientific = false },
                                contentAlignment = Alignment.Center
                            ) {
                                Icon(Icons.Default.Calculate, "Standard Calculator", tint = primaryColor)
                            }
                        } else {
                            CalculatorButton(
                                text = btn,
                                onClick = { onAction(btn) },
                                isScientific = isScientific,
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
}

@Composable
fun CalculatorButton(text: String, onClick: () -> Unit, isScientific: Boolean = false, isDark: Boolean = true, primaryColor: Color = Color(0xFF2196F3), modifier: Modifier = Modifier) {
    val isRed = text == "C"
    val isOperator = text in listOf("÷", "×", "-", "+", "( )", "%")
    val isEqual = text == "="
    val isScientificKey = text in listOf("2nd", "deg", "sin", "cos", "tan", "x^y", "lg", "ln", "x²", "|x|", "√x", "x!", "1/x", "π", "e")

    val isNumber = text in listOf("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", "+/-")
    val bgColor = when {
        isEqual -> primaryColor
        isOperator -> if(isDark) Color(0xFF2B2B2B) else Color(0xFFE0E0E0)
        isRed -> if(isDark) Color(0xFF2B2B2B) else Color(0xFFE0E0E0)
        isScientificKey -> if(isDark) Color(0xFF212121) else Color(0xFFE8E8E8)
        else -> if(isDark) Color(0xFF2B2B2B) else Color(0xFFF0F0F0)
    }
    
    val textColor = when {
        isRed -> primaryColor
        isEqual -> Color.White
        isOperator -> primaryColor
        isScientificKey -> if(isDark) Color(0xFFA0A0A0) else Color(0xFF707070)
        else -> if(isDark) Color.White else Color.Black
    }
    
    val buttonSize = if (isScientific) 56.dp else 72.dp
    val fontSize = if (isScientific) 24.sp else 32.sp

    val baseModifier = if (modifier == Modifier) Modifier.size(buttonSize) else modifier

    Box(
        modifier = baseModifier
            .clip(CircleShape)
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
                if (func == "π") {
                    x = Math.PI
                } else if (func == "e") {
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
                        "√" -> Math.sqrt(x)
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
