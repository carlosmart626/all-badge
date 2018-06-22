# All-badge

Script to generate badges based in [coverage-badge](https://github.com/dbrgn/coverage-badge). Generates coverage badge, git tag badge and you can make your own.

Badge styles from [shields.io](https://shields.io)

## Instalation
```bash
pip install all_badge
```

## Examples:

#### Coverage
```bash
all_badge -f -cov -s flat -o cov.svg
```
![15%](https://cdn.rawgit.com/carlosmart626/all-badge/master/media/15.svg)

![45%](https://cdn.rawgit.com/carlosmart626/all-badge/master/media/45.svg)

![65%](https://cdn.rawgit.com/carlosmart626/all-badge/master/media/65.svg)

![80%](https://cdn.rawgit.com/carlosmart626/all-badge/master/media/80.svg)

![93%](https://cdn.rawgit.com/carlosmart626/all-badge/master/media/93.svg)

![97%](https://cdn.rawgit.com/carlosmart626/all-badge/master/media/97.svg)


#### Git
```bash
all_badge -c brightgreen -f -git -s flat -o git.svg
```
![Gitlab example 1](https://cdn.rawgit.com/carlosmart626/all-badge/master/media/git.svg)

```bash
all_badge -c blue -f -git -s flat -o git.svg
```
![Gitlab example 2](https://cdn.rawgit.com/carlosmart626/all-badge/master/media/git-2.svg)

#### Custom
```bash
all_badge -c brightgreen -o version.svg -f -t 'made by' -v Carlosmart -s flat
```

![Custom 1](https://cdn.rawgit.com/carlosmart626/all-badge/master/media/example-custom.svg)

```bash
all_badge -c brightgreen -o version.svg -f -t 'made by' -v Carlosmart -s for-the-baddge
```

![Custom 2](https://cdn.rawgit.com/carlosmart626/all-badge/master/media/example-custom-2.svg)

```bash
all_badge -c brightgreen -f -t 'made by' -v Carlosmart -s flat-square -o media/example-custom-3.svg
```
![Custom 3](https://cdn.rawgit.com/carlosmart626/all-badge/master/media/example-custom-3.svg)

## Usage:
```
usage: all_badge [-h] [-o FILEPATH] [-p] [-f] [-q] [-version] [-git] [-cov]
                 [-t TEXT] [-v VALUE] [-c COLOR] [-s STYLE]

Generate badges

optional arguments:
  -h, --help   show this help message and exit
  -o FILEPATH  Save the file to the specified path.
  -p           Plain color mode. Standard green badge.
  -f           Force overwrite image, use with -o key.
  -q           Don't output any non-error messages.
  --version    Show version.
  -git         Build badge for git tag.
  -cov         Build badge for coverage.
  -t TEXT      Badge text.
  -v VALUE     Badge value.
  -c COLOR     Badge color.
  -s STYLE     Badge style.
```

## Contributing
Install requirements:
```
pip install -e ".[test]"
```
Run tests
```
pytest .
```
