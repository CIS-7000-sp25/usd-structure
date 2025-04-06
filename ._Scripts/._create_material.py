from pxr import Usd, Sdf, UsdShade, UsdGeom

"""
Follewed tutorial at https://openusd.org/release/tut_simple_shading.html but modifed to match our new asset interface structure.

Materials use override logic, so `OverridePrim(...)` is used.

To save instead of export uncomment the line at the bottom of this file
"""

### PATHS
material_variant_path = "../Assets/campfire/contrib/material/pbr/material_pbr.usda" # modify based on where you run python from
prim_paths = [Sdf.Path("/campfire/geometry/lod/campfire_LOD0/rocks"), Sdf.Path("/campfire/geometry/lod/campfire_LOD0/logs")]
texture_filepaths = ["./texture/rock.png", "./texture/wood.png"]
scopeIdentifiers = ["rocksScope", "logsScope"]
output_path = "../Assets/campfire/contrib/material/pbr/._script_modified_material_pbr.usda"

scope_path = "/campfire/material/{}"
material_path = "/campfire/material/{}/material"
shader_path = "/campfire/material/{}/shader"
stReader_shader_path = "/campfire/material/{}/stReader"
diffuse_shader_path = "/campfire/material/{}/diffuseTexture"
###


stage = Usd.Stage.Open(material_variant_path)

for i, prim in enumerate(prim_paths):
    scope_prim = UsdGeom.Scope.Define(stage, scope_path.format(scopeIdentifiers[i])) 

    # get/create override prim at prim_path
    usdprim = stage.OverridePrim(prim)

    # define material prim within over specifier
    material = UsdShade.Material.Define(stage, material_path.format(scopeIdentifiers[i]))


    # define shader prim
    pbrShader = UsdShade.Shader.Define(stage, shader_path.format(scopeIdentifiers[i]))
    pbrShader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.4)
    pbrShader.CreateIdAttr("UsdPreviewSurface")

    # connect the material’s surface output to the UsdPreviewSurface ‘s surface output - this is what identifies the source of the Material’s surface shading.
    material.CreateSurfaceOutput().ConnectToSource(pbrShader.ConnectableAPI(), "surface")

    # texturing logic - see src above for more info
    stReader = UsdShade.Shader.Define(stage, stReader_shader_path.format(scopeIdentifiers[i]))
    stReader.CreateIdAttr('UsdPrimvarReader_float2')

    diffuseTextureSampler = UsdShade.Shader.Define(stage, diffuse_shader_path.format(scopeIdentifiers[i]))
    diffuseTextureSampler.CreateIdAttr('UsdUVTexture')
    diffuseTextureSampler.CreateInput('file', Sdf.ValueTypeNames.Asset).Set(texture_filepaths[i])
    diffuseTextureSampler.CreateInput("st", Sdf.ValueTypeNames.Float2).ConnectToSource(stReader.ConnectableAPI(), 'result')
    diffuseTextureSampler.CreateOutput('rgb', Sdf.ValueTypeNames.Float3)
    pbrShader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).ConnectToSource(diffuseTextureSampler.ConnectableAPI(), 'rgb')

    stInput = material.CreateInput('frame:stPrimvarName', Sdf.ValueTypeNames.Token)
    stInput.Set('st')

    stReader.CreateInput('varname',Sdf.ValueTypeNames.Token).ConnectToSource(stInput)

    # apply MaterialBindingAPI to the "rocks" / desired prim, bind the Mesh to our new Material
    usdprim.ApplyAPI(UsdShade.MaterialBindingAPI)
    UsdShade.MaterialBindingAPI(usdprim).Bind(material)

# save the results or export to another location
# stage.Save()
    
stage.Export(output_path)