import inspect
import re

from astro.sql.table import Table


def process_params(parameters):
    return {k: (v.table_name if type(v) == Table else v) for k, v in parameters.items()}


def _parse_template(sql, python_callable):
    param_types = inspect.signature(python_callable).parameters
    sql = sql.replace("{", "%(").replace("}", ")s")
    all_vals = re.findall("%\(.*?\)s", sql)
    mod_vals = {
        f: f"IDENTIFIER({f})"
        if param_types.get(f[2:-2], None)
        and param_types.get(f[2:-2], None).annotation == Table
        else f
        for f in all_vals
    }
    for k, v in mod_vals.items():
        sql = sql.replace(k, v)
    return sql
