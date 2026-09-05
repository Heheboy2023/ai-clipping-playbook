"""Print a proposed clip name. Never create, rename, or move media."""
import argparse
import re


def slug(value: str) -> str:
    result = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    if not result:
        raise ValueError("creator and moment must contain an English letter or digit")
    return result


def propose_name(creator: str, moment: str, version: int) -> str:
    if isinstance(version, bool) or not isinstance(version, int) or version < 1:
        raise ValueError("version must be an integer of at least 1")
    return f"{slug(creator)}__{slug(moment)}__v{version:02d}.mp4"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--creator", required=True)
    parser.add_argument("--moment", required=True)
    parser.add_argument("--version", required=True, type=int)
    args = parser.parse_args()
    try:
        name = propose_name(args.creator, args.moment, args.version)
    except ValueError as exc:
        parser.error(str(exc))
    print(name)


if __name__ == "__main__":
    main()
