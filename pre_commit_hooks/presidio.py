from typing import List, Sequence
from typing import Optional
from typing import Sequence
from presidio_analyzer import AnalyzerEngine
from enum import Enum
from termcolor import colored
import sys
import argparse
import yaml


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    parser.add_argument('--config', dest="config", help="The presidio configuration")
    args = parser.parse_args(argv)

    # Set up the engine, loads the NLP module (spaCy model by default)
    # and other PII recognizers
    analyzer = AnalyzerEngine()

    all_results = []

    returnValue = 0
    language = "en"
    entities = ["PHONE_NUMBER"]

    if args.config:
        try:
            with open(args.config) as config:
                config_data = yaml.load(config, yaml.FullLoader)
                language = config_data["language"]
                entities = config_data["entities"]
        except Exception as e:
            print(colored(f'Presidio config file not found at {args.config}. Using defaults', 'yellow', attrs=['bold']))
            print()

    for filename in args.filenames:
        with open(filename) as f:
            text = f.read()
            results = analyzer.analyze(text=text, entities=entities, language=language)
            if len(results) > 0:
                all_results.append(dict(filename=filename, results=results))

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
