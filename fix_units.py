import re

with open('app/src/main/java/com/example/ui/UnitConverter.kt', 'r') as f:
    content = f.read()

# Update UnitType class
content = content.replace('data class UnitType(val name: String, val value: Double)', 'data class UnitType(val name: String, val value: Double, val symbol: String)')

# Update lists
replacements = {
    'UnitType("Nanometers", 1e-9)': 'UnitType("Nanometers", 1e-9, "nm")',
    'UnitType("Micrometers", 1e-6)': 'UnitType("Micrometers", 1e-6, "μm")',
    'UnitType("Millimeters", 0.001)': 'UnitType("Millimeters", 0.001, "mm")',
    'UnitType("Centimeters", 0.01)': 'UnitType("Centimeters", 0.01, "cm")',
    'UnitType("Decimeters", 0.1)': 'UnitType("Decimeters", 0.1, "dm")',
    'UnitType("Meters", 1.0)': 'UnitType("Meters", 1.0, "m")',
    'UnitType("Kilometers", 1000.0)': 'UnitType("Kilometers", 1000.0, "km")',
    'UnitType("Inches", 0.0254)': 'UnitType("Inches", 0.0254, "in")',
    'UnitType("Feet", 0.3048)': 'UnitType("Feet", 0.3048, "ft")',
    'UnitType("Yards", 0.9144)': 'UnitType("Yards", 0.9144, "yd")',
    'UnitType("Miles", 1609.344)': 'UnitType("Miles", 1609.344, "mi")',
    'UnitType("Nautical miles", 1852.0)': 'UnitType("Nautical miles", 1852.0, "NM")',

    'UnitType("Square millimeters", 0.000001)': 'UnitType("Square millimeters", 0.000001, "mm²")',
    'UnitType("Square centimeters", 0.0001)': 'UnitType("Square centimeters", 0.0001, "cm²")',
    'UnitType("Square meters", 1.0)': 'UnitType("Square meters", 1.0, "m²")',
    'UnitType("Hectares", 10000.0)': 'UnitType("Hectares", 10000.0, "ha")',
    'UnitType("Square kilometers", 1000000.0)': 'UnitType("Square kilometers", 1000000.0, "km²")',
    'UnitType("Square inches", 0.00064516)': 'UnitType("Square inches", 0.00064516, "sq in")',
    'UnitType("Square feet", 0.09290304)': 'UnitType("Square feet", 0.09290304, "sq ft")',
    'UnitType("Square yards", 0.83612736)': 'UnitType("Square yards", 0.83612736, "sq yd")',
    'UnitType("Acres", 4046.8564224)': 'UnitType("Acres", 4046.8564224, "ac")',
    'UnitType("Square miles", 2589988.110336)': 'UnitType("Square miles", 2589988.110336, "sq mi")',

    'UnitType("Milliliters", 0.001)': 'UnitType("Milliliters", 0.001, "ml")',
    'UnitType("Cubic centimeters", 0.001)': 'UnitType("Cubic centimeters", 0.001, "cm³")',
    'UnitType("Liters", 1.0)': 'UnitType("Liters", 1.0, "l")',
    'UnitType("Cubic meters", 1000.0)': 'UnitType("Cubic meters", 1000.0, "m³")',
    'UnitType("Teaspoons (US)", 0.00492892)': 'UnitType("Teaspoons (US)", 0.00492892, "tsp")',
    'UnitType("Tablespoons (US)", 0.0147868)': 'UnitType("Tablespoons (US)", 0.0147868, "tbsp")',
    'UnitType("Fluid ounces (US)", 0.0295735)': 'UnitType("Fluid ounces (US)", 0.0295735, "fl oz")',
    'UnitType("Cups (US)", 0.236588)': 'UnitType("Cups (US)", 0.236588, "c")',
    'UnitType("Pints (US)", 0.473176)': 'UnitType("Pints (US)", 0.473176, "pt")',
    'UnitType("Quarts (US)", 0.946353)': 'UnitType("Quarts (US)", 0.946353, "qt")',
    'UnitType("Gallons (US)", 3.78541)': 'UnitType("Gallons (US)", 3.78541, "gal")',
    'UnitType("Cubic inches", 0.0163871)': 'UnitType("Cubic inches", 0.0163871, "cu in")',
    'UnitType("Cubic feet", 28.3168)': 'UnitType("Cubic feet", 28.3168, "cu ft")',

    'UnitType("Micrograms", 1e-9)': 'UnitType("Micrograms", 1e-9, "μg")',
    'UnitType("Milligrams", 1e-6)': 'UnitType("Milligrams", 1e-6, "mg")',
    'UnitType("Grams", 0.001)': 'UnitType("Grams", 0.001, "g")',
    'UnitType("Kilograms", 1.0)': 'UnitType("Kilograms", 1.0, "kg")',
    'UnitType("Metric tonnes", 1000.0)': 'UnitType("Metric tonnes", 1000.0, "t")',
    'UnitType("Ounces", 0.0283495)': 'UnitType("Ounces", 0.0283495, "oz")',
    'UnitType("Pounds", 0.453592)': 'UnitType("Pounds", 0.453592, "lb")',
    'UnitType("Stones", 6.35029)': 'UnitType("Stones", 6.35029, "st")',
    'UnitType("Short tons (US)", 907.185)': 'UnitType("Short tons (US)", 907.185, "ton")',
    'UnitType("Long tons (UK)", 1016.05)': 'UnitType("Long tons (UK)", 1016.05, "ton")',

    'UnitType("Bits", 0.125)': 'UnitType("Bits", 0.125, "bit")',
    'UnitType("Bytes", 1.0)': 'UnitType("Bytes", 1.0, "B")',
    'UnitType("Kilobits", 128.0)': 'UnitType("Kilobits", 128.0, "kb")',
    'UnitType("Kilobytes", 1024.0)': 'UnitType("Kilobytes", 1024.0, "KB")',
    'UnitType("Megabits", 131072.0)': 'UnitType("Megabits", 131072.0, "Mb")',
    'UnitType("Megabytes", 1048576.0)': 'UnitType("Megabytes", 1048576.0, "MB")',
    'UnitType("Gigabits", 134217728.0)': 'UnitType("Gigabits", 134217728.0, "Gb")',
    'UnitType("Gigabytes", 1073741824.0)': 'UnitType("Gigabytes", 1073741824.0, "GB")',
    'UnitType("Terabits", 137438953472.0)': 'UnitType("Terabits", 137438953472.0, "Tb")',
    'UnitType("Terabytes", 1099511627776.0)': 'UnitType("Terabytes", 1099511627776.0, "TB")',
    'UnitType("Petabytes", 1125899906842624.0)': 'UnitType("Petabytes", 1125899906842624.0, "PB")',
    
    'UnitType("Celsius", 1.0)': 'UnitType("Celsius", 1.0, "°C")',
    'UnitType("Fahrenheit", 1.0)': 'UnitType("Fahrenheit", 1.0, "°F")',
    'UnitType("Kelvin", 1.0)': 'UnitType("Kelvin", 1.0, "K")'
}

for k, v in replacements.items():
    content = content.replace(k, v)

with open('app/src/main/java/com/example/ui/UnitConverter.kt', 'w') as f:
    f.write(content)
