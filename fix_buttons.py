with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Only replace inside the tablet portrait branch
start_idx = content.find('if (isTabletPortrait) {')
end_idx = content.find('} else if (isTabletLandscape) {')
if start_idx != -1 and end_idx != -1:
    sub = content[start_idx:end_idx]
    sub = sub.replace('isLandscape = true)', 'isTabletPortrait = true)')
    content = content[:start_idx] + sub + content[end_idx:]

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
