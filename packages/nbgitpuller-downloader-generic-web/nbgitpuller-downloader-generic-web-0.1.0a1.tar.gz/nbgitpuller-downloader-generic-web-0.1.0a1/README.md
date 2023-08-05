# nbgitpuller - generic web download plugin

This plugin is used by nbgitpuller to download archives
from any publicly available URL.

This plugin expects the Dropbox URL included in the nbgitpuller link to look like this:
- https://www.example.com/materials-sp20-external.zip

In this plugin, there is no special handling of the URL so it must point directly to
the archive and the archive must by accessible to anyone with the link.

## Installation

```shell
python3 -m pip install nbgitpuller-downloader-generic-web
```


