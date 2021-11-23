from typing import Sequence


from typing import Optional
from typing import Sequence
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
import argparse
import en_core_web_lg

def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)

    # Set up the engine, loads the NLP module (spaCy model by default) 
    # and other PII recognizers
    en_core_web_lg.load()
    analyzer = AnalyzerEngine()

    text="My phone number is 212-555-5555"

    results = analyzer.analyze(text=text,
                           entities=["PHONE_NUMBER"],
                           language='en')
    print(results)

    return 0

if __name__ == '__main__':
    raise SystemExit(main())