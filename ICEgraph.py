import numpy as np
# Network data
from shape import CKTqgis


class Vertex():
    """Vertex mother class.

    Buses, Loads and Transformers are subclasses
    of Vertex each object is labeled with a unique
    string type :py:attr:`graph.Vertex.ICEobjID`.

    It may model any kind of point-like object in the
    network such as a *Model Free Subestation* or *Fuses*,
    with the below priority or ``weight``:

        1. :py:class:`ModelFree_SubEstat`
        2. :py:class:`Transformer`
        3. :py:class:`Regulator`
        4. :py:class:`Load`
        5. :py:class:`Recloser`
        6. :py:class:`Fuse`
        7. :py:class:`PV`
        8. :py:class:`PublicLight`
        9. :py:class:`Bus`
        10. :py:class:`Node`

    Where after *Subestation* the *Transformer*
    is the **heaviest** subset of Vertex.

    """

    def __init__(self,
                 x: float = None,
                 y: float = None,
                 idcode: str = None):
        self.X1 = x
        self.Y1 = y
        self.ICEobjID = idcode

    def __sub__(self, other):
        """Change between vertices.

        Returns a new vertex with no `_idcode` that represents
        the difference of two vertices on each component.

        """
        deltaX = self.X1 - other.X1
        deltaY = self.Y1 - other.Y1
        return Vertex(x=deltaX, y=deltaY)

    def __abs__(self) -> float:
        c = (self.X1**2 + self.Y1**2) ** 0.5
        return c

    def __eq__(self, other) -> bool:
        """Neighboring vertices.

        If coordinates `x` and `y` are in meter, **1cm**
        is good enough distance tolerance to consider
        two vertices the same in spite of their
        subclass or ID :py:attr:`graph.Vertex.ICEobjID`;
        however, ``Neplan`` unit is **km**.

        """
        tol = 1e-3     # 1 meter
        return abs(self - other) < tol

    def __repr__(self) -> str:
        return f"<{self.ICEobjID}>"


class Bus(Vertex):
    pass


class Load(Vertex):
    pass


class LVload(Load):
    pass


class MVload(Load):
    pass


class Transformer(Vertex):
    pass


class Node(Vertex):
    """Ends of lines.

    A :py:class:`Node` would be seen as a subclass of
    :py:class:`Vertex` that represents ends of arbitrary line;
    however, it may also be useful to model internal vertices of a
    polyline (null-injection nodes).

    Note: It is **lightest** kind of Vertex, and they all
    are supposed to be replaced by heavier vertices
    once the whole network is built-up.

    """
    def __init__(self, x, y, idcode):
        super().__init__(x, y, idcode)


class Edge():
    """Edge mother class.

    If Vertex is in *meter* so does the length;
    However, in ``Neplan`` the length attribute
    is in **km** while coordinates in *meter*.
    Each object is labeled with a unique
    string type :py:attr:`graph.Node.ICEobjID`.

    Subclasses of Edges:

        - OH_LVline: Overhead Low Voltage Line.
        - UG_LVline: Underground Low Voltage Line.
        - OH_Servline: Overhead service line.

    All subclasses are heavy the same.

    """
    def __init__(self,
                 from_vertex: Vertex = None,
                 to_vertex: Vertex = None,
                 idcode: str = None):
        self._from_vertex = from_vertex
        self._to_vertex = to_vertex
        self.ICEobjID = idcode

    @property
    def length(self):
        """Length of line.

        It uses the unit of its coordinates [m]; however,
        if data is comming from Neplan is recomended
        so convert the returned value to km
        by multiplying 1e-3.

        """
        d = abs(self._from_vertex - self._to_vertex)
        self._length = d
        return d

    def __repr__(self):
        """Pretty print.

        An edge would be represented in parenthesis
        by the two vertices such edge consists of.

        """
        return f"{self.ICEobjID}: ({self._from_vertex}, {self._to_vertex})"


