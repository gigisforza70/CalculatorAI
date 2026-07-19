#!/bin/bash
sed -i 's/listOf("sin", "cos", "tan", "^", "(", ")", "%", "÷")/listOf("sin", "cos", "tan", "^", "C", "( )", "%", "÷")/g' app/src/main/java/com/example/MainActivity.kt
sed -i 's/listOf("ln", "lg", "g", "e", "0", ",", "=")/listOf("ln", "lg", "g", "e", "+\/-", "0", ",", "=")/g' app/src/main/java/com/example/MainActivity.kt
sed -i 's/modifier = Modifier.weight(if (btn == "0") 2f else 1f).padding(horizontal = 4.dp)/modifier = Modifier.weight(1f).padding(horizontal = 4.dp)/g' app/src/main/java/com/example/MainActivity.kt
