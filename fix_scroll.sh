#!/bin/bash
sed -i '/val scrollState = rememberScrollState()/d' app/src/main/java/com/example/MainActivity.kt
sed -i '/LaunchedEffect(expression.text.length) {/,/}/d' app/src/main/java/com/example/MainActivity.kt
sed -i 's/modifier = Modifier.horizontalScroll(scrollState),/modifier = Modifier.fillMaxWidth(),/g' app/src/main/java/com/example/MainActivity.kt
