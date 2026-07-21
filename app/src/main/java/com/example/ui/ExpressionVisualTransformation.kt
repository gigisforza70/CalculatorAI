package com.example.ui

import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.input.OffsetMapping
import androidx.compose.ui.text.input.TransformedText
import androidx.compose.ui.text.input.VisualTransformation

class ExpressionVisualTransformation : VisualTransformation {
    override fun filter(text: AnnotatedString): TransformedText {
        val original = text.text
        val regex = Regex("([0-9]+(,[0-9]*)?)")
        val builder = StringBuilder()
        
        val originalToTransformed = mutableListOf<Int>()
        val transformedToOriginal = mutableListOf<Int>()
        
        var originalIndex = 0
        var formattedIndex = 0
        
        for (match in regex.findAll(original)) {
            val start = match.range.first
            
            // Append non-matching part
            while (originalIndex < start) {
                builder.append(original[originalIndex])
                originalToTransformed.add(formattedIndex)
                transformedToOriginal.add(originalIndex)
                originalIndex++
                formattedIndex++
            }
            
            // Append matching part with dots
            val numStr = match.value
            val parts = numStr.split(',')
            val integerPart = parts[0]
            
            var integerIndex = 0
            val integerLen = integerPart.length
            for (i in 0 until integerLen) {
                if (integerPart[i] == '-') {
                    builder.append('-')
                    originalToTransformed.add(formattedIndex)
                    transformedToOriginal.add(originalIndex)
                    originalIndex++
                    formattedIndex++
                    integerIndex++
                    continue
                }
                
                originalToTransformed.add(formattedIndex)
                builder.append(integerPart[i])
                transformedToOriginal.add(originalIndex)
                originalIndex++
                formattedIndex++
                integerIndex++
                
                // Add dot if needed
                val remaining = integerLen - integerIndex
                if (remaining > 0 && remaining % 3 == 0) {
                    builder.append('.')
                    transformedToOriginal.add(originalIndex)
                    formattedIndex++
                }
            }
            
            if (parts.size > 1 || numStr.endsWith(",")) {
                // Append comma
                builder.append(',')
                originalToTransformed.add(formattedIndex)
                transformedToOriginal.add(originalIndex)
                originalIndex++
                formattedIndex++
                
                // Append fractional part
                if (parts.size > 1) {
                    val fractionalPart = parts[1]
                    for (i in fractionalPart.indices) {
                        builder.append(fractionalPart[i])
                        originalToTransformed.add(formattedIndex)
                        transformedToOriginal.add(originalIndex)
                        originalIndex++
                        formattedIndex++
                    }
                }
            }
        }
        
        // Append remaining non-matching part
        while (originalIndex < original.length) {
            builder.append(original[originalIndex])
            originalToTransformed.add(formattedIndex)
            transformedToOriginal.add(originalIndex)
            originalIndex++
            formattedIndex++
        }
        originalToTransformed.add(formattedIndex)
        transformedToOriginal.add(originalIndex)
        
        val offsetMapping = object : OffsetMapping {
            override fun originalToTransformed(offset: Int): Int {
                return if (offset < originalToTransformed.size) originalToTransformed[offset] else formattedIndex
            }
            override fun transformedToOriginal(offset: Int): Int {
                return if (offset < transformedToOriginal.size) transformedToOriginal[offset] else originalIndex
            }
        }
        
        return TransformedText(
            AnnotatedString(builder.toString()),
            offsetMapping
        )
    }
}
