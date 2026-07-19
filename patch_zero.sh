#!/bin/bash
sed -i 's/if (text == "0") Modifier.fillMaxWidth(0.95f).height(buttonHeight)/Modifier.size(buttonHeight)/g' app/src/main/java/com/example/MainActivity.kt
sed -i 's/else Modifier.size(buttonHeight)//g' app/src/main/java/com/example/MainActivity.kt
