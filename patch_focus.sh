#!/bin/bash
sed -i 's/            ) {/            ) {\n                val focusRequester = remember { androidx.compose.ui.focus.FocusRequester() }\n                LaunchedEffect(Unit) {\n                    try { focusRequester.requestFocus() } catch (e: Exception) {}\n                }/' app/src/main/java/com/example/MainActivity.kt
sed -i 's/modifier = Modifier.fillMaxWidth(),/modifier = Modifier.fillMaxWidth().androidx.compose.ui.focus.focusRequester(focusRequester),/' app/src/main/java/com/example/MainActivity.kt
