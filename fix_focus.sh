#!/bin/bash
sed -i '/val focusRequester = remember { androidx.compose.ui.focus.FocusRequester() }/d' app/src/main/java/com/example/MainActivity.kt
sed -i '/LaunchedEffect(Unit) {/d' app/src/main/java/com/example/MainActivity.kt
sed -i '/try { focusRequester.requestFocus() } catch (e: Exception) {}/d' app/src/main/java/com/example/MainActivity.kt
