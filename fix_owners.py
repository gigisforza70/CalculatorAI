with open('app/src/main/java/com/example/FloatingServiceOwners.kt', 'r') as f:
    content = f.read()

content = content.replace('savedStateRegistryController.performRestore(null)', 'savedStateRegistryController.performAttach()\n        savedStateRegistryController.performRestore(null)')

with open('app/src/main/java/com/example/FloatingServiceOwners.kt', 'w') as f:
    f.write(content)
