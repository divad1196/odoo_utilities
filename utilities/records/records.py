# -*- coding: utf-8 -*-


def _group_record_by_func(records, func):
    record_by_func = {}
    for rec in records:
        key = func(rec)
        if key in record_by_func:
            record_by_func[key] |= rec
        else:
            record_by_func[key] = rec
    return record_by_func

def _group_record_by_attr(records, attr):
    record_by_attr = {}
    for rec in records:
        key = getattr(rec, attr)
        if key in record_by_attr:
            record_by_attr[key] |= rec
        else:
            record_by_attr[key] = rec
    return record_by_attr

def groupby(records, attributes):
    if isinstance(attributes, (tuple, list)):
        attr = attributes[0]
        attributes = attributes[1:]
    else:
        attr = attributes
        attributes = []

    if callable(attr):
        grouped_records = _group_record_by_func(records, attr)
    else:
        grouped_records = _group_record_by_attr(records, attr)

    if not attributes:
        return grouped_records

    return {
        key: groupby(records, attributes)
        for key, records in grouped_records.items()
    }