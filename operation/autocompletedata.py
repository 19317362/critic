# -*- mode: python; encoding: utf-8 -*-
#
# Copyright 2012 Jens Lindström, Opera Software ASA
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License.  You may obtain a copy of
# the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
# License for the specific language governing permissions and limitations under
# the License.

import dbutils

from operation import Operation, OperationResult, OperationError, Optional

class GetAutoCompleteData(Operation):
    def __init__(self):
        Operation.__init__(self, { "values": [set(["users", "paths"])],
                                   "review_id": Optional(int) })

    def process(self, db, user, values, review_id=None):
        cursor = db.cursor()
        data = {}

        if "users" in values:
            cursor.execute("SELECT name, fullname FROM users WHERE status!='retired' ORDER BY name")
            data["users"] = dict(cursor)

        if review_id is not None:
            if "paths" in values:
                cursor.execute("""SELECT fullfilename(file), deleted, inserted
                                    FROM (SELECT file, SUM(deleted) AS deleted, SUM(inserted) AS inserted
                                            FROM reviewfiles
                                           WHERE review=%s
                                        GROUP BY file) AS files""",
                               (review_id,))

                paths = {}

                for filename, deleted, inserted in cursor:
                    paths[filename] = (0, deleted, inserted)

                    components = filename.split("/")
                    for index in range(len(components) - 1, 0, -1):
                        directory = "/".join(components[:index]) + "/"
                        nfiles, current_deleted, current_inserted = paths.get(directory, (0, 0, 0))
                        paths[directory] = nfiles + 1, current_deleted + deleted, current_inserted + inserted

                data["paths"] = paths

        return OperationResult(**data)
