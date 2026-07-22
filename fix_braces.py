with open('app/src/main/java/com/example/ui/UnitConverter.kt', 'r') as f:
    lines = f.readlines()

# The extra `}` is at 378 and 467. Let's look at lines 375-385.
# Let's just fix it by string manipulation.

for i in range(len(lines)):
    if "        }" in lines[i] and "                }" in lines[i+1] and "            }" in lines[i+2] and "        )" in lines[i+3]:
        lines[i] = "                }\n"
        lines[i+1] = "            }\n"
        lines[i+2] = "        )\n"
        lines[i+3] = "        }\n"

with open('app/src/main/java/com/example/ui/UnitConverter.kt', 'w') as f:
    f.writelines(lines)
