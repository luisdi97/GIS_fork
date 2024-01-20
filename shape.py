"""Parse *.shp attributes.

This program translates and adapts a given format of
certain kind of shape file attribute's name into a
standard notation requires for QGIS based on the manual
of "QGIS2OPENDSS" plug-in.

   Mario Roberto Peralta A.
   Universidad de Costa Rica (UCR)

email: Mario.Peralta@ucr.ac.cr
Electric Power & Energy Research Laboratory (EPERLab).

"""
import numpy as np       # To adjacency matrix
import pandas as pd      # To read and convert data
# To creat points and lines in coordinates sys
from shapely.geometry import Point, LineString
import geopandas as gpd   # To generate shapesfiles


class CKTdata():
    """Retrieve circuit data.

    Class that contains all of the objects (devices) of the circuit
    and its data regarding the sheets of the *.xlsx file whose
    attributes come in Naplan notation.

    """
    def __init__(self):
        self._buses = {}
        self._lines = {}
        self._AsymTx = {}
        self._Tx = {}
        self._loads = {}
        self._fuses = {}
        self._regulators = {}
        self._ders = {}
        self._reclosers = {}
        self._publicLights = {}

    def call_data(self, path: str) -> None:
        # Read data
        df = pd.read_excel(path,
                           sheet_name=None)
        # List of all sheets
        sheets = list(df.keys())

        # Set data regarding the sheet
        for sheet in df.keys():
            # Buses
            if sheet == sheets[0]:
                for c in df[sheet].columns:
                    values = [v for v in df[sheet][c]]
                    # Update attribute
                    self._buses[c] = values
            # Lines
            elif sheet == sheets[1]:
                for c in df[sheet].columns:
                    values = [v for v in df[sheet][c]]
                    # Update attribute
                    self._lines[c] = values
            # Asymetrical Transformer
            elif sheet == sheets[2]:
                for c in df[sheet].columns:
                    values = [v for v in df[sheet][c]]
                    # Update attribute
                    self._AsymTx[c] = values
            # Transformer
            elif sheet == sheets[3]:
                for c in df[sheet].columns:
                    values = [v for v in df[sheet][c]]
                    # Update attribute
                    self._Tx[c] = values
            # Loads
            elif sheet == sheets[4]:
                for c in df[sheet].columns:
                    values = [v for v in df[sheet][c]]
                    # Update attribute
                    self._loads[c] = values
            # Fuses
            elif sheet == sheets[5]:
                for c in df[sheet].columns:
                    values = [v for v in df[sheet][c]]
                    # Update attribute
                    self._fuses[c] = values
            # Regulators
            elif sheet == sheets[6]:
                for c in df[sheet].columns:
                    values = [v for v in df[sheet][c]]
                    # Update attribute
                    self._regulators[c] = values
            # DER's
            elif sheet == sheets[7]:
                for c in df[sheet].columns:
                    values = [v for v in df[sheet][c]]
                    # Update attribute
                    self._ders[c] = values
            # Reclosers
            elif sheet == sheets[8]:
                for c in df[sheet].columns:
                    values = [v for v in df[sheet][c]]
                    # Update attribute
                    self._reclosers[c] = values
            # PublicLights
            elif sheet == sheets[9]:
                for c in df[sheet].columns:
                    values = [v for v in df[sheet][c]]
                    # Update attribute
                    self._publicLights[c] = values

    def concat_linecols(self) -> list[str]:
        """Concatenate columns.

        Resulting shape of a single row:
        ['NodeFrom1'&'NodeTo1'&'LibraryType1'&... &'attr1M',
        'NodeFrom2'&'NodeTo2'&'LibraryType2'&... &'attr2M', ...
        ...,
        'NodeFromN'&'NodeToN'&'LibraryTypeN'&... &'attrNM'].

        """
        linesData = self._lines
        for k, v in linesData.items():
            if k == "Node1":
                col1 = v
            elif k == "Node2":
                col2 = v
            elif k == "Name":
                col3 = v
            elif k == "LibraryType":
                col4 = v
            elif k == "Length":
                col5 = v
            elif k == "Un":
                col6 = v

        cols = zip(col1, col2, col3, col4, col5, col6)
        linesID = [f"{c1}&{c2}&{c3}&{c4}&{c5}&{c6}"
                   for c1, c2, c3, c4, c5, c6 in cols]

        return linesID

    def concat_buscols(self) -> list[str]:
        """Concatenate columns.

        Resulting shape of a single row:
        ['Name'&'Un'&'CoordX1'&... &'attr1M',
        'Name'&'Un'&'CoordX1'&... &'attr2M', ...
        ...,
        'NodeFromN'&'NodeToN'&'LibraryTypeN'&... &'attrNM'].

        """
        busesData = self._buses
        for k, v in busesData.items():
            if k == "Name":
                col1 = v
            elif k == "Un":
                col2 = v
            elif k == "CoordX1":
                col3 = v
            elif k == "CoordY2":
                col4 = v

        cols = zip(col1, col2, col3, col4)
        busID = [f"{c1}&{c2}&{c3}&{c4}"
                 for c1, c2, c3, c4 in cols]

        return busID

    def concat_Txcols(self) -> list[str]:
        """Concatenate columns.

        Resulting shape of a single row:
        ['Name'&'Node1'&'Node2'&... &'attr1M',
        'Name'&'Un'&'CoordX1'&... &'attr2M', ...
        ...,
        'NodeFromN'&'NodeToN'&'LibraryTypeN'&... &'attrNM'].

        """
        TxData = self._AsymTx
        for k, v in TxData.items():
            if k == "Name":
                col1 = v
            elif k == "Node1":
                col2 = v
            elif k == "Node2":
                col3 = v
            elif k == "Switch1":
                col4 = v
            elif k == "Switch2":
                col5 = v
            elif k == "IsRegulated":
                col6 = v
            elif k == "Un1":
                col7 = v
            elif k == "Un2":
                col8 = v
            elif k == "Sr":
                col9 = v
            elif k == "LibraryType":
                col10 = v
            elif k == "CoordX1":
                col11 = v
            elif k == "CoordY1":
                col12 = v

        cols = zip(col1, col2, col3, col4, col5,
                   col6, col7, col8, col9, col10,
                   col11, col12)
        TxID = []
        for attrs in cols:
            row = ""
            for attr in attrs:
                row += f"{attr}&"
            TxID.append(row.strip("&"))

        return TxID

    def concat_loadcols(self) -> list[str]:
        """Concatenate columns.

        Resulting shape of a single row:
        ['Name'&'Node1'&'Node2'&... &'attr1M',
        'Name'&'Un'&'CoordX1'&... &'attr2M', ...
        ...,
        'NodeFromN'&'NodeToN'&'LibraryTypeN'&... &'attrNM'].

        """
        loadsData = self._loads
        for k, v in loadsData.items():
            if k == "Node1":
                col1 = v
            elif k == "Name":
                col2 = v
            elif k == "Phase":
                col3 = v
            elif k == "Switch1":
                col4 = v
            elif k == "Un":
                col5 = v
            elif k == "E":
                col6 = v
            elif k == "VelanderK1":
                col7 = v
            elif k == "LfType":
                col8 = v
            elif k == "Unit":
                col9 = v
            elif k == "CosPhi":
                col10 = v
            elif k == "CoordX1":
                col11 = v
            elif k == "CoordY1":
                col12 = v
            elif k == "Tipo":
                col13 = v

        cols = zip(col1, col2, col3, col4, col5,
                   col6, col7, col8, col9, col10,
                   col11, col12, col13)
        loadID = []
        for attrs in cols:
            row = ""
            for attr in attrs:
                row += f"{attr}&"
            loadID.append(row.strip("&"))

        return loadID

    def concat_fusecols(self) -> list[str]:
        """Concatenate columns.

        Resulting shape of a single row:
        ['Name'&'Phase'&'IsActive'&... &'attr1M',
        'Name'&'Phase'&'IsActive'&... &'attr2M', ...
        ...,
        'NameN'&'PhaseN'&'IsActive'&... &'attrNM'].

        """
        fuseData = self._fuses
        for k, v in fuseData.items():
            if k == "Name":
                col1 = v
            elif k == "Phase":
                col2 = v
            elif k == "IsActive":
                col3 = v
            elif k == "OnElement":
                col4 = v
            elif k == "X":
                col5 = v
            elif k == "Y":
                col6 = v
        cols = zip(col1, col2, col3, col4, col5, col6)
        fuseID = [f"{c1}&{c2}&{c3}&{c4}&{c5}&{c6}"
                  for c1, c2, c3, c4, c5, c6 in cols]

        return fuseID

    def concat_regulatorcols(self) -> list[str]:
        """Concatenate regulator columns.

        Resulting shape of a single row:
        ['Name'&'Node1'&'Node2'&... &'attr1M',
        'Name'&'Node1'&'Node2'&... &'attr2M', ...
        ...,
        'NameN'&'Node1N'&'Node2N'&... &'attrNM'].

        """
        regulatorData = self._regulators
        for k, v in regulatorData.items():
            if k == "Name":
                col1 = v
            elif k == "Node1":
                col2 = v
            elif k == "Node2":
                col3 = v
            elif k == "Switch1":
                col4 = v
            elif k == "Switch2":
                col5 = v
            elif k == "Un1":
                col6 = v
            elif k == "Un2":
                col7 = v
            elif k == "Phase":
                col8 = v
            elif k == "LibraryType":
                col9 = v
            elif k == "X":
                col10 = v
            elif k == "Y":
                col11 = v

        cols = zip(col1, col2, col3, col4,
                   col5, col6, col7,
                   col8, col9, col10, col11)
        regulatorID = []
        for attrs in cols:
            row = ""
            for attr in attrs:
                row += f"{attr}&"
            regulatorID.append(row.strip("&"))

        return regulatorID

    def concat_PVcols(self) -> list[str]:
        """Concatenate PV columns.

        Resulting shape of a single row:
        ['Name'&'Node1'&'Switch1'&... &'attr1M',
        'Name'&'Node1'&'Switch1'&... &'attr2M', ...
        ...,
        'NameN'&'Node1N'&'Switch1N'&... &'attrNM'].

        """
        pvData = self._ders
        for k, v in pvData.items():
            col1 = []
            col2 = []
            col3 = []
            col4 = []
            col5 = []
            col6 = []
            col7 = []
            col8 = []
            col9 = []
            col10 = []
            col11 = []
            col12 = []
            col13 = []
            col14 = []
            col15 = []

            if k == "Name":
                col1 = v
            elif k == "Node1":
                col2 = v
            elif k == "Switch1":
                col3 = v
            elif k == "Pset":
                col4 = v
            elif k == "Cosr":
                col5 = v
            elif k == "Unit":
                col6 = v
            elif k == "Phase":
                col7 = v
            elif k == "Sr":
                col8 = v
            elif k == "nProductionType":
                col9 = v
            elif k == "Ur":
                col10 = v
            elif k == "Un":
                col11 = v
            elif k == "Sk2max":
                col12 = v
            elif k == "Sk2min":
                col13 = v
            if k == "CURVE1_P":
                col14 = v
            if k == "CURVE2_Q":
                col15 = v

        cols = zip(col1, col2, col3, col4, col5, col6,
                   col7, col8, col9, col10,
                   col11, col12, col13, col14, col15)

        pvID = []
        for attrs in cols:
            row = ""
            for attr in attrs:
                row += f"{attr}&"
            pvID.append(row.strip("&"))

        return pvID

    def concat_reclosercols(self) -> list[str]:
        """Concatenate recloser columns.

        Resulting shape of a single row:
        ['Name'&'Phase'&'Switch'&... &'attr1M',
        'Name'&'Phase'&'Switch'&... &'attr2M', ...
        ...,
        'NameN'&'PhaseN'&'SwitchN'&... &'attrNM'].

        """
        recloserData = self._reclosers
        for k, v in recloserData.items():
            if k == "Name":
                col1 = v
            elif k == "Phase":
                col2 = v
            elif k == "Switch":
                col3 = v
            elif k == "OnElement":
                col4 = v
            elif k == "X":
                col5 = v
            elif k == "Y":
                col6 = v

        cols = zip(col1, col2, col3, col4, col5, col6)

        recloserID = []
        for attrs in cols:
            row = ""
            for attr in attrs:
                row += f"{attr}&"
            recloserID.append(row.strip("&"))

        return recloserID

    def concat_publicLightscols(self) -> list[str]:
        """Concatenate public lights columns.

        Resulting shape of a single row:
        ['Node1'&'Name'&'Phase'&... &'attr1M',
        'Node1'&'Name'&'Phase'&... &'attr2M', ...
        ...,
        'Node1N'&'NameN'&'PhaseN'&... &'attrNM'].

        """
        publicLightsData = self._publicLights
        for k, v in publicLightsData.items():
            if k == "Node1":
                col1 = v
            elif k == "Name":
                col2 = v
            elif k == "Phase":
                col3 = v
            elif k == "Switch1":
                col4 = v
            elif k == "Potencia_kW":
                col5 = v
            elif k == "LfType":
                col6 = v
            elif k == "Unit":
                col7 = v
            elif k == "CosPhi":
                col8 = v
            elif k == "CoordX1":
                col9 = v
            elif k == "CoordY1":
                col10 = v
            elif k == "Un":
                col11 = v

        cols = zip(col1, col2, col3, col4,
                   col5, col6, col7, col8,
                   col9, col10, col11)
        publicLightsID = []
        for attrs in cols:
            row = ""
            for attr in attrs:
                row += f"{attr}&"
            publicLightsID.append(row.strip("&"))

        return publicLightsID

    def loc_buscoord(self, busname: str) -> tuple[float]:
        """Localize bus coordinates.

        Given the bus name ID it looks for its
        X, Y coordinates and return them
        as floats in a tuple.

        """
        busesData = self._buses
        indx = busesData["Name"].index(busname)
        X = float(busesData["CoordX1"][indx])
        Y = float(busesData["CoordY1"][indx])

        return (X, Y)


