#!/bin/bash
sed -i '283,285c\
                    cursorBrush = androidx.compose.ui.graphics.SolidColor(primaryColor)\
                )\
                }\
' app/src/main/java/com/example/MainActivity.kt
