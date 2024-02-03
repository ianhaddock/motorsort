# Racelinks
Automatically organize racing videos into seasons and create custom poster images. For use with a personal media server.

<p align="center">
  <img width="60%" height="auto" src="readme.jpg">
</p>

### Uses:
* Python
* ImageMagick

### What it does:
* Searches a source directory for .mkv or .m4v files
* Parses filenames by keyword to sort by series, weekend, and session. 
* Detects sprint and regular weekends and orders them correctly. 
* Creates poster images with race name, event number, track map, and race year.
* Creates background images with event number.
* Links files to target directory, saving space and leaving source files unaltered.

### Example:

Source files:
```
sourcefiles/
├── Formula1.2022.Round00.Example.FP1.SimSportHD.1080p.mkv
├── Formula1.2022.Round00.Example.FP2.SimSportHD.1080p.mkv
├── Formula1.2022.Round00.Example.FP3.SimSportHD.1080p.mkv
├── Formula1.2022.Round00.Example.Onboard.Channel.SimSportHD.1080p.mkv
├── Formula1.2022.Round00.Example.Quali.Analysis.SimSportHD.1080p.mkv
├── Formula1.2022.Round00.Example.Qualifying.Buildup.SimSportHD.1080p.mkv
├── Formula1.2022.Round00.Example.Qualifying.SimSportHD.1080p.mkv
├── Formula1.2022.Round00.Example.Qualifying.Teds.Notebook.SimSportHD.1080p.mkv
├── Formula1.2022.Round00.Example.Race.Analysis.SimSportHD.1080p.mkv
├── Formula1.2022.Round00.Example.Race.Buildup.SimSportHD.1080p.mkv
├── Formula1.2022.Round00.Example.Race.SimSportHD.1080p.mkv
├── Formula1.2022.Round00.Example.Sprint.Shootout.SimSportHD.1080p.mkv
├── Formula1.2022.Round00.Example.Sprint.SimSportHD.1080p.mkv
├── Formula1.2022.Round00.Example.Teds.Race.Notebook.SimSportHD.1080p.mkv
├── Formula1.2022.Round00.Example.Teds.Sprint.Notebook.SimSportHD.1080p.mkv
```
Resulting structure:
```
mediafiles/Formula 1/2022-00 - Example GP/
├── Example GP - S00E01 - Free Practice 1 [SimSportHD 1080p].mkv
├── Example GP - S00E02 - Quali Buildup [SimSportHD 1080p].mkv
├── Example GP - S00E03 - Qualifying [SimSportHD 1080p].mkv
├── Example GP - S00E04 - Quali Analysis [SimSportHD 1080p].mkv
├── Example GP - S00E05 - Quali Notebook [Teds Notebook SimSportHD 1080p].mkv
├── Example GP - S00E06 - Free Practice 2 [SimSportHD 1080p].mkv
├── Example GP - S00E07 - Sprint Shootout [SimSportHD 1080p].mkv
├── Example GP - S00E08 - Sprint [SimSportHD 1080p].mkv
├── Example GP - S00E10 - Sprint Notebook [Notebook SimSportHD 1080p].mkv
├── Example GP - S00E11 - Free Practice 3 [SimSportHD 1080p].mkv
├── Example GP - S00E12 - Race Buildup [SimSportHD 1080p].mkv
├── Example GP - S00E13 - Race [SimSportHD 1080p].mkv
├── Example GP - S00E14 - Race Analysis [SimSportHD 1080p].mkv
├── Example GP - S00E15 - Race Notebook [Notebook SimSportHD 1080p].mkv
├── Example GP - S00E16 - Onboard Channel [SimSportHD 1080p].mkv
├── background.jpg
└── show.png
```

### Setup:
* Install ImageMagick
* Run the script once to automatically download the needed font files.
* Copy the subdirectory created in fonts/ to your system fonts dirctory (often in /usr/share/fonts/). 
* Edit the config.ini to set your source and destination directories.
* Make sure your user has correct permissions on source (read) and target (read write) directories.
* Run the script.

### Images:
* Track SVGs from [Wikimedia][021]
* Posters and Backgrounds created in [Assetto Corsa][022] using [Race Sim Studios][023] cars with skins found online.

### Notes:
* Poster and background images are unique by year and can be easily customized.
* [Plex Media Server][025] users should select TV Shows as the library type, install the [Absolute Series Scanner][024], and select the 'Personal Media Shows' Agent when creating a library for these files. This will keep Plex from incorrectly matching files to its online medatata sources.
* This script is provided AS-IS with no warranty expressed or implied. Use at your own risk.


[021]: https://commons.wikimedia.org/w/index.php?fulltext=1&profile=advanced&search=%E3%81%94%E3%81%B2%E3%82%87%E3%81%86%E3%81%86%E3%81%B9%E3%81%93+svg&title=Special%3ASearch&ns0=1&ns6=1&ns12=1&ns14=1&ns100=1&ns106=1
[022]:https://store.steampowered.com/app/244210/Assetto_Corsa/
[023]:https://racesimstudio.com/
[024]:https://github.com/ZeroQI/Absolute-Series-Scanner
[025]:https://www.plex.tv/
