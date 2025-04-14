"""
Put the contents of the folder 'Final Assets v1/Assets/' in our Google Drive in this project under the path './OldAssets/'
If any errors occur, check the paths at the bottom of this script to make sure they line up with your directory structure 
AS WELL AS where you are running Python from.
"""

from pxr import Usd, UsdGeom, UsdShade, Sdf, Gf
from functools import partial
import os
import shutil

assets = {
    "paniniPress":      Gf.Vec3f(0.91, 0.30, 0.24),  # red
    "cartoonFish":      Gf.Vec3f(1.00, 0.60, 0.00),  # vivid orange
    "parkBench":        Gf.Vec3f(0.00, 0.59, 0.29),  # jade green
    "beegCrab":         Gf.Vec3f(0.83, 0.13, 0.18),  # crimson
    "yellowDuck":       Gf.Vec3f(0.98, 0.85, 0.00),  # bright yellow
    "bookStack":        Gf.Vec3f(0.42, 0.18, 0.81),  # purple
    "cafeTable":        Gf.Vec3f(0.86, 0.44, 0.11),  # bronze orange
    "pickleBarrels":    Gf.Vec3f(0.11, 0.61, 0.13),  # leafy green
    "penTablet":        Gf.Vec3f(0.17, 0.45, 0.87),  # azure blue
    "yugiohClockArc":   Gf.Vec3f(0.89, 0.13, 0.56),  # fuchsia
    "skateboard":       Gf.Vec3f(0.00, 0.66, 0.72),  # teal
    "mug":              Gf.Vec3f(0.60, 0.00, 0.80),  # violet
    "sushi":            Gf.Vec3f(1.00, 0.48, 0.56),  # watermelon pink
    "woodenChair":      Gf.Vec3f(0.55, 0.27, 0.07),  # deep brown
    "sittingMoomin":    Gf.Vec3f(0.00, 0.74, 0.83),  # sky cyan
    "oldTelevision":    Gf.Vec3f(0.63, 0.17, 0.17),  # reddish brown
    "kitchenaid":       Gf.Vec3f(0.86, 0.08, 0.23),  # cherry red
    "wineGlass":        Gf.Vec3f(0.29, 0.59, 1.00),  # bright blue
    "teapot":           Gf.Vec3f(0.96, 0.76, 0.19),  # warm gold
    "carrot":           Gf.Vec3f(1.00, 0.35, 0.00),  # carrot orange
    "vintageLamp":      Gf.Vec3f(0.98, 0.76, 0.20),  # amber gold
}

def CreateLayerAndPopulate(layer_path, stage_func):
    layer = Sdf.Layer.CreateNew(layer_path)
    stage = Usd.Stage.Open(layer)

    stage_func(stage)

    stage.Save()
    # print(layer.ExportToString())

def copy_to_prim_on_stage(oldFilePath: str, oldPrimPath: str, currStage: Usd.Stage, currPrim: Usd.Prim):
    Sdf.CopySpec(Sdf.Layer.OpenAsAnonymous(oldFilePath), 
        oldPrimPath, 
        currStage.GetRootLayer(), 
        currPrim.GetPath()
    )

def create_assetName_usd_stage(stage: Usd.Stage):
    Xform_assetName = stage.DefinePrim(f"/{ASSET_NAME}", "Xform")
    Xform_assetName.SetAssetInfoByKey("name", ASSET_NAME)
    Xform_assetName.SetKind("component")
    Xform_assetName.GetReferences().SetReferences([Sdf.Reference('./contrib/material/material.usda'), Sdf.Reference('./contrib/geometry/geometry.usda')])

    stage.SetDefaultPrim(Xform_assetName)
    UsdGeom.SetStageMetersPerUnit(stage, 0.01)
    UsdGeom.SetStageUpAxis(stage, "Y")


