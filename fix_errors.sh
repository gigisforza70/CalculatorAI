#!/bin/bash
sed -i 's/viewModel.addHistory(expression,/viewModel.addHistory(expression.text,/g' app/src/main/java/com/example/MainActivity.kt
sed -i 's/expression = resultPreview.replace/expression = androidx.compose.ui.text.input.TextFieldValue(resultPreview.replace/g' app/src/main/java/com/example/MainActivity.kt
sed -i 's/expression\[i\]/expression.text[i]/g' app/src/main/java/com/example/MainActivity.kt
sed -i 's/expression\[i-1\]/expression.text[i-1]/g' app/src/main/java/com/example/MainActivity.kt
sed -i 's/expression = expression.text.substring(0, i - 1)/expression = androidx.compose.ui.text.input.TextFieldValue(expression.text.substring(0, i - 1)/g' app/src/main/java/com/example/MainActivity.kt
sed -i 's/expression = expression.text.substring(0, i + 1)/expression = androidx.compose.ui.text.input.TextFieldValue(expression.text.substring(0, i + 1)/g' app/src/main/java/com/example/MainActivity.kt
sed -i 's/expression = expression.text.dropLast(1)/expression = androidx.compose.ui.text.input.TextFieldValue(expression.text.dropLast(1))/g' app/src/main/java/com/example/MainActivity.kt
sed -i 's/text = formatExpression(expression),/text = formatExpression(expression.text),/g' app/src/main/java/com/example/MainActivity.kt
sed -i 's/expression = entry.expression/expression = androidx.compose.ui.text.input.TextFieldValue(entry.expression)/g' app/src/main/java/com/example/MainActivity.kt

# Also expression is used where I might have added ")" previously, wait, line 180 and 183 needs an extra closing parenthesis because I wrapped them in TextFieldValue().
