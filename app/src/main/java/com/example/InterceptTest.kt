package com.example
import androidx.compose.ui.platform.InterceptPlatformTextInput
import androidx.compose.runtime.Composable
import kotlinx.coroutines.awaitCancellation
import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.ui.ExperimentalComposeUiApi

@OptIn(ExperimentalComposeUiApi::class, ExperimentalFoundationApi::class)
@Composable
fun Test() {
    InterceptPlatformTextInput(
        interceptor = { _, _ -> awaitCancellation() }
    ) {
        
    }
}
