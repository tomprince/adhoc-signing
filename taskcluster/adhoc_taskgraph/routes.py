# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import absolute_import, print_function, unicode_literals

import time

from taskgraph.transforms.task import index_builder

SIGNING_ROUTE_TEMPLATES = [
    "index.{trust-domain}.v2.{project}.{name}.{build_date}.latest",
    "index.{trust-domain}.v2.{project}.{name}.latest",
]


def add_signing_indexes(config, task):
    routes = task.setdefault("routes", [])

    if config.params["level"] != "3":
        return task

    subs = config.params.copy()
    subs["build_date"] = time.strftime(
        "%Y.%m.%d", time.gmtime(config.params["build_date"])
    )
    subs["trust-domain"] = config.graph_config["trust-domain"]
    manifest_name =  task.get("extra", {}).get("manifest-name")
    if manifest_name:
        subs["name"] = manifest_name
        for tpl in SIGNING_ROUTE_TEMPLATES:
            routes.append(tpl.format(**subs))
    return task


@index_builder("signing")
def add_release_signing_indexes(config, task):
    return add_signing_indexes(config, task)
