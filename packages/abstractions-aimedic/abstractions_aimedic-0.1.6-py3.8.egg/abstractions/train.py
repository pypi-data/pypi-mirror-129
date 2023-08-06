import argparse
from pathlib import Path
import os
from abstractions import Orchestrator
from abstractions.orchestration import MLFLOW_TRACKING_URI, EVAL_REPORTS_DIR


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--run_name',
                        type=str,
                        help='name of the folder which contains config file',
                        required=True)

    parser.add_argument('--data_dir',
                        type=str,
                        help='absolute path to directory of the dataset',
                        required=True)

    return parser.parse_args()


def main():
    args = parse_args()

    data_dir = Path(args.data_dir)
    run_name = str(args.run_name)
    # project_root = Path(args.project_root)
    project_root = Path(__file__).parent.parent

    mlflow_tracking_uri = os.getenv('MLFLOW_TRACKING_URI')
    if mlflow_tracking_uri is None:
        mlflow_tracking_uri = MLFLOW_TRACKING_URI
    else:
        mlflow_tracking_uri = Path(mlflow_tracking_uri)

    eval_reports_dir = os.getenv('EVAL_REPORTS_DIR')
    if eval_reports_dir is None:
        eval_reports_dir = EVAL_REPORTS_DIR
    else:
        eval_reports_dir = Path(eval_reports_dir)

    orchestrator = Orchestrator(run_name=run_name,
                                data_dir=data_dir,
                                project_root=project_root,
                                eval_reports_dir=eval_reports_dir,
                                mlflow_tracking_uri=mlflow_tracking_uri)
    orchestrator.run()


def cmd():
    args = parse_args()
    print('hello from main!')
    print(args.__dict__)


if __name__ == '__main__':
    main()
