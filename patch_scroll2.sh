#!/bin/bash
sed -i 's/modifier = Modifier.fillMaxWidth()/modifier = Modifier.fillMaxWidth().androidx.compose.foundation.horizontalScroll(androidx.compose.foundation.rememberScrollState())/g' app/src/main/java/com/example/MainActivity.kt
