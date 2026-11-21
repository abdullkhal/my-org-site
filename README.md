# PIIK Kenya

An independent static property verification and intelligence site. The four primary services are PIIK Check, PIIK Directory, PIIK Weekly and PIIK Watch. The Knowledge Centre contains practical guides, including buying property from overseas.

## Develop and test

Use the existing isolated checkout at `/workspace/my-org-site`. Run the server in a persistent terminal.

```sh
python3 -m http.server 3000 --bind 0.0.0.0
```

There is no dependency installation for serving the site. The browser checks use Node.js, Playwright and Chromium. The cloud provides all three. The environment variables `PIIK_TEST_URL`, `PIIK_CHROMIUM` and `PIIK_TEST_OUTPUT` override the defaults. Set `PIIK_AXE_PATH` to an installed axe-core script to run the accessibility audit.

```sh
python3 scripts/build-site.py --check
python3 scripts/check-links.py
python3 scripts/render-source-review.py --check
python3 -m unittest discover -s tests -p 'test_*.py'
node --check app.js
node --check editorial.js
node tests/site.cjs
node tests/imagery.cjs
node tests/phase2.cjs
node tests/review-links.cjs
node tests/official-hub.cjs
node tests/integration-preparation.cjs
```

## Maintain and publish

Edit source templates in `site/` and reviewed content in `data/`. Regenerate the site and sitemap with `python3 scripts/build-site.py`. For changes to the verification register, also run `python3 scripts/render-source-review.py`. Commit the inputs and the generated output together. See [editorial operations](docs/editorial-operations.md) for data review, automation, publication and rollback.

The public site uses no analytics, payment service, registration or enquiry endpoint. Keep credentials, customer records and sensitive editorial drafts outside this public repository. The disabled prototypes and QA fixtures are for synthetic data only.

Generate a local review ZIP with `python3 scripts/package-preview.py /tmp/piik-preview`. The previous design remains available in Git history at `f441124606e73e1ee44197981236fc130ce3957d`. Editorial image source notes are in [the image credits](credits.html).
