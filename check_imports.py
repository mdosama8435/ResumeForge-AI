import sys
import os
import importlib

sys.path.append(os.path.abspath('.'))

errors = []
for root, dirs, files in os.walk('.'):
    if not (root.startswith('.\\src') or root.startswith('.\\pages') or root.startswith('.\\frontend') or root == '.\\app.py'):
        continue
    for f in files:
        if f.endswith('.py') and not f.startswith('__'):
            path = os.path.join(root, f)
            mod_name = path[2:-3].replace('\\', '.')
            try:
                importlib.import_module(mod_name)
            except Exception as e:
                errors.append(f"{mod_name}: {type(e).__name__}: {str(e)}")

for e in errors:
    print("ERROR:", e)