def create_geometry_usda_stage(stage: Usd.Stage):
    assetName = stage.DefinePrim(f"/{ASSET_NAME}")
    Scope_Geometry = stage.DefinePrim(f"/{ASSET_NAME}/Geometry", "Scope")

    variantSet_varset_Geometry = Scope_Geometry.GetVariantSets().AddVariantSet('varset_Geometry')

    # iterate through all variants, add them to the variant set, and add a payload
    for variant in ["lod0", "lod1", "lod2", "bbox"]:
        variantSet_varset_Geometry.AddVariant(variant)
        variantSet_varset_Geometry.SetVariantSelection(variant)
        with variantSet_varset_Geometry.GetVariantEditContext():
            Scope_Geometry.GetPayloads().AddPayload(f"./{variant}/geometry_{variant}.usda", )

    # default is lod0
    variantSet_varset_Geometry.SetVariantSelection('lod0')

    stage.DefinePrim(f"/{ASSET_NAME}/Materials")
    stage.DefinePrim(f"/{ASSET_NAME}/Materials/MaterialClasses")
    class_class_Default = stage.CreateClassPrim(f"/{ASSET_NAME}/Materials/MaterialClasses/class_Default")

    UsdShade.MaterialBindingAPI.Apply(class_class_Default)

    stage.SetDefaultPrim(assetName)


def create_geom_variant_usda_stage(name: str, stage: Usd.Stage):
    def create_bbox_stage():
        temp_stage = Usd.Stage.Open(OLD_GEOM_PATHS["LOD0"])
        lod0_prim = temp_stage.GetPrimAtPath(f"/{ASSET_NAME}_LOD0")

        lod0bbox = UsdGeom.Imageable(lod0_prim).ComputeWorldBound(0.0, UsdGeom.Tokens.default_).ComputeAlignedBox()

        Cube_cube_Bbox = UsdGeom.Cube.Define(stage, f"/{ASSET_NAME}/Geometry/{ASSET_NAME}_{name}/cube_Bbox")
        Cube_cube_Bbox.GetExtentAttr().Set([Gf.Vec3f(-0.5, -0.5, -0.5), Gf.Vec3f(0.5, 0.5, 0.5)])
        Cube_cube_Bbox.GetSizeAttr().Set(1.0)
        Cube_cube_Bbox.AddTranslateOp().Set(lod0bbox.GetMidpoint())
        Cube_cube_Bbox.AddScaleOp().Set(lod0bbox.GetSize())

    Geometry = stage.DefinePrim(f"/{ASSET_NAME}/Geometry")
    Xform_assetName_geom = stage.DefinePrim(f"/{ASSET_NAME}/Geometry/{ASSET_NAME}_{name}", "Xform")

    if name == "bbox":
        create_bbox_stage()
    else:
        copy_to_prim_on_stage(OLD_GEOM_PATHS[name], f"/{ASSET_NAME}_{name}", stage, Xform_assetName_geom)

    for x in stage.Traverse():
        famType = x.GetAttribute("subsetFamily:materialBind:familyType")
        if famType.IsValid():
            famType.Block()

        famName = x.GetAttribute("familyName")
        if famName.IsValid():
            famName.Block()

        bindRel = x.GetRelationship("material:binding")
        for tgt in bindRel.GetTargets():
            bindRel.RemoveTarget(tgt)
            # if not stage.GetPrimAtPath(tgt).IsValid():
            #     bindRel.RemoveTarget(tgt)

    Xform_assetName_geom.GetInherits().AddInherit(f"/{ASSET_NAME}/Materials/MaterialClasses/class_Default")

    stage.SetDefaultPrim(Geometry)

