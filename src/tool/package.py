import zipfile
import tomllib
from typing import Literal
from pathlib import Path

import pyjson5


CWD = Path.cwd()
_2001 = CWD / "src/1.20.1"
_2101 = CWD / "src/1.21.1"

package_type = Literal["data_pack", "resource_pack", "mod"]
base_map = {
    "1.20.1": _2001,
    "1.21.1": _2101,
}


def get_metadata(game_version: str):
    base = base_map.get(game_version)
    if base is None:
        raise ValueError(f"Unsupported game version: {game_version}")

    if (forge_metadata := base / "META-INF/mods.toml").is_file():
        with forge_metadata.open("rb") as file:
            return ("forge", tomllib.load(file))
    elif (neoforge_metadata := base / "META-INF/neoforge.mods.toml").is_file():
        with neoforge_metadata.open("rb") as file:
            return ("neoforge", tomllib.load(file))
    elif (fabric_metadata := base / "fabric.mod.json").is_file():
        with fabric_metadata.open("r", encoding="utf-8") as file:
            return ("fabric", pyjson5.load(file))
    else:
        raise FileNotFoundError(
            "No metadata file found. Please ensure META-INF/mods.toml, META-INF/neoforge.mods.toml or fabric.mod.json exists."
        )


def get_files(type: package_type, game_version: str):
    """get files from src/main/ folder

    Args:
        type (str): type of file to get
    """

    base = base_map.get(game_version)
    if base is None:
        raise ValueError(f"Unsupported game version: {game_version}")

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
            ]
    return filter(lambda path: path.exists(), map(lambda path: base / path, files))


def get_version(game_version: str) -> str:
    """get version from src/main/META-INF/mods.toml"""
    type, metadata = get_metadata(game_version)

    if type in {"forge", "neoforge"}:
        return metadata["mods"][0]["version"]
    elif type == "fabric":
        return metadata["version"]
    else:
        raise FileNotFoundError(
            "No metadata file found. Please ensure META-INF/mods.toml, META-INF/neoforge.mods.toml or fabric.mod.json exists."
        )


def get_output_filename(
    type: package_type, package_version: str, game_version: str
) -> str:
    """get extension for package

    Args:
        type (package_type): type of package to create
        version (str): version of package to create
    """
    loader_type, metadata = get_metadata(game_version)
    filename = ""

    if loader_type in {"forge", "neoforge"}:
        filename = metadata["mods"][0]["displayName"].replace(" ", "_")
    else:
        filename = metadata["name"].replace(" ", "_")

    suffix = {
        "data_pack": "data",
        "resource_pack": "resource",
        "mod": "mod",
    }
    extension = "jar" if type == "mod" else "zip"

    return f"{filename}-{suffix[type]}-{game_version}-{package_version}.{extension}"


def package(type: package_type, game_version: str):
    """package mod or data pack

    Args:
        type (str): type of package to create
    """
    base = base_map.get(game_version)
    if base is None:
        raise ValueError(f"Unsupported game version: {game_version}")

    version = get_version(game_version)
    output_filename = get_output_filename(type, version, game_version)
    files = get_files(type, game_version)

    output_path = (output_dir:=CWD / "versions" / version) / output_filename
    output_dir.mkdir(parents=True, exist_ok=True)
    if output_path.exists():
        output_path.unlink()

    with zipfile.ZipFile(output_path, "w") as zip:
        for file in files:
            if file.is_dir():
                for path in file.rglob("*"):
                    zip.write(path, path.relative_to(base))
            else:
                zip.write(file, file.name)
        print(f"Packaged {type} for version {version} to {output_filename}")


def main():
    package("resource_pack", "1.20.1")
    package("mod", "1.20.1")
    package("resource_pack", "1.21.1")
    package("mod", "1.21.1")

if __name__ == "__main__":
    main()
