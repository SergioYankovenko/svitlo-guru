# svitlo.guru publication

This repository publishes the existing public website from
[SergioYankovenko/svitlo](https://github.com/SergioYankovenko/svitlo) at
https://svitlo.guru/. The original website and installed web apps keep their
existing origin at https://sergioyankovenko.github.io/svitlo/.

The workflow copies only the published website, app, assets, downloads and
update manifest. It adjusts the landing page's absolute URLs for the new domain.
It does not build or modify the app, change its API URL, or deploy any backend.

GitHub Actions checks the original main branch every 15 minutes. Scheduled runs
skip publication when the deployed source and publication pipeline are unchanged.
Use Actions → Publish svitlo.guru → Run workflow for an immediate refresh.
`deployment-source.json` records both source and publication commit hashes.

GitHub Pages must use GitHub Actions as its source and `svitlo.guru` as its custom
domain. Both websites use the existing Supabase project. Its allowed origins
include the original GitHub Pages origin and the new domain; existing keys,
database records, API endpoints and notification subscriptions are preserved.
