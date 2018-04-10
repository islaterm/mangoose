# Mangoose
This is a python script to download mangas from _mangastream_.
It's a very early build, so don't expect much.
To use it just execute the python script with the commands specified in the 
help section.
By default the mangas are downloaded to `C:/tmp`, you can change by passing the
argument `--SetDownloadFolder "path/to/folder"` to the script.

To set which series you want to download just add an entry to the downloads list
by passing the argument `--NewSeries "Series Name" "Mangastream URL"` to the 
script.

You can also call the script with the `-h` command to get more detailed info 
about the parameters that can be given to the script.

## Some use examples of the script:
In the following examples I will be using the short version of the commands, 
call the help command for more detailed info.
```
python3 mangoose.py -h
```
This will show a message with help.
```
python3 mangoose.py -d "D:\Downloads\Downloaded Manga" -n "A Trail of Blood" "https://readms.net/manga/a_trail_of_blood"
```
This will set the downloads folder and will add A Trail of Blood to be 
downloaded (note that it will not be downloaded until you run the script again).
```
python3 mangoose.py -a -l
```
This will download all the manga previously added and create a log file with 
execution info.