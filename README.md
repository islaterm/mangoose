## Mangoose
This is a python script to download mangas from _mangastream_.
It's a very early build, so don't expect much.
To use it just execute the python script.
By default the mangas are downloaded to `C:/tmp`, you can change that in the 
`downloads_folder` property in the `settings.json` file.

To set which series you want to download just add an entry to the `series` 
property of the json file following the format:
```
<Series name>: {
    "url": <mangastream url>,
    "downloaded_chapters": []
}
```
I included 2 series to the json file as an example.