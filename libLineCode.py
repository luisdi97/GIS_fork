import pandas as pd
import numpy as np

"""
Create a LineCode matrix witch each line structure based in
some considerations:

- If any phase has a measurement with respect to the neutral, 
then so do the others and in the same way the neutral value.

- If any phase 1 does not has measurement with respect to other phase 2,
the phase 2 also does not has measurement with respect to other phase 1,
so if exists zeros rows, exists zeros columns in the same index.

- If linecode matrix does not have the cmatrix, it is because
all values of capacitance are zero.

"""

class LineCode():

    def set_LibraryType(self, libname:str):
        """ Set the appropiate structure LibraryType for
        better comprehension when iterating.
        """
        
        arguments = {"SUB": "SUB_",
                     "MT":"MT_",
                     "BT":"BT_",
                     ":":"_"}
        for k,v in arguments.items():
            Libname = libname.replace(k,v)
        
        return Libname

    def get_linecodes(self, df) -> list:
        """
        Get the matrix LineCode needed for lines in 
        OpenDSS simulator.

        The main consideration for build the matrix
        is that if there are zeros rows so there are
        zeros columns in the same index.

        Note 1: To assign the number of phases depending of count 
        of zeros in R mutual phases, the count is only in R phase
        therefore it can produce problems if LibraryType does not has
        phase designation and line in S or T phase.

        Note 2: The Linecode matrix was build with the linecode 
        OpenDSS structure so was necessary assign some string elements.

        Note 3: For LibraryTypes that does not has
        phase designation, we count the zeros in R mutual impedances
        because all of this Libraries have always R phase.

        +-----------------+-------------------+
        | Number of zeros |  Number of phases |
        +-----------------+-------------------+
        |        0        |        3          |
        |-----------------|-------------------|
        |        1        |        2          |
        |-----------------|-------------------|
        |        2        |        1          |
        |-----------------|-------------------|
        |        3        |        0          |
        +-----------------|-------------------+
        """
        
        # Number of lines
        nLines = len(df["LibraryType"])

        # List with each of the lines
        lines = []
        
        # For each line insert its attributes in dictionarie and append in list(lines)
        for n in range(nLines):
            line = {}
            for k in df.keys():
                line[k] = df[k][n]
            lines.append(line)
        
        LineCode_Data = []
        # Iterate in each dict line
        for line in lines:
            # LibraryType
            Libname = line["LibraryType"]
            # LibraryType modified
            libname = self.set_LibraryType(libname=Libname)
            # LibraryType as list
            libnameMod = libname.split("_")
            # If line is for BT or MT
            if "BT" in libnameMod or "MT" in libnameMod:
                # Assign the number of phases 
                if "ABC" in libnameMod:
                    nphases = 3
                elif "AB" in libnameMod or "AC" in libnameMod or "BC" in libnameMod:
                    nphases = 2
                elif "A" in libnameMod or "B" in libnameMod or "C" in libnameMod:
                    nphases = 1
                # Assign the number of phases depending of count of zeros in R mutual phases
                else:
                    Ltype = libnameMod[-1]
                    zeros_list = [line["R_RR"], line["R_RS"], line["R_RT"]]
                    zeros_count = zeros_list.count(0)
                    if zeros_count == 1 and Ltype=="3":    # Triplex only
                        nphases = 3
                    elif zeros_count == 1:
                        nphases = 2      # Reminder: type 6 as duplex
                    elif zeros_count == 2:
                        nphases = 1      # Raise exception
                    elif zeros_count == 0:
                        nphases = 3      # LV three-ph

                # Create 4x4 zeros matrix (1 neutral line)
                Zcarson = np.zeros([4,4], dtype=complex)
                # Zij
                Zcarson[0,0] += line["R_RR"] + 1j*line["X_RR"]
                Zcarson[0,1] += line["R_RS"] + 1j*line["X_RS"]
                Zcarson[0,2] += line["R_RT"] + 1j*line["X_RT"]
                Zcarson[1,0] += line["R_RS"] + 1j*line["X_RS"]
                Zcarson[1,1] += line["R_SS"] + 1j*line["X_SS"]
                Zcarson[1,2] += line["R_ST"] + 1j*line["X_ST"]
                Zcarson[2,0] += line["R_RT"] + 1j*line["X_RT"]
                Zcarson[2,1] += line["R_ST"] + 1j*line["X_ST"]
                Zcarson[2,2] += line["R_TT"] + 1j*line["X_TT"]

                # Zin
                Zcarson[0,3] += line["R_RN"] + 1j*line["X_RN"]
                Zcarson[1,3] += line["R_SN"] + 1j*line["X_SN"]
                Zcarson[2,3] += line["R_TN"]  + 1j*line["X_TN"] 
                
                # Znj
                Zcarson[3,0] += line["R_RN"] + 1j*line["X_RN"]
                Zcarson[3,1] += line["R_SN"] + 1j*line["X_SN"]
                Zcarson[3,2] += line["R_TN"] + 1j*line["X_TN"]

                # Znn
                Zcarson[3,3] += line["R_NN"] + 1j*line["X_NN"]

                Cmatrix = np.zeros([4,4], dtype=complex)
                
                # Cij
                Cmatrix[0,0] += line["C_RR"]
                Cmatrix[0,1] += line["C_RS"]
                Cmatrix[0,2] += line["C_RT"]
                Cmatrix[1,0] += line["C_RS"]
                Cmatrix[1,1] += line["C_SS"]
                Cmatrix[1,2] += line["C_ST"]
                Cmatrix[2,0] += line["C_RT"]
                Cmatrix[2,1] += line["C_ST"]
                Cmatrix[2,2] += line["C_TT"]

                # Cin
                Cmatrix[0,3] += line["C_RN"]
                Cmatrix[1,3] += line["C_SN"]
                Cmatrix[2,3] += line["C_TN"] 
                
                # Cnj
                Cmatrix[3,0] += line["C_RN"]
                Cmatrix[3,1] += line["C_SN"]
                Cmatrix[3,2] += line["C_TN"]

                # Cnn
                Zcarson[3,3] += line["C_NN"]

                # Store Zcarson zeros rows index 
                deleted_rows_index = []
                for i, row in enumerate(Zcarson):
                    if all(element == 0 for element in row):
                        deleted_rows_index.append(i)

                # Store Cmatrix zeros rows index 
                deleted_rows_index_C = []
                for i, row in enumerate(Cmatrix):
                    if all(element == 0 for element in row):
                        deleted_rows_index_C.append(i)

                # Removing zeros rows and columns per index
                Zcarson = np.delete(Zcarson, deleted_rows_index, axis=0)
                Zcarson = np.delete(Zcarson, deleted_rows_index, axis=1)
                Cmatrix = np.delete(Cmatrix, deleted_rows_index_C, axis=0)
                Cmatrix = np.delete(Cmatrix, deleted_rows_index_C, axis=1)

                # Resistances
                clean_rows_R = []
                for row in Zcarson:
                    clean_rows_R.append(str(list(np.real(row))).strip("]").strip("[").replace(",", ""))

                # Converting each row of the Zcarson matrix in rmatrix LineCode row
                rows_linecode_R = ""
                for row in clean_rows_R:
                    if len(clean_rows_R) == 1:
                        rows_linecode_R += f"[ {row} ]"
                    elif row == clean_rows_R[0]:
                        rows_linecode_R += f"[ {row} "
                    elif row == clean_rows_R[-1]:
                        rows_linecode_R += f"| {row} ]"
                    elif row == clean_rows_R[-2]:
                        rows_linecode_R += f"| {row} |"
                    else:
                        rows_linecode_R += f"| {row} |"

                # Putting together the linecode
                linecode_matrix_R = f"""New Linecode.{line["LibraryType"].replace(" ", "")} nphases={nphases} units=km
~ rmatrix = {rows_linecode_R}  \n"""

                # Reactances
                clean_rows_X = []
                for row in Zcarson:
                    clean_rows_X.append(str(list(np.real(row))).strip("]").strip("[").replace(",", ""))

                # Converting each row of the Zcarson matrix in xmatrix LineCode row
                rows_linecode_X = ""
                for row in clean_rows_X:
                    if len(clean_rows_X) == 1:
                        rows_linecode_X += f"[ {row} ]"
                    elif row == clean_rows_X[0]:
                        rows_linecode_X += f"[ {row} "
                    elif row == clean_rows_X[-1]:
                        rows_linecode_X += f"| {row} ]"
                    else:
                        rows_linecode_X += f"| {row} |"

                # Putting together the linecode
                linecode_matrix_X = f"""~ xmatrix = {rows_linecode_X}  
"""

                # Capacitances
                clean_rows_C = []
                for row in Cmatrix:
                    clean_rows_C.append(str(list(np.real(row))).strip("]").strip("[").replace(",", ""))

                if len(clean_rows_C) != 0:
                    # Converting each row of the Cmatrix in rmatrix LineCode row
                    rows_linecode_C = ""
                    for row in clean_rows_C:
                        if len(clean_rows_C) == 1:
                            rows_linecode_C += f"[ {row} ]"
                        elif row == clean_rows_C[0]:
                            rows_linecode_C += f"[ {row} "
                        elif row == clean_rows_C[-1]:
                            rows_linecode_C += f"| {row} ]"
                        elif row == clean_rows_R[-2]:
                            rows_linecode_C += f"| {row} |"
                        else:
                            rows_linecode_C += f"| {row} |"

                        # Putting together the linecode
                    linecode_matrix_C = f"""~ cmatrix = {rows_linecode_C}
~ normamps={line["IrLimit1"]} \n"""
                else:
                    linecode_matrix_C = f"""~ normamps={line["IrLimit1"]} \n"""

                # Concateing the rmatrix with xmatrix and cmatrix
                lineCode_Matrix = linecode_matrix_R + linecode_matrix_X + linecode_matrix_C + "\n"

                # Store each linecode in a list
                LineCode_Data.append(lineCode_Matrix)

        return LineCode_Data

    def get_LineCode(self, df) -> None:
        
        # Call the linecode creator method
        LineCode_Data = self.get_linecodes(df)

        LineCode_DataMod = []
        for linecode in LineCode_Data:
            linecode = linecode.replace("||", "|").replace("|[", "|").replace("   "," ]") # For this need 2 spaces after rmatrix and xmatrix
            LineCode_DataMod.append(linecode)

        # Output file
        output_file = "Lineas_LineCode.dss"
        # Generate .dss file 
        with open(output_file, "w") as f:
            for linecode in LineCode_DataMod:
                f.write(linecode)
        
        return LineCode_DataMod


if __name__ == "__main__":

    # Create instance
    linecode = LineCode()

    # Input file
    input_file = "./data/Lineas.xlsx"

    # Create a dataframe -> drop_duplicates() delete the duplicate rows
    df = pd.read_excel(input_file, sheet_name= "Lineas", skiprows= 2).drop_duplicates()
    f = lambda x: x*1e3   # From micro to nano per mile
    # Convert capacitance from microF to nanoF
    for c in df.columns:
        if "C_" in c:
            df[c] = df[c].apply(f)

    # Execute method that obtains LineCodes
    linecode.get_LineCode(df)
