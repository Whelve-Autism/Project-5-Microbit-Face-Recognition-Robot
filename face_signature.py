"""Summarise an enrolled K210 feature vector as a local 64-bit signature."""


def feature_signature(feature):
    """Fold the signs of the coefficients into 64 bits."""
    bits = 0
    for position, coefficient in enumerate(feature):
        if coefficient >= 0:
            bits |= 1 << (position % 64)
    return bits


def save_enrolment_signature(records, feature, path="data.txt"):
    """Append a signature and write the current session's signatures."""
    records.append(feature_signature(feature))
    with open(path, "w") as output:
        output.write(str(records))
