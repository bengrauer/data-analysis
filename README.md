# data-analysis
Simple package that performs data profiling and exports to excel for easy viewing and analysis

 Designed for quicker exploratory of datasets from Kaggle.

## Installation
```bash
pip install data-analysis
git clone --depth 1 -b $GITHUB_BRANCH $GITHUB_REPO /tmp/$GITHUB_PACKAGE
```

## Usage

- Package Install
```python
from data_analysis.analysis import generate_analysis
generate_analysis.run_analysis_routine('//fullpath/file_or_path')
```

- Script Install
```bash
#!/bin/bash
export PTYHONPATH="${PYTHONPATH}:$INSTALL_PATH"
python -m data_analysis $FILE_OR_PATH
```

