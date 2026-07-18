package com.example

import androidx.compose.ui.text.input.TextFieldValue
import androidx.compose.ui.text.TextRange
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.input.TransformedText
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.text.input.OffsetMapping

fun insertAtCursor(current: TextFieldValue, textToInsert: String): TextFieldValue {
    val min = current.selection.min
    val max = current.selection.max
    val before = current.text.substring(0, min)
    val after = current.text.substring(max)
    val newText = before + textToInsert + after
    return TextFieldValue(newText, TextRange(min + textToInsert.length))
}

fun deleteAtCursor(current: TextFieldValue): TextFieldValue {
    val min = current.selection.min
    val max = current.selection.max
    if (min != max) {
        val before = current.text.substring(0, min)
        val after = current.text.substring(max)
        return TextFieldValue(before + after, TextRange(min))
    } else if (min > 0) {
        val before = current.text.substring(0, min - 1)
        val after = current.text.substring(min)
        return TextFieldValue(before + after, TextRange(min - 1))
    }
    return current
}

class ExpressionVisualTransformation : VisualTransformation {
    override fun filter(text: AnnotatedString): TransformedText {
        val rawString = text.text
        val formattedString = formatExpression(rawString)
        
        val offsetMapping = object : OffsetMapping {
            override fun originalToTransformed(offset: Int): Int {
                if (offset <= 0) return 0
                if (offset >= rawString.length) return formattedString.length
                
                var rawPos = 0
                var formattedPos = 0
                while (rawPos < offset && formattedPos < formattedString.length) {
                    if (formattedString[formattedPos] == rawString[rawPos]) {
                        rawPos++
                    }
                    formattedPos++
                }
                return formattedPos
            }

            override fun transformedToOriginal(offset: Int): Int {
                if (offset <= 0) return 0
                if (offset >= formattedString.length) return rawString.length
                
                var rawPos = 0
                var formattedPos = 0
                while (formattedPos < offset && rawPos < rawString.length) {
                    if (formattedString[formattedPos] == rawString[rawPos]) {
                        rawPos++
                    }
                    formattedPos++
                }
                return rawPos
            }
        }
        return TransformedText(AnnotatedString(formattedString), offsetMapping)
    }
}
