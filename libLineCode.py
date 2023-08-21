"""Convert to a suitable Library Name.

It calls ./data/Lineas.xlsx in order to convert it into
a suitable file to be called for QGIS2OPENDSS plug-in.

"""

import pandas as pd


class LineCode():

    def get_linecodes(self, df):

        # Dictionary that contents all of line data
        linesData = {}
    
        # Inserting str(key) and list(value) in dict
        for key in df.keys():
            values = [i for i in df[key]]
            linesData[key] = values
        
        # Number of lines
        nLines = len(linesData["LibraryType"])

        # List with each of the lines
        lines = []
        
        # For each line insert its attributes in dictionarie and append in list(lines)
        for n in range(nLines):
            line = {}
            for k in df.keys():
                line[k] = linesData[k][n]
            lines.append(line)
        
        # For dict(line) in list(lines) construct the LineCode from its attributes
        LineCodeData = []
        for line in lines:
            Libname = line["LibraryType"]
            if "BT" in Libname:
                matrix = (
                    "New.Linecode." + line["LibraryType"] + " nphases=" + " units=mile" + "\n"
                    + "~" + " rmatrix=[ " + str(line["R_RR"]) + " " + str(line["R_RS"]) + " " + str(line["R_RT"]) + " | "
                                          + str(line["R_RN"]) + " " + str(line["R_RG"]) + " " + str(line["R_SS"]) + " | "
                                          + str(line["R_ST"]) + " " + str(line["R_SN"]) + " " + str(line["R_SG"]) + " | " + "\n"
                    
                    
                    + "~" + " xmatrix=[ " + "\n"
                    + "~" + " Normamps=" + "\n"
                    + "~" + " kron=y" + "\n"
                )
                LineCodeData.append(f"{matrix}\n")

        # Output file
        output_file = "LineCode.dss"

        # Generate .txt file 
        with open(output_file, "w") as f:
            for linecode in LineCodeData:
                f.write(linecode)


if __name__ == "__main__":

    # Create instance
    linecode = LineCode()

    # Input file
    input_file = "./data/Lineas.xlsx"

    # Create a dataframe -> drop_duplicates() delete the duplicate rows
    df = pd.read_excel(input_file, sheet_name= "Lineas", skiprows= 2).drop_duplicates()

    # Execute method that obtains LineCodes
    linecode.get_linecodes(df=df)



    # Mario
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
    """
