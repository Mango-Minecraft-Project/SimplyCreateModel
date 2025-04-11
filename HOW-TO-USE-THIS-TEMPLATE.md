# How To Use This Template

This template is designed to help you create a new project quickly and efficiently. Follow the steps below to get started:

1. Click `Use this template` button at the top right of the page.
2. Fill in the repository name and description. You can also choose to make it public or private.
3. Click `Create repository from template`.

## After Creating the Repository

1. Clone the repository to your local machine using `git clone <repository-url>`.
2. Open the project in your favorite IDE (e.g., IntelliJ IDEA, Eclipse).
3. Update the `README.md` file with your project's information. You can use the provided template as a starting point.
   1. Replace `{ModName}` with the name of your mod.
   2. Replace `{Description}` with a brief description of your mod.
   3. Remove unused sections or add new ones as needed.
      1. Replace `{modrinth-project-id}` with your Modrinth project ID.
      2. Replace `{curseforge-project-id}` with your CurseForge project ID.
      3. Replace `{discord-id}` with your Discord server ID.
4. Update `src/main/pack.png` with your mod's icon. The image should be 128x128 pixels or a power of 2 size (e.g., 256x256, 512x512).
5. Update `src/main/fabric.mod.json` / `src/main/META-INF/mods.toml` / `src/main/META-INF/neoforge.mods.toml` with your mod's metadata.
   1. Update the `id`, `name`, `version`, and `description` fields.
   2. Add any required dependencies as needed.
   3. Delete unused mod loader files.
6. Add your content to the `src/main/data` or `src/main/assets` directory. This is where you will place your mod's resources, such as textures, models, and data packs.
7. (Forge Only) Update `src/main/pack.mcmeta` with your mod's pack metadata. This file is used to define the pack format and other settings for your mod.

## Building the Mod

1. Make sure you have the required dependencies installed. You need to have [Python](https://www.python.org/downloads/) installed on your system.
2. Open a terminal in your project directory.
3. Edit `src/tool/__main__.py` to uncomment the build command you want to package to (e.g., data_pack, resource_pack, or mod).
4. Run the build command using `python src/tool/__main__.py`.
5. The built mod will be located in the `versions/` directory.

## Last Steps

1. Remove All unused files and folders from the repository.
2. Update the `.gitignore` file to exclude any files or directories you don't want to include in your repository.
3. Commit your changes and push them to your remote repository using `git add .`, `git commit -m "Initial commit"`, and `git push origin main`.
4. (Optional) Create a new release on GitHub by going to the "Releases" tab and clicking "Draft a new release". Fill in the version number and any release notes, then click "Publish release".
5. (Optional) Share your mod on social media or relevant forums to promote it and gather feedback from the community.
6. (Optional) Create a wiki or documentation for your mod to help users understand how to use it and its features.
