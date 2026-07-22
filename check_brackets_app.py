with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    lines = f.readlines()

count = 0
for i, line in enumerate(lines):
    count += line.count('{') - line.count('}')
    print(f"Line {i+1}: count {count}")