class Lines():
    def __init__(self) -> None:
        """Line object.

        Kind of lines:
        - Líneas de MT subterráneas: "underG_MVline"
        - Líneas de MT aéreas: "overH_MVline"
        - Líneas de BT subterráneas: "underG_LVline"
        - Líneas de BT aéreas: "overH_LVline"
        - Conductores de acometidas: "service_LVline"

        New values:
            NEUT(PHASE/INSUL)MAT:
                - AL: Aluminum
                - SCU: Solid Copper
                - BCU: Bundle Copper
                - None: No data
            NEUT(PHASE)SIZ:
                - None: No data
            INSULVOLT:
                *String* datatype, usually for underground conductors
                in case of Over Head LV line is converted to (kV) as follow:
                - 0.6: 600 V
                - 1.0: 1000 V
                - 2.0: 2000 V
                - None: No data
            INSULMAT:
                - RHH: RHH/RHW-2/USE-2
                In case of Over Head MV/LV:
                - BARE: No insulated
                - COVER: Half-insulated
                - INSUL: Insulated
            LINEGEO:
                *String* datatype. For overhead MV lines if
                it starts with "Y" or "N" (meaning with LV Cable beneath
                the MV conductor or not) then will be followed by
                a geometry SIRDE code and finally information about the
                Guard Conductor (material & size). Such attribute has will
                have the next format:

                    <LVC>_<SIRDEcodeID>_<GUARDMAT>_<GUARDSIZ>

                - Y_2.1B_None_None: Flag style three-phase with neutral
                                    conductor ("2.1B") with LV
                                    cable beneath ("Y") but
                                    no information about
                                    guard conductor at all.
                - Y_2.1_AAAC_123.3: Horizontal three-phase with
                                    neutral conductor ("2.1")
                                    with LV cable beneath ("Y") and
                                    guard conductor whose material
                                    is: "AAAC" and size "123.3".
                - N_3_None_1/0: Horizontal with no neutral three-phase ("3")
                                with No LV cable beneath ("N")
                                whose guard conductor's size is 1/0 but the is
                                not information about its material.
                In case of underground MV kind of line, only the SIRDEcodeID
                will be taken in this attribute.
            TYPE:
                For Over Head LV
                - LVC: Low Voltage Cable (Three Wire cable)
                - CC: Concentric Cable
                - SLC: Street Lighting Cable
                Other
                - PLC: Public Lighting Conductor
                - SPH: Single-Phase
                - BPH: Split-Phase
                - TPH: Three-Phase

            LibraryName:
                Mandatory new string type attribute for ICE circuits with
                the following notation:

                    <LC(LG)>::<LibraryType>

                Where "LC" stands for "LineCode" and "LG" to
                "LineGeometry" depending on the electric model
                of the line defined in the `*.dss` library.

        1. Note: Optional attributes: "geometry" is not explicitly
                 mencioned in the manual of "QGIS2OPENDSS" plug-in.
                 It is the spatial points the line pass through.
                 "ICEobjectID" works as an extra unique label
                 for all circuit objects.
        2. Note: "Conductor" for HV/MV line & "Cable" for LV line.
        3. Note: *RHH* is also used for TYPE of underground LV lines.
        4. Note: *BARE* is now also used for INSULMAT not only for
                 TYPE attribute in second network anymore.
        5. Note: "None" = {
                    "NE": "No Existe",
                    "NT": "No tiene",
                    "UNK": "Desconocido",
                    "NA": "No aplica"
                }
        """
        # "*" symbol stands for mandator attribute
        self._ICEobjID = []   # New (*)
        self._LibName = []    # New (*)
        self._NEUTMAT = []       # *
        self._NEUTSIZ = []       # *
        self._PHASEMAT = []      # *
        self._PHASESIZ = []      # *
        self._INSULVOLT = []     # * (UG MVline)
        self._PHASEDESIG = []    # * (UG & OH MVline)
        self._INSULMAT = []      # * (UG's)
        self._NOMVOLT = []       # *
        self._SHIELDING = []     # * (UG MVline)
        self._INSULEV = []
        self._NEUTPER = []
        self._LINEGEO = []       # * (OH MVline)
        self._TYPE = []          # * (OH & serv LVline)
        self._LENGTH = []
        self._LENUNIT = []
        self._X1 = []
        self._Y1 = []
        self._X2 = []
        self._Y2 = []


class UG_MVlines(Lines):
    def __init__(self):
        super().__init__()
        self._line_layer = "underG_MVlines"


class OH_MVlines(Lines):
    def __init__(self):
        super().__init__()
        self._line_layer = "overH_MVlines"


class UG_LVlines(Lines):
    def __init__(self):
        super().__init__()
        self._line_layer = "underG_LVlines"


class OH_LVlines(Lines):
    def __init__(self):
        super().__init__()
        self._line_layer = "overH_LVlines"

    def split_overHLVlines(self, service_LV: Lines) -> Lines:
        """Define services LV lines layers.

        It gets services LV lines layer with empty
        attributes and returns it with its features
        by splitting overhead LV lines in general with
        those ones whose type is "DPX", "TPX" and "QPX"
        and which will be taken as *service* overhead
        LV lines layer. See method
        :py:meth:`CKTqgis.set_attributes_lines`
        for more details.

        """
        oh_lvlayer = self.__dict__
        serviceLayer_data = {}
        servicetype = {"DPX", "TPX", "QPX"}
        serv_i = []

        for i, t in enumerate(oh_lvlayer["_TYPE"]):
            if t in servicetype:
                serv_i.append(i)

        for attr, ft in oh_lvlayer.items():
            if (type(ft) is list) and (len(ft) != 0):
                serv_fts = []
                for i in serv_i:
                    serv_fts.append(ft[i])
                serviceLayer_data[attr] = serv_fts

        # Remove services lines from OH_LVlines layer
        # Sort in reverse to avoid index shifting
        serv_i.sort(reverse=True)
        for attr, ft in oh_lvlayer.items():
            if (type(ft) is list) and (len(ft) != 0):
                for i in serv_i:
                    oh_lvlayer[attr].pop(i)

        # Update attributes for LV secondary lines
        for attr, fts in oh_lvlayer.items():
            setattr(self, attr, fts)
        # Set new attributes for services lines
        for k, v in serviceLayer_data.items():
            setattr(service_LV, k, v)

        return service_LV


class serv_LVlines(Lines):
    def __init__(self):
        super().__init__()
        self._line_layer = "service_LVlines"


class Buses():
    """Bus object.

    Kind of buses:
    - Barras de MT subterráneas: "underG_MVbus"
    - Barras de MT aéreas: "overH_MVbus"
    - Barras de BT subterráneas: "underG_LVbus"
    - Barras de BT aéreas: "overH_LVbus"

    Buses do not have obligatory attributes and only need to
    identify themselves with their ID, nominal voltage and
    geometry (X1,Y1).

    """
    def __init__(self) -> None:
        self._ICEobjID = []
        self._NOMVOLT = []
        self._X1 = []
        self._Y1 = []


class OH_MVbuses(Buses):
    def __init__(self):
        super().__init__()
        self._bus_layer = "overH_MVbuses"


class OH_LVbuses(Buses):
    def __init__(self):
        super().__init__()
        self._bus_layer = "overH_LVbuses"


class UG_MVbuses(Buses):
    def __init__(self):
        super().__init__()
        self._bus_layer = "underG_MVbuses"


class UG_LVbuses(Buses):
    def __init__(self):
        super().__init__()
        self._bus_layer = "underG_LVbuses"


class Transformers():
    """Transformer object.

    Kind of tranformers:

    - Transformadores:
        "Distribution_transformers"

    - Subestación unidad trifásica:
        "Subestation_three_phase_transformer"

    - Subestación autotransformador:
        "Subestation_autotransformer"

    - Subestación sin modelar:
        "Subestation_without_modeling_transformer"

    New values:
        SECCONN:
            - OD: Open Delta
            - 4D: Delta four wires

    1. Note: In case of (AB, BC, AC)
             then PRIMCONN = "OY" and SECCONN = "OD".

    2. Note: In case of (A, B, C)
             then PRIMCONN = "LG" and SECCONN = "SP".

    """
    def __init__(self) -> None:
        self._ICEobjID = []
        self._NODE1 = []
        self._NODE2 = []
        self._SWITCH1 = []
        self._SWITCH2 = []
        self._ISREG = []       # _ISREGULATED
        self._PHASEDESIG = []
        self._PRIMVOLT = []
        self._SECVOLT = []
        self._PRIMCONN = []
        self._SECCONN = []
        self._KVAPHASEA = []
        self._KVAPHASEB = []
        self._KVAPHASEC = []
        self._RATEDKVA = []
        self._TAPSETTING = []
        self._TAPS = []
        self._MV_MV = []      # Label must be MV/MV
        self._HIGHVOLT = []
        self._MEDVOLT = []
        self._LOWVOLT = []
        self._XHL = []
        self._XHT = []
        self._XLT = []
        self._HIGHCONN = []
        self._MEDCONN = []
        self._LOWCONN = []
        self._KVAHIGH = []
        self._KVAMED = []
        self._KVALOW = []
        self._WINDINGS = []
        self._TAPMAX_MI = []    # Label must be TAPMAX/MI
        self._ISC_3P = []
        self._ISC_1P = []
        self._TTYPE = []
        self._X1 = []
        self._Y1 = []


class Distribution_Txs(Transformers):
    def __init__(self):
        super().__init__()
        self._Tx_layer = "Distribution_transformers"


class Subestation_three_phase_unit_Tx(Transformers):
    def __init__(self):
        super().__init__()
        self._Tx_layer = "Subestation_three_phase_transformer"


class Subestation_auto_Tx(Transformers):
    def __init__(self):
        super().__init__()
        self._Tx_layer = "Subestation_autotransformer"


class Subestation_without_modeling_Tx(Transformers):
    def __init__(self):
        super().__init__()
        self._Tx_layer = "Subestation_without_modeling_transformer"


class Loads():
    """Load object.

    Kind of loads:

    - Cargas de media tensión: "MV_load"

    - Cargas de baja tensión: "LV_load"

    The bool type attribute _ODDLOAD is `True` only
    for those loads right over a transformer; at
    the same time, such loads will be drag 10cm
    in X1 then 10cm in Y1 away from the transformer.
    Hence generate auxiliary lines
    between them is recommended.

    Note: See :py:meth:`CKTqgis.add_AuxServLine`
          for more details.

    """
    def __init__(self):
        self._ICEobjID = []
        self._NODE1 = []
        self._SWITCH1 = []
        self._PHASEDESIG = []
        self._NOMVOLT = []
        self._KWHMONTH = []
        self._PF = []
        self._MODEL = []
        self._CONN = []
        self._CLASS = []
        self._SERVICE = []
        self._AMI = []
        self._ID = []
        self._X1 = []
        self._Y1 = []
        self._ODDLOAD = False


class LV_Loads(Loads):
    def __init__(self):
        super().__init__()
        self._load_layer = "LV_load"


class MV_Loads(Loads):
    def __init__(self):
        super().__init__()
        self._load_layer = "MV_load"


class Fuse():
    """Fuse object.

    Kind of fuses:

    - Fusibles: "Fuses".

    """
    def __init__(self):
        self._fuse_layer = "Fuses"
        self._ICEobjID = []
        self._PHASEDESIG = []
        self._ONELEMENT = []
        self._NC = []
        self._CURVE = []
        self._RATED_C = []
        self._X1 = []
        self._Y1 = []


