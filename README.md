# OdooTools

Set of tools for Odoo developpement

```python
import OdooTools
```

## Debug

Debug utilities

```python
from odoo.ONS import debug
```

* **print_func_code**: print function code and its inheritance (considering loading order)

  ```python
  print_func_code(env, model, function)
  ```

  * env: odoo environnement
  * model: model _name value, e.g. "sale.order"
  * function: function to analyse, e.g. "onchange_partner_id"

* **printTraceBack**: print the call path up to this function call

  ```python
  printTraceBack(printer)
  ```

  * printer: display function, default is "print", we can use the logger from logging library

    ```python
    printTraceBack(_logger.critical)
    ```

    

* **get_depends_methods**: return a list of dict containing trigger keys and function object of all "api.depends" of a model

  ```python
  for depends in get_onchange_methods(env, model):
      print(x["keys"], x["function"])
  ```

  * env: environnement odoo
  * model: model from which to extract depends methods, e.g. "sale.order"

* **get_onchange_methods**: same as get_depends_methods but for "api.onchange"

* **analyse_depends**: call print_func_code on get_depends_methods result

  ```python
  analyse_depends(env, model)
  ```

* **analyse_onchange**: call print_func_code on get_onchange_methods result

  ```python
  analyse_onchange(env, model)
  ```



## Records

Tools to handle recordset

* **groupby**: group recordset according to list of key (or key getter)

  ```python
  groupby(records, attributes)
  ```

  * records: recordset to group
  * attributes: list of grouping key, that can be either:
    * an object attribute's name as string, e.g. `"name"`
    * a function taking a record and returning the key, e.g. `lambda line: line.move_id.sale_line_id.order_id`

  Example:

  ```python
  lines = self.mapped("move_line_ids").filtered("result_package_id")
  grouped = groupby(lines, [
      "result_package_id",
      "picking_id",
      lambda line: line.move_id.sale_line_id.order_id,
  ])
  for package, package_data in grouped.items(): 
  	for picking_id, picking_id_data in package_data.items():
  		for sale_id, records in package_data.items():
              print(records)
  ```

* **set_fold_groupby**

  ```python
  @api.model
  def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
      res = super(Note, self).read_group(
      	domain, fields, groupby, offset=offset, limit=limit, orderby=orderby, lazy=lazy
      )
      set_fold_groupby(self, res, groupby, groupby_field="ons_stage_id")
  
  	return res
  ```

  


## Datetime

Tools to handle date and datetime.

* **client_specific_to_utc**: There 's some cases where you need to convert a datetime for the write, for example a datetime built from the controller

  ```python
  utc_date = client_specific_to_utc(env, mydate)
  ```

  