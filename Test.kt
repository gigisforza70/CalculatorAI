import java.text.DecimalFormat
import java.text.DecimalFormatSymbols
import java.util.Locale

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

fun main() {
    val expr = "13824"
    val evalResult = 13824.0
    val df = DecimalFormat("#.########")
    val resultStr = df.format(evalResult).replace(".", ",")
    val resultPreview = formatExpression(resultStr)
    println(resultPreview)
}
