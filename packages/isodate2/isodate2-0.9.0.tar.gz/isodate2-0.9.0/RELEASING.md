# Release Checklist

- [ ] Get `main` to the appropriate code release state.
      [GitHub Actions](https://github.com/isodate/isodate/actions) should be
      running cleanly for all merges to `main`.
      [![GitHub Actions status](https://github.com/isodate/isodate/workflows/Test/badge.svg)](https://github.com/isodate/isodate/actions)

- [ ] Edit release draft, adjust text if needed:
      https://github.com/isodate/isodate/releases

- [ ] Check next tag is correct, amend if needed

- [ ] Publish release

- [ ] Check the tagged
      [GitHub Actions build](https://github.com/isodate/isodate/actions/workflows/deploy.yml)
      has deployed to [PyPI](https://pypi.org/project/isodate2/#history)

- [ ] Check installation:

```bash
pip3 uninstall -y isodate2 && pip3 install -U isodate2
```
