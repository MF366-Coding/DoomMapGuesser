# DoomMapGuessr
<!--suppress HtmlDeprecatedAttribute, CheckImageSize -->
<img src="assets/Logo.png" alt="DoomMapGuessr's logo" align="right" width="150" height="150">

> **DoomMapGuessr - the geo-guessing game of Doom.** Guess the game, the episode, the map and the exact location...

[![Latest Version](https://img.shields.io/github/v/release/matty-the-dev/DoomMapGuessr?sort=semver&display_name=tag&style=for-the-badge&logo=github&color=red)](https://github.com/matty-the-dev/DoomMapGuessr/releases/latest)
[![License](https://img.shields.io/github/license/matty-the-dev/DoomMapGuessr?style=for-the-badge&color=blue)](https://raw.githubusercontent.com/matty-the-dev/DommMapGuesser/main/LICENSE)
![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/matty-the-dev/DoomMapGuessr/total?style=for-the-badge&logo=github&color=yellow)
![GitHub top language](https://img.shields.io/github/languages/top/matty-the-dev/DoomMapGuessr?style=for-the-badge&logo=.net&logoSize=auto&label=%20&labelColor=purple&color=purple)
<a href="https://mf366.itch.io/doommapguessr"><img src="https://static.itch.io/images/badge-color.svg" alt="Available on itch.io" height="30"></a>
<a href="https://www.moddb.com/games/doommapguessr" title="View DoomMapGuessr on ModDB"><img src="https://button.moddb.com/popularity/medium/games/84847.png" height="30" alt="DoomMapGuessr"></a>

> If you know what DoomMapGuessr is about, and you just want to know how to install, scroll down
> to [Installation](#installation).

## What is DoomMapGuessr?
**DoomMapGuessr** is a **geo-guessing game** where, instead of guessing in which part of
the world you are, you try to guess where the screenshot being shown to you was taken, in the Classic DOOM franchise and
some extra WADs.
DoomMapGuessr allows for fun gameplay with customization settings available, such as being able to pick your own
screenshots and WADs!

### Version 3 *(WIP - coming out soon!)*
Currently in development, version 3 will include several new exciting features, such as:

* **Precision game mode.** Now, instead of having to simply guess what's the game, the episode and the map, you can guess
  exactly where it was taken, and coordinates count! Just drop your pin in the map and see how close you were to the actual location.
* **Inclusion of [Legacy of Rust](https://doomwiki.org/wiki/Legacy_of_Rust).** Legacy of Rust will be included as a game
  in this major update.
* **Language and Accessibility settings.** How awesome would it be to play DoomMapGuessr in your mother tongue? Pretty
  awesome, I think.
* **Achievements and Unlockables.** This is the reward for guessing correctly. The more you guess, the more achievements
  you get! And with achievements, come great rewards...
* **Database Modifications.** Essentially, we moved from JSON to SQLite.
* **Cross-Platform Compatibility.** With the new C# + Avalonia codebase, 99% of platform-specific issues will be
  decimated.
* **And much more!**

**Read more about what's coming to DoomMapGuessr
v3.0.0 [right here](https://www.moddb.com/games/doommapguessr/news/whats-next24)** - we made it to the ModDB homepage!
_(You can also read the same article [here](https://mf366.itch.io/doommapguessr/devlog/1483155/whats-next).)_

## Official Database Contents
The official database contains:

<ul>
<li><strong><a href="https://doomwiki.org/wiki/The_Ultimate_Doom" target="_blank" rel="noopener">The Ultimate DOOM</a></strong></li>
<li><strong><a href="https://doomwiki.org/wiki/Doom_II" target="_blank" rel="noopener">Doom II: Hell on Earth</a></strong></li>
<li><strong><a href="https://doomwiki.org/wiki/Master_Levels_for_Doom_II" target="_blank" rel="noopener">Master Levels for Doom II</a></strong></li>
<li><strong><a href="https://doomwiki.org/wiki/TNT:_Evilution" target="_blank" rel="noopener">Final Doom - TNT: Evilution</a></strong></li>
<li><strong><a href="https://doomwiki.org/wiki/The_Plutonia_Experiment" target="_blank" rel="noopener">Final Doom - The Plutonia Experiment</a></strong></li>
<li><strong><a href="https://doomwiki.org/wiki/Doom_64" target="_blank" rel="noopener">Doom 64</a></strong></li>
<li><strong><a href="https://doomwiki.org/wiki/No_Rest_for_the_Living" target="_blank" rel="noopener">No Rest for the Living</a></strong></li>
<li><strong>Legacy of Rust</strong> (as of version 3)</li>
</ul>

## Find this project on

* [**itch.io**](https://mf366.itch.io/doommapguessr)
* [**ModDB**](https://www.moddb.com/games/doommapguessr)
* [**DoomWorld**](https://www.doomworld.com/forum/topic/146388-doommapguesser-the-geoguesser-of-doom/?tab=comments#comment-2821321)
* and of course, in here, where you can download it!

***

## Installation
DoomMapGuessr can be installed in several ways. Below you can find the most common ways to do so.

### Installer *(recommended)*
You can use the official DoomMapGuessr installer to install it on Windows, macOS *(untested)* and Linux.

**Get the installer at:** [itch.io](https://mf366.itch.io/doommapguessr) |
[ModDB Download Section](https://www.moddb.com/games/doommapguessr/downloads) |
[GitHub Releases](https://github.com/matty-the-dev/DoomMapGuessr/releases/latest)

### Portable Version
If you wish to play DoomMapGuessr without having to install it, but you also don't want to have to go through the boring
process of compiling yourself, the portable version is the best way to play the game. Available for Windows.

**Get the portable version at:** [itch.io](https://mf366.itch.io/doommapguessr) |
[ModDB Download Section](https://www.moddb.com/games/doommapguessr/downloads) |
[GitHub Releases](https://github.com/matty-the-dev/DoomMapGuessr/releases/latest)

### Build it yourself!
You can also build the game yourself, for whatever machine you have *(as long as it supports .NET 10.0)*.

> [!NOTE]
> Detailed instructions on how to build the program yourself coming soon.

You will need to install the [.NET 10.0 SDK](https://dotnet.microsoft.com/download/dotnet/thank-you/sdk-10.0.101-windows-x64-installer). Then run:

```
git clone https://github.com/matty-the-dev/DoomMapGuessr.git
cd src/DoomMapGuessr
dotnet publish -r <rid> -c Release DoomMapGuessr.csproj
```

Once it's done, you'll find the executable somewhere inside `src/DoomMapGuessr/bin`.

> [!WARNING]
> Even though this project supports the usage of Avalonia's **Parcel**, it is recommended to compile it as usual, with
`dotnet publish`.

***

**Made with** :heart: **by Matthew**
