# MISP Feed Generator

This project aims to be a MISP multi-tool for generating feeds from MISP

## Usage

```  
usage: generate.py [-h] [--debug] [-a | -f FEEDS] config  
  
positional arguments:  
config The configuration file to run  
  
optional arguments:  
-h, --help show this help message and exit  
--debug Debug output  
-a, --all Process all feeds  
-f FEEDS, --feeds FEEDS  Comma list of case sensitve feeds  
```

## Existing Modules

### Output Formats
* [MISP Format](https://github.com/coolacid/misp_feedgen/wiki/%5BFormats%5D-MISP)
* [Screen](https://github.com/coolacid/misp_feedgen/wiki/%5BFormats%5D-Screen)

### Modifiers
* [Anonymize](https://github.com/coolacid/misp_feedgen/wiki/%5BModifier%5D-Anonymize)

