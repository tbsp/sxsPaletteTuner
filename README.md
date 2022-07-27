# Side-by-Side PaletteTuner
A simple program to tune Game Boy Color palettes for a variety of screen types.

Originally Game Boy Color games only had to worry about how they looked on an actual GBC LCD (though even those had more variation than most people know). Later came the Game Boy Advance, Game Boy Player, and now after-market screen mods, not to mention emulators with a varity of ways of displaying colors.

I made this tool as a means of fairly quickly finding colors which should look alright on a range of screens/emulators, base on the color correction methods from [SameBoy](https://github.com/LIJI32/SameBoy).

# How to Use

* Run your game in an emulator without color correction or with color correction disabled (disabling frame blending and shaders is also a good idea)
* Take a screenshot (ideally at 1x zoom or 160x144 resolution)
* Load the image into sxsPaletteTuner
* Adjust each of the 3 color correction options to those you'd like to compare
* Tweak the colors present in the image using the color picker, text controls, and sliders provided
* Copy the final palette values in hex for use in your game

![screenshot](https://user-images.githubusercontent.com/10489588/181376306-ae62d9f3-c4ee-4e77-9778-2b433e150a86.png)

# Notes

* This program is completely unaware of the actual GBC palettes (8 background, 8 object), and operates entirely on the image it's provided
* It's up to you to figure out which color maps to which palette entry in your game
