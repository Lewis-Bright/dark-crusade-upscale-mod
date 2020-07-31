# dark-crusade-upscale-mod
A mod to upscale all textures 4x in Dawn of War - Dark Crusade

# Current Workflow
Before any of this, make sure you extract the DXP2/DXP2Data-SharedTextures-Full.sga file using Relic's Mod Packager tool. When editing a texture, my basic starting point is to copy the file I want to edit to its own folder, then create a "new" folder at the same level as the file. This makes it easier to revisit old edits. At the moment I've only changed RSH and WTP files.
## WTP files
I believe these files are used for any model which has a team colouring. They contain many different elements, the most important for us is the model_name_default.tga file. This is what we will be actually upscaling (the rest I'm just enlarging).
Currently for WTP files I am doing the following:
* Using the Dawn of War texture tool (can be found online) to extract the WTP file into several TGA files. These Targa files have lots of formatting that is frankly irritating to try and get right, before they can be repackaged into WTP files, so keep this in mind. I run the gimp script I have attached to transform everything but the \_default.tga file by 4x (you need to have a "new" folder in the same place as the TGA's. I have two powershell aliases that help me run this:

```
function upscale($defaultName) {
        gimp-2.10 -i -b "(resize-image-keep-ratio \`"$defaultName\`" 2048 2048)" -b "(gimp-quit 0)"
}

function upscaleSmall($defaultName) {
        gimp-2.10 -i -b "(resize-image-keep-ratio \`"$defaultName\`" 1024 1024)" -b "(gimp-quit 0)"
}
```

but the basic usage is: `gimp-2.10 -i -b "(resize-image-keep-ratio \`"ig_imperial_captain_default\`" 2048 2048)" -b "(gimp-quit 0)"`. (I use 1024 scaling for smaller images). It is important to note I haven't bothered with the badges as I don't really find them that useful (and they are a pain to make). If you want to make them then you can add the relevant line to the gimp script. After they have been made, you will need to convert that white square (that represents the badge location) back into a 64x64 square, as it doesn't work with a larger one (perhaps this would change if we found a way to resize the badge textures?)

*Next step is the upscaling of the _default.tga. You can use any method here, but make sure that the resolution matches the other files. I do this by using ESRGAN (there's plenty of documentation on this) and ImageEnhancingUtility.winforms. At the moment I am using two models to upscale this, [LADDIER1_282500_G](https://de-next.owncube.com/index.php/s/aAojXwLTPZto8rP) for the 4x blur removal, and [1x_Fatality_DeBlur_270000_G](https://de-next.owncube.com/index.php/s/aAojXwLTPZto8rP) for further blur removal (Credit to Alexander Syring, License: [CC0](https://creativecommons.org/publicdomain/zero/1.0/) and [Twittman](https://upscale.wiki/wiki/User:Twittman), License: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/ respectively and respectably). First I convert to a .png using paint.net, then upscale as appropriate. Then you need to save the file in paint.net again, as the upscale application can result in compression (you will get an error when you try to compile back to a WTP). Finally I export the file from Gimp as a TGA file, making sure to remove the option for RLE compression.

*Finally, use the dawn of war texture tool to convert all these back into WTP textures (just select one of the TGA's in the folder, it will find the rest). Then place this file in the relevant folder of your mod (as seen in this Repo).

## RSH files
I think these are files for anything that is not affected by team colouring (buildings etc). These contain DDS files, which contain mipmaps. Mipmaps are essentially different resolution drawings of the same image, so that you can render smaller images if you need to. It's clear in Dawn of War that this is used when you zoom out, as the texture on certain buildings change (tested by drawing some random squiggles on different mipmap levels and seeing them appear at certain zoom levels). The important thing here (took me hours to figure out) is that you need to have a logarithmic sequence of resolutions for each of these. What I mean by that, is for a 64x64 texture image, you would need the following: 64x64, 32x32, 16x16, 8x8, 4x4, 2x2, 1x1. If you do not follow this sequence, you will get pink textures (although the texture tool will still compile these into RSH files, and the DoW logs will not tell you what is going on, just that it can't load them).

My steps are as follows:
*Use dawn of war texture tool to extract RSH files into DDS files. Keep these in a separate folder as with the WTP method.

*Download NVidia's tool [DDS Utilities](https://developer.nvidia.com/legacy-texture-tools). This is the only tool I could use to reliably create these files, every other tool I found did not work (pink textures)

*Use the detach tool (explanation how is in the terribly named "nvDXT.pdf" that comes with the tools)

*Use the python script in this repo's Tools directory to bump the numbers up at the end of these new files (for example `python rename_files.py ig_hq_concret01 2 ` to rename  by two, so 01->03, 02->04 etc)

*Copy the biggest file twice (_02 if you have bumped it twice). You will need to upscale one of these files by x2 and the other one by x4. It's up to you if you want to use a deep learning tool like before for the x2, it might not make much of a difference, since by definition this mipmap won't be rendered unless you're far away, but it won't harm performance, so I guess do it if you have time. You will also need to rename these files to fit the pattern (_00 and _01).

*Use the Texture tool to repackage these into a RSH files again.

*Drop this file into your mod folder, as long as you haven't missed a step in the 2^n pattern this should work without rendering pink textures

## Extra Tips
I'd advise starting a skirmish map, using cheats and getting yourself to the most advanced stage you can, then saving. That way you can immediately load up a game, and don't have to waste time capturing relics etc for a baneblade
