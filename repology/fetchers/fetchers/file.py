# Copyright (C) 2016-2018 Dmitry Marakasov <amdmi3@amdmi3.ru>
#
# This file is part of repology
#
# repology is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# repology is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with repology.  If not, see <http://www.gnu.org/licenses/>.

import time

from repology.fetchers import ScratchFileFetcher
from repology.fetchers.http import save_http_stream


class FileFetcher(ScratchFileFetcher):
    def __init__(self, url, compression=None, post=None, headers=None, nocache=False, fetch_timeout=60):
        super(FileFetcher, self).__init__(binary=True)

        self.url = url
        self.compression = compression
        self.post = post
        self.headers = headers
        self.fetch_timeout = fetch_timeout

        # cache bypass
        if nocache:
            if '?' in self.url:
                self.url += '&nocache=' + str(int(time.time()))
            else:
                self.url += '?nocache=' + str(int(time.time()))

    def do_fetch(self, statefile, logger):
        fetching_what = [self.url]
        if isinstance(self.post, dict):
            fetching_what.append('{} fields of form data'.format(len(self.post)))
        elif self.post:
            fetching_what.append('{} bytes of post data'.format(len(self.post)))

        if self.headers:
            fetching_what.append('{} extra headers'.format(len(self.headers)))

        logger.Log('fetching ' + ', with '.join(fetching_what))

        save_http_stream(self.url, statefile, compression=self.compression, data=self.post, headers=self.headers, timeout=self.fetch_timeout)

        logger.Log('size is {} byte(s)'.format(statefile.tell()))