class Line(Edge):
    pass


class UG_MVline(Line):
    pass


class OH_MVline(Line):
    pass


class UG_LVline(Line):
    pass


class OH_LVline(Line):
    pass


class OH_Servline(Line):
    pass


class CKTgraph():
    """Network.

    It creats intances of each object in the
    circuit so that studies of a network connection
    and topology can be drive.

    The :py:class:`CKTgraph` is fundamentally
    a undirected kind of Graph. After the whole
    network is built up in case a new vertex
    or edge is added or deleted the adjacency matrix
    has to be recalculated by
    calling the property :py:attr:`Graph.adjacency_matrix`.

    The attribute :py:attr:`CKTgraph._odd_bucket` allows
    handling overlap conflicts objects of same weight. It
    stores any object of :py:mod:`graph`
    with some unique key either :py:attr:`Vertex.ICEobjID` or
    :py:attr:`Edge.ICEobjID` in order to retrieve the
    instance itself.

    """
    def __init__(self):
        self._vertices = []
        self._edges = []
        self._odd_bucket = {}

    def add_vertex(self, dotObj: Vertex) -> Vertex:
        """Stores Vertex instance.

        Where parameter ``dotObj`` is instance of Vertex,
        meaning it could be a Vertex class or any subclass
        of it that represents a point-like object. Also
        filters vertex object regarding how heavy they are.

        """
        v = dotObj
        IDname = dotObj.ICEobjID
        hevier_types = (Transformer, Load)
        flyweight_types = (Bus, Node)

        # In case dotObj is a light vertex
        if type(v) == Vertex or isinstance(v, flyweight_types):
            # Assess repeated item
            if v in self._vertices:
                # Get old vertex
                vold = self._vertices[self._vertices.index(v)]
                # Not to add
                if isinstance(vold, hevier_types) or isinstance(vold, Bus):
                    return v
                # Update Node
                elif isinstance(vold, Node):
                    self._vertices.remove(vold)
                    self._vertices.append(v)
                    return v
                # Replace old vertex by bus
                elif type(vold) == Vertex and isinstance(v, Bus):
                    self._vertices.remove(vold)
                    self._vertices.append(v)
                    return v
                else:
                    return v

            # Add unique flyweight vertex
            else:
                self._vertices.append(v)
                return v

        # In case dotObj is a heavy vertex
        elif isinstance(v, (Transformer, Load)):
            # Assess repeated item
            if v in self._vertices:
                # Get old vertex
                vold = self._vertices[self._vertices.index(v)]
                # Override old flyweight vertex
                if type(vold) == Vertex or isinstance(vold, flyweight_types):
                    self._vertices.remove(vold)
                    self._vertices.append(v)
                    return v
                # Assess overlap of two heavy vertices
                else:
                    try:
                        if isinstance(vold, (Transformer, Load)):
                            raise Exception("SameSpot")
                    except Exception as e:
                        # print(f"{e}: {v} over {vold}")
                        if isinstance(v, Transformer):
                            self._vertices.remove(vold)
                            self._vertices.append(v)
                            print(f"{v} overrode {vold}")
                            return v
                        else:
                            # print(f"Load {v} not added.")
                            self._odd_bucket[IDname] = v
                            return v
            # Add unique heavy vertex
            else:
                self._vertices.append(v)
                return v

    def add_edge(self, chainObj: Edge) -> Edge:
        """Stores Edge instance.

        Where parameter `chainObj` is instance of
        Edge, meaning it could be an Edge or any subclass
        of it that represents a chain-like object;
        Also, replaces the ends :py:class:`Node` by
        a heavier vertex subclass at same spot.
        Conflicts like loops, bridge or parallel lines
        may be filter and report here.

        """
        x1 = chainObj.X1
        y1 = chainObj.Y1
        x2 = chainObj.X2
        y2 = chainObj.Y2
        from_node = Node(x1, y1, idcode=None)
        to_node = Node(x2, y2, idcode=None)
        # Update from_node
        if from_node in self._vertices:
            from_node = self._vertices[self._vertices.index(from_node)]
        # Add to vertices otherwise
        else:
            self._vertices.append(from_node)
        # Update to_node
        if to_node in self._vertices:
            to_node = self._vertices[self._vertices.index(to_node)]
        # Add to vertices otherwise
        else:
            self._vertices.append(to_node)

        # Creat new attributes
        chainObj._from_vertex = from_node
        chainObj._to_vertex = to_node

        self._edges.append(chainObj)
        return chainObj

    def add_buses(self, cktQgis: CKTqgis) -> None:
        """Buses intances.

        Treats all buses in the network the same weight;
        in spite of the layer they belong to.

        """
        OHMVbus_data = cktQgis._buses["overH_MVbuses"]
        OHLVbus_data = cktQgis._buses["overH_LVbuses"]
        UGMVbus_data = cktQgis._buses["underG_MVbuses"]
        UGLVbus_data = cktQgis._buses["underG_LVbuses"]
        busLayers = [OHMVbus_data, OHLVbus_data,
                     UGMVbus_data, UGLVbus_data]
        for layer in busLayers:
            Nbuses = len(layer["ICEobjID"])
            attrs = []
            # Gather known attributes only
            for k, v in layer.items():
                if isinstance(v, list) and len(v) != 0:
                    attrs.append(k)
            # Set such attributes
            for b in range(Nbuses):
                bus = Bus()
                for ft in attrs:
                    val = layer[ft][b]
                    setattr(bus, ft, val)
                _ = self.add_vertex(bus)

    def add_loads(self, cktQgis: CKTqgis) -> None:
        """Loads intances.

        Creats either Low Voltage Load (LV_load)
        or Medium Voltage Load (MV_load) vertex objects with
        regard to the subset they belong to.

        """
        lvloads_data = cktQgis._LVloads["LV_load"]
        mvloads_data = cktQgis._MVloads["MV_load"]
        loads_layers = [lvloads_data, mvloads_data]
        for layer in loads_layers:
            lenLoad = len(layer["ICEobjID"])
            if lenLoad == 0:
                continue
            attrs = []
            # Gather known attributes only
            for k, v in layer.items():
                if isinstance(v, list) and len(v) != 0:
                    attrs.append(k)
            # Set attributes for each layer
            for i in range(lenLoad):
                if layer["load_layer"] == "LV_load":
                    load = LVload()
                elif layer["load_layer"] == "MV_load":
                    load = MVload()
                for ft in attrs:
                    val = layer[ft][i]
                    setattr(load, ft, val)
                _ = self.add_vertex(load)

    def add_transformers(self, cktQgis: CKTqgis) -> None:
        """Static machine instances.

        Fundamentally any subset of static machine, including
        Model Free SubEstation, AutoTransformer among others.
        These subsets are usually treated as the heaviests
        sort of vertices meaning difficult to replace or override.

        """
        tx_data = cktQgis._transformers["Distribution_transformers"]
        NTx = len(tx_data["ICEobjID"])
        attrs = []
        # Gather known attributes only
        for k, v in tx_data.items():
            if isinstance(v, list) and len(v) != 0:
                attrs.append(k)
        # Set such attributes
        for i in range(NTx):
            tx = Transformer()
            for ft in attrs:
                val = tx_data[ft][i]
                setattr(tx, ft, val)
            _ = self.add_vertex(tx)

    def add_lines(self, cktQgis: CKTqgis) -> None:
        """Lines instances.

        Creats chain-like objects with
        regard to the Edge subset they belong to.
        If :py:func:`graph.ends` is called only the extremes
        and the net length between them is consider in order
        to avoid polylines.

        """

        def ends(namesID: list, lineslen: list) -> tuple[dict]:
            """External vertices only."""

            lines = {}
            for n, name in enumerate(namesID):
                objID, _ = name.split("__")
                if n == 0:
                    lines[objID] = [n]
                    prevID = objID
                    continue
                # Not to consider if objID still the same
                elif prevID == objID:
                    continue
                else:
                    # Add previous index to previous key
                    lines[prevID].append(n-1)
                    # New key: Initialize list with last index
                    lines[objID] = [n]
                    prevID = objID
                    continue
            linelen = {}
            for nameID, ij in lines.items():
                # Add up net polyline length
                if len(ij) == 2:
                    i, j = ij
                    n = j + 1
                    linelen[nameID] = sum(lineslen[i:n])
                # Single line
                else:
                    i = ij[0]
                    linelen[nameID] = lineslen[i]
            return lines, linelen

        UGMVline_data = cktQgis._lines["underG_MVlines"]
        OHMVline_data = cktQgis._lines["overH_MVlines"]
        UGLVline_data = cktQgis._lines["underG_LVlines"]
        OHLVline_data = cktQgis._lines["overH_LVlines"]
        Servline_data = cktQgis._lines["service_LVlines"]
        lineLayers = [UGMVline_data, OHMVline_data,
                      UGLVline_data, OHLVline_data,
                      Servline_data]
        for layer in lineLayers:
            IDends, lineLen = ends(layer["ICEobjID"], layer["LENGTH"])
            attrs = []
            # Gather known attributes only
            for k, v in layer.items():
                if isinstance(v, list) and len(v) != 0:
                    attrs.append(k)
            # Only for complete lines
            for nameID, ij in IDends.items():
                # Single line index
                if len(ij) == 1:
                    i = ij[0]
                    j = i
                # Ends of polyline index
                else:
                    i, j = ij
                # Instance with regard to subclass of line
                if layer["line_layer"] == "underG_MVlines":
                    line = UG_MVline()
                elif layer["line_layer"] == "underG_LVlines":
                    line = UG_LVline()
                elif layer["line_layer"] == "overH_MVlines":
                    line = OH_MVline()
                elif layer["line_layer"] == "overH_LVlines":
                    line = OH_LVline()
                elif layer["line_layer"] == "service_LVlines":
                    line = OH_Servline()
                # Set known attributes only
                for ft in attrs:
                    val_i = layer[ft][i]
                    val_j = layer[ft][j]
                    if ft == "X2":
                        setattr(line, ft, val_j)
                    elif ft == "Y2":
                        setattr(line, ft, val_j)
                    elif ft == "LENGTH":
                        setattr(line, ft, lineLen[nameID])
                    else:
                        setattr(line, ft, val_i)
                _ = self.add_edge(line)

    def adjacency_dict(self) -> dict:
        """Adjacent vertices in a edge.

        Returns the adjacency list vertex
        representation of the graph.

        Note: For undirected graph only.

        """
        adj = {vertex.ICEobjID: [] for vertex in self._vertices}
        for e in self._edges:
            from_v = e._from_vertex
            to_v = e._to_vertex
            adj[from_v.ICEobjID].append(to_v)
            adj[to_v.ICEobjID].append(from_v)

        return adj

    @property
    def adjacency_matrix(self) -> np.array:
        """Number of adjacent edges.

        Returns the adjacency matrix of the graph.
        Assumes that the attribute :py:attr:`Graph._vertices`
        is equivalent to the :py:func:`range` so that
        indexation can be used and at the same time respect
        isomorphism; furthermore, it creats
        the attribute :py:attr:`CKTgraph._adj_matrix`.

        """
        n_V = len(self._vertices)
        Adj = np.zeros((n_V, n_V), dtype=int)
        for e in self._edges:
            from_v = e._from_vertex
            to_v = e._to_vertex
            # Modify specific element of matrix
            i = self._vertices.index(from_v)
            j = self._vertices.index(to_v)
            Adj[i, j] += 1
            Adj[j, i] += 1

        self._adj_matrix = Adj
        return Adj
