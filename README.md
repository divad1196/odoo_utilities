# ONS_PRODUCTIVITY_UTILITIES

Le but de ce module est de fournir des utilitaires pour nos développements.
Les outils sont accessibles à travers la variable global Odoo et nécessite souvent un objet `env`

```python
from odoo import ONS
```

Les sous-modules se trouvent dans l'objet ONS



## Debug

Set d'utilitaire servant à débug du code

```python
from odoo.ONS import debug
```

* **print_func_code**: print le code d'une fonction et son héritage (permet de savoir le chemin parcouru par une fonction)

  ```python
  print_func_code(env, model, function)
  ```

  * env: environnement odoo
  * model: string du model, e.g. "sale.order"
  * function: fonction à analyser, e.g. "onchange_partner_id"

* **printTraceBack**: print le chemin parcouru dans Odoo pour arriver à l'endroit où est appelé cette fonction

  ```python
  printTraceBack(printer)
  ```

  * printer: fonction à utiliser pour le display, par défaut utilise "print", on peut lui donner le logger odoo:

    ```python
    printTraceBack(_logger.critical)
    ```

    

* **get_depends_methods**: retourne la liste des dictionnaires keys-function des depends d'un model

  ```python
  for depends in get_onchange_methods(env, model):
      print(x["keys"], x["function"])
  ```

  * env: environnement odoo
  * model: le model dont on veut les depends, e.g. "sale.order"

* **get_onchange_methods**: pareil que get_depends_methods mais pour les onchange

* **analyse_depends**: appel print_func_code sur tous les résultat de  get_depends_methods

  ```python
  analyse_depends(env, model)
  ```

* **analyse_onchange**: appel print_func_code sur tous les résultat de  get_onchange_methods

  ```python
  analyse_onchange(env, model)
  ```



## Records

Set d'utilitaire servant sur les records Odoo.

* **groupby**: sert à regrouper un recordset selon les attributs donnés

  ```python
  groupby(records, attributes)
  ```

  * records: recordset à regrouper
  * attributs: liste de clef de regroupement, les clefs peuvent être:
    * une string de l'attribut voulu, e.g. `"name"`
    * une fonction retournant une clef de regroupement, e.g. `lambda line: line.move_id.sale_line_id.order_id`

  Exemple concrès:

  ```python
  lines = self.mapped("move_line_ids").filtered("result_package_id")
  grouped = ons_groupby(lines, [
      "result_package_id",
      "picking_id",
      lambda line: line.move_id.sale_line_id.order_id,
  ])
  for package, package_data in grouped.items(): 
  	for picking_id, picking_id_data in package_data.items():
  		for sale_id, records in package_data.items():
              print(records)
  ```

  

