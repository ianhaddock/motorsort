# Motorsort 
Organize motorsport videos and create custom poster images. For use with a personal media server.

<p align="center">
  <img width="60%" height="auto" src="readme.jpg">
</p>


### Uses:
* Python
* ImageMagick
* Docker


### What it does:
* Parses source filenames by keyword to sort series, year, race weekend, and event session for both sprint weekends and regular weekends.
* Creates customizable poster images with race name, event number, track map, and race year.
* Creates customizable background images with event number.
* Links files to target directory, saving space and leaving source files unaltered.


### Usage:
In this example source media is located on the host computer at `/mnt/my_files/downloads/complete/` and sorted files will be created in `/mnt/my_files/motorsort/`:

```
docker run \
    -d \
    --name motorsort \
    -e MEDIA_SOURCE_PATH=/mnt/media/downloads/complete \
    -e MEDIA_DESTINATION_PATH=/mnt/media/motorsort \
    -v /mnt/my_files:/mnt/media \
    docker.io/ianhaddock/motorsort
```

### Parameters:
* `-v <your_media_path>:/mnt/media` This mounts your media to the container at `/mnt/media`.
* `-e MEDIA_SOURCE_PATH` This is the path mounted at /mnt/media the container will search for source files.
* `-e MEDIA_DESTINATION_PATH` This is the path mounted at /mnt/media the container will output files.

NOTE:  Both `MEDIA_SOURCE_PATH` and `MEDIA_DESTINATION_PATH` must be on the mount point.


### Optional Parameters:
* `-e SLEEP_SECONDS` Motorsort will check for new files every 5 minutes by default unless changed here. Set to `-e SLEEP_SECONDS=0` if you want the container to run once and quit.
* `-e COPY_FILES` Set this to `-e COPY_FILES=True` if you want Motorsort to copy files instead of hardlinking them (this will take longer and consume more drive space).


### Custom Images:
All images can be customized. To access them, create a local `custom` directory and add it as the `/custom` mountpoint on the container:

```
docker run \
    -d \
    --name motorsort \
    -e MEDIA_SOURCE_PATH=/mnt/media/downloads/complete \
    -e MEDIA_DESTINATION_PATH=/mnt/media/motorsort \
    -v /mnt/my_files:/mnt/media \
    -v ./custom:/custom \
    docker.io/ianhaddock/motorsort
```

* When the container starts the custom folder will be populated with image and track files.
* Any updates made in this directory will be used on the next run.
* To start over: stop the container, erase the local custom folder contents, and start the container again.
* Images are not overwritten on each run, remove any existing show.png and background.jpg files to see your changes.

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


### Notes:
* Track SVGs from [Wikimedia][021]
* Posters and Backgrounds created in [Assetto Corsa][022] using [Race Sim Studios][023] cars with skins found online.
* [Plex Media Server][025] users should select 'TV Shows' as the library type, install the [Absolute Series Scanner][024], and select the 'Personal Media Shows' Agent when creating a library. This will keep Plex from incorrectly sorting files and applying medatata from other sources.


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
