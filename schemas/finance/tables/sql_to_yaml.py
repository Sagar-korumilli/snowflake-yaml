import os
import re
import yaml
from collections import defaultdict

# Pattern to detect start of an object (CREATE/ALTER + optional OR REPLACE)
OBJECT_START_PATTERN = re.compile(
    r"""
    ^\s*
    (?P<action>CREATE|ALTER)               # Action
    (?:\s+OR\s+REPLACE)?                   # Optional OR REPLACE
    \s+
    (?P<object_type>TABLE|VIEW|PROCEDURE|FUNCTION|SEQUENCE)
    \s+
    (?P<full_name>[A-Za-z0-9_\.]+)         # schema.object
    """,
    re.IGNORECASE | re.MULTILINE | re.VERBOSE
)

def strip_comments(sql_text):
    # Remove any line that starts with "--"
    lines = sql_text.splitlines()
    return "\n".join(line for line in lines if not line.lstrip().startswith("--"))

def split_sql_objects(clean_sql):
    # find start positions
    starts = [m.start() for m in OBJECT_START_PATTERN.finditer(clean_sql)]
    if not starts:
        return []
    starts.append(len(clean_sql))
    chunks = []
    for i in range(len(starts)-1):
        chunk = clean_sql[starts[i]:starts[i+1]].strip()
        if chunk:
            chunks.append(chunk)
    return chunks

def extract_info(stmt):
    m = OBJECT_START_PATTERN.search(stmt)
    if not m:
        return None
    action = m.group("action").upper()
    obj_type = m.group("object_type").capitalize()
    full_name = m.group("full_name")
    if "." in full_name:
        schema, name = full_name.split(".", 1)
    else:
        schema, name = "Unknown", full_name
    return schema, name, obj_type, "New" if action == "CREATE" else "Alter"

def determine_version(versions, key, action):
    if action == "New":
        versions[key] = 1.0
    else:
        versions[key] += 0.1
    v = versions[key]
    return str(int(v)) if v.is_integer() else f"{v:.1f}"

def process_sql_file(path, versions):
    raw = open(path).read()
    clean = strip_comments(raw)
    stmts = split_sql_objects(clean)
    out = []
    for stmt in stmts:
        info = extract_info(stmt)
        if not info: 
            continue
        schema, name, typ, act = info
        key = f"{schema}.{name}"
        ver = determine_version(versions, key, act)
        out.append({
            "Schema": schema,
            "ObjectName": name,
            "ObjectType": typ,
            "Action": act,
            "Version": ver,
            "custom_TSQL": stmt
        })
    return out

def write_yaml(data, dest):
    if not data:
        print("⚠️ No objects parsed; skipping YAML.")
        return
    with open(dest, "w") as f:
        yaml.dump(data, f, sort_keys=False, default_flow_style=False)
    print(f"✅ Wrote {dest}")

if __name__ == "__main__":
    folder = "."  # change to your SQL folder
    versions = defaultdict(float)
    for fn in os.listdir(folder):
        if fn.lower().endswith(".sql"):
            sql_path = os.path.join(folder, fn)
            yaml_path = os.path.splitext(sql_path)[0] + ".yaml"
            parsed = process_sql_file(sql_path, versions)
            write_yaml(parsed, yaml_path)
