# Packaging

```bash
pip3 install build
python3 -m build --sdist
twine upload --repository testpypi dist/*
```
