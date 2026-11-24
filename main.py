"""The Worst App Idea Ever Pitched entry.

Writes one sentence (at most 240 characters) pitching the worst, most
useless app imaginable to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output/entry.txt). Pure stdlib; deterministic.
"""

import os
import sys

# Why this pitch targets the judge's criteria (in order):
# 1. Names a specific app (NapCast) and what it uselessly does: livestreams
#    naps, ranks snoring, texts your boss a drool highlight reel.
# 2. Funny through absurd logic and deadpan confidence: a premium subscription
#    for a problem nobody has, pitched like a real founder means every word.
# 3. Sounds like a real pitch: product name, price ($10-a-month), features,
#    and an audience (nappers, their bosses).
# 4. One clean sentence, 191 of 240 characters, no padding, no second idea.
# 5. Vivid and specific: 4K nap livestreams, a snoring leaderboard, a drool
#    highlight reel sent to your boss.
PITCH = (
    "NapCast is a $10-a-month app that livestreams your naps in 4K to "
    "strangers, ranks your snoring on a global leaderboard, and texts your "
    "boss a highlight reel every time you drool on the couch."
)


def check_pitch(text):
    """Self-check gates; return a list of failures (empty means pass)."""
    failures = []
    if not text:
        failures.append("empty pitch")
    if text != text.strip():
        failures.append("leading or trailing whitespace")
    if not (1 <= len(text) <= 240):
        failures.append("length %d not in 1..240" % len(text))
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in text):
        failures.append("control characters present")
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        failures.append("not UTF-8 encodable: %s" % exc)
    if not text.endswith("."):
        failures.append("does not end with a period")
    if not text[0].isupper():
        failures.append("does not start with a capital letter")
    if "  " in text:
        failures.append("double space present")
    if text.count(".") != 1 or "!" in text or "?" in text:
        failures.append("not exactly one sentence")
    if not text.strip():
        failures.append("whitespace-only")
    return failures


def main():
    failures = check_pitch(PITCH)
    if failures:
        for failure in failures:
            print("gate failed: %s" % failure, file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(PITCH)
    # Read back and verify byte-identical before reporting success.
    with open(path, "rb") as fh:
        data = fh.read()
    if data != PITCH.encode("utf-8"):
        print("gate failed: entry.txt not byte-identical to pitch",
              file=sys.stderr)
        return 1
    print("wrote %s (%d chars)" % (path, len(PITCH)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
