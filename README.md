[![Test](https://github.com/ianhaddock/motorsort/actions/workflows/test.yml/badge.svg)](https://github.com/ianhaddock/motorsort/actions/workflows/test.yml)
[![Build](https://github.com/ianhaddock/motorsort/actions/workflows/build.yml/badge.svg)](https://github.com/ianhaddock/motorsort/actions/workflows/build.yml)

# MotorSort

Are you a motorsport fan who uses [PLEX Personal Media Server][025] to host your historical content? Frustrated with empty poster images and how often PLEX will auto-parse file names incorrectly? Wish you didn't have to do all that manual work?

MotorSort is a stateless, self contained Docker app that:

* Sorts motorsport files by race series, weekend, and session (including sprint weekends).
* Reformats file names to the PLEX compatible, [Absolute-Series-Scanner][024] convention.
* Hardlinks source files into race series, race weekend directories to save drive space (with an option to copy if you prefer).
* Generates dynamic poster images with event name, country flag, track map, and season event number.

MotorSort was created to automate my least favorite part of curating a Plex media library.

<p align="center">
  <img width="80%" height="auto" src="readme.jpg">
</p>


### Uses:
* Python
* ImageMagick
* Docker
* Pytest


### Usage:

```
docker run \
    -d \
    --name motorsort \
    -e MEDIA_SOURCE_PATH=/mnt/media/downloads/complete \
    -e MEDIA_DESTINATION_PATH=/mnt/media/motorsort \
    -v /mnt/my_files:/mnt/media \
    ghcr.io/ianhaddock/motorsort:latest
```

### Required Parameters:
* `-v <your_media_path>:/mnt/media` This mounts your media to the container at `/mnt/media`.
* `-e MEDIA_SOURCE_PATH` This is the path mounted at /mnt/media the container will search for source files.
* `-e MEDIA_DESTINATION_PATH` This is the path mounted at /mnt/media the container will output files.

Both source and destination need to be on the _same mount point_ (drive) to allow hardlinks. If you want to source from one drive (mountpoint) and output to another drive, use `COPY_FILES='True'` (see below).


### Optional Parameters:
* `-e SLEEP_SECONDS=n` check for new files every _n_ seconds. Defaults to 300 seconds (5 minutes). 
* `-e SLEEP_SECONDS=0` will set the container to run once and quit.
* `-e COPY_FILES='True'` will copy files instead of hardlinking them.
* `-e CONFIG_PATH='path/to/config'` to change config directory path.

### Custom Images:
All images can be customized. To access them, create a local directory and add it as the `/custom` mountpoint on the container:

```
docker run \
    -d \
    --name motorsort \
    -e MEDIA_SOURCE_PATH=/mnt/media/downloads/complete \
    -e MEDIA_DESTINATION_PATH=/mnt/media/motorsort \
    -v /mnt/my_files:/mnt/media \
    -v /mnt/my_files/custom:/custom \
    ghcr.io/ianhaddock/motorsort:latest
```

* When the container starts the custom folder will be populated with image, flag, and track files.
* Any updates made in this directory will be used on the next run.
* To start over: stop the container, erase the local custom folder contents, and start the container again.
* Generated images on the destination path are not overwritten, remove existing show.png and background.jpg images to generate new versions with your changes.

For the best results:
* Poster art should be 600x900 .jpg files and will be reformatted (squished) to fit 600x900 otherwise.
* Background art should be 1920x1080 .jpg files and will be reformatted to fit 1920x1080 otherwise.
* Poster art is selected in order of track name, season, or default. e.g. COTA-poster.jpg, 2022-poster.jpg, poster.jpg.
* Background art is selected in order of track name, season, or default. E.g. COTA-background.jpg, 2022-background.jpg, background.jpg


### Example Logs Output:
```
$ docker logs motorsort
Mon Jun 10 18:20:55 UTC 2024: Starting
Found 166 items to process.
Found 17 sprint weekends.
Creating files.
Background: 2022-00 - Example GP
Poster: 2022-00 - Example GP
Linked: Example GP - S00E01 - Free Practice 1 [FastChannelHD 1080p].mkv
Linked: Example GP - S00E06 - Free Practice 2 [FastChannelHD 1080p].mkv
...
Mon Jun 10 18:20:55 UTC 2024: Sleeping 300 seconds
```

### Example Source Files:
```
/mnt/my_files/downloads/complete/
├── Formula1.2022.Round00.Example.FP1.FastChannelHD.1080p.50fps.X264.Multi-AOA11.mkv
├── Formula1.2022.Round00.Example.FP2.FastChannelHD.1080p.50fps.X264.Multi-AOA11.mkv
├── Formula1.2022.Round00.Example.FP3.FastChannelHD.1080p.50fps.X264.Multi-AOA11.mkv
├── Formula1.2022.Round00.Example.Onboard.Channel.FastChannelHD.1080p.50fps.X264.Multi-AOA11.mkv
├── Formula1.2022.Round00.Example.Quali.Analysis.FastChannelHD.1080p.50fps.X264.Multi-AOA11.mkv
├── Formula1.2022.Round00.Example.Qualifying.Buildup.FastChannelHD.1080p.50fps.X264.Multi-AOA11.mkv
├── Formula1.2022.Round00.Example.Qualifying.FastChannelHD.1080p.50fps.X264.Multi-AOA11.mkv
├── Formula1.2022.Round00.Example.Qualifying.Teds.Notebook.FastChannelHD.1080p.50fps.X264.Multi-AOA11.mkv
├── Formula1.2022.Round00.Example.Race.Analysis.FastChannelHD.1080p.50fps.X264.Multi-AOA11.mkv
├── Formula1.2022.Round00.Example.Race.Buildup.FastChannelHD.1080p.50fps.X264.Multi-AOA11.mkv
├── Formula1.2022.Round00.Example.Race.FastChannelHD.1080p.50fps.X264.Multi-AOA11.mkv
├── Formula1.2022.Round00.Example.Sprint.FastChannelHD.1080p.50fps.X264.Multi-AOA11.mkv
├── Formula1.2022.Round00.Example.Sprint.Shootout.FastChannelHD.1080p.50fps.X264.Multi-AOA11.mkv
├── Formula1.2022.Round00.Example.Teds.Race.Notebook.FastChannelHD.1080p.50fps.X264.Multi-AOA11.mkv
└── Formula1.2022.Round00.Example.Teds.Sprint.Notebook.FastChannelHD.1080p.50fps.X264.Multi-AOA11.mkv
```

### Example Resulting Structure:
```
/mnt/my_files/motorsort/Formula 1/
└── 2022-00 - Example GP
    ├── Example GP - S00E01 - Free Practice 1 [FastChannelHD 1080p 50fps X264 Multi-AOA11].mkv
    ├── Example GP - S00E02 - Quali Buildup [FastChannelHD 1080p 50fps X264 Multi-AOA11].mkv
    ├── Example GP - S00E03 - Qualifying [FastChannelHD 1080p 50fps X264 Multi-AOA11].mkv
    ├── Example GP - S00E04 - Quali Analysis [FastChannelHD 1080p 50fps X264 Multi-AOA11].mkv
    ├── Example GP - S00E05 - Quali Notebook [FastChannelHD 1080p 50fps X264 Multi-AOA11].mkv
    ├── Example GP - S00E06 - Free Practice 2 [FastChannelHD 1080p 50fps X264 Multi-AOA11].mkv
    ├── Example GP - S00E07 - Sprint Shootout [FastChannelHD 1080p 50fps X264 Multi-AOA11].mkv
    ├── Example GP - S00E08 - Sprint [FastChannelHD 1080p 50fps X264 Multi-AOA11].mkv
    ├── Example GP - S00E10 - Sprint Notebook [FastChannelHD 1080p 50fps X264 Multi-AOA11].mkv
    ├── Example GP - S00E11 - Free Practice 3 [FastChannelHD 1080p 50fps X264 Multi-AOA11].mkv
    ├── Example GP - S00E12 - Race Buildup [FastChannelHD 1080p 50fps X264 Multi-AOA11].mkv
    ├── Example GP - S00E13 - Race [FastChannelHD 1080p 50fps X264 Multi-AOA11].mkv
    ├── Example GP - S00E14 - Race Analysis [FastChannelHD 1080p 50fps X264 Multi-AOA11].mkv
    ├── Example GP - S00E15 - Race Notebook [FastChannelHD 1080p 50fps X264 Multi-AOA11].mkv
    ├── Example GP - S00E16 - Onboard Channel [FastChannelHD 1080p 50fps X264 Multi-AOA11].mkv
    ├── background.jpg
    └── show.png
```

### Plex Absolute Series Scanner settings:
[Plex Media Server][025] users should install [Absolute Series Scanner][024]. This will keep Plex from incorrectly sorting files and applying medatata from online sources.

When creating the library:
* select 'TV Shows' as the library type
* use the 'Personal Media Shows' Agent

### Sources:
* Track SVGs from [Wikimedia][021] commons.
* flag images from [lipis.dev][035].
* Poster and Background images created in [Assetto Corsa][022].
* Car models from [Race Sim Studios][023], skins found on [overtake.gg][031].
* [Motion Control Neue][032] font from [ffonts.net][029].
* [Titillium Web][033] from [Google Fonts][034].
* Racing font set from [Smithographic][026] free font collection.
* [Chavelite][027] and [AliciOne Demo][028] from [ffonts.net][029].


### Support:
If you found this useful or would like to support projects like this you can buy me a coffee:

<p align="center">
<a href="https://www.buymeacoffee.com/ianhaddock" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 41px; width: 174px;" ></a>
</p>  

[021]: https://commons.wikimedia.org/w/index.php?fulltext=1&profile=advanced&search=%E3%81%94%E3%81%B2%E3%82%87%E3%81%86%E3%81%86%E3%81%B9%E3%81%93+svg&title=Special%3ASearch&ns0=1&ns6=1&ns12=1&ns14=1&ns100=1&ns106=1
[022]:https://store.steampowered.com/app/244210/Assetto_Corsa/
[023]:https://racesimstudio.com/
[024]:https://github.com/ZeroQI/Absolute-Series-Scanner
[025]:https://www.plex.tv/
[026]:https://imjustcreative.com/category/free-font
[027]:https://www.ffonts.net/Chavelite.font.download
[028]:https://www.ffonts.net/AliciOne-Demo.font.download
[029]:https://www.ffonts.net/
[031]:https://www.overtake.gg/
[032]:https://www.ffonts.net/Motion-Control-Neue-Lite-Bold.font.download
[033]:https://fonts.google.com/specimen/Titillium+Web
[034]:https://fonts.google.com/
[035]:https://flagicons.lipis.dev/
