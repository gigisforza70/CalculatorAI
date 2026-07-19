#!/bin/bash
sed -i 's/} else if (isLandscape) {/} else if (isLandscape) {/g' app/src/main/java/com/example/MainActivity.kt
sed -i 's/} \n                )/} else Modifier.size(buttonHeight)\n                )/g' app/src/main/java/com/example/MainActivity.kt
