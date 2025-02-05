# data-analysis
Personal project used for data profiling, show dov distributions, sample, data, etc.  Exports data to excel for 
analysis and notes.  Was Used as a starting point for Kaggle competitions to look at data and think about features.

Not open for PRs due to this being a personal project.

## Example Output
![Alt text](/docs/data_analysis_example_pic_dov.png)


## Installation
- Package Install
```bash
pip install git+https://github.com/bengrauer/data-analysis.git@main
```
- Script Install / Command Line (still requires virtual env or underlying packages)
```bash
RUN pip install --target $INSTALL_PATH git+https://github.com/bengrauer/data-analysis.git@main --no-dependencies
```

## Usage

- From Package
```python
from data_analysis.analysis import generate_analysis
generate_analysis.run_analysis_routine(file_or_directory="/input_dir/", output_directory="/output_dir/")
```

- From Command Line / Script Install 
```bash
#!/bin/bash
export PTYHONPATH="${PYTHONPATH}:$INSTALL_PATH"
python -m data_analysis --input_file_dir $INPUT_FILE_OR_PATH --output_dir $OUTPUT_FILE_OR_PATH
```