class LSDG():
    """Large scale distributed generation

    The main differences between large scale and small scale
    are the active and reactive power curves and installed power.

    +-------------+-------------+
    | Small scale | Large scale |
    +-------------+-------------+
    |     KVA     |     MVA     |       
    |    CURVE1   |    DAILY    |
    |    CURVE2   |      -      |
    +-------------+-------------+

    """
    def __init__(self):
        self._ICEobjID = []
        self._NODE1 = []
        self._SWITCH1 = []
        self._TECH = []
        self._MVA = []  # LSGD
        self._XDP = []
        self._XDPP = []
        self._DAILY = []  # LSGD
        self._X1 = []
        self._Y1 = []


class LSDG_PV(LSDG):
    def __init__(self):
        super.__init__()
        self._LSDG_GD_layer = "LSDG_PVs"


class LSDG_HYDRO(LSDG):
    def __init__(self):
        super().__init__()
        self._LSDG_GD_layer = "LSDG_HYDROs"


class LSDG_WIND(LSDG):
    def __init__(self):
        super().__init__()
        self._LSDG_GD_layer = "LSDG_WINDs"


class LSDG_GD(LSDG):
    def __init__(self):
        super().__init__()
        self._LSDG_GD_layer = "LSDG_GDs"


class SSDG():
    """Small scale distributed generation.

    The main differences between large scale and small scale
    are the active and reactive power curves and installed power.

    +-------------+-------------+
    | Small scale | Large scale |
    +-------------+-------------+
    |     KVA     |     MVA     |       
    |    CURVE1   |    DAILY    |
    |    CURVE2   |      -      |
    +-------------+-------------+

    """
    def __init__(self):
        self._ICEobjID = []
        self._NODE1 = []
        self._SWITCH1 = []
        self._TECH = []
        self._KVA = []
        self._XDP = []
        self._XDPP = []
        self._CURVE1 = []
        self._CURVE2 = []
        self._X1 = []
        self._Y1 = []


class SSDG_PV(SSDG):
    def __init__(self):
        super().__init__()
        self._SSDG_GD_layer = "SSDG_PVs"


class SSDG_HYDRO(SSDG):
    def __init__(self):
        super().__init__()
        self._SSDG_GD_layer = "SSDG_HYDROs"


class SSDG_WIND(SSDG):
    def __init__(self):
        super().__init__()
        self._SSDG_GD_layer = "SSDG_WINDs"


class SSDG_GD(SSDG):
    def __init__(self):
        super().__init__()
        self._SSDG_GD_layer = "SSDG_GDs"


class Reclosers():
    """Recloser object.

    Kind of reclosers:

    - Reconectadores: "Reclosers".

    """
    def __init__(self):
        self._recloser_layer = "Reclosers"
        self._ICEobjID = []
        self._PHASEDESIG = []
        self._NC = []
        self._GRD_D = []
        self._PH_D = []
        self._GRD_F = []
        self._PH_F = []
        self._GRD_I = []
        self._PH_I = []
        self._GRD_TRIP = []
        self._PH_TRIP = []
        self._X1 = []
        self._Y1 = []


class Regulators():
    """Regulator object.

    Kind of regulators:

    - Reguladores: "Regulators".

    """
    def __init__(self):
        self._regulator_layer = "Regulators"
        self._ICEobjID = []
        self._NOMVOLT = []
        self._PHASEDESIG = []
        self._KVA = []
        self._VREG = []
        self._PT_RATIO = []
        self._BANDWIDTH = []
        self._TAPS = []
        self._VCAP = []
        self._X1 = []
        self._Y1 = []


class PublicLights():
    """Public lights object.

    Kind of public lights:

    - Alumbrado Público: "Public_Lights".

    """
    def __init__(self):
        self._PublicLights_layer = "Public_Lights"
        self._ICEobjID = []
        self._SERVICE = []
        self._KW = []
        self._NOMVOLT = []
        self._ID = []
        self._MODEL = []
        self._X1 = []
        self._Y1 = []


