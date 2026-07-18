#!/bin/bash
sed -i 's/var expression by remember { mutableStateOf("") }/var expression by remember { mutableStateOf(androidx.compose.ui.text.input.TextFieldValue("")) }/g' app/src/main/java/com/example/MainActivity.kt
# Now replace the read accesses.
sed -i 's/expression.isEmpty()/expression.text.isEmpty()/g' app/src/main/java/com/example/MainActivity.kt
sed -i 's/expression.isNotEmpty()/expression.text.isNotEmpty()/g' app/src/main/java/com/example/MainActivity.kt
sed -i 's/expression.length/expression.text.length/g' app/src/main/java/com/example/MainActivity.kt
sed -i 's/expression.count/expression.text.count/g' app/src/main/java/com/example/MainActivity.kt
sed -i 's/expression.last()/expression.text.last()/g' app/src/main/java/com/example/MainActivity.kt
sed -i 's/expression.lastIndex/expression.text.lastIndex/g' app/src/main/java/com/example/MainActivity.kt
sed -i 's/expression\[i\]/expression.text[i]/g' app/src/main/java/com/example/MainActivity.kt
sed -i 's/expression.substring/expression.text.substring/g' app/src/main/java/com/example/MainActivity.kt
sed -i 's/expression.dropLast/expression.text.dropLast/g' app/src/main/java/com/example/MainActivity.kt
sed -i 's/expression.split/expression.text.split/g' app/src/main/java/com/example/MainActivity.kt
sed -i 's/evaluate(expression.replace/evaluate(expression.text.replace/g' app/src/main/java/com/example/MainActivity.kt

# Replace modifications
# expression = ""
sed -i 's/expression = ""/expression = androidx.compose.ui.text.input.TextFieldValue("")/g' app/src/main/java/com/example/MainActivity.kt
# expression += ...
sed -i 's/expression += \(.*\)/expression = insertAtCursor(expression, \1)/g' app/src/main/java/com/example/MainActivity.kt
