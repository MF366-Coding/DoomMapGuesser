# MAPDAT4 Statistics Report
**Author:** Matthew

**Date:** 13/06/2026 _(DD/MM/YYYY)_

***

## Average Amount of Images per Map
The average amount of images per map is around `2.3` images, a very low number of images when compared with the project's goals.
In fact, even if we ignore the maps with no images, the average is still not looking that great, with it being around `10.6`.

The relative deviation between those two averages (relative to the actual) is very high (`-352%`).
As for the relative deviation between the actual average (`2.3`) and what would be considered the "perfect" average (`20.0`) is pretty high: a `774%` deficit, measured relative to the actual average.

Lastly, the deviation between the image count and the map count is below zero (a deficit), which means that there are less images than there are maps, which goes against the project's goals.

|                                Variable                                |  Value  |
| ---------------------------------------------------------------------- | ------- |
| Average Amount of Images per Map (`x`)                                 | 2.3     |
| Average Amount of Images per Map (ignoring maps with no images, `y`)   | 10.6    |
| Ideal Average Amount of Images per Map (`p`)                           | 20.0    |

| Relative deviation between a and b | Value |   Absolute Value   |
| ---------------------------------- | ----- | ------------------ |
| `x` and `y`, relative to `x`       | -3.52 | 352 %              |
| `x` and `p`, relative to `x`       | -7.74 | 774 %              |

***

## Top 10 Maps by Image Count
The following chart displays the ten maps with the highest image count, with some having the same numeric amount.

The red vertical line marks the recommended minimum amount of images per map (`20`).

The bars were colored green when above the recommended minimum amount and red when below said amount.

<image src="top-10-maps-by-img-count.svg" align="center"></image>

This leads to the conclusion that there are only nine maps that comply with the image count recommendations.

### Maps included in the chart
* **The Ultimate Doom: Knee-Deep In The Dead**
    * E1M1: Hangar
    * E1M2: Nuclear Plant
    * E1M3: Toxin Refinery
* **The Ultimate Doom: Shores of Hell**
    * E2M1: Deimos Anomaly
    * E2M2: Containment Area
    * E2M3: Refinery
    * E2M4: Deimos Lab
* **DOOM II: Hell on Earth**
    * MAP01: Entryway
    * MAP02: Underhalls
* **DOOM 64: Main Campaign**
    * MAP38: Thy Glory

***

## Top 10 Worst Maps by Image Count
The following chart displays the ten maps with the lowest non-zero image count, with some having the same numeric amount.

The red vertical line marks the recommended minimum amount of images per map (`20`).

None of the maps shown in the chart comply with the criteria for their image count to be considered "adequate".

<image src="bottom-10-maps-by-img-count.svg" align="center"></image>

This way, we can easily tell that the maps with the lowest non-zero image count have extremely low image counts, way lower than the recommended minimum amount.

### Maps included in the chart
* **DOOM 64: Main Campaign**
    * MAP09: Even Simpler
    * MAP14: Eye of The Storm
    * MAP17: Watch Your Step
    * MAP19: The Spiral
    * MAP24: No Escape
    * MAP25: Cat And Mouse
    * MAP26: HardCore
    * MAP28: The Absolution
    * MAP30: The Lair
    * MAP39: Final Judgement

***

## Maps by Qualitative Amount of Images
The following pie of a pie chart shows how many maps there are for each qualitative image count.

The image counts considered were:
* No Images (when 0 images)
* Below Recommended (when between 1 and 19 images)
* Recommended (when 20 images)
* Above Recommended (when between 21 and 34 images)
* Too Many (when above 34 images)

<image src="maps-by-qualitative-img-count.svg" align="center"></image>

Despite the extreme amount of maps that lack images, and the equally extreme amount of maps with too few images, the maps that do have images taken after the creation of MAPDAT3 present pretty much perfect amounts of images.

***

Learn how you can help make MAPDAT4 comply with DoomMapGuessr's goals [here](https://github.com/mf366-dev/DoomMapGuessr-Image-Library/blob/main/README.md)!

And, if you go there, check the [TODO file](https://github.com/mf366-dev/DoomMapGuessr-Image-Library/blob/main/TODO.md) as well.
