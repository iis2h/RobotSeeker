# RobotSeeker
![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/iis2h/RobotSeeker?label=version)
![GitHub top language](https://img.shields.io/github/languages/top/iis2h/RobotSeeker?color=15E245)



RobotSeeker is a tool that grabs `robots.txt` files from a bunch of subdomains and does the following stuff:

* Generate a wordlist from the words in all the `robots.txt` files. Helpful for fuzzing the same target.
* Map the directories from each `robots.txt` file with its URL.
* Write all the working URLs into one file.

## Why is grabbing robots.txt useful ?
`robots.txt` can include sensitive information and directories intended to be hidden.

## Installation & Usage
#### Installation
``` bash
git clone https://github.com/iis2h/RobotSeeker.git
cd RobotSeeker
pip3 install -r requirements.txt
```
#### Usage
``` bash
robotseeker.py -f Subdomains.txt -mgv -r 3
````
* `-f` : path to the file
* `-m` : Map the content of `robots.txt` to its corresponding URL
* `-g` : Generate a wordlist
* `-v` : Enable verbose output
* `-r` : Requests per second "Default is 3"
* `-h` : Help menu
* `--version` : Display version


## CHANGELOG
| VERSION | UPDATE |
|---|---|
| 1.0.0 | Initial Release |
