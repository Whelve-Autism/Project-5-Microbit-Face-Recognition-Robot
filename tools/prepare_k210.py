"""Prepare a standalone K210 script from the Yahboom face recognition example."""

import argparse
import ast
from pathlib import Path


SIGNATURE_SOURCE = Path(__file__).resolve().parents[1] / "face_signature.py"
TEMPLATE_LIST = "record_ftrs = []"
ENROLMENT = [
    "record_ftrs.append(feature)",
    'print("record_ftrs:%d" % len(record_ftrs))',
    "start_processing = False",
]


def prepare(source, signature_source):
    """Add the project's signature writer at the example's enrolment step."""
    lines = source.splitlines()
    enrolment_steps = [i for i, line in enumerate(lines) if line.strip() == ENROLMENT[0]]
    if lines.count(TEMPLATE_LIST) != 1 or len(enrolment_steps) != 1:
        raise ValueError("Use the original Yahboom 2.8_face_recog.py example.")

    enrolment = enrolment_steps[0]
    indentation = lines[enrolment][:-len(ENROLMENT[0])]
    hook = enrolment + len(ENROLMENT)
    if lines[enrolment:hook] != [indentation + line for line in ENROLMENT]:
        raise ValueError("The enrolment block differs from the supported Yahboom example.")

    lines.insert(hook, indentation + "save_enrolment_signature(signature_records, feature)")
    definitions = [
        "# Project 5 addition: signature recording for the Yahboom K210 example.",
        signature_source.rstrip(),
        "",
        "signature_records = []",
        "",
    ]
    at = lines.index(TEMPLATE_LIST)
    lines[at:at] = definitions
    result = "\n".join(lines) + "\n"
    ast.parse(result, filename="main.py")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("vendor_example", type=Path, help="path to the official 2.8_face_recog.py")
    parser.add_argument("--output", type=Path, default=Path("build/main.py"))
    args = parser.parse_args()

    try:
        source = args.vendor_example.read_text(encoding="utf-8-sig")
        signature_source = SIGNATURE_SOURCE.read_text(encoding="utf-8")
        program = prepare(source, signature_source)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8") as output:
            output.write(program)
    except FileExistsError:
        parser.error("Output already exists. Choose a new output path.")
    except (OSError, ValueError, SyntaxError) as error:
        parser.error(str(error))

    print("Prepared", args.output)


if __name__ == "__main__":
    main()
