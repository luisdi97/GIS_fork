"""Parse *.shp attributes.

This program translates and adapts a given format of
certain kind of shape file attribute's name into a
standard notation requires for QGIS based on the manual
of "QGIS2OPENDSS" plug-in.

   Mario Roberto Peralta A.
   Universidad de Costa Rica (UCR)

Electric Power & Energy Research Laboratory (EPERLab).
"""
import pandas as pd


class CKTdata:
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
        self._breakers = {}

    def call_data(self, path: str) -> None:
        import pandas as pd
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
            # Breakers
            elif sheet == sheets[8]:
                for c in df[sheet].columns:
                    values = [v for v in df[sheet][c]]
                    # Update attribute
                    self._breakers[c] = values


class Line():
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
                *String* datatype. Usually for overhead MV lines if
                it starts with "Y" or "N" (meaning with LV cable beneath
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
            TYPE:
                For Over Head LV
                - LVC: Low Voltage Cable
                - CC: Concentric Cable
                - SLC: Street Lighting Cable
                Other
                - PLC: Public Lighting Conductor
                - SPH: Single-Phase
                - BPH: Split-Phase
                - TPH: Three-Phase

        1. Note: Optional attributes: "geometry" is not explicitly
                 mencioned in the manual of "QGIS2OPENDSS" plug-in.
                 It is the spatial points the line pass through.
                 "objectID" works as an extra unique label
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
        self._objectID = []         # New
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


class UG_MVline(Line):
    def __init__(self):
        super().__init__()
        self._line_type = "underG_MVlines"


class OH_MVline(Line):
    def __init__(self):
        super().__init__()
        self._line_type = "overH_MVlines"


class UG_LVline(Line):
    def __init__(self):
        super().__init__()
        self._line_type = "underG_LVlines"


class OH_LVline(Line):
    def __init__(self):
        super().__init__()
        self._line_type = "overH_LVlines"


class serv_LVline(Line):
    def __init__(self):
        super().__init__()
        self._line_type = "service_LVlines"


class CKT_QGIS():
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
        self.EVs = {}
        self.EbusesC = {}

    def add_linelayers(self, busesData: dict[list],
                       linesData: dict[list]) -> tuple[Line]:
        """Creats line layers.

        It gets lines data, creat the objects and sets its
        attributes.
        """
        # lineID
        linesID = concat_linecols(linesData)
        # Creat instances
        underG_LVline = UG_LVline()
        underG_MVline = UG_MVline()
        overH_LVline = OH_LVline()
        overH_MVline = OH_MVline()
        # Unpack libraryType
        line_layers = self.set_attributes(underG_LVline,
                                          underG_MVline,
                                          overH_LVline,
                                          overH_MVline,
                                          busesData,
                                          linesID)
        # Update attribute
        for LL in line_layers:
            L = LL._line_type
            dictAttrs = LL.__dict__
            self._lines[L] = {col.strip("_"): vals for (col, vals)
                              in dictAttrs.items()}

        return (underG_LVline, underG_MVline,
                overH_LVline, overH_MVline)

    def set_attributes(self,
                       underG_LVline: Line,
                       underG_MVline: Line,
                       overH_LVline: Line,
                       overH_MVline: Line,
                       busesData: dict[list],
                       linesID: list[str]) -> tuple[Line]:
        """Unpack the data of line layers.

        It gets some SIRDE code "subtipos" and gives them all
        another Manual format name depending on the zone
        voltage level.
        Note: For Underground MV line next attributes are taking
        as typical values:
        _SHIELDING: "CN"
        _NEUTMAT: "CU"
        _NEUTSIZ: "1/0"
        _LINEGEO: It's "None" but it will adopt
                  specific code in the future.
        Note: For Underground LV line next attributes are taking
        as typical values:
        _NEUTMAT: "CU"
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
            # LibraryType
            Ltype = cols[3]
            Ltype = set_Label(Ltype)
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
                    # _NEUTMAT
                    underG_LVline._NEUTMAT.append("CU")
                    # _NOMVOLT
                    nomV = float(cols[5].strip())
                    codenomV = get_NOMVOLT(nomV)
                    underG_LVline._NOMVOLT.append(codenomV)
                    # _X1, _Y1, _X2, _Y2
                    from_bus = cols[0]
                    to_bus = cols[1]
                    (X1, Y1) = loc_buscoord(from_bus, busesData)
                    (X2, Y2) = loc_buscoord(to_bus, busesData)
                    underG_LVline._X1.append(X1)
                    underG_LVline._Y1.append(Y1)
                    underG_LVline._X2.append(X2)
                    underG_LVline._Y2.append(Y2)
                    # _objectID
                    nameID = cols[2]
                    underG_LVline._objectID.append(nameID)
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
                        # [_INSULMAT, _NEUTPER]
                        elif n == 3:
                            attrs = ft.split("_")
                            underG_MVline._INSULMAT.append(attrs[0])
                            underG_MVline._NEUTPER.append(attrs[1])
                    # _NEUTMAT
                    underG_MVline._NEUTMAT.append("CU")
                    # _NEUTSIZ
                    underG_MVline._NEUTSIZ.append("1/0")
                    # _LINEGEO
                    underG_MVline._LINEGEO.append("None")
                    # _SHIELDING
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
                    (X1, Y1) = loc_buscoord(from_bus, busesData)
                    (X2, Y2) = loc_buscoord(to_bus, busesData)
                    underG_MVline._X1.append(X1)
                    underG_MVline._Y1.append(Y1)
                    underG_MVline._X2.append(X2)
                    underG_MVline._Y2.append(Y2)
                    # _objectID
                    nameID = cols[2]
                    underG_MVline._objectID.append(nameID)
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
                    # _NOMVOLT
                    nomV = float(cols[5].strip())
                    codenomV = get_NOMVOLT(nomV)
                    overH_LVline._NOMVOLT.append(codenomV)
                    # _X1, _Y1, _X2, _Y2
                    from_bus = cols[0]
                    to_bus = cols[1]
                    (X1, Y1) = loc_buscoord(from_bus, busesData)
                    (X2, Y2) = loc_buscoord(to_bus, busesData)
                    overH_LVline._X1.append(X1)
                    overH_LVline._Y1.append(Y1)
                    overH_LVline._X2.append(X2)
                    overH_LVline._Y2.append(Y2)
                    # _objectID
                    nameID = cols[2]
                    overH_LVline._objectID.append(nameID)
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
                    # _NOMVOLT
                    nomV = float(cols[5].strip())
                    codenomV = get_NOMVOLT(nomV)
                    overH_MVline._NOMVOLT.append(codenomV)
                    # _X1, _Y1, _X2, _Y2
                    from_bus = cols[0]
                    to_bus = cols[1]
                    (X1, Y1) = loc_buscoord(from_bus, busesData)
                    (X2, Y2) = loc_buscoord(to_bus, busesData)
                    overH_MVline._X1.append(X1)
                    overH_MVline._Y1.append(Y1)
                    overH_MVline._X2.append(X2)
                    overH_MVline._Y2.append(Y2)
                    # _objectID
                    nameID = cols[2]
                    overH_MVline._objectID.append(nameID)
                    # _LENGTH
                    length = float(cols[4].strip())
                    overH_MVline._LENGTH.append(length)

        return (underG_LVline, underG_MVline,
                overH_LVline, overH_MVline)


def get_PHASEDESIG(ph: str, code: int = None) -> int:
    """Phase designation.

    Set the phase code based on the manual either
    Neplan code or Phase letter if `ph` is passed.
    PARAMETERS:
        ph: Phase (A/R, B/S, C/T)
        code: Neplan code

    * --------|---------------*
    |  code   |      ph       |
    *---------|---------------*
    |    3    |  1: C (T)     |
    |    2    |  2: B (S)     |
    |    6    |  3: BC (ST)   |
    |    1    |  4: A (R)     |
    |    5    |  5: AC (RT)   |
    |    4    |  6: AB (RS)   |
    |    0    |  7: ABC (RST) |
    |    7    |  7: ABC (RST) |
    *---------|---------------*
    """

    if code is None:
        if ph == "C" or ph == "T":
            return 1
        elif ph == "B" or ph == "S":
            return 2
        elif ph == "BC" or ph == "ST":
            return 3
        elif ph == "A" or ph == "R":
            return 4
        elif ph == "AC" or ph == "RT":
            return 5
        elif ph == "AB" or ph == "RS":
            return 6
        elif ph == "ABC" or ph == "RST":
            return 7
    else:
        if code == 3:
            return 1
        elif code == 2:
            return 2
        elif code == 6:
            return 3
        elif code == 1:
            return 4
        elif code == 5:
            return 5
        elif code == 4:
            return 6
        elif code == 0 or code == 7:
            return 7


def get_NOMVOLT(nomVLL: float) -> int:
    """Nominal voltage.

    *---------|-----------------|-----------------|----------------*
    |  Code   | Voltage LN [kV] | Voltage LL [kV] |   Connection   |
    *---------|-----------------|-----------------|----------------*
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
    *---------|-----------------|-----------------|----------------*
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
    """
    if nomVLL <= 15:
        return "15"
    elif 15 < nomVLL <= 25:
        return "25"
    elif 25 < nomVLL <= 35:
        return "35"
    elif nomVLL > 35:
        return "45"


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
    for (k, v) in insulvolt.items():
        LibType = LibType.replace(k, v)

    # SUB_
    uunderg = {"SUB": "SUB_"}
    for (k, v) in uunderg.items():
        LibType = LibType.replace(k, v)
    return LibType


def concat_linecols(linesData: dict) -> list[str]:
    """Concatenate columns.

    Resulting shape of a single element
    ['NodeFrom1'&'NodeTo1'&'LibraryType1'&... &'attr1M',
    'NodeFrom2'&'NodeTo2'&'LibraryType2'&... &'attr2M', ...
    ...,
    'NodeFromN'&'NodeToN'&'LibraryTypeN'&... &'attrNM']
    """
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


def loc_buscoord(busname: str,
                 busesData: dict[list]) -> tuple[float]:
    """Localize bus coordinates.

    Given the bus name ID it looks for its
    X, Y coordinates and return them
    as floats in a tuple.
    """
    indx = busesData["Name"].index(busname)
    X = float(busesData["CoordX1"][indx])
    Y = float(busesData["CoordY1"][indx])
    return (X, Y)


def layer2df(layer: dict) -> pd.DataFrame:
    """Convert to pd.DataFrame.

    It gets the layer of certain object as dict
    and returns a DataFrame of pandas.
    Format of the layer:
    overH_MVline = {
        "line_type": "LayerName",
        "objectID": [val1, val2, ..., valN],
        "NEUTMAT": [val1, val2, ..., valN],
        ...,
        "Y2": [val1, val2, ..., valN]
    }
    """
    data = dict()
    for (k, v) in layer.items():
        if type(v) == list:
            if len(v) != 0:
                data[k] = v
    return pd.DataFrame.from_dict(data)


if __name__ == "__main__":
    # Import circuit data
    directory = "./data/Circuito.xlsx"
    cktNeplan = CKTdata()
    cktNeplan.call_data(directory)
    # New QGIS circuit
    cktQgis = CKT_QGIS()
    _ = cktQgis.add_linelayers(cktNeplan._buses, cktNeplan._lines)
    # Turn OH_LVline layer into df
    OH_LVlines_df = layer2df(cktQgis._lines["overH_MVlines"])
    # Show first & last 10 values
    print(OH_LVlines_df.head(10))
    print(OH_LVlines_df.tail(10))
