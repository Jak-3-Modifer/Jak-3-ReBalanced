import pathlib
import sys
import tarfile
import zipfile


SAVE_DIRECTORY_NAMES = {
    "save",
    "saves",
    "savestate",
    "savestates",
    "memorycard",
    "memorycards",
    "memory-card",
    "memory-cards",
}
SAVE_FILE_EXTENSIONS = {".mcd", ".mc2", ".p2s", ".ps2", ".sav", ".save", ".srm"}


def is_save_path(member_name):
    path = pathlib.PurePosixPath(member_name.replace("\\", "/"))
    parts = [part.lower() for part in path.parts]

    for part in parts[:-1]:
        if (
            part in SAVE_DIRECTORY_NAMES
            or part.endswith("-saves")
            or part.endswith("_saves")
        ):
            return True

    return path.suffix.lower() in SAVE_FILE_EXTENSIONS


def archive_members(archive_path):
    if archive_path.suffix.lower() == ".zip":
        with zipfile.ZipFile(archive_path) as archive:
            return archive.namelist()

    if archive_path.name.lower().endswith((".tar.gz", ".tgz")):
        with tarfile.open(archive_path, "r:gz") as archive:
            return archive.getnames()

    return []


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: verify-no-saves.py <release-directory>")

    release_directory = pathlib.Path(sys.argv[1])
    archives = [path for path in release_directory.iterdir() if path.is_file()]
    if not archives:
        raise SystemExit(f"No release archives found in {release_directory}")

    violations = []
    checked_archives = 0
    for archive_path in archives:
        members = archive_members(archive_path)
        if not members:
            continue
        checked_archives += 1
        violations.extend(
            f"{archive_path.name}: {member}"
            for member in members
            if is_save_path(member)
        )

    if checked_archives == 0:
        raise SystemExit(f"No supported release archives found in {release_directory}")

    if violations:
        print("Save data was found in the release bundles:")
        print("\n".join(violations))
        raise SystemExit(1)

    print(f"Verified {checked_archives} release bundle(s): no save data found.")


if __name__ == "__main__":
    main()
