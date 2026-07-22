import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

target = "fun CalculatorButton(text: String, onClick: () -> Unit, isScientific: Boolean = false, isDark: Boolean = true, primaryColor: Color = Color(0xFF2196F3), modifier: Modifier = Modifier, isLandscape: Boolean = false, isTabletPortrait: Boolean = false) {"

replacement = "fun CalculatorButton(text: String, onClick: () -> Unit, isScientific: Boolean = false, isDark: Boolean = true, primaryColor: Color = Color(0xFF2196F3), modifier: Modifier = Modifier, isLandscape: Boolean = false, isTabletPortrait: Boolean = false, isPortraitScientific: Boolean = false) {"

content = content.replace(target, replacement)

target2 = "val buttonHeight = if (isTabletPortrait) 64.dp else if (isLandscape) 48.dp else if (isScientific) 52.dp else 76.dp"
replacement2 = "val buttonHeight = if (isTabletPortrait) 64.dp else if (isLandscape) 48.dp else if (isPortraitScientific) 52.dp else if (isScientific) 52.dp else 76.dp"

content = content.replace(target2, replacement2)

target3 = "val fontSize = if (isTabletPortrait) 24.sp else if (isLandscape) 20.sp else if (isScientific) 24.sp else 36.sp"
replacement3 = "val fontSize = if (isTabletPortrait) 24.sp else if (isLandscape) 20.sp else if (isPortraitScientific) 22.sp else if (isScientific) 24.sp else 36.sp"

content = content.replace(target3, replacement3)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
