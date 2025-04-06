# CIS7000 USD Asset Directory & Interface

This will be our new structure for OpenUSD asset storage. It is inspired by the design decisions made in NVIDIA's [da Vinci's Workshop](https://docs.omniverse.nvidia.com/usd/latest/usd_content_samples/davinci_workshop.html) and [Residential Lobby](https://docs.omniverse.nvidia.com/usd/latest/usd_content_samples/res_lobby.html) datasets, as well as Disney's [Moana](https://disneyanimation.com/resources/moana-island-scene/) dataset

In this example folder, I have included several folders & features in general as placeholders for future usage. They have not been implemented yet. If I mention such features in this README, I will denote a ***TBI*** (i.e. to be implemented) indication next to them, meaning they can be disregarded for now.

The main design focus is on the `Assets` subdirectory and the new design for the USD interface of a singular asset.

## Folder Structure Overview

- `Assets/`: Main subdirectory containing individual asset folders.
- `Assemblies/`: USD-based logic for higher-level groupings of assets. ***TBI***
- `DCCs/`: Location for DCC pipeline USD logic. ***TBI***

## Contributions (`contrib/`)

A primary feature of this new asset interface is the new `contrib/` subfolder under each individual asset folder.
This is inspired largely by the structure of da Vinci's workshop scene. They explain the "contribution" based workflow quite well, so I've linked the specific section [here](https://docs.omniverse.nvidia.com/usd/latest/usd_content_samples/davinci_workshop.html#asset-composition-arcs) for everyone to hop over to and quickly read.

Pretty cool right!? To put it in my own words, the gist is that this `contrib/` folder structure allowed the NVIDIA team to contribute modular units of work by making each subfolder an individual composition arc. For example, their `material/` subfolder has a variant-set based design, where the top-level `material.usda` composes the material variants located in the next level of subfolders (i.e. `off`, `render`, `renderLow`, etc.).

I thought this particularly insightful for our class' overarching goal. In a way, each student's role in the final project is actually very likely to coincide with a "contribution" to our asset structure, making a "contribution-based" modular structure perfect for our use case.

Current folders inside `contrib/` include:
- `geometry/`: Direct translation to our previous LOD files
- `material/`: Currently contains a simple variant set switching between a PBR material with shaders and textures, and a simple diffuse material.
- `source/`: ***TBI*** Where any additional customized behavior of the asset will come from, such as instancing, animations, etc. Can be left alone for specific assets if no custom behavior is needed
- `tag/`: This is a big ***TBI***. I have been inspired by a few discussions on asset resolvers, such as [this tutorial project](https://lucascheller.github.io/VFX-UsdAssetResolver/) and [this usd plugin](https://github.com/rodeofx/rdo_replace_resolver). They mention using a USD file containing a custom `mappingPairs` array, mapping source files to target files. Let me know if you'd like to help me tackle this!

To summarize the Asset structure loosely follows these conventions:
1. `<asset_name>.usd`
2. `contrib/<contribution>/<contribution>.usda`

3. `contrib/<contribution>/<variant>/<contribution>_<variant>.usda`

### And this is the best part!
Besides the above requirements (actually, the 3rd one isn't even neccesary), data organization and composition under each contribution can be modified to fit each task's use case! Although the variantSet-based structure explained above is established as a guide, all we really need to enforce is having each contribution be an individual composition arc that will be referenced by the top-level `.usd` file.

#### As long as this rule-of-thumb is followed, this becomes a very flexible and expandable structure!

## File Types and Naming Conventions

- `.usd`: Neutral format for root/base files.
- `.usda`: ASCII, editable. Used for interface layers and user contributions.
- `.usdc`: Binary, non-editable. Used for large datasets and performance. ***TBI***

The file extension helps team members quickly understand whether a file should be edited or left alone.

## Variants and Versioning

Assets can support:
- Switching between LODs, different materials, and more attribute categories.
- Versioning: Currently not hashed out. Will be made possible through the asset reolver + `tag/` contribution detailed above. ***TBI***
  - Note: A best practice that is talked about in this [video](https://youtu.be/YgVTS5oIJqM?si=3bUczCRT3axPE4JL&t=532) is that whole asset versioning is not important, rather individual material versions and geometry versions should be resolved and versioned as they are created. Hence, the reasoning behind the mappingPairs array in `tag.usda`.
  
## Placement of external assets

As an example I've placed texture files under `Assets/campfire/contrib/material/pbr/texture/`). Other needs for external assets as they arise should also be placed within individual asset subfolders, rather than shared database wide. Although that would result in less data usage, this ensures assets are modular and self-contained.

## Scripting examples

I wrote a Python script to make the "pbr" variant file at `Assets/campfire/contrib/material/pbr/material_pbr.usda` work for the `campfire` asset. I included it to demonstrate how this asset structure also can be easily integrated with scripts / procedural workflows (shoutout DCC team). From the root directory, you can run:

```bash
cd ._Scripts
vim ._create_material.py # i.e. open in your desired text editor
# look through code logic and change default paths, etc.
python ._create_material.py
```

## Design Highlights

- Can scale up as our final project progresses.
- Contributions from multiple students can coincide easily.
- Layer-based design makes it easy to inspect and modify different interface layers of our USD assets.

## Aide Mémoire
There are various `.readme.md` files scattered throughout the directory containing additional documentation and tidbits. Also, any file or directory that is pre-pended with a `._` is auxiliary and not meant to be included in the final file directory.


## The End!

Note: This document and overall design is a work-in-progress and will evolve as the pipeline comes together.

Please message me (Amy) or other members of the USD team if you have any questions or concerns.

I also really recommend skimming through the entire da Vinci's workshop document. It's a cool project and the documentation does a good job of helping to visualize many of the best practices and composition arcs we've been learning about.
