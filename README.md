# RobotSeeker

<p>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/github/license/iis2h/RobotSeeker.svg"></a>
  <a href="https://github.com/iis2h/RobotSeeker/releases"><img src="https://img.shields.io/github/v/tag/iis2h/RobotSeeker?label=version"></a>
  <a href="https://www.python.org"><img src="https://img.shields.io/github/languages/top/iis2h/RobotSeeker?color=15E245"></a>
  <a href="https://github.com/iis2h/RobotSeeker/issues"><img src="https://img.shields.io/badge/contributes-welcome-blue"></a>
</p>

<p>
  <a href="#features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#status">Status</a> •
  <a href="#flags">Flags</a> •
  <a href="#output">Output</a> •
  <a href="https://raw.githubusercontent.com/iis2h/RobotSeeker/main/CHANGELOG.txt">CHANGELOG</a>
</p>


RobotSeeker is fast and reliable python tool that grabs `robots.txt` files from a bunch of subdomains

#### Why is grabbing robots.txt useful ?
`robots.txt` can include sensitive information and endpoints intended to be hidden

## Features

* Write all found `robots.txt` URLs into one file
* Generate a wordlist from the words in all the `robots.txt` files. Helpful for fuzzing the same target
* Map the endpoints from each `robots.txt` with its subdomain

## Installation

```bash
git clone https://github.com/iis2h/RobotSeeker.git &&
cd RobotSeeker &&
pip3 install -r requirements.txt
```

## Usage
### Flags
| Flag | Description
|---|---|
| `-h` | Help menu |
| `-f` | Path to the input file |
| `-m` | Map the content of robots.txt to its corresponding URL |
| `-g` | Generate a wordlist |
| `-r` | Requests per second (Default is 3) *Increasing the rate might affect the result* |
| `-v` | Enable verbose output |
| `-q` | Quite Mode (no banner) |
| `--version` | Display version |

### Status

| Status | Description |
|---|---|
| `[Satus Code]` | HTTP status codes (200, 404, 502 ...) |
| `BLANK` | Either an empty page or a Soft 404 page |
| `ERROR` | Error when trying to connect |

*normal*
```bash
pyhton3 robotseeker.py -f subdomains.txt -m -g
```
```bash
  ___  ___  ___  ___ _____ ___ ___ ___ _  _____ ___
 | _ \/ _ \| _ )/ _ |_   _/ __| __| __| |/ | __| _ \
 |   | (_) | _ | (_) || | \__ | _|| _|| ' <| _||   /
 |_|_\\___/|___/\___/ |_| |___|___|___|_|\_|___|_|_\

 Crafted with Passion by iis2h aka Frenzy

[200]: http://sub.example-1.com/robots.txt
[200]: http://sub.example-2.com/robots.txt
[200]: http://sub.example-3.com/robots.txt
[200]: http://sub.example-4.com/robots.txt
[200]: http://sub.example-5.com/robots.txt
```

*verbos*
```bash
pyhton3 robotseeker.py -f subdomains.txt -m -g -v
```
```bash
  ___  ___  ___  ___ _____ ___ ___ ___ _  _____ ___
 | _ \/ _ \| _ )/ _ |_   _/ __| __| __| |/ | __| _ \
 |   | (_) | _ | (_) || | \__ | _|| _|| ' <| _||   /
 |_|_\\___/|___/\___/ |_| |___|___|___|_|\_|___|_|_\

 Crafted with Passion by iis2h aka Frenzy

[404]: https://sub.example-1.com/robots.txt
[200]: https://sub.example-2.com/robots.txt
[ERROR]: Cannot connect to https://sub.example-3.com
[502]: https://sub.example-4.com/robots.txt
[BLANK]: https://sub.example-5.com/robots.txt
```


### Output
| File | Description | Created When |
|---|---|---|
| valid | Valid URLs | Automatically |
| wordlist | Generated Wordlist | When using `-g` flag |
| mapped | Endpoints Mapped to its Subdomain | When using `-m` flag |

*valid*
<p><img width="500" alt="valid" src="https://github.com/iis2h/RobotSeeker/assets/43062742/4117d68f-21c3-48b9-abac-2370784f2fde"></p>

*wordlist*
<p><img width="500" alt="wordlist" src="https://github.com/iis2h/RobotSeeker/assets/43062742/061146ee-5fa3-4953-9803-09863e14bd2c"></p>

*mapped*
<p><img width="500" alt="mapped" src="https://github.com/iis2h/RobotSeeker/assets/43062742/db0f385f-583f-495d-a8c0-6a6206411b9f"></p>

---
> Your stars greatly support our project ⭐ 
