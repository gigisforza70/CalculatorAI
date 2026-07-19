#!/bin/bash
sed -i 's/readOnly = true,/readOnly = false,/g' app/src/main/java/com/example/MainActivity.kt
