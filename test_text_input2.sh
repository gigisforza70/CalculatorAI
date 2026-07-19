#!/bin/bash
sed -i 's/androidx.compose.foundation.text.BasicTextField(/androidx.compose.runtime.CompositionLocalProvider(\n                    androidx.compose.ui.platform.LocalTextInputService provides null\n                ) {\n                    androidx.compose.foundation.text.BasicTextField(/g' app/src/main/java/com/example/MainActivity.kt
sed -i 's/cursorBrush = androidx.compose.ui.graphics.SolidColor(primaryColor)/cursorBrush = androidx.compose.ui.graphics.SolidColor(primaryColor)\n                    )\n                }/g' app/src/main/java/com/example/MainActivity.kt
