import re

with open('app/src/main/java/com/example/ui/UnitConverter.kt', 'r') as f:
    content = f.read()

old_keypad = """@Composable
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
    Column(verticalArrangement = Arrangement.Bottom, modifier = Modifier.fillMaxSize()) {"""

new_keypad = """@Composable
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
    Column(verticalArrangement = Arrangement.Bottom, modifier = Modifier.fillMaxWidth()) {"""

content = content.replace(old_keypad, new_keypad)

# Replace 84.dp with buttonHeight
content = content.replace('.size(84.dp)', '.size(buttonHeight)')

# Pass isLandscape and isTabletPortrait to CalculatorButton
calc_button_old = """                            com.example.CalculatorButton(
                                text = btn,
                                onClick = { onAction(btn) },
                                isDark = isDark,
                                primaryColor = primaryColor
                            )"""

calc_button_new = """                            com.example.CalculatorButton(
                                text = btn,
                                onClick = { onAction(btn) },
                                isDark = isDark,
                                primaryColor = primaryColor,
                                isLandscape = isLandscape,
                                isTabletPortrait = isTabletPortrait
                            )"""

content = content.replace(calc_button_old, calc_button_new)

with open('app/src/main/java/com/example/ui/UnitConverter.kt', 'w') as f:
    f.write(content)
