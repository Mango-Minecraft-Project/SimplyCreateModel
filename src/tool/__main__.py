import zipfile
import tomllib
import pyjson5
from pathlib import Path

CWD = Path.cwd()


def get_files(type):
    """get files from src/main/ folder

    Args:
        type (str): type of file to get
    """
    files = []
    match type:
        case "data_pack":
            files = ["data/", "pack.png", "pack.mcmeta"]
        case "resource_pack":
            files = ["assets/", "pack.png", "pack.mcmeta"]
        case "mod":
            files = [
                "assets/",
                "data/",
                "META-INF/",
                "pack.png",
                "pack.mcmeta",
                "fabric.mod.json",
            ]
    return filter(
        lambda path: path.exists(), map(lambda path: CWD / "src/main" / path, files)
    )


def get_version() -> str:
    """get version from src/main/META-INF/mods.toml"""
    forge_metadata = CWD / "src/main/META-INF/mods.toml"
    neoforge_metadata = CWD / "src/main/META-INF/neoforge.mods.toml"
    fabric_metadata = CWD / "src/main/fabric.mod.json"

    if forge_metadata.is_file() and neoforge_metadata.is_file():
        with (forge_metadata if forge_metadata.is_file() else neoforge_metadata).open(
            "rb"
        ) as file:
            return tomllib.load(file)["mods"][0]["version"]
    elif fabric_metadata.is_file():
        with fabric_metadata.open("r", encoding="utf-8") as file:
            return pyjson5.load(file)["version"]
    else:
        raise FileNotFoundError(
            "No metadata file found. Please ensure META-INF/mods.toml, META-INF/neoforge.mods.toml or fabric.mod.json exists."
        )


def get_output_filename(type):
    """get extension for package

    Args:
        type (str): type of package to create
    """
    match type:
        case "data_pack":
            return "Create_Mortar_Mango_Edition-{version}-data.zip"
        case "resource_pack":
            return "Create_Mortar_Mango_Edition-{version}-resource.zip"
        case "mod":
            return "Create_Mortar_Mango_Edition-{version}-mod.jar"
    return ""


def package(type):
    """package mod or data pack

    Args:
        type (str): type of package to create
    """
    version = get_version()
    output_filename = get_output_filename(type).format(version=version)
    files = get_files(type)

    output_path = CWD / "versions" / output_filename
    if output_path.exists():
        output_path.unlink()

    with zipfile.ZipFile(CWD / "versions" / output_filename, "w") as zip:
        for file in files:
            if file.is_dir():
                for path in file.rglob("*"):
                    zip.write(path, path.relative_to(CWD / "src/main"))
            else:
                zip.write(file, file.name)
        print(f"Packaged {type} for version {version} to {output_filename}")


def main():
    # package("data_pack")
    package("resource_pack")
    package("mod")
    ...


if __name__ == "__main__":
    main()
