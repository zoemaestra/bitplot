from PIL import Image

img = Image.open("test.bmp")
img = img.convert('RGB')
print(f"Image size: {img.size}")
papersize = input("Enter X*Y paper size: ")
paperX = int(papersize.split('*')[0])
paperY = int(papersize.split('*')[1])

margin = input("Enter minimum margin size: ")
margin = int(margin)

minsize = min(paperX, paperY) - margin
pixelSize = min(img.size[0], img.size[1]) / minsize

print(f"Pixel size: {round(pixelSize, 2)}mm^2")

colours = set()
for i in range(img.size[0]):
    for j in range(img.size[1]):
        pixel = img.getpixel((i, j))
        colours.add(pixel)

print('Colour count = ', len(colours))

input("Generate gcode? (press enter to continue)")

for colour in colours:
    open(f"gcode_{colour[0]}_{colour[1]}_{colour[2]}.gcode", 'w').close()
    file = open(f"gcode_{colour[0]}_{colour[1]}_{colour[2]}.gcode", "a")
    file.write("G28 ; Home all axes\n")
    file.write("G21 ; Set units to millimeters\n")
    file.write("G90 ; Use absolute positioning\n")
    file.write("G1 Z5 F5000 ; Lift pen\n")
    file.write("G1 X0 Y0 F3000 ; Move to origin\n")
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            pixel = img.getpixel((i, j))
            if pixel == colour:
                x = round(i / pixelSize, 2)
                y = round(j / pixelSize, 2)
                file.write(f"G1 X{x} Y{y} F3000 ; Move to pixel\n")
                file.write("G1 Z0 F5000 ; Lower pen\n")
                file.write("G1 Z5 F5000 ; Lift pen\n")