# Course website

Public URL: https://emanuelaboros.github.io/ie-course/

This uses the same GitHub Pages Primer theme and `docs/` structure as USTH-classroom/ml-course, under EmanuelaBoros's own account.

## One-time GitHub Pages setup

In https://github.com/EmanuelaBoros/ie-course/settings/pages select **Deploy from a branch**, branch **main**, folder **/docs**, and save. GitHub builds Jekyll and publishes the site after pushes to main. Check the Actions tab for the Pages build result.

## Editing

- Homepage: `docs/index.md`
- Theme and site URL: `docs/_config.yml`
- Module pages and materials: numbered folders under `docs/`
- Add a notebook before adding its download / GitHub / NBViewer links.
- Keep internal links relative so they work under `/ie-course/`.
- The root README is the original teaching preparation document, not the public homepage.

## Optional local preview

With a supported Ruby installation and Bundler:

```bash
bundle install
bundle exec jekyll serve --source docs --destination _site --baseurl /ie-course
```

Open http://127.0.0.1:4000/ie-course/ .

The original template's MIT notice is retained in `docs/template-license.txt`; it does not relicense other course material.
