package com.example.ui
import androidx.compose.foundation.layout.*
import androidx.compose.ui.Modifier
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment

@Composable
fun test4() {
    Row(Modifier.wrapContentHeight()) {
        BoxWithConstraints(Modifier.weight(1f).fillMaxHeight()) {
            // this is what CalculatorButton does inside tabletPortrait
        }
    }
}
