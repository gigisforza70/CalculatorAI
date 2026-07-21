import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

replacement = """                IconButton(onClick = onThemeToggle) {
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
                        Icon(imageVector = androidx.compose.material.icons.Icons.Default.OpenInNew, contentDescription = "Floating Window", tint = if(isDark) Color(0xFFA0A0A0) else Color(0xFF707070))
                    }
                }"""

content = content.replace("""                IconButton(onClick = onThemeToggle) {
                    Crossfade(targetState = themeMode, animationSpec = tween(500), label = "theme") { mode ->
                        val icon = when(mode) {
                            "auto" -> Icons.Default.BrightnessAuto
                            "light" -> Icons.Default.LightMode
                            else -> Icons.Default.DarkMode
                        }
                        Icon(imageVector = icon, contentDescription = "Theme", tint = if(isDark) Color(0xFFA0A0A0) else Color(0xFF707070))
                    }
                }""", replacement)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
