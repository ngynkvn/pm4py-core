from pm4py.objects.ocel.obj import OCEL
from typing import Optional, Dict, Any
from pm4py.util import pandas_utils


def apply(ocel: OCEL, parameters: Optional[Dict[Any, Any]] = None):
    """
    Feature: assigns to each event the number of related objects per object type.
    If N different object types are present in the log, then N different columns are created.

    Parameters
    ----------------
    ocel
        OCEL
    parameters
        Parameters of the algorithm

    Returns
    ----------------
    data
        Extracted feature values
    feature_names
        Feature names
    """
    if parameters is None:
        parameters = {}

    ordered_events = parameters["ordered_events"] if "ordered_events" in parameters else ocel.events[
        ocel.event_id_column].to_numpy()

    rel_objs = ocel.relations.groupby(ocel.event_id_column)[ocel.object_id_column].agg(list).to_dict()

    object_types = pandas_utils.format_unique(ocel.objects[ocel.object_type_column].unique())

    object_type_association = ocel.objects[[ocel.object_id_column, ocel.object_type_column]].to_dict("records")
    object_type_association = {x[ocel.object_id_column]: x[ocel.object_type_column] for x in object_type_association}

    data = []
    feature_names = ["@@event_num_rel_objs_type_"+ot for ot in object_types]

    for ev in ordered_events:
        data.append([])
        for ot in object_types:
            rel_objs_ot = {x for x in rel_objs[ev] if object_type_association[x] == ot}
            data[-1].append(len(rel_objs_ot))

    return data, feature_names
