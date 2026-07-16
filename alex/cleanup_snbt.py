from alex.utils import OverlayPath, getSNBTVersions, check_for_item

versions = getSNBTVersions()

existingFiles: dict[str, str] = {}
deletedFile = False


def get_version_snbt(version: str, shouldFix=False):
    versionPath = OverlayPath.joinpath(version)
    global deletedFile
    for file in versionPath.iterdir():
        if not file.is_file():
            continue

        fileName = str(file.relative_to(file.parent))
        if not check_for_item(fileName.replace(".snbt", "")):
            print(f"error: {file} does not have a corresponding item!")
            if shouldFix:
                deletedFile = True
                file.unlink()
            continue

        if file.name in existingFiles:
            print("Duplicate file: {} in version {} (also in {})"
                  .format(file.name, version, existingFiles[file.name]))
            if shouldFix:
                deletedFile = True
                file.unlink()

        existingFiles[file.name] = version


def Main():
    for version in versions:
        get_version_snbt(version, __name__ == "__main__")


if __name__ == "__main__":
    Main()
    if deletedFile:
        exit(1)
