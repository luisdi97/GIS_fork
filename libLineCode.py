"""Convert to a suitable Library Name.

It calls ./data/Lineas.txt in order to convert it into
a suitable file to be called for the Blue.
"""

directory = "./data/Lineas.txt"
libraries = []
with open(directory, "r") as file:
    for lib in file:
        if "Element" in lib:
            continue
        if "LineAsym" in lib:
            continue
        if "LibraryType" in lib:
            continue
        if len(lib) > 1:
            libName = lib.replace(" ", "")
            libraries.append(libName)

newfile = "./data/libLineCode.dss"
with open(newfile, "w") as file:
    for linecode in libraries:
        file.write("New Linecode." + linecode)