class CKTqgis():
    """Result ciruict.

    Circuit layers with all data attributes ready to be converted
    to a shape file *.shp suitable for QGIS.
    Circuit in jSon style:
    lines = {
        "underG_MVline": {
            "NEUTMAT": [val0, val1, val3, ..., valN],
            "NEUTSIZ": [val0, val1, val3, ..., valN],
            "PHASEMAT": [val0, val1, val3, ..., valN],

            ...,

            "Y2": [val0, val1, val3, ..., valN]
        }
        "overH_MVline": {
            "NEUTMAT": [val0, val1, val3, ..., valN],
            "NEUTSIZ": [val0, val1, val3, ..., valN],
            "PHASEMAT": [val0, val1, val3, ..., valN],

            ...,

            "Y2": [val0, val1, val3, ..., valN]
        }
        "underG_LVline": {
            "NEUTMAT": [val0, val1, val3, ..., valN],
            "NEUTSIZ": [val0, val1, val3, ..., valN],
            "PHASEMAT": [val0, val1, val3, ..., valN],

            ...,

            "Y2": [val0, val1, val3, ..., valN]
        }
        "overH_LVline": {
            "NEUTMAT": [val0, val1, val3, ..., valN],
            "NEUTSIZ": [val0, val1, val3, ..., valN],
            "PHASEMAT": [val0, val1, val3, ..., valN],

            ...,

            "Y2": [val0, val1, val3, ..., valN]
        }
        "service_LVline": {
            "NEUTMAT": [val0, val1, val3, ..., valN],
            "NEUTSIZ": [val0, val1, val3, ..., valN],
            "PHASEMAT": [val0, val1, val3, ..., valN],

            ...,

            "Y2": [val0, val1, val3, ..., valN]
        }
    }

    """
    def __init__(self):
        self._buses = {}
        self._lines = {}
        self._transformers = {}
        self._MVloads = {}
        self._LVloads = {}
        self._publicLights = {}
        self._disconnectors = {}
        self._fuses = {}
        self._reclosers = {}
        self._largeScale_DG = {}
        self._smallScale_DG = {}
        self._regulators = {}
        self._capacitors = {}
        self._EVs = {}
        self._EbusesC = {}

    def add_linelayers(self, cktNeplan: CKTdata) -> tuple[Lines]:
        """Creats line layers.

        It gets lines data, creat the objects and sets its
        attributes.

        """
        # lineID
        linesID = cktNeplan.concat_linecols()

        # Creat instances
        underG_LVline = UG_LVlines()
        underG_MVline = UG_MVlines()
        overH_LVline = OH_LVlines()
        overH_MVline = OH_MVlines()
        service_LVline = serv_LVlines()
        # Unpack libraryType
        line_layers = self.set_attributes_lines(
            underG_LVline,
            underG_MVline,
            service_LVline,
            overH_LVline,
            overH_MVline,
            cktNeplan,
            linesID)

        # Update attribute
        for LL in line_layers:
            L = LL._line_layer
            dictAttrs = LL.__dict__
            self._lines[L] = {col.strip("_"): vals for (col, vals)
                              in dictAttrs.items()}

        return (underG_LVline, underG_MVline,
                overH_LVline, overH_MVline, service_LVline)

    def add_AuxServLine(self,
                        service_LV: serv_LVlines) -> serv_LVlines:
        """Creat auxiliary lines.

        It connects new fiction service overhead LV
        line from a transformer to the "odd" load
        right over it with these typical
        mandatory features:
        typic_ft = {
            "_ICEobjID": [TxObjID__0],
            "_LibName": [
                "LC::BT_1/0 AAAC_AAAC_2_3_aux",
                "LC::BT_2 ACSR_ACSR_2_4_aux"
                ],
            "_NEUTMAT": ["AAAC", "ACSR"],
            "_NEUTSIZ": ["2", "2"],
            "_PHASEMAT": ["AAAC", "ACSR"],
            "_PHASESIZ": ["1/0", "2"],
            "_NOMVOLT": [, ],
            "_TYPE": ["TPX", "QPX"],
            "_X1": [],
            "_Y1": [],
            "_X2": [],
            "_Y2": [],
            "_LENGTH: []"
        }
        Blank lists will be taken with regard to
        transformer and odd-load objects.

        Note: While unit of _LENGTH is km unit of X1, Y1
        X2 and Y2 is meter and it must be i bit bigger than
        the tolerance in DN-Corrector plug-in.

        """
        loadsdata = self._LVloads["LV_load"]
        txsdata = self._transformers["Distribution_transformers"]
        # Retrieve oddloads ID
        oddloadsID = [oddL.strip("_T") for oddL
                      in loadsdata["ICEobjID"] if "_T" in oddL]
        # Typical features
        for oddLID in oddloadsID:
            i = txsdata["ICEobjID"].index(oddLID)
            j = loadsdata["ICEobjID"].index(f"{oddLID}_T")
            x1 = txsdata["X1"][i]
            y1 = txsdata["Y1"][i]
            x2 = loadsdata["X1"][j]
            y2 = loadsdata["Y1"][j]
            # _LENGTH to km
            aux_len = np.sqrt((x2-x1)**2 + (y2-y1)**2) * 1e-3
            # _NOMVOLT
            nom_volt = loadsdata["NOMVOLT"][j]
            # Add feature
            service_LV._ICEobjID.append(f"{oddLID}__0")
            service_LV._X1.append(x1)
            service_LV._Y1.append(y1)
            service_LV._X2.append(x2)
            service_LV._Y2.append(y2)
            service_LV._LENGTH.append(aux_len)
            service_LV._NOMVOLT.append(nom_volt)
            # QPX type
            if (loadsdata["SERVICE"][j] in {123, "ABC", "RST"}):
                service_LV._LibName.append("LC::BT_2 ACSR_ACSR_2_4_aux")
                service_LV._NEUTMAT.append("ACSR")
                service_LV._NEUTSIZ.append("2")
                service_LV._PHASEMAT.append("ACSR")
                service_LV._PHASESIZ.append("2")
                service_LV._TYPE.append("QPX")
            # TPX type
            else:
                service_LV._LibName.append("LC::BT_1/0 AAAC_AAAC_2_3_aux")
                service_LV._NEUTMAT.append("AAAC")
                service_LV._NEUTSIZ.append("2")
                service_LV._PHASEMAT.append("AAAC")
                service_LV._PHASESIZ.append("1/0")
                service_LV._TYPE.append("TPX")

        return service_LV

    def add_buslayers(self, cktNeplan: CKTdata) -> tuple[Buses]:
        """Create bus layers.

        It gets buses data, create the objects and sets its
        attributes.

        """
        # BusID
        busID = cktNeplan.concat_buscols()
        # Create instances
        underG_LVbus = UG_LVbuses()
        underG_MVbus = UG_MVbuses()
        overH_LVbus = OH_LVbuses()
        overH_MVbus = OH_MVbuses()

        # Unpack
        bus_layers = self.set_attributes_buses(
            underG_LVbus=underG_LVbus,
            underG_MVbus=underG_MVbus,
            overH_LVbus=overH_LVbus,
            overH_MVbus=overH_MVbus,
            busID=busID)

        # Update attribute
        for BL in bus_layers:
            B = BL._bus_layer
            dictAttrs = BL.__dict__
            self._buses[B] = {col.strip("_"): vals for (col, vals)
                              in dictAttrs.items()}

        return (underG_LVbus, underG_MVbus,
                overH_LVbus, overH_MVbus)

    def add_txlayers(self, cktNeplan: CKTdata) -> tuple[Transformers]:
        """Create transformer layers.

        It gets transformer data, create the objects and sets its
        attributes.

        To store the layers of transformers was necessary change
        the name of the attributes MV_MV and TAPMAX_MI to
        MV/MV and TAPMAX/MI according to the manual.

        Make a single sheet of transformers weather asym or not
        by adding Trafo2Winding at tail tacking advantage
        both sheets have same columns in CKTdata object.

        """
        AsymTxData = cktNeplan._AsymTx
        TxData = cktNeplan._Tx
        # Number of Trafo2WindingAsym in CKTdata obj
        N_asymTXs = len(list(AsymTxData.values())[0])
        # Stack
        for k, v in TxData.items():
            AsymTxData[k] += v

        # TransformerID
        txID = cktNeplan.concat_Txcols()
        # Create instances
        Distribution_transformers = Distribution_Txs()
        Sub_three_phase_unit_Tx = Subestation_three_phase_unit_Tx()
        Sub_autoTx = Subestation_auto_Tx()
        Sub_without_modeling_Tx = Subestation_without_modeling_Tx()

        transformer_layers = self.set_attributes_tx(
            Distribution_transformers=Distribution_transformers,
            Sub_three_phase_unit_Tx=Sub_three_phase_unit_Tx,
            Sub_autoTx=Sub_autoTx,
            Sub_without_modeling_Tx=Sub_without_modeling_Tx,
            txID=txID,
            n_asymTxs=N_asymTXs
        )

        for TL in transformer_layers:
            T = TL._Tx_layer
            dictAttrs = TL.__dict__

            # Dictionay of modified attributes
            dictAttrsTx = {}
            for (col, vals) in dictAttrs.items():
                col = col.strip("_")
                if "MV_MV" in col:
                    col = col.replace("_", "/")
                    dictAttrsTx[col] = vals
                elif "TAPMAX_MI" in col:
                    col = col.replace("_", "/")
                    dictAttrsTx[col] = vals
                else:
                    dictAttrsTx[col] = vals

            self._transformers[T] = dictAttrsTx

        return (Distribution_transformers,
                Sub_three_phase_unit_Tx,
                Sub_autoTx,
                Sub_without_modeling_Tx)

    def add_load_layers(self, cktNeplan: CKTdata) -> tuple[Loads]:
        """Missing documentation.

        Here goes the missing description of this method.

        """
        # Rows
        loadID = cktNeplan.concat_loadcols()
        # Create instances
        LVload = LV_Loads()
        MVload = MV_Loads()

        load_layers = self.set_attributes_loads(
            LVload=LVload,
            MVload=MVload,
            loadID=loadID)

        for LL in load_layers:
            L = LL._load_layer
            if L == "LV_load":
                dictAttrs = LL.__dict__
                self._LVloads[L] = {col.strip("_"): vals for (col, vals)
                                    in dictAttrs.items()}
            else:
                dictAttrs = LL.__dict__
                self._MVloads[L] = {col.strip("_"): vals for (col, vals)
                                    in dictAttrs.items()}

        return (LVload, MVload)

    def add_fuse_layer(self, cktNeplan: CKTdata) -> Fuse:
        """Missing documentation.

        Here goes the missing description of this method.

        """
        # Concat columns
        fuseID = cktNeplan.concat_fusecols()
        # Create instance
        fuse = Fuse()

        fuse_layer = self.set_attributes_fuse(fuse=fuse,
                                              fuseID=fuseID)
        F = fuse_layer._fuse_layer
        dictAttrs = fuse_layer.__dict__
        self._fuses[F] = {col.strip("_"): vals
                          for (col, vals) in dictAttrs.items()}

        return (fuse)

    def add_SSDG_PV_layer(self, cktNeplan: CKTdata) -> SSDG_PV:
        """Missing documentation.

        Here goes the missing description of this method.

        """
        # Concat columns
        pvID = cktNeplan.concat_PVcols()
        # Create instance
        pv = SSDG_PV()
        pv_layer = self.set_attributes_PV(
            ssdg_pv=pv,
            cktNeplan=cktNeplan,
            pvID=pvID)

        PVL = pv_layer._SSDG_GD_layer
        dictAttrs = pv_layer.__dict__
        self._smallScale_DG[PVL] = {col.strip("_"): vals
                                    for (col, vals) in dictAttrs.items()}

        return pv

    def add_recloser_layer(self, cktNeplan: CKTdata) -> Reclosers:
        """Missing documentation.

        Here goes the missing description of this method.

        """
        # Concat recloserData rows
        recloserID = cktNeplan.concat_reclosercols()
        # Create instance
        recloser = Reclosers()
        recloser_layer = self.set_attributes_recloser(recloser=recloser,
                                                      recloserID=recloserID)

        R = recloser_layer._recloser_layer
        dictAttrs = recloser_layer.__dict__
        self._reclosers[R] = {cols.lstrip("_"): vals
                              for (cols, vals) in dictAttrs.items()}

        return recloser

    def add_regulator_layer(self, cktNeplan: CKTdata) -> Regulators:
        """Layer of regularos.

        It creats regulators layers attributes suitable to
        be converted to shapefiles.

        """
        # Concat columns
        regulatorID = cktNeplan.concat_regulatorcols()
        # Create instance
        regulator = Regulators()
        regulator_layer = self.set_attributes_regulator(
            regulatorID=regulatorID,
            regulator=regulator)

        R = regulator_layer._regulator_layer
        dictAttrs = regulator_layer.__dict__
        self._regulators[R] = {cols.lstrip("_"): vals
                               for (cols, vals) in dictAttrs.items()}

        return regulator

    def add_PublicLights_layer(self, cktNeplan: CKTdata) -> PublicLights:
        """Missing documentation.

        Missing description of this method.

        """

        # Concatenate columns
        publicLightsID = cktNeplan.concat_publicLightscols()

        # Create instance
        public_lights = PublicLights()

        public_lights_layer = self.set_attributes_publicLights(
            public_lights=public_lights,
            publicLightsID=publicLightsID)

        PL = public_lights_layer._PublicLights_layer
        dictAttrs = public_lights_layer.__dict__
        self._publicLights[PL] = {cols.strip("_"): vals
                                  for cols, vals in dictAttrs.items()}

        return public_lights

    def set_attributes_lines(self,
                             underG_LVline: Lines,
                             underG_MVline: Lines,
                             service_LVline: Lines,
                             overH_LVline: Lines,
                             overH_MVline: Lines,
                             cktNeplan: CKTdata,
                             linesID: list[str]) -> tuple[Lines]:
        """Unpack the data of line layers.

        It gets some SIRDE code "subtipos" and gives them all
        another Manual format name depending on the zone
        voltage level. Finally it separates overhead LV lines from
        service lines.
        Note: For Underground MV line next attributes are taking
        as typical values:
        _SHIELDING: "CN"
        _NEUTMAT: "CU"
        _NEUTSIZ: "1/0"
        _INSULEV: String type. "100" For a insulated level of 100%.
                  This is a default value of for systems
                  with grounded neutral.
        Note: For Underground LV line next attributes are taking
        as typical values:
        _NEUTMAT: "CU".

        """
        # _TYPE
        oh_lvline = {
            "1": "LVC",
            "2": "DPX",
            "3": "TPX",
            "4": "QPX",
            "5": "CC",
            "6": "SLC"
        }

        for row in linesID:
            # ["Node1", "Node2", "Name", "LibraryType", "Length", "Un"]
            cols = row.split("&")
            # LibraryType -> LibraryName
            lineName = cols[3].replace(" ", "").strip()
            originalLib = cols[3]
            # Replace label
            Ltype = set_Label(originalLib)
            line = Ltype.split()
            # Underground
            if "SUB" in line[0]:
                # LV
                if "BT" in line[0]:
                    for n, ft in enumerate(line):
                        # _PHASEDESIG
                        if n == 0:
                            attrs = ft.split("_")
                            ph = attrs[2][:-1]
                            phcode = get_PHASEDESIG(ph)
                            underG_LVline._PHASEDESIG.append(phcode)
                        # _PHASESIZ
                        elif n == 1:
                            attr = ft.strip("_")
                            underG_LVline._PHASESIZ.append(attr)
                        # _PHASEMAT
                        elif n == 2:
                            attr = ft.strip()
                            underG_LVline._PHASEMAT.append(attr)
                        # [_INSULMAT, _NEUTSIZ]
                        elif n == 3:
                            attrs = ft.split("_")
                            underG_LVline._INSULMAT.append(attrs[0])
                            underG_LVline._NEUTSIZ.append(attrs[1])
                    # _LibName: LineCode (LC)
                    underG_LVline._LibName.append(f"LC::{lineName}")
                    # _NEUTMAT: *Typical Value*
                    underG_LVline._NEUTMAT.append("CU")
                    # _NOMVOLT
                    nomV = float(cols[5].strip())
                    codenomV = get_NOMVOLT(nomV)
                    underG_LVline._NOMVOLT.append(codenomV)
                    # _X1, _Y1, _X2, _Y2
                    from_bus = cols[0]
                    to_bus = cols[1]
                    (X1, Y1) = cktNeplan.loc_buscoord(from_bus)
                    (X2, Y2) = cktNeplan.loc_buscoord(to_bus)
                    underG_LVline._X1.append(X1)
                    underG_LVline._Y1.append(Y1)
                    underG_LVline._X2.append(X2)
                    underG_LVline._Y2.append(Y2)
                    # _ICEobjID
                    nameID = cols[2]
                    underG_LVline._ICEobjID.append(nameID)
                    # _LENGTH
                    length = float(cols[4].strip())
                    underG_LVline._LENGTH.append(length)

                # MV
                else:
                    for n, ft in enumerate(line):
                        # _PHASEDESIG
                        if n == 0:
                            attrs = ft.split("_")
                            ph = attrs[2][:-1]
                            phcode = get_PHASEDESIG(ph)
                            underG_MVline._PHASEDESIG.append(phcode)
                        # _PHASESIZ
                        elif n == 1:
                            attr = ft.strip("_")
                            underG_MVline._PHASESIZ.append(attr)
                        # _PHASEMAT
                        elif n == 2:
                            attr = ft.strip()
                            underG_MVline._PHASEMAT.append(attr)
                        # [_INSULMAT, _NEUTPER, _LINEGEO, _INSULVOLT]
                        elif n == 3:
                            attrs = ft.split("_")
                            underG_MVline._INSULMAT.append(attrs[0])
                            underG_MVline._NEUTPER.append(attrs[1])
                            underG_MVline._LINEGEO.append(attrs[2])
                    # _LibName: LineCode (LC)
                    underG_MVline._LibName.append(f"LC::{lineName}")
                    # _NEUTMAT: *Typical Value*
                    underG_MVline._NEUTMAT.append("CU")
                    # _NEUTSIZ: *Typical Value*
                    underG_MVline._NEUTSIZ.append("1/0")
                    # _SHIELDING: *Typical Value*
                    underG_MVline._SHIELDING.append("CN")
                    # _NOMVOLT
                    nomV = float(cols[5].strip())
                    codenomV = get_NOMVOLT(nomV)
                    underG_MVline._NOMVOLT.append(codenomV)
                    # _INSULVOLT
                    insulV = get_INSULVOLT(nomV)
                    underG_MVline._INSULVOLT.append(insulV)
                    # _X1, _Y1, _X2, _Y2
                    from_bus = cols[0]
                    to_bus = cols[1]
                    (X1, Y1) = cktNeplan.loc_buscoord(from_bus)
                    (X2, Y2) = cktNeplan.loc_buscoord(to_bus)
                    underG_MVline._X1.append(X1)
                    underG_MVline._Y1.append(Y1)
                    underG_MVline._X2.append(X2)
                    underG_MVline._Y2.append(Y2)
                    # _ICEobjID
                    nameID = cols[2]
                    underG_MVline._ICEobjID.append(nameID)
                    # _LENGTH
                    length = float(cols[4].strip())
                    underG_MVline._LENGTH.append(length)

            # Overhead
            else:
                # LV
                if "BT" in line[0]:
                    for n, ft in enumerate(line):
                        # _PHASESIZ[1]
                        if n == 0:
                            attrs = ft.split("_")
                            overH_LVline._PHASESIZ.append(attrs[1])
                        # [_PHASEMAT, _NEUTMAT, _NEUTSIZ, _TYPE]
                        elif n == 1:
                            attrs = ft.split("_")
                            # Set _TYPE
                            for (k, v) in oh_lvline.items():
                                attrs[-1] = attrs[-1].replace(k, v)
                            # Update attributes
                            overH_LVline._PHASEMAT.append(attrs[0])
                            overH_LVline._NEUTMAT.append(attrs[1])
                            overH_LVline._NEUTSIZ.append(attrs[2])
                            overH_LVline._TYPE.append(attrs[3])
                    # _LibName: LineCode (LC)
                    overH_LVline._LibName.append(f"LC::{lineName}")
                    # _NOMVOLT
                    nomV = float(cols[5].strip())
                    codenomV = get_NOMVOLT(nomV)
                    overH_LVline._NOMVOLT.append(codenomV)
                    # _X1, _Y1, _X2, _Y2
                    from_bus = cols[0]
                    to_bus = cols[1]
                    (X1, Y1) = cktNeplan.loc_buscoord(from_bus)
                    (X2, Y2) = cktNeplan.loc_buscoord(to_bus)
                    overH_LVline._X1.append(X1)
                    overH_LVline._Y1.append(Y1)
                    overH_LVline._X2.append(X2)
                    overH_LVline._Y2.append(Y2)
                    # _ICEobjID
                    nameID = cols[2]
                    overH_LVline._ICEobjID.append(nameID)
                    # _LENGTH
                    length = float(cols[4].strip())
                    overH_LVline._LENGTH.append(length)
                # MV
                else:
                    for n, ft in enumerate(line):
                        # _PHASEDESIG
                        if n == 0:
                            attrs = ft.split("_")
                            ph = attrs[1][:-1]
                            phcode = get_PHASEDESIG(ph)
                            overH_MVline._PHASEDESIG.append(phcode)
                        # _PHASESIZ
                        elif n == 1:
                            attr = ft.strip()
                            overH_MVline._PHASESIZ.append(attr)
                        # [_PHASEMAT, _NEUTMAT, _NEUTSIZ,
                        # GUARDMAT, GUARDSIZ, SIRDEcodeID, LVC]
                        elif n == 2:
                            attrs = ft.split("_")
                            overH_MVline._PHASEMAT.append(attrs[0])
                            overH_MVline._NEUTMAT.append(attrs[1])
                            overH_MVline._NEUTSIZ.append(attrs[2])
                            # _LINEGEO
                            geo_format = f"{attrs[6]}_{attrs[5]}" \
                                         f"_{attrs[4]}_{attrs[3]}"
                            overH_MVline._LINEGEO.append(geo_format)
                    # _LibName: LineCode (LC)
                    overH_MVline._LibName.append(f"LC::{lineName}")
                    # _NOMVOLT
                    nomV = float(cols[5].strip())
                    codenomV = get_NOMVOLT(nomV)
                    overH_MVline._NOMVOLT.append(codenomV)
                    # _X1, _Y1, _X2, _Y2
                    from_bus = cols[0]
                    to_bus = cols[1]
                    (X1, Y1) = cktNeplan.loc_buscoord(from_bus)
                    (X2, Y2) = cktNeplan.loc_buscoord(to_bus)
                    overH_MVline._X1.append(X1)
                    overH_MVline._Y1.append(Y1)
                    overH_MVline._X2.append(X2)
                    overH_MVline._Y2.append(Y2)
                    # _ICEobjID
                    nameID = cols[2]
                    overH_MVline._ICEobjID.append(nameID)
                    # _LENGTH
                    length = float(cols[4].strip())
                    overH_MVline._LENGTH.append(length)

        # Switch _layer_type attribute for those
        # Services lines within overH_LVline layer
        service_LVline = overH_LVline.split_overHLVlines(
            service_LV=service_LVline)

        # Add Aux. LV service lines
        if not self.loadTx_matcher():
            print("No able to creat aux. service lines")
        else:
            service_LVline = self.add_AuxServLine(
                service_LV=service_LVline)

        return (underG_LVline, underG_MVline, service_LVline,
                overH_LVline, overH_MVline)

    def set_attributes_buses(self,
                             underG_LVbus: Buses,
                             underG_MVbus: Buses,
                             overH_LVbus: Buses,
                             overH_MVbus: Buses,
                             busID: list[str]) -> tuple[Buses]:
        """Unpack the data of bus layers.

        Optional layer requested for ICE.

        """
        for row in busID:
            # ["Name", "Un", "CoordX1", "CoordY1"]
            cols = row.split("&")
            bus = cols[0]
            # Overhead layers
            if "AREA" in bus:
                # MV buses
                if "MT" in bus:
                    overH_MVbus._ICEobjID.append(bus)
                    # _NOMVOLT
                    nomV = float(cols[1].strip())
                    codenomV = get_NOMVOLT(nomV)
                    overH_MVbus._NOMVOLT.append(codenomV)
                    # _X1, _Y1
                    X1 = float(cols[2])
                    Y1 = float(cols[3])
                    overH_MVbus._X1.append(X1)
                    overH_MVbus._Y1.append(Y1)
                # LV buses
                else:
                    overH_LVbus._ICEobjID.append(bus)
                    # _NOMVOLT
                    nomV = float(cols[1].strip())
                    codenomV = get_NOMVOLT(nomV)
                    overH_LVbus._NOMVOLT.append(codenomV)
                    # _X1, _Y1
                    X1 = float(cols[2])
                    Y1 = float(cols[3])
                    overH_LVbus._X1.append(X1)
                    overH_LVbus._Y1.append(Y1)

            # Odd buses
            elif "_T" in bus:
                overH_LVbus._ICEobjID.append(bus.strip("_T"))
                # _NOMVOLT
                nomV = float(cols[1].strip())
                codenomV = get_NOMVOLT(nomV)
                overH_LVbus._NOMVOLT.append(codenomV)
                # _X1, _Y1
                X1 = float(cols[2])
                Y1 = float(cols[3])
                overH_LVbus._X1.append(X1)
                overH_LVbus._Y1.append(Y1)

            # Underground layers
            else:
                # MV buses
                if "MT" in bus:
                    # MV
                    underG_MVbus._ICEobjID.append(bus)
                    # _NOMVOLT
                    nomV = float(cols[1].strip())
                    codenomV = get_NOMVOLT(nomV)
                    underG_MVbus._NOMVOLT.append(codenomV)
                    # _X1, _Y1
                    X1 = float(cols[2])
                    Y1 = float(cols[3])
                    underG_MVbus._X1.append(X1)
                    underG_MVbus._Y1.append(Y1)
                # LV buses
                else:
                    underG_LVbus._ICEobjID.append(bus)
                    # _NOMVOLT
                    nomV = float(cols[1].strip())
                    codenomV = get_NOMVOLT(nomV)
                    underG_LVbus._NOMVOLT.append(codenomV)
                    # _X1, _Y1
                    X1 = float(cols[2])
                    Y1 = float(cols[3])
                    underG_LVbus._X1.append(X1)
                    underG_LVbus._Y1.append(Y1)

        return (underG_MVbus, underG_LVbus,
                overH_MVbus, overH_LVbus)

    def set_attributes_tx(self,
                          Distribution_transformers: Transformers,
                          Sub_three_phase_unit_Tx: Transformers,
                          Sub_autoTx: Transformers,
                          Sub_without_modeling_Tx: Transformers,
                          txID: list[str],
                          n_asymTxs: int) -> tuple[Transformers]:
        """Unpack transformer attributes.

        In case of single phase with neutral will be
        considered as split-phase (A, B, C) in case of
        single phase with no neutral (AB, BC, AC) it is
        taken as special connection (OY, OD) in case of
        three phase transformer (ABC) it will depend on
        its LibraryType to asign its connection.

        1. Note: Tap position is unknown, therefore it is
                 set to 1 however is passed as float type:
                  _TAPSETTING: 1.0

        2. Note: Accordance with "Supervisión
                 de la calidad del suministro
                 eléctrico en baja y media tensión”
                 (AR-NT-SUCAL) CAPITULO I
                 BT =< 1 kV and 1 kV < MT <= 100 kV.

        """
        distrib_TX = Distribution_transformers
        for i, row in enumerate(txID):
            # ["Name", "Node1", "Node2", "Switch1", "Switch2",
            # "IsRegulated", "Un1", "Un2", "Sr",
            # "LibraryType", "CoordX1", "CoordY1"]
            cols = row.split("&")
            # LibraryType
            LLype = cols[9]
            LLype2 = set_Label_Tx(LLype)
            # Asym case: ->
            # [PHASEDESIG, Sr, PRIMVOLT, kV, SECVOLT, kV, TxType]
            # Tx case: ->
            # [PHASEDESIG, Sr, PRIMVOLT, kV, SECVOLT, kV, TxType,
            # PRIMCONN, SECCONN]
            LLype3 = LLype2.split("_")

            # Trafo2Winding
            if i >= n_asymTxs:
                for n, ft in enumerate(LLype3):
                    # PHASEDESIGN
                    if n == 0:
                        ph = ft.strip()
                        phcode = get_PHASEDESIG(ph)
                        distrib_TX._PHASEDESIG.append(phcode)

                        # KVAPHASEA
                        if ph == "A":
                            kvaphaseA = float(cols[8].strip())
                            distrib_TX._KVAPHASEA.append(kvaphaseA)
                            distrib_TX._KVAPHASEB.append(float(0))
                            distrib_TX._KVAPHASEC.append(float(0))
                        # KVAPHASEB
                        elif ph == "B":
                            kvaphaseB = float(cols[8].strip())
                            distrib_TX._KVAPHASEA.append(float(0))
                            distrib_TX._KVAPHASEB.append(kvaphaseB)
                            distrib_TX._KVAPHASEC.append(float(0))
                        # KVAPHASEC
                        elif ph == "C":
                            kvaphaseC = float(cols[8].strip())
                            distrib_TX._KVAPHASEA.append(float(0))
                            distrib_TX._KVAPHASEB.append(float(0))
                            distrib_TX._KVAPHASEC.append(kvaphaseC)
                        elif ph == "AB":
                            kvaphaseA = float(cols[8].strip())/2
                            kvaphaseB = float(cols[8].strip())/2
                            distrib_TX._KVAPHASEA.append(kvaphaseA)
                            distrib_TX._KVAPHASEB.append(kvaphaseB)
                            distrib_TX._KVAPHASEC.append(float(0))
                        elif ph == "BC":
                            kvaphaseB = float(cols[8].strip())/2
                            kvaphaseC = float(cols[8].strip())/2
                            distrib_TX._KVAPHASEA.append(float(0))
                            distrib_TX._KVAPHASEB.append(kvaphaseB)
                            distrib_TX._KVAPHASEC.append(kvaphaseC)
                        elif ph == "AC":
                            kvaphaseA = float(cols[8].strip())/2
                            kvaphaseC = float(cols[8].strip())/2
                            distrib_TX._KVAPHASEA.append(kvaphaseA)
                            distrib_TX._KVAPHASEB.append(float(0))
                            distrib_TX._KVAPHASEC.append(kvaphaseC)
                        elif ph == "ABC":
                            kvaphaseA = float(cols[8].strip())/3
                            kvaphaseB = float(cols[8].strip())/3
                            kvaphaseC = float(cols[8].strip())/3
                            distrib_TX._KVAPHASEA.append(kvaphaseA)
                            distrib_TX._KVAPHASEB.append(kvaphaseB)
                            distrib_TX._KVAPHASEC.append(kvaphaseC)
                    # TTYPE
                    elif n == 6:
                        txtype = ft.strip()
                        txtypecode = get_TxType(txtype)
                        distrib_TX._TTYPE.append(txtypecode)
                    # PRIMCONN
                    elif n == 7:
                        primconn = ft
                        primmconncode = primconn.strip()
                        distrib_TX._PRIMCONN.append(primmconncode)
                    # SECCONN
                    elif n == 8:
                        secconn = ft
                        secconncode = secconn.strip()
                        distrib_TX._SECCONN.append(secconncode)

                # PRIMVOLT
                pnomv = float(cols[6].strip())
                pnomvcode = get_NOMVOLT(pnomv)
                distrib_TX._PRIMVOLT.append(pnomvcode)
                # SECVOLT
                snomv = float(cols[7].strip())
                snomvcode = get_NOMVOLT(snomv)
                distrib_TX._SECVOLT.append(snomvcode)
                # MV/MV
                if (1 < pnomv < 100) and (1 < snomv <= 100):
                    distrib_TX._MV_MV.append("YES")
                else:
                    distrib_TX._MV_MV.append("NO")
                # RATEDKVA
                ratedkva = float(cols[8].strip())
                distrib_TX._RATEDKVA.append(ratedkva)
                # TAPSETTING
                tapsetting = float(1)
                distrib_TX._TAPSETTING.append(tapsetting)
                # NODE1
                from_bus = cols[1].strip()
                distrib_TX._NODE1.append(from_bus)
                # NODE2
                to_bus = cols[2].strip()
                distrib_TX._NODE2.append(to_bus)
                # X1
                X1 = float(cols[10])
                distrib_TX._X1.append(X1)
                # Y1
                Y1 = float(cols[11])
                distrib_TX._Y1.append(Y1)
                # ICEobjectID
                name = cols[0]
                distrib_TX._ICEobjID.append(name.strip("_T"))
                # SWITCH1
                switch1 = cols[3].strip()
                distrib_TX._SWITCH1.append(switch1)
                # SWITCH2
                switch2 = cols[4].strip()
                distrib_TX._SWITCH2.append(switch2)
                # ISREGULATED
                isregulated = cols[5].strip()
                distrib_TX._ISREG.append(isregulated)

            # Trafo2WindingAsym
            else:
                for n, ft in enumerate(LLype3):
                    # PHASEDESIGN
                    if n == 0:
                        ph = ft.strip()
                        phcode = get_PHASEDESIG(ph)
                        distrib_TX._PHASEDESIG.append(phcode)
                        if ph in {"AB", "AC", "BC"}:
                            # PRIMCONN
                            primconn = ph
                            primmconncode = "OY"    # Open Wye
                            distrib_TX._PRIMCONN.append(primmconncode)
                            # SECCONN
                            secconncode = "OD"    # Open Delta
                            distrib_TX._SECCONN.append(secconncode)
                        else:
                            # PRIMCONN
                            primconn = ph
                            primmconncode = "LG"   # Line-Ground
                            distrib_TX._PRIMCONN.append(primmconncode)
                            # SECCONN
                            secconncode = "SP"     # Split-Phase
                            distrib_TX._SECCONN.append(secconncode)

                        # KVAPHASEA
                        if ph == "A":
                            kvaphaseA = float(cols[8].strip())
                            distrib_TX._KVAPHASEA.append(kvaphaseA)
                            distrib_TX._KVAPHASEB.append(float(0))
                            distrib_TX._KVAPHASEC.append(float(0))
                        # KVAPHASEB
                        elif ph == "B":
                            kvaphaseB = float(cols[8].strip())
                            distrib_TX._KVAPHASEA.append(float(0))
                            distrib_TX._KVAPHASEB.append(kvaphaseB)
                            distrib_TX._KVAPHASEC.append(float(0))
                        # KVAPHASEC
                        elif ph == "C":
                            kvaphaseC = float(cols[8].strip())
                            distrib_TX._KVAPHASEA.append(float(0))
                            distrib_TX._KVAPHASEB.append(float(0))
                            distrib_TX._KVAPHASEC.append(kvaphaseC)
                        elif ph == "AB":
                            kvaphaseA = float(cols[8].strip())/2
                            kvaphaseB = float(cols[8].strip())/2
                            distrib_TX._KVAPHASEA.append(kvaphaseA)
                            distrib_TX._KVAPHASEB.append(kvaphaseB)
                            distrib_TX._KVAPHASEC.append(float(0))
                        elif ph == "BC":
                            kvaphaseB = float(cols[8].strip())/2
                            kvaphaseC = float(cols[8].strip())/2
                            distrib_TX._KVAPHASEA.append(float(0))
                            distrib_TX._KVAPHASEB.append(kvaphaseB)
                            distrib_TX._KVAPHASEC.append(kvaphaseC)
                        elif ph == "AC":
                            kvaphaseA = float(cols[8].strip())/2
                            kvaphaseC = float(cols[8].strip())/2
                            distrib_TX._KVAPHASEA.append(kvaphaseA)
                            distrib_TX._KVAPHASEB.append(float(0))
                            distrib_TX._KVAPHASEC.append(kvaphaseC)
                        elif ph == "ABC":
                            kvaphaseA = float(cols[8].strip())/3
                            kvaphaseB = float(cols[8].strip())/3
                            kvaphaseC = float(cols[8].strip())/3
                            distrib_TX._KVAPHASEA.append(kvaphaseA)
                            distrib_TX._KVAPHASEB.append(kvaphaseB)
                            distrib_TX._KVAPHASEC.append(kvaphaseC)
                    # TTYPE
                    elif n == 6:
                        txtype = ft.strip()
                        txtypecode = get_TxType(txtype)
                        distrib_TX._TTYPE.append(txtypecode)

                # PRIMVOLT
                pnomv = float(cols[6].strip())
                pnomvcode = get_NOMVOLT(pnomv)
                distrib_TX._PRIMVOLT.append(pnomvcode)
                # SECVOLT
                snomv = float(cols[7].strip())
                snomvcode = get_NOMVOLT(snomv)
                distrib_TX._SECVOLT.append(snomvcode)
                # MV/MV
                if (1 < pnomv < 100) and (1 < snomv <= 100):
                    distrib_TX._MV_MV.append("YES")
                else:
                    distrib_TX._MV_MV.append("NO")
                # RATEDKVA
                ratedkva = float(cols[8].strip())
                distrib_TX._RATEDKVA.append(ratedkva)
                # TAPSETTING
                tapsetting = float(1)
                distrib_TX._TAPSETTING.append(tapsetting)
                # NODE1
                from_bus = cols[1].strip()
                distrib_TX._NODE1.append(from_bus)
                # NODE2
                to_bus = cols[2].strip()
                distrib_TX._NODE2.append(to_bus)
                # X1
                X1 = float(cols[10])
                distrib_TX._X1.append(X1)
                # Y1
                Y1 = float(cols[11])
                distrib_TX._Y1.append(Y1)
                # ICEobject_ID
                name = cols[0]
                distrib_TX._ICEobjID.append(name.strip("_T"))
                # SWITCH1
                switch1 = cols[3].strip()
                distrib_TX._SWITCH1.append(switch1)
                # SWITCH2
                switch2 = cols[4].strip()
                distrib_TX._SWITCH2.append(switch2)
                # ISREGULATED
                isregulated = cols[5].strip()
                distrib_TX._ISREG.append(isregulated)

        return (distrib_TX,
                Sub_three_phase_unit_Tx,
                Sub_autoTx,
                Sub_without_modeling_Tx)

    def set_attributes_loads(self,
                             loadID: list[str],
                             LVload: Loads,
                             MVload: Loads) -> tuple[Loads]:
        """Unpack LV and MV loads attributes.

        In spite of is possible to retrieve MV loads
        there is no data about such kind of loads currently.

        Note: Attribute "AMI" is "NO" for all loads
              since there is no information yet.
              In case was "YES" a _ID attribute must
              be provided so do its shapeload file.

        """
        for row in loadID:
            # ["Node1", "Name", "Phase", "Switch1",
            # "Un", "E", "VelanderK1", "LfType", "Unit",
            # "CosPhi", "CoordX1", "CoordY1", "Tipo"]
            cols = row.split("&")
            load = cols[0]

            if "BT" in load:
                # KWHMONTH
                kwhmonth = float(cols[5].strip())
                LVload._KWHMONTH.append(kwhmonth)
                # NOMVOLT
                nomvolt = float(cols[4])
                nomvoltcode = get_NOMVOLT(nomvolt)
                LVload._NOMVOLT.append(nomvoltcode)
                # SERVICE
                phase = int(cols[2].strip())
                srvc = get_SERVICE(phase)
                LVload._SERVICE.append(srvc)
                # PHASEDESIG
                phasedesig = int(cols[2].strip())
                phasedesigcode = get_PHASEDESIG(phcode=phasedesig)
                LVload._PHASEDESIG.append(phasedesigcode)
                # SWITCH1
                switch1 = cols[3].strip()
                LVload._SWITCH1.append(switch1)
                # NODE1
                node1 = cols[0].strip()
                LVload._NODE1.append(node1)
                # PF
                pf = float(cols[9].strip())
                LVload._PF.append(pf)
                # ICEobjectID
                objectID = cols[1].strip()
                LVload._ICEobjID.append(objectID)
                # X1
                X1 = float(cols[10].strip())
                LVload._X1.append(X1)
                # Y1
                Y1 = float(cols[11].strip())
                LVload._Y1.append(Y1)
                # CLASS
                loadType = get_CLASS(cols[12])
                LVload._CLASS.append(loadType)
                # AMI
                LVload._AMI.append("NO")

            # Odd loads
            elif "_T" in load:
                # KWHMONTH
                kwhmonth = float(cols[5].strip())
                LVload._KWHMONTH.append(kwhmonth)
                # NOMVOLT
                nomvolt = float(cols[4])
                nomvoltcode = get_NOMVOLT(nomvolt)
                LVload._NOMVOLT.append(nomvoltcode)
                # SERVICE
                phase = int(cols[2].strip())
                srvc = get_SERVICE(phase)
                LVload._SERVICE.append(srvc)
                # PHASEDESIG
                phasedesig = int(cols[2].strip())
                phasedesigcode = get_PHASEDESIG(phcode=phasedesig)
                LVload._PHASEDESIG.append(phasedesigcode)
                # SWITCH1
                switch1 = cols[3].strip()
                LVload._SWITCH1.append(switch1)
                # NODE1
                node1 = cols[0].strip()
                LVload._NODE1.append(node1)
                # PF
                pf = float(cols[9].strip())
                LVload._PF.append(pf)
                # ICEobjectID
                objectID = cols[1].strip().strip("L")
                LVload._ICEobjID.append(objectID)
                # X1
                X1 = float(cols[10].strip())
                # Y1
                Y1 = float(cols[11].strip())
                # Drag odd loads 10cm and update attr
                X1 += 10e-2
                Y1 += 10e-2
                LVload._X1.append(X1)
                LVload._Y1.append(Y1)
                # CLASS
                loadType = get_CLASS(cols[12])
                LVload._CLASS.append(loadType)
                # Update _ODDLOAD attr
                LVload._ODDLOAD = True
                # AMI
                LVload._AMI.append("NO")

            elif "MT" in load:
                # Missing Data
                pass

        return (LVload, MVload)

    def set_attributes_fuse(self,
                            fuse: Fuse,
                            fuseID: list[str]) -> Fuse:
        """Unpack fuses attributes.

        One layer of fuses only.

        """
        for row in fuseID:
            # ["Name", "Phase", "IsActive", "OnElement", "X", "Y"]
            cols = row.split("&")

            # ICEObjectID
            objetID = cols[0].strip("F")
            fuse._ICEobjID.append(objetID)
            # PHASEDESIGN
            phasedesign = int(cols[1].strip())
            phasedesigncode = get_PHASEDESIG(phcode=phasedesign)
            fuse._PHASEDESIG.append(phasedesigncode)
            # NC
            nc = cols[2].strip()
            nccode = get_NC(nc)
            fuse._NC.append(nccode)
            # ONELEMENT
            onelement = cols[3].strip()
            fuse._ONELEMENT.append(onelement)
            # _X1
            fuse._X1.append(float(cols[4]))
            # _Y1
            fuse._Y1.append(float(cols[5]))
        return (fuse)

    def set_attributes_PV(self,
                          ssdg_pv: SSDG_PV,
                          cktNeplan: CKTdata,
                          pvID: list[str]) -> SSDG_PV:
        """Unpack attributes of Photovoltaic technologies.

        In order to make hosting capacity in low voltage networks.

        """
        for row in pvID:
            # cols: ["Name", "Node1", "Switch1", "Pset", "Cosr", "Unit",
            # "Phase", "Sr", "nProductionType", "Ur", "Un", "Sk2max", "Sk2min",
            # CURVE1_P, CURVE2_Q]
            cols = row.split("&")

            # ICEobjectID
            objectID = cols[0].strip("_PV")
            ssdg_pv._ICEobjID.append(objectID)
            # NODE1
            node1 = cols[1].strip()
            ssdg_pv._NODE1.append(node1)
            # SWITCH1
            switch1 = cols[2].strip()
            ssdg_pv._SWITCH1.append(switch1)
            # KVA
            kva = float(cols[7].strip())
            ssdg_pv._KVA.append(kva)
            # TECH
            ssdg_pv._TECH.append("PV")
            # X1, Y1
            busname = cols[1].strip()
            (X1, Y1) = cktNeplan.loc_buscoord(busname)
            ssdg_pv._X1.append(X1)
            ssdg_pv._Y1.append(Y1)
            # CURVE1
            ssdg_pv._CURVE1.append(cols[-2])
            # CURVE2
            ssdg_pv._CURVE2.append(cols[-1])

        return (ssdg_pv)

    def set_attributes_recloser(self,
                                recloser: Reclosers,
                                recloserID: list[str]) -> Reclosers:
        """"Reclosers (also considered breakers).

        One layer for reclosers only.

        """
        # ["Name", "Phase", "Switch", "OnElement", "X", "Y"]
        for row in recloserID:
            cols = row.split("&")

            # ICEobjectID
            objectID = cols[0].strip("R")
            recloser._ICEobjID.append(objectID)
            # PHASEDESIG
            phasedesig = int(cols[1].strip())
            phasedesigcode = get_PHASEDESIG(phcode=phasedesig)
            recloser._PHASEDESIG.append(phasedesigcode)
            # NC
            NC = cols[2].strip()
            recloser._NC.append(NC)
            # X1
            X1 = float(cols[4])
            recloser._X1.append(X1)
            # Y1
            Y1 = float(cols[5])
            recloser._Y1.append(Y1)

        return (recloser)

    def set_attributes_regulator(self,
                                 regulatorID: list[str],
                                 regulator: Regulators) -> Regulators:
        """Unpack data of regulars and set its attributes.

        To assign the unknown attributes given the lack of information
        in the circuit, the following should be considered:

        `VREG:` is typically used 120V in distribution network.
        `BANDWIDTH:` is typically used 2 in distributon network.
        `PT_RATIO:` use the nominal voltage of the circuit and regulated
                    voltage for its calculation.
        `TAPS:` are asigned as 32.

        """
        # ["Name", "Node1", "Node2", "Switch1", "Switch2",
        # "Un1", "Un2", "Phase", "LibraryType", "X", "Y"]
        for row in regulatorID:
            cols = row.split("&")
            libraryType = cols[8].split("_")

            # ICEobjectID
            objectID = cols[0].strip("_R")
            regulator._ICEobjID.append(objectID)
            # PHASEDESIG
            phasedesig = int(cols[7])
            phasedesigcode = get_PHASEDESIG(phcode=phasedesig)
            regulator._PHASEDESIG.append(phasedesigcode)
            # NOMVOLT
            nomvolT = float(cols[5])
            nomvolTcode = get_NOMVOLT(nomvolT)
            regulator._NOMVOLT.append(nomvolTcode)
            # KVA
            kva = float(libraryType[1])
            regulator._KVA.append(kva)
            # VREG
            vreg = float(120)
            regulator._VREG.append(vreg)
            # PT_RATIO
            pt_ratio = get_TP_RATIO(vnom=nomvolT, vreg=vreg)
            regulator._PT_RATIO.append(pt_ratio)
            # BANDWIDTH
            bandwidth = float(2)
            regulator._BANDWIDTH.append(bandwidth)
            # X1
            X1 = float(cols[9])
            regulator._X1.append(X1)
            # Y1
            Y1 = float(cols[10])
            regulator._Y1.append(Y1)
            # TAPS
            regulator._TAPS.append(int(32))

        return (regulator)

    def set_attributes_publicLights(self,
                                    public_lights: PublicLights,
                                    publicLightsID: list[str]) -> PublicLights:
        """Missing documentation.

        Missing description of this method.

        """
        # ["Node1", "Name", "Phase", "Switch1",
        # "Potencia_kW", "Lftype", "Unit", "CosPhi",
        # "CoordX1", "CoordY1", "Un"]
        for row in publicLightsID:
            cols = row.split("&")

            # ICEobjectID
            objectID = cols[1]
            public_lights._ICEobjID.append(objectID)
            # SERVICE
            phase = int(cols[2])
            srvc = get_SERVICE(phase)
            public_lights._SERVICE.append(srvc)
            # KW
            kw = float(cols[4])
            public_lights._KW.append(kw)
            # NOMVOLT
            nomvolt = float(cols[10])
            nomvoltcode = get_NOMVOLT(nomvolt)
            public_lights._NOMVOLT.append(nomvoltcode)
            # X1
            X1 = float(cols[8])
            public_lights._X1.append(X1)
            # Y1
            Y1 = float(cols[9])
            public_lights._Y1.append(Y1)

        return (public_lights)

    def loadTx_matcher(self) -> bool:
        """Verify consistency of connections.

        This method assesses whether _SECCONN
        attribute of transformers possess
        matching features with _SERVICE code of
        those odd loads right over them taking advantage
        that such loads _ICEobjID are labeled
        with "_T" at tail.
        It returns `True` if all load are
        perfectly align and `False` otherwise; however,
        in case either transformer or loads layers
        do not exist also returns `False`.

        by following below criterion:

        matcher = {
            "OD": {123, 12, 23, 13},
            "SP": {1, 2, 3, 12, 23, 13},
            "4D": {123}
        }

        Where the key is the _SECCONN and
        the integers set the _SERVICE code.

        Note: This method should be called before
        creat auxiliary lines.

        """
        matcher = {
            "OD": {123, 12, 23, 13},
            "SP": {1, 2, 3, 12, 23, 13},
            "4D": {123}
        }
        try:
            loadsdata = self._LVloads["LV_load"]
            txsdata = self._transformers["Distribution_transformers"]
        except KeyError as e:
            print(f"No layer called {e}")
            return False

        # Odd loads name
        loadsfree = []
        for c in loadsdata["ICEobjID"]:
            if "_T" in c:
                loadsfree.append(c)
        loadsfree = [t.strip("_T") for t in loadsfree]

        # Retrieve match attribute
        for v in loadsfree:
            i = txsdata["ICEobjID"].index(v)
            j = loadsdata["ICEobjID"].index(f"{v}_T")
            for k, c in txsdata.items():
                if k == "SECCONN":
                    conn = c[i]
                    for m, f in loadsdata.items():
                        if m == "SERVICE":
                            srvc = f[j]
                            try:
                                if srvc not in matcher[conn]:
                                    raise Exception("ConnError")
                            except Exception as e:
                                print(
                                    (f"{e}:"),
                                    ("Connection does not match"),
                                    (f"in object {v}"))
                                return False
        return True


