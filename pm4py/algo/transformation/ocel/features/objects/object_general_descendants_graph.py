from pm4py.objects.ocel.obj import OCEL
from typing import Optional, Dict, Any
from pm4py.algo.transformation.ocel.graphs import object_descendants_graph


def apply(ocel: OCEL, parameters: Optional[Dict[Any, Any]] = None):
    """
    Adds for each object the number of descendants as feature

    Parameters
    -----------------
    ocel
        OCEL
    parameters
        Parameters of the algorithm

    Returns
    -----------------
    data
        Values of the added features
    feature_names
        Names of the added features
    """
    if parameters is None:
        parameters = {}

    ordered_objects = parameters["ordered_objects"] if "ordered_objects" in parameters else ocel.objects[
        ocel.object_id_column].to_numpy()

    g0 = object_descendants_graph.apply(ocel, parameters=parameters)

    data = []
    feature_names = ["@@object_general_descendants_graph_ascendants", "@@object_general_descendants_graph_descendants"]

    ascendants = {}
    descendants = {}

    for obj in ordered_objects:
        ascendants[obj] = []
        descendants[obj] = []
    for el in g0:
        descendants[el[0]].append(el[1])
        ascendants[el[1]].append(el[0])

    for obj in ordered_objects:
        data.append([len(ascendants[obj]), len(descendants[obj])])

    return data, feature_names
