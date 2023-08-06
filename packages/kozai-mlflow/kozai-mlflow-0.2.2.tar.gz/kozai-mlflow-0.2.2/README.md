## Build Instructions

Update the version in `src/kozai/mlflow/__init__.py`
`source cloud_keys/config.sh` (or setup your pypi creds manually)
`python -m build`
`python -m twine upload dist/*`