def get_PHASEDESIG(phcode) -> int:
    """Phase designation.

    Set the phase code based on the manual either
    Neplan code or Phase letter if `phcode` is a string.
    Columns:
        Code: Neplan
        ph: Manual
    +---------+---------------+
    |  code   |      ph       |
    +---------+---------------+
    |    3    |  1: C (T)     |
    |    2    |  2: B (S)     |
    |    6    |  3: BC (ST)   |
    |    1    |  4: A (R)     |
    |    5    |  5: AC (RT)   |
    |    4    |  6: AB (RS)   |
    |    0    |  7: ABC (RST) |
    |    7    |  7: ABC (RST) |
    +---------+---------------+

    If `phcode` is a integer SIRDE translation will be taken.

    """
    if type(phcode) is str:
        if phcode == "C" or phcode == "T":
            return 1
        elif phcode == "B" or phcode == "S":
            return 2
        elif phcode == "BC" or phcode == "ST":
            return 3
        elif phcode == "A" or phcode == "R":
            return 4
        elif phcode == "AC" or phcode == "RT":
            return 5
        elif phcode == "AB" or phcode == "RS":
            return 6
        elif phcode == "ABC" or phcode == "RST":
            return 7
    else:
        if phcode == 3:
            return 1
        elif phcode == 2:
            return 2
        elif phcode == 6:
            return 3
        elif phcode == 1:
            return 4
        elif phcode == 5:
            return 5
        elif phcode == 4:
            return 6
        elif phcode == 0 or phcode == 7:
            return 7


