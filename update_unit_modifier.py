import re

with open('app/src/main/java/com/example/ui/UnitConverter.kt', 'r') as f:
    content = f.read()

# Add modifier to UnitConverterScreen
content = content.replace(
    'fun UnitConverterScreen(onBack: () -> Unit, isDark: Boolean = true, primaryColor: Color = Color(0xFF2196F3)) {',
    'fun UnitConverterScreen(modifier: Modifier = Modifier, onBack: () -> Unit, isDark: Boolean = true, primaryColor: Color = Color(0xFF2196F3)) {'
)

# Replace Column(modifier = Modifier.fillMaxSize().background(bgColor)) with the passed modifier
content = content.replace(
    """    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(bgColor)
    ) {""",
    """    Column(
        modifier = modifier
            .fillMaxSize()
            .background(bgColor)
    ) {"""
)

with open('app/src/main/java/com/example/ui/UnitConverter.kt', 'w') as f:
    f.write(content)

