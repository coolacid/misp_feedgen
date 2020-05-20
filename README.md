# MISP Feed Generator

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/2cabe5b6408d42d28d150e9da29a1644)](https://app.codacy.com/manual/coolacid/misp_feedgen?utm_source=github.com&utm_medium=referral&utm_content=coolacid/misp_feedgen&utm_campaign=Badge_Grade_Dashboard)
[![CodeFactor](https://www.codefactor.io/repository/github/coolacid/misp_feedgen/badge)](https://www.codefactor.io/repository/github/coolacid/misp_feedgen)

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
-f FEEDS, --feeds FEEDS  Comma list of case sensitive feeds  
```

## Existing Modules

### Output Formats
* [MISP Format](https://github.com/coolacid/misp_feedgen/wiki/%5BFormats%5D-MISP)
* [CSV](https://github.com/coolacid/misp_feedgen/wiki/%5BFormats%5D-CSV)
* [Screen](https://github.com/coolacid/misp_feedgen/wiki/%5BFormats%5D-Screen)

### Modifiers
* [Anonymize](https://github.com/coolacid/misp_feedgen/wiki/%5BModifier%5D-Anonymize)

### Post-Hooks
* [Shell](https://github.com/coolacid/misp_feedgen/wiki/%5BHook%5D-Shell)

### Dotty Notation
Some paramaters (where documented) use dotty notation. This makes deeply nested fields accesable in as a text variable.

You can find out more in the [dotty notation](https://github.com/coolacid/misp_feedgen/wiki/Dotty-Notation) wiki page.

## Docker Image

A [docker image](https://hub.docker.com/r/coolacid/misp_feedgen) is provided for use.

The docker image includes 
* cron
* ssh
* rsync
* /entrypoint_cron.sh which launches crond

You can load cron.d tab files by volumemounting them into /etc/cron.d/feedgen

See the example docker-compoase.yml file
