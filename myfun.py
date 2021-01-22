from jsonschema import validate
from yaml import safe_load, safe_load_all

with open("metrics_schema.yaml") as f:
    METRICS_SCHEMA = safe_load(f)

with open("metrics/firefox_desktop/total_uri_count.yaml") as f:
    documents = safe_load_all(f)
    data = next(documents)
    validate(instance=data, schema=METRICS_SCHEMA)
    data["behavior"] = next(documents)

print(data)
