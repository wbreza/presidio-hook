from typing import List, Sequence
from typing import Optional
from typing import Sequence
from presidio_analyzer import AnalyzerEngine
from enum import Enum
from termcolor import colored
from globmatch import glob_match
import sys
import argparse
import yaml


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'filenames',
        nargs='*',
        help="Filenames pre-commit believes are changed"
    )
    parser.add_argument(
        '--config',
        dest="config",
        default="./presidio.yaml",
        help="The presidio configuration"
    )
    args = parser.parse_args(argv)

    returnValue = 0
    config_data = {}

    if args.config is not None:
        try:
            with open(args.config) as config:
                config_data = yaml.load(config, yaml.FullLoader)
                print(colored(f'Using Presidio config from from {args.config}', 'cyan'))
        except:
            print(colored(f'Presidio config file not found at {args.config}. Using defaults', 'yellow', attrs=['bold']))
            print()
    else:
        print(colored(f'Presidio config file not set. Using defaults', 'yellow', attrs=['bold']))
        print()

    config = {
        "language": config_data["language"] or "en",
        "entities": config_data["entities"] or [],
        "ignore": config_data["ignore"] or [],
    }

    # Set up the engine, loads the NLP module (spaCy model by default)
    # and other PII recognizers
    analyzer = AnalyzerEngine()
    all_results = []

    for filename in args.filenames:
        try:
            with open(filename) as f:
                if not glob_match(filename, config["ignore"]):
                    text = f.read()
                    results = analyzer.analyze(text=text, entities=config["entities"], language=config["language"])
                    if len(results) > 0:
                        all_results.append(dict(filename=filename, results=results))
        except Exception as e:
            print(colored(f'Error analyzing {filename} for sensitive data. Error: {e}', 'red'))

    if len(all_results) > 0:
        returnValue = 1
        print_results(all_results)

    return returnValue


def print_results(results: List) -> None:
    print(colored('ERROR: Potential sensitive data about to be committed to git repo!', 'red'))

    for fileResult in results:
        print(colored(f'file: {fileResult["filename"]}', 'cyan', attrs=["bold"]))
        for result in fileResult["results"]:
            print(colored(f' - {result}', 'magenta'))


if __name__ == '__main__':
    raise sys.exit(main())
