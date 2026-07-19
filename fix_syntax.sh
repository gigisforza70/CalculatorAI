#!/bin/bash
sed -i 's/                    cursorBrush = androidx.compose.ui.graphics.SolidColor(primaryColor)/                    cursorBrush = androidx.compose.ui.graphics.SolidColor(primaryColor)/g' app/src/main/java/com/example/MainActivity.kt
sed -i '283,286c\
                    cursorBrush = androidx.compose.ui.graphics.SolidColor(primaryColor)\
                }\
' app/src/main/java/com/example/MainActivity.kt
