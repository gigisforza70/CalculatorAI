import re

def replace_provider(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Find the CompositionLocalProvider block and replace with InterceptPlatformTextInput
    pattern = r"androidx\.compose\.runtime\.CompositionLocalProvider\(\s*androidx\.compose\.ui\.platform\.LocalTextInputService provides null\s*\)\s*\{"
    
    replacement = """androidx.compose.ui.platform.InterceptPlatformTextInput(
                    interceptor = { _, _ -> kotlinx.coroutines.awaitCancellation() }
                ) {"""
    
    new_content = re.sub(pattern, replacement, content)
    
    # We also need to add @OptIn if not present, but actually we can just suppress it with @OptIn(androidx.compose.ui.ExperimentalComposeUiApi::class) on the composable, or just add @file:OptIn
    # But wait, we can just use @androidx.compose.ui.ExperimentalComposeUiApi at the top of the function or file
    
    if "InterceptPlatformTextInput" in new_content:
        # Let's just add it to the file level
        opt_in_str = "@file:OptIn(androidx.compose.ui.ExperimentalComposeUiApi::class)\n"
        if opt_in_str not in new_content:
            new_content = opt_in_str + new_content

    with open(filepath, 'w') as f:
        f.write(new_content)

replace_provider('app/src/main/java/com/example/MainActivity.kt')
replace_provider('app/src/main/java/com/example/ui/UnitConverter.kt')