def get_NOMVOLT(nomVLL: float) -> int:
    """Nominal voltage.

    +---------+-----------------+-----------------+----------------+
    |  Code   | Voltage LN [kV] | Voltage LL [kV] |   Connection   |
    +---------+-----------------+-----------------+----------------+
    |   20    |     0.12        |       0.208     |      wye       |
    |   30    |     0.12        |       0.24      |  split-phase   |
    |   35    |     0.254       |       0.44      |      wye       |
    |   40    |     0.24        |       0.48      |  split-phase*  |
    |   50    |     0.277       |       0.48      |      wye       |
    |   60    |     0.48        |       0.48      |     delta      |
    |   70    |     0.24        |       0.416     |      wye       |
    |   80    |     2.40        |       2.40      |     delta      |
    |   110   |     4.16        |       4.16      |     delta      |
    |   120   |     2.40        |       4.16      |      wye       |
    |   150   |     7.20        |       7.20      |     delta      |
    |   160   |     4.16        |       7.20      |      wye       |
    |   210   |     7.22        |       12.5      |      wye       |
    |   230   |     7.62        |       13.2      |      wye       |
    |   260   |     13.8        |       13.8      |     delta      |
    |   270   |     7.97        |       13.8      |      wye       |
    |   340   |     14.38       |       24.9      |      wye       |
    |   380   |     19.92       |       34.5      |      wye       |
    +---------+-----------------+-----------------+----------------+
    Note: Code 40 refers to special delta of splitted phase.

    """
    nomVs = [0.208, 0.24, 0.44, 0.48, 0.48,
             0.48, 0.416, 2.40, 4.16, 4.16,
             7.20, 7.20, 12.5, 13.2, 13.8,
             13.8, 24.9, 34.5]
    codes = [20, 30, 35, 40, 50, 60, 70, 80,
             110, 120, 150, 160, 210, 230,
             260, 270, 340, 380]

    return codes[nomVs.index(nomVLL)]