def create_material_usda_stage(stage: Usd.Stage):
    assetName = stage.DefinePrim(f"/{ASSET_NAME}")
    Scope_Materials = stage.DefinePrim(f"/{ASSET_NAME}/Materials", "Scope")

    Scope_Materials.GetReferences().AddReference("./default/material_default.usda")

    stage.DefinePrim(f"/{ASSET_NAME}/Materials/MaterialClasses", "Scope")
    over_class_Default = stage.OverridePrim(f"/{ASSET_NAME}/Materials/MaterialClasses/class_Default")
    
    over_class_Default.CreateRelationship("material:binding", False)
    over_class_Default.GetRelationship("material:binding").AddTarget(f"/{ASSET_NAME}/Materials/mat_Default")

    stage.SetDefaultPrim(assetName)

def create_material_variant_usda_stage(name: str, stage: Usd.Stage):
    def create_pbr_nodegraph():
        Shader_usdPreviewSurface = UsdShade.Shader.Define(stage, path_matnet.AppendChild("usdPreviewSurface"))
        Shader_usdPreviewSurface.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.8)
        Shader_usdPreviewSurface.CreateIdAttr().Set("UsdPreviewSurface")
        diffuseColorIn = Shader_usdPreviewSurface.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f)
        Shader_usdPreviewSurface.CreateOutput("surface", Sdf.ValueTypeNames.Token)

        Shader_stReader = UsdShade.Shader.Define(stage, path_matnet.AppendChild('stReader'))
        Shader_stReader.CreateIdAttr().Set("UsdPrimvarReader_float2")
        Shader_stReader.CreateInput("varname", Sdf.ValueTypeNames.Token).Set("st")
        Shader_stReader.CreateOutput("result", Sdf.ValueTypeNames.Float2)

        Shader_diffuseTexture = UsdShade.Shader.Define(stage, path_matnet.AppendChild('diffuseTexture'))
        Shader_diffuseTexture.CreateIdAttr().Set("UsdUVTexture")
        Shader_diffuseTexture.CreateInput("file", Sdf.ValueTypeNames.Asset).Set(f"./texture/{name.lower()}.png")
        stIn = Shader_diffuseTexture.CreateInput("st", Sdf.ValueTypeNames.Float2)
        Shader_diffuseTexture.CreateOutput("rgb", Sdf.ValueTypeNames.Float3)

        diffuseColorIn.ConnectToSource(Shader_diffuseTexture.ConnectableAPI(), "rgb")
        stIn.ConnectToSource(Shader_stReader.ConnectableAPI(), "result")

        matnetSurfaceOut.ConnectToSource(Shader_usdPreviewSurface.ConnectableAPI(), "surface")

    def create_diffuse_nodegraph():
        Shader_usdPreviewSurface = UsdShade.Shader.Define(stage, path_matnet.AppendChild("usdPreviewSurface"))
        Shader_usdPreviewSurface.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.3)
        Shader_usdPreviewSurface.CreateInput("ior", Sdf.ValueTypeNames.Float).Set(1.3)
        Shader_usdPreviewSurface.CreateIdAttr().Set("UsdPreviewSurface")
        Shader_usdPreviewSurface.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set(DIFFUSE_COLOR)
        Shader_usdPreviewSurface.CreateOutput("surface", Sdf.ValueTypeNames.Token)

        matnetSurfaceOut.ConnectToSource(Shader_usdPreviewSurface.ConnectableAPI(), "surface")

    Materials = stage.DefinePrim(f"/{ASSET_NAME}/Materials")
    variantSet_varset_MatName = Materials.GetVariantSets().AddVariantSet(f"varset_{name}")

    for variant in ["pbr", "diffuse"]:
        variantSet_varset_MatName.AddVariant(variant)
        variantSet_varset_MatName.SetVariantSelection(variant)
        with variantSet_varset_MatName.GetVariantEditContext():
            path_MatName = Sdf.Path(f"/{ASSET_NAME}/Materials/mat_{name}")
            MatName = UsdShade.Material.Define(stage, path_MatName)
            MatNameSurfaceOut = MatName.CreateSurfaceOutput()
            
            path_matnet = path_MatName.AppendChild(f"matnet")
            NodeGraph_matnet = UsdShade.NodeGraph.Define(stage, path_matnet)
            matnetSurfaceOut = NodeGraph_matnet.CreateOutput("surface", Sdf.ValueTypeNames.Token)

            MatNameSurfaceOut.ConnectToSource(NodeGraph_matnet.ConnectableAPI(), "surface")

            if variant == "pbr":
                create_pbr_nodegraph()
            else:
                create_diffuse_nodegraph()

    variantSet_varset_MatName.SetVariantSelection("pbr")

    stage.SetDefaultPrim(Materials)


