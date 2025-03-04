import sys
from data_analysis.analysis import generate_analysis
from data_analysis.utility.run_settings import RunSettings, RunType, EnvRun

if __name__ == '__main__':
    run_settings = RunSettings(
        run_type=RunType.PYTHON,
        env_run=EnvRun.LOCAL,
        input_dir=sys.argv[1],
        output_dir=sys.argv[2]
    )
    generate_analysis.run_analysis_routine_local_csv(run_settings=run_settings)