from dataclasses import dataclass
from typing import List

import yaml
from jsonschema import validate
from yaml import safe_load, safe_load_all

with open("metrics_schema.yaml") as f:
    METRICS_SCHEMA = safe_load(f)

@dataclass
class Link:
    description: str
    url: str

@dataclass
class Metric:
    """Base class for metrics."""

    name: str
    type: str
    description: str
    features: List[str]
    links: List[Link]
    known_issues_md: str
    derived_metrics_md: str
    other_notes_md: str


@dataclass
class LegacyProbe(Metric):
    expiry_version: str


@dataclass
class GleanMetric(Metric):
    expires: str
    disabled: bool
    send_in_pings: List[str]

    @classmethod
    def from_file(cls, filepath):
        with open(filepath) as f:
            documents = f.read().split("\n---")
        if len(documents) != 5:
            raise IOError(f"Expected 5 documents, but found {len(documents)}!")
        data = {}
        data.update(safe_load(documents[0]))
        data.update(safe_load(documents[1]))
        return GleanMetric(
            **data,
            known_issues_md=documents[2],
            derived_metrics_md=documents[3],
            other_notes_md=documents[4]
        )


def main():
    metric = GleanMetric.from_file("metrics/firefox_desktop/about_page.libraries_tapped.yaml")
    print(metric)
    # documents = safe_load_all(f)
    # data = next(documents)
    # validate(instance=data, schema=METRICS_SCHEMA)
    # data["behavior"] = next(documents)


if __name__ == "__main__":
    main()
