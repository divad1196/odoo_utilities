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






def set_fold_groupby(self, res, groupby, groupby_field, undefined_default=False):
    # Ensure that this is a list
    if isinstance(groupby, str):
        groupby = [groupby]
    if groupby and groupby[0] == groupby_field:
        field = getattr(type(self), groupby_field, None)
        comodel_name = (
            field and
            getattr(field, "relational", None) and
            getattr(field, "comodel_name", None)
        )
        if not comodel_name:
            return
        # Nb: order is preserved and undefined is False
        group_ids = self.env[comodel_name].browse([
            g[groupby_field] and g[groupby_field][0]
            for g in res
        ])
        # We might get something like: "comodel_name(2, 3, 4, False)" which is valid
        for index, group_id in enumerate(group_ids):
            res[index]["__fold"] = group_id.fold if group_id.id else undefined_default 