# CIS7000 USD Asset Directory & Interface

![layer](._Images/Flattened_Asset_Layer.png)

### [Structure Walkthrough Video](https://youtu.be/hNuHniOKjt4)
### [User Workflows Breakdown Presentation PDF](https://drive.google.com/file/d/1ZxiKbZk2xu4kw1len1eW1ywzZlvCVUjK/view?usp=sharing)

This will be our new structure for OpenUSD asset storage. It is inspired by the design decisions made in NVIDIA's [da Vinci's Workshop](https://docs.omniverse.nvidia.com/usd/latest/usd_content_samples/davinci_workshop.html) and [Residential Lobby](https://docs.omniverse.nvidia.com/usd/latest/usd_content_samples/res_lobby.html) datasets, as well as Disney's [Moana](https://disneyanimation.com/resources/moana-island-scene/) dataset.

In this example folder, we have included several folders & features in general as placeholders for future usage. They have not been implemented yet. If such features are mentioned in this README, we will denote a ***TBI*** (i.e. to be implemented) indication next to them, meaning they can be disregarded for now.

## What is important about this directory?
The main design focus is on the `Assets` subdirectory and the new design for the USD interface of a singular asset.

The directory contains an example asset (`campfire`) that has been restructured to fit the new guidelines.

## How does it fit into our pipeline?
The contents of this directory, along with all of our existing assets restructured and ported inside, will be placed in an Amazon S3 bucket. i.e. `Assets`, `Assemblies`, `DCCs` will be "sub-buckets" under the top-level.

## Folder Structure Overview

- `Assets/`: Main subdirectory containing individual asset folders.
- `Assemblies/`: USD-based logic for higher-level groupings of assets. ***TBI***
- `DCCs/`: Location for DCC pipeline USD logic. ***TBI***

## Contributions (`contrib/`)

A primary feature of this new asset interface is the new `contrib/` subfolder under each individual asset folder.
This is motivated largely by the structure of the da Vinci's workshop scene. They explain the "contribution" based workflow quite well, so the specific section is linked [here](https://docs.omniverse.nvidia.com/usd/latest/usd_content_samples/davinci_workshop.html#asset-composition-arcs) for everyone to hop over to and quickly read.

Pretty cool right!? To rephrase, the gist is that this `contrib/` folder structure allowed the NVIDIA team to contribute modular units of work by making each subfolder an individual composition arc. For example, their `material/` subfolder has a variant-set based design, where the top-level `material.usda` composes the material variants located in the next level of subfolders (i.e. `off`, `render`, `renderLow`, etc.).

We thought this particularly insightful for our class' overarching goal. In a way, each student's role in the final project is actually very likely to coincide with a "contribution" to our asset structure, making a "contribution-based" modular structure perfect for our use case.

Current folders inside `contrib/` include:
- `geometry/`: Direct translation to our previous LOD files
- `material/`: Currently contains a simple variant set switching between a PBR material with shaders and textures, and a simple diffuse material.
- `source/`: ***TBI*** Where any additional customized behavior of the asset will come from, such as instancing, animations, etc. Can be left alone for specific assets if no custom behavior is needed
- `tag/`: This is a big ***TBI***. I have been inspired by a few discussions on asset resolvers, such as [this tutorial project](https://lucascheller.github.io/VFX-UsdAssetResolver/) and [this usd plugin](https://github.com/rodeofx/rdo_replace_resolver). They mention using a USD file containing a custom `mappingPairs` array, mapping source files to target files. Let us know if you'd like to help tackle this!

To summarize the Asset structure loosely follows these conventions:
1. `<asset_name>.usd`
2. `contrib/<contribution>/<contribution>.usda`

3. `contrib/<contribution>/<variant>/<contribution>_<variant>.usda`

### And this is the best part!
Besides the above requirements (actually, the 3rd one isn't even neccesary), data organization and composition under each contribution can be modified to fit each task's use case! Although the variantSet-based structure explained above is established as a guide, all we really need to enforce is having each contribution be an individual composition arc that will be referenced by the top-level `.usd` file.

#### As long as this rule-of-thumb is followed, this becomes a very flexible and expandable structure!

## File Types and Naming Conventions

- `.usd`: Neutral format for root/base files. ***TBI***
- `.usda`: ASCII, editable. Used for interface layers and user contributions.
- `.usdc`: Binary, non-editable. Used for large datasets and performance. ***TBI***

The file extension helps team members quickly understand whether a file should be edited or left alone.

## Variants and Versioning

Assets can support:
- Switching between LODs, different materials, and more attribute categories.
- Versioning: Currently not hashed out. Will be made possible through the asset reolver + `tag/` contribution detailed above. ***TBI***
  - Note: A best practice that is talked about in this [video](https://youtu.be/YgVTS5oIJqM?si=3bUczCRT3axPE4JL&t=532) is that whole asset versioning is not important, rather individual material versions and geometry versions should be resolved and versioned as they are created. Hence, the reasoning behind the mappingPairs array in `tag.usda`.
  
## Placement of external assets

As an example we've placed texture files under `Assets/campfire/contrib/material/<type>/texture/`). Other needs for external assets as they arise should also be placed within individual asset subfolders, rather than shared database wide. Although that would result in less data usage, this ensures assets are modular and self-contained.

## Scripting examples

I wrote a Python script to build our USD scenes from scratch and copy over our previous USD asset data. It is included to demonstrate how this asset structure also can be easily integrated with scripts / procedural workflows (shoutout DCC team!). Please use it for reference.

## Design Highlights

- Can scale up as our final project progresses.
- Contributions from multiple students can coincide easily.
- Layer-based design makes it easy to inspect and modify different interface layers of our USD assets.

## Aide Mémoire
There are various `.readme.md` files scattered throughout the directory containing additional documentation and tidbits. Also, any file or directory that is pre-pended with a `._` is auxiliary and not meant to be included in the final file directory.


## The End!

Note: This document and overall design is a work-in-progress and will evolve as the pipeline comes together.

Please message members of the USD team (Jackie, Clara, and Amy) if you have any questions or concerns.

I also really recommend skimming through the entire da Vinci's workshop document. It's a cool project and the documentation does a good job of helping to visualize many of the best practices and composition arcs we've been learning about.