def get_INSULVOLT(nomVLL: float) -> str:
    """Insulation standardized voltage (kV).

    For Underground MV lines. Usually:
    - 15
    - 25
    - 35
    - 45
    Otherwise QGIS2OPENDSS handbook should be considered.

    """
    if nomVLL <= 15:
        return "15"
    elif 15 < nomVLL <= 25:
        return "25"
    elif 25 < nomVLL <= 35:
        return "35"
    elif nomVLL > 35:
        return "45"


def get_SERVICE(code: int) -> int:
    """Load connection.

    Connection type designation of Loads and Public
    Lighting.
    It corresponds to the type of connection presented
    by the load. It must have a type of connection
    consistent with the type of cable of the phase
    to which the load is connected.
    Turns the given Neplan phase code into the one used in
    the manual also integer.
    Columns:
        srvc: Service Plug-in Manual code
        code: Neplan code

    +---------+-----------------+----------------------------------------+
    |  code   |      srvc       |              Description               |
    +---------+-----------------+----------------------------------------+
    |    1    |  1: A (R)       | Load connected to alive 1 and neutral. |
    |    2    |  2: B (S)       | Load connected to alive 2 and neutral. |
    |    3    |  3: C (T)       | Load connected to phase 3 and neutral. |
    |    4    |  12: AB (RS)    | Load connected to alive 1 and alive 2. |
    |    6    |  23: BC (ST)    | Load connected to phase 2 and phase 3. |
    |    5    |  13: AC (RT)    | Load connected to phase 1 and phase 3. |
    |    0    |  123: ABC (RST) | Load connected to three phase.         |
    |    7    |  123: ABC (RST) | Load connected to three phase.         |
    +---------+-----------------+----------------------------------------+

    """
    if code == 1:
        return int(1)
    elif code == 2:
        return int(2)
    elif code == 3:
        return int(3)
    elif code == 4:
        return int(12)
    elif code == 5:
        return int(13)
    elif code == 6:
        return int(23)
    elif code == 0 or code == 7:
        return int(123)


def get_TxType(txtype: str) -> str:
    """Transformer type designation.

    Set the type code based on the SIRDE either
    Neplan code.
    PARAMETERS:
        Subtipo: Phase (1, 2, 3, 4, 5) SIRDE code
        Descripcion: SIRDE code

    +---------+-----------------+
    | Subtipo |   Descripcion   |
    +---------+-----------------+
    |    1    |  Tipo poste     |
    |    2    |  Pedestal       |
    |    3    |  Sumergible     |
    |    4    |  Subestacion    |
    |    5    |  Seco           |
    +---------+-----------------+

    """
    if txtype == "1":
        return "Tipo poste"
    elif txtype == "2":
        return "Pedestal"
    elif txtype == "3":
        return "Sumergible"
    elif txtype == "4":
        return "Subestacion"
    elif txtype == "5":
        return "Seco"


def get_NC(nc: str) -> str:
    """Fuse Normally Closed.

    Indicates if the fuse is open or closed.
    NEPLAN code : IsActive
    Manual code : NC

    +----------+-------+
    | IsActive |   NC  |
    +----------+-------+
    |    1     |  Yes  |
    |    0     |  No   |
    +----------+-------+

    """
    if nc == "1":
        return "Yes"
    else:
        return "No"


def get_TP_RATIO(vnom: float, vreg: float) -> float:
    """Tap ratio.

    Return the transformation ratio of the regulator
    PT voltages.

    Note: Typically the secondary winding is at 120V.
    Note: Manual considers this attribute as real number
          this function rounds and returns a
          float according to the manual.

    """
    tp_ratio = ((vnom*1e3)/np.sqrt(3))*(1/vreg)
    return float(round(tp_ratio))


def get_CLASS(code: str) -> str:
    """
    Load type designation.

    Set the type code based on the manual either
    SIRDE code.
    PARAMETERS:
        class: Manual description
        code: SIRDE code

    Note: Manual description does not have Social class
        R: Residential
        C: Commercial
        I: Industrial

    +--------+--------------------------------------------------+------------+
    |  Code  |                 Customer class                   |  class     |
    +--------+--------------------------------------------------+------------+
    |    1   | Residencial                                      |  R         |
    |    2   | General                                          |  C         |
    |    3   | Industrial                                       |  I         |
    |    4   | Social                                           |  R         |
    |   22   | General                                          |  C         |
    |   23   | General                                          |  C         |
    |   32   | Industrial                                       |  I         |
    |   33   | Industrial                                       |  I         |
    |   41   | Social                                           |  R         |
    |   80   | Media Tensión A                                  |  I         |
    |   85   | Media Tensión B                                  |  I         |
    |   15   | Usuarios Directos del Servicio de Generación ICE |  I         |
    |   13   | Ventas a ICE Distribución y CNFL                 |  I         |
    |   14   | Ventas al Servicio de Distribución               |  I         |
    +--------+--------------------------------------------------+------------+


    """

    if code == "1":
        return "R"

    elif code in ["2", "22", "23"]:
        return "C"

    elif code in ["3", "32", "33", "80", "85", "15", "13", "14"]:
        return "I"

    elif code in ["4", "41"]:
        return "R"


