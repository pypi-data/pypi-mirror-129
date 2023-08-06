# Quality LAC Data Reference - Local Authority Data

This is a redistribution of the ONS dataset on **Lower Tier Local Authority to
Upper Tier Local Authority (April 2021) Lookup in England and Wales** shaped 
to be used in the Quality Lac Data project.

This repository contains pypi and npm distributions of
subsets of this dataset as well as the scripts to
generate them from source.

Source: Office for National Statistics licensed under the Open Government Licence v.3.0

Read more about this dataset here:

* https://geoportal.statistics.gov.uk/datasets/ons::lower-tier-local-authority-to-upper-tier-local-authority-april-2021-lookup-in-england-and-wales/about

## Regular updates

When a new authority distribution is available, download it and add it to the source folder and
at the same time delete the existing file from this location. There can only be one file
in the source folder at a time.

After updating the sources, run the script found in `bin/generate-output-files.py` to 
regenerate the output file.

Commit everything to GitHub. If ready to make a release, make sure to update the version in 
[pyproject.toml](./pyproject.toml), push to GitHub and then create a GitHub release. The 
[GitHub Action](.github/workflows/python-publish.yml) will then create the distribution files and
upload to [PyPI][pypi].

Release naming should follow a pseudo-[semantic versioning][semver] format:
`<YEAR>.<MONTH>.<PATCH>`. Alpha and beta releases can be flagged by appending 
`-alpha.<number>` and `-beta.<number>`. 

For example, the April 2021 release is named [2021.4][2021.4] with the associated tag [v2021.4][tag-v2021.4].

[pypi]: https://pypi.org/project/quality-lac-data-ref-authorities/
[semver]: https://semver.org/
[2021.4]: https://github.com/SocialFinanceDigitalLabs/quality-lac-data-ref-authorities/releases/tag/v2021.4
[tag-v2021.4]: https://github.com/SocialFinanceDigitalLabs/quality-lac-data-ref-authorities/tree/v2021.4