def CreateAll():
    CreateLayerAndPopulate(GEOMETRY_USDA_PATH, create_geometry_usda_stage)
    CreateLayerAndPopulate(ASSETNAME_USDA_PATH, create_assetName_usd_stage)

    CreateLayerAndPopulate(NEW_GEOM_PATHS["LOD0"], partial(create_geom_variant_usda_stage, "LOD0"))
    CreateLayerAndPopulate(NEW_GEOM_PATHS["LOD1"], partial(create_geom_variant_usda_stage, "LOD1"))
    CreateLayerAndPopulate(NEW_GEOM_PATHS["LOD2"], partial(create_geom_variant_usda_stage, "LOD2"))
    CreateLayerAndPopulate(NEW_GEOM_PATHS["bbox"], partial(create_geom_variant_usda_stage, "bbox"))

    CreateLayerAndPopulate(MATERIAL_USDA_PATH, create_material_usda_stage)

    CreateLayerAndPopulate(MATERIAL_DEFAULT_USDA_PATH, partial(create_material_variant_usda_stage, "Default"))

    os.makedirs(os.path.dirname(DEFAULT_TEXTURE_PNG_PATH), exist_ok=True)
    shutil.copyfile("./._Scripts/._default.png", DEFAULT_TEXTURE_PNG_PATH)

for asset, color in assets.items():
    ASSET_NAME = asset
    DIFFUSE_COLOR = color

    ASSETNAME_USDA_PATH = f"./Assets/{ASSET_NAME}/{ASSET_NAME}.usda"
    GEOMETRY_USDA_PATH = f"./Assets/{ASSET_NAME}/contrib/geometry/geometry.usda"
    MATERIAL_USDA_PATH = f"./Assets/{ASSET_NAME}/contrib/material/material.usda"

    MATERIAL_USDA_PATH = f"./Assets/{ASSET_NAME}/contrib/material/material.usda"
    MATERIAL_DEFAULT_USDA_PATH = f"./Assets/{ASSET_NAME}/contrib/material/default/material_default.usda"

    DEFAULT_TEXTURE_PNG_PATH = f"./Assets/{ASSET_NAME}/contrib/material/default/texture/default.png"

    NEW_GEOM_PATHS = {
        "LOD0": f"./Assets/{ASSET_NAME}/contrib/geometry/LOD0/geometry_LOD0.usda",
        "LOD1": f"./Assets/{ASSET_NAME}/contrib/geometry/LOD1/geometry_LOD1.usda",
        "LOD2": f"./Assets/{ASSET_NAME}/contrib/geometry/LOD2/geometry_LOD2.usda",
        "bbox": f"./Assets/{ASSET_NAME}/contrib/geometry/bbox/geometry_bbox.usda"
    }

    OLD_GEOM_PATHS = {
        "LOD0": f"./OldAssets/{ASSET_NAME}/contrib/geometry/lod/LODs/{ASSET_NAME}_LOD0.usda",
        "LOD1": f"./OldAssets/{ASSET_NAME}/contrib/geometry/lod/LODs/{ASSET_NAME}_LOD1.usda",
        "LOD2": f"./OldAssets/{ASSET_NAME}/contrib/geometry/lod/LODs/{ASSET_NAME}_LOD2.usda",
        "bbox": f"./OldAssets/{ASSET_NAME}/contrib/geometry/proxy/geometry_proxy.usda"
    }

    CreateAll()