def set_Label(LibType: str) -> str:
    """Replace to labels used in manual.

    Notation from Neplan/SIRDE to manual notation.
    No data {
            "NE": "No Existe",
            "NT": "No tiene",
            "UNK": "Desconocido",
            "NA": "No aplica"
        }
    ALL to "None": No data (Empty) instead.

    MATERIAL = {
        "CO_SO": "SCU",
        "CO_TR": "BCU",
        "COBRE": "CU",
        "ALUMI": "AL",
    }
    INSULVOLT = {
        "600": "0.6",
        "1000": "1.0",
        "2000": "2.0"
    }
    INSULMAT = {
            "DESNU": "BARE",
            "SEMIA": "COVER",
            "AISLA": "INSUL",
    }
    TYPE = {
        "OH_MVline": {
            "1": "SPH",
            "2": "BPH",
            "3": "TPH"
        },
        "UG_MVline" : {
            "": ""
        },
        "OH_LVline" : {
            "1": "LVC",
            "2": "DPX",
            "3": "TPX",
            "4": "QPX",
            "5": "CC",
            "6": "SLC"
        },
        "UG_LVline" : {
            "1": "SPH",
            "2": "TPH",
            "3": "PLC"
        }
    }
    1. Note: keys "1", "2" & "3" are seen like string
             and could take different values depending on
             the zone voltage level.
    2. Note: Neplan notation LibraryType does not have the
            label code (TYPE) for UG's conducors.
    3. Note: UG_MVline type has no data about conductors TYPE.

    """
    # Missing data:
    noData = ["NE", "NT", "UNK", "NA"]
    for b in noData:
        LibType = LibType.replace(b, "None")
    # MATERIAL
    material = {
        "CO_SO": "SCU",
        "CO_TR": "BCU",
        "COBRE": "CU",
        "ALUMI": "AL",
    }
    for (k, v) in material.items():
        LibType = LibType.replace(k, v)
    # INSULVOLT
    insulvolt = {
        "600": "0.6",
        "1000": "1.0",
        "2000": "2.0"
    }
    for (k, v) in insulvolt.items():
        LibType = LibType.replace(k, v)
    # INSULMAT
    insulmat = {
            "DESNU": "BARE",
            "SEMIA": "COVER",
            "AISLA": "INSUL",
    }
    for (k, v) in insulmat.items():
        LibType = LibType.replace(k, v)

    return LibType


def set_Label_Tx(LibType: str) -> str:
    """Change name of labels.

    It replaces the original labels (values's name of
    attributes comming from Neplan) in LibraryType of
    transformers, for common notation used in the manual of
    `QGIS2OPENDSS` plug-in.
    _PRIMCONN
    primconn = {
        "Estrella": "Y",
        "Delta":, "D",
        "OpenWye":, "OY",
        "LineGound": "LG"
    }
    _SECCONN
    secconn = {
        "SplitPhase": "SP",
        "Fase_Partida": "4D",
        "OpenDelta": "OD"
    }

    Note: _SECCONN of 4D means delta of four-wires.

    """
    # Library Type Modified
    newTxLibType = LibType
    # NOMVOLT
    nomvolt = {
        ".240": "0.24",
        ".208": "0.208",
        ".480": "0.48"
    }

    for (k, v) in nomvolt.items():
        newTxLibType = newTxLibType.replace(k, v)

    # Connection at any side
    conn = {
        "Estrella": "Y",
        "Delta": "D",
        "Fase_Partida": "4D"
    }

    for (k, v) in conn.items():
        newTxLibType = newTxLibType.replace(k, v)

    return newTxLibType


def layer2df(layer: dict) -> tuple[pd.DataFrame]:
    """Convert to pd.DataFrame.

    It gets the layer of certain object as dict
    and returns a DataFrame of pandas as well as such dict.
    Format of the layer:
    overH_MVline = {
        "line_type": "LayerName",
        "ICEobjectID": [val1, val2, ..., valN],
        "NEUTMAT": [val1, val2, ..., valN],
        ...,
        "Y2": [val1, val2, ..., valN]
    }

    """
    dictData = dict()
    for (k, v) in layer.items():
        if isinstance(v, list):
            if len(v) != 0:
                dictData[k] = v
    return pd.DataFrame.from_dict(dictData), dictData


def df2shp(df: pd.DataFrame, namestr: str, output_path: str):
    """From pandas.DataFrame to shapefile.

    It will create a folder named "GIS" in the current
    working directory (where your Python script is located),
    if it doesn't already exist.
    Then, it will write the specified content to a file
    named "namestr.shp" within the `GIS` folder.
    If you encounter any permission-related issues,
    you might need to adjust the file paths or run the
    script with appropriate privileges.
    It gets DataFrame as argument to be converted to
    `pd.GeoDataFrame` and finally into shapefile `*.shp`.
    After have been create the DataFrame, add the
    geometry column when create tha GeoDataFrame.

    The crs argument EPSG = 5367 means that this
    geographic coordinate
    system is typically used in Costa Rica.

    Note: For create the shapefile, create a path
          called GIS, this for store the .shp and
          the other files generated.

    """
    import os

    # Define the folder name
    folder_name = output_path + r"\GIS\Capas"

    # Create the folder if it does not exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Define the file path within the folder
    file_path = os.path.join(".", folder_name, namestr)

    if not df.empty:
        if "X2" and "Y2" in df.columns:
            from_buses = [Point(X1, Y1) for X1, Y1 in zip(df["X1"], df["Y1"])]
            to_buses = [Point(X2, Y2) for X2, Y2 in zip(df["X2"], df["Y2"])]
            lines = [
                LineString([p1, p2]) for p1, p2 in zip(from_buses, to_buses)
                ]
            gdf = gpd.GeoDataFrame(df, geometry=lines, crs="EPSG:5367")
            gdf.to_file(file_path+".shp")
            return gdf

        else:
            geometry = [Point(X, Y) for X, Y in zip(df["X1"], df["Y1"])]
            gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:5367")
            gdf.to_file(file_path+".shp")
            return gdf


if __name__ == "__main__":
    # Import Neplan circuit data
    directory = r"C:\Users\luisd\Dropbox\Practica_UCR\Juan_Ilama_Jaco"\
                r"\Circuito_5.xlsx"
    output_path = r"C:\Users\luisd\OneDrive\Escritorio\ICE CYME"\
                  r"\Circuito_Juan_Ilama_Jaco"
    cktNeplan = CKTdata()
    cktNeplan.call_data(directory)
    # New QGIS circuit
    cktQgis = CKTqgis()

    # ------------------------
    # Buses layers *.shp files
    # ------------------------
    _ = cktQgis.add_buslayers(cktNeplan)
    OH_LVbuses_df, _ = layer2df(cktQgis._buses["overH_LVbuses"])
    OH_MVbuses_df, _ = layer2df(cktQgis._buses["overH_MVbuses"])
    UG_LVbuses_df, _ = layer2df(cktQgis._buses["underG_LVbuses"])
    UG_MVbuses_df, _ = layer2df(cktQgis._buses["underG_MVbuses"])
    # Finally write shapefiles within "./GIS/shapename.shp"
    OH_LVbuses_gdf = df2shp(OH_LVbuses_df, "overH_LVbuses", output_path)
    OH_MVbuses_gdf = df2shp(OH_MVbuses_df, "overH_MVbuses", output_path)
    UG_LVbuses_gdf = df2shp(UG_LVbuses_df, "underG_LVbuses", output_path)
    UG_MVbuses_gdf = df2shp(UG_MVbuses_df, "underG_MVbuses", output_path)

    # ------------------------------
    # Transformer layers *.shp files
    # ------------------------------
    _ = cktQgis.add_txlayers(cktNeplan)
    # Turn layers into df
    Distribution_transformers_df, _ = layer2df(
        cktQgis._transformers["Distribution_transformers"])
    # Subestation_three_phase_transformer_df, _ = layer2df(
    #     cktQgis._transformers["Subestation_three_phase_transformer"])
    # Subestation_autotransformer_df, _ = layer2df(
    #     cktQgis._transformers["Subestation_autotransformer"])
    # Subestation_without_modeling_transformer_df, _ = layer2df(
    #     cktQgis._transformers["Subestation_without_modeling_transformer"])
    # Finally write shapefiles within "./GIS/shapename.shp"
    Distribution_transformers_gdf = df2shp(
        Distribution_transformers_df, "Distribution_transformers", output_path)
    # Subestation_three_phase_transformer_gdf = df2shp(
    #     Subestation_three_phase_transformer_df,
    #     "Subestation_three_phase_transformer",
    #     output_path)
    # Subestation_autotransformer_gdf = df2shp(
    #     Subestation_autotransformer_df,
    #     "Subestation_autotransformer",
    #     output_path)
    # Subestation_without_modeling_transformer_gdf = df2shp(
    #     Subestation_without_modeling_transformer_df,
    #     "Subestation_without_modeling_transformer",
    #     output_path)

    # Provisional model of subestation
    subestation_without_modeling = {"MEDVOLT": [34.5],
                                    "X1": [427371.8305],
                                    "Y1": [1102298.898]}
    modelFree_subEstat_df = pd.DataFrame(subestation_without_modeling)
    x1, y1 = modelFree_subEstat_df["X1"], modelFree_subEstat_df["Y1"]
    modelFree_subEstat_gdf = gpd.GeoDataFrame(
        modelFree_subEstat_df,
        geometry=gpd.points_from_xy(x1, y1),
        crs="EPSG:5367")

    modelFree_subEstat_gdf.to_file(
        output_path + r"\GIS\Capas\modelFree_subEstat.shp")

    # -----------------------
    # Load layers *.shp files
    # -----------------------
    _ = cktQgis.add_load_layers(cktNeplan)
    # Turn layers into df
    LV_load_df, _ = layer2df(cktQgis._LVloads["LV_load"])
    MV_load_df, _ = layer2df(cktQgis._MVloads["MV_load"])
    # Finally write shapefiles within "./GIS/shapename.shp"
    LV_load_gdf = df2shp(LV_load_df, "LV_load", output_path)
    # MV_load_gdf = df2shp(MV_load_df, "MV_load", output_path)

    # -----------------------
    # Line layers *.shp files
    # -----------------------
    _ = cktQgis.add_linelayers(cktNeplan)
    # Turn layers into df
    OH_LVlines_df, _ = layer2df(cktQgis._lines["overH_LVlines"])
    OH_MVlines_df, _ = layer2df(cktQgis._lines["overH_MVlines"])
    UG_LVlines_df, _ = layer2df(cktQgis._lines["underG_LVlines"])
    UG_MVlines_df, _ = layer2df(cktQgis._lines["underG_MVlines"])
    service_LVlines_df, _ = layer2df(cktQgis._lines["service_LVlines"])
    # Finally write shapefiles within "./GIS/shapename.shp"
    OH_LVline_gdf = df2shp(OH_LVlines_df, "overH_LVlines", output_path)
    OH_MVline_gdf = df2shp(OH_MVlines_df, "overH_MVlines", output_path)
    UG_LVline_gdf = df2shp(UG_LVlines_df, "underG_LVlines", output_path)
    UG_MVline_gdf = df2shp(UG_MVlines_df, "underG_MVlines", output_path)
    service_LVlines_gdf = df2shp(
        service_LVlines_df,
        "service_LVlines",
        output_path)

    # -----------------------
    # Fuse layers *.shp files
    # -----------------------
    _ = cktQgis.add_fuse_layer(cktNeplan)
    # Turn layers into df
    fuse_df, _ = layer2df(cktQgis._fuses["Fuses"])
    # Finally write shapefiles within "./GIS/shapename.shp"
    fuse_gdf = df2shp(fuse_df, "Fuses", output_path)

    # ----------------------------
    # Regulator layers *.shp files
    # ----------------------------
    _ = cktQgis.add_regulator_layer(cktNeplan)
    # Turn layers into df
    regulator_df, _ = layer2df(cktQgis._regulators["Regulators"])
    # Finally write shapefiles within "./GIS/shapename.shp"
    regulator_gdf = df2shp(regulator_df, "Regulators", output_path)

    # ---------------------
    # PV layers *.shp files
    # ---------------------
    _ = cktQgis.add_SSDG_PV_layer(cktNeplan)
    # Turn layers into df
    PV_df, _ = layer2df(cktQgis._smallScale_DG["SSDG_PVs"])
    # Finally write shapefiles within "./GIS/shapename.shp"
    PV_gdf = df2shp(PV_df, "SSDG_PVs", output_path)

    # ---------------------------
    # Recloser layers *.shp files
    # ---------------------------
    _ = cktQgis.add_recloser_layer(cktNeplan)
    # Turn layers into df
    recloser_df, _ = layer2df(cktQgis._reclosers["Reclosers"])
    # Finally write shapefiles within "./GIS/shapename.shp"
    recloser_gdf = df2shp(recloser_df, "Reclosers", output_path)

    # ---------------------------------
    # Public Lights layers *.shp files
    # ---------------------------------
    _ = cktQgis.add_PublicLights_layer(cktNeplan)
    # Turn layers into df
    public_Lights_df, _ = layer2df(cktQgis._publicLights["Public_Lights"])
    # Finally write shapefiles within "./GIS/shapename.shp"
    public_Lights_gdf = df2shp(public_Lights_df, "Public_Lights", output_path)
