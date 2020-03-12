# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import absolute_import, print_function, unicode_literals

from copy import deepcopy
import glob
import json
import os
import time
from datetime import datetime

from six import text_type

from taskgraph.config import load_graph_config
from taskgraph.util.schema import validate_schema
from taskgraph.util.vcs import calculate_head_rev, get_repo_path, get_repository_type
from taskgraph.util import yaml
from taskgraph.util.memoize import memoize
from taskgraph.util.readonlydict import ReadOnlyDict
from voluptuous import ALLOW_EXTRA, Optional, Required, Schema, Any

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
ROOT = os.path.join(BASE_DIR, "taskcluster", "ci")
MANIFEST_DIR = os.path.join(BASE_DIR, "signing-manifests")


base_schema = Schema(
    {
        Required("url"): text_type,
        Required("bug"): int,
        # XXX flesh out these enums
        Required("signing-product"): Any("firefox", "fenix", "fennec", "thunderbird", "xpi", "mpd001"),
        Required("signing-cert-level"): Any("dep", "nightly", "release"),
        Required("signing-formats"): [Any("gpg", "authenticode")],
        Required("sha256"): text_type,
        Required("filesize"): int,
        Required("requestor"): basestring,
        Required("reason"): basestring,
        Optional("gpg-signature"): basestring,
        Optional("artifact-name"): basestring,
        Required("manifest_name"): basestring,
    }
)


def check_manifest(manifest):
    # XXX add any manifest checks we want.
    # XXX sha256 is a valid sha256?
    # XXX url is a reachable url?
    # XXX bug exists in bugzilla?
    pass


@memoize
def get_manifest():
    manifest_paths = glob.glob(os.path.join(MANIFEST_DIR, "*.yml"))
    all_manifests = []
    for path in manifest_paths:
        rw_manifest = yaml.load_yaml(path)
        rw_manifest["manifest_name"] = os.path.basename(path)
        validate_schema(base_schema, deepcopy(rw_manifest), "Invalid manifest:")
        check_manifest(deepcopy(rw_manifest))
        all_manifests.append(ReadOnlyDict(rw_manifest))
    return tuple(all_manifests)
