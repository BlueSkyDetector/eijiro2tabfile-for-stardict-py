# eijiro2tabfile-for-stardict-py

A converter for converting from eijiro data to tabfile format.
tabfile can be converted to stardict dict format by `tabfile` command in stardict.

## Requirement

- Python 2.7 or 3.x

## Usage

```
$ ./eijiro2tabfile-for-stardict.py -h
usage: eijiro2tabfile-for-stardict.py [-h] -i INPUT -o OUTPUT [-e ENCODE]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input original dictionary file
  -o OUTPUT, --output OUTPUT
                        Output converted tab format dictionary file
  -e ENCODE, --encode ENCODE
                        Character encode of input file (default: "cp932")
```

## Example command

For using `tabfile` command, installing stardict is needed.

```
$ ./eijiro2tabfile-for-stardict.py -i EIJI-141.TXT -o EIJI-141.tab
$ tabfile EIJI-141.tab
```

Then, you can import the generated stardict dict files.
