# Side-by-Side PaletteTuner
A simple program to tune Game Boy Color palettes for a variety of screen types.

Originally Game Boy Color games only had to worry about how they looked on an actual GBC LCD (though even those had more variation than most people know). Later came the Game Boy Advance, Game Boy Player, and now after-market screen mods, not to mention emulators with a varity of ways of displaying colors.

I made this tool as a means of fairly quickly finding colors which should look alright on a range of screens/emulators, base on the color correction methods from [SameBoy](https://github.com/LIJI32/SameBoy). Many thanks to LIJI for their endless work on researching/documenting/emulating the corner case quirks of these devices. I wouldn't have been able to throw this tool together without their color correction work.

Thanks to Eievui for their Kirby's Dreamland DX colorization hack which is used here as an example image.

![screenshot](https://user-images.githubusercontent.com/10489588/181621350-3240362b-6a3b-4c47-a58f-72e6432bf3fe.png)

# Requirements

* Python 3
* Pillow package

# Usage

* Run your game in an emulator without color correction or with color correction disabled (disabling frame blending and shaders is also a good idea)
* Take a screenshot (ideally at 1x zoom or 160x144 resolution)
* Start sxsPaletteTuner `python main.py`
* Load the image into sxsPaletteTuner
* Adjust each of the color correction options to those you'd like to compare
* Tweak the colors present in the image using the color picker, text controls, and sliders provided
* Copy the final palette values in hex for use in your game

# Notes

* This program is completely unaware of the actual GBC palettes (8 background, 8 object), and operates entirely on the image it's provided, therefore it's up to you to figure out which color maps to which palette entry in your game.
* Implementing this in another language, or as an extension of an accurate emulator which is palette aware would likely be far better, but this is the option I went with given time available.
* There may be slight variations in the final hex color values compared to those in a game's source (even when no changes are made) due to rounding operations or how bit 16 is handled in 15bit color values.
