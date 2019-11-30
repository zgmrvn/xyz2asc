import argparse
import os

# Reads an xyz.
def read_xyz(filename):
    coordinates = []

    with open(filename) as file:
        for line in file:
            line = line.split()
            line[0] = int(line[0])
            line[1] = int(line[1])
            line[2] = float(line[2])

            coordinates.append(line)

    return coordinates
    
# Writes a TB/TP ready Esri grid file (.asc).
def write_asc(coordinates, filename, cell_size, flip_y):
    last = coordinates[len(coordinates) - 1]
    grid_size = last[0] + 1

    with open(filename + ".asc", "w") as file:
        # Write headers.
        file.write("ncols " + str(grid_size) + "\n")
        file.write("nrows " + str(grid_size) + "\n")
        file.write("xllcorner 200000.000000\n")
        file.write("yllcorner 0.000000\n")
        file.write("cellsize " + str(cell_size) + "\n")
        file.write("NODATA_value -9999.000000\n")

        # flip on Y axis.
        if flip_y:
            temp_coordinates = []

            for y in range(grid_size):
                row = coordinates[(grid_size * y):(grid_size * y + grid_size)]
                row.reverse()
                temp_coordinates.extend(row)

            temp_coordinates.reverse()

            coordinates = temp_coordinates

        # Write coordinates.
        y = coordinates[0][1]

        for coordinate in coordinates:
            file.write(str(coordinate[2]))

            if (coordinate[1] != y):
                y = coordinate[1]
                file.write("\n")
            else:
                file.write(" ")

# Main.
# Find file.
xyz_files = list(filter(lambda f : f.endswith(".xyz"), os.listdir("./")))

if len(xyz_files) != 1:
    print("No .xyz or more than one .xyz in the current directory.")
    exit()

# Args.
cell_size = float(input("Cell size: "))
flip_y = input("Flip Y [y/N] ? ") == "y" if True else False

# Read xyz.
coordinates = read_xyz(xyz_files[0])

# Prepare data.
filename = xyz_files[0].split(".")[0]

# Write .asc.
write_asc(coordinates, filename, cell_size, flip_y)

print("Done.")
