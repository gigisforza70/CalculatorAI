package com.example

import org.junit.Test
import java.text.DecimalFormat
import java.text.DecimalFormatSymbols
import java.util.Locale

class FormatTest {

fun formatExpression(expr: String): String {
    val regex = Regex("([0-9]+(,[0-9]*)?)")
    return expr.replace(regex) { matchResult ->
        val numStr = matchResult.value
        val parts = numStr.split(',')
        val integerPart = parts[0]
        val formattedInteger = if (integerPart.isNotEmpty() && integerPart != "-") {
            try {
                val reversed = integerPart.reversed()
                val chunked = reversed.chunked(3)
                chunked.joinToString(".").reversed()
            } catch (e: Exception) {
                integerPart
            }
        } else integerPart
        
        if (parts.size > 1) {
            "$formattedInteger,${parts[1]}"
        } else if (numStr.endsWith(",")) {
            "$formattedInteger,"
        } else {
            formattedInteger
        }
    }
}

    @Test
    fun testFormat() {
        println("Italian Locale: " + formatExpression(DecimalFormat("#.########", DecimalFormatSymbols(Locale.ITALY)).format(13824.0).replace(".", ",")))
        println("US Locale: " + formatExpression(DecimalFormat("#.########", DecimalFormatSymbols(Locale.US)).format(13824.0).replace(".", ",")))
    }
}
