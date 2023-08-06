[![builds.sr.ht status](https://builds.sr.ht/~supergrizzlybear/gemtide.svg)](https://builds.sr.ht/~supergrizzlybear/gemtide?)

# GemTide

A Jetforce application for serving information about UK tidal events over the Gemini Protocol.

[Take a look](gemini://tides.grizzlybear.site) |
[Report a bug](https://todo.sr.ht/~supergrizzlybear/gmi-sourcehut-lists) | [Contact the author](#contact)

## Built with

* [Jetforce](https://github.com/michael-lazar/jetforce) - framework for writing Gemini applications
* [UKHO Tides](https://github.com/ianByrne/PyPI-ukhotides) - client wrapper for the Admiralty UK Tidal API
* [Jinja2](https://github.com/pallets/jinja/) - templating engine

## Requirements

* Python 3.7 or newer
* API key for the [UK Tidal API](https://admiraltyapi.portal.azure-api.net/docs/services) from Admiralty Maritime Data Solutions Developer Portal. The Discovery subscription is free and provides current plus 6 days' worth of events. Follow the [Start up guide](https://admiraltyapi.portal.azure-api.net/docs/startup) for help.

## Getting Started

### Recommended

Create a virtual environment
```bash
$ mkdir /opt/gemtide
$ python3 -m venv /opt/gemtide/venv
$ python3 -m pip install -U pip
$ . /opt/gemtide/venv/bin/activate
```

### Installation

From pip
```bash
$ pip install gemtide
```

Or, from source
```bash
$ git clone https://git.sr.ht/~supergrizzlybear/gemtide
$ cd gemtide
$ pip install .
```

Create file `config.yaml` and add:
```yaml
api_key: Your UK Tidal API key
station_prefix: (Optional) the path / prefix that the responses will be served with
```

### Usage

Run the application with a default Jetforce server
```bash
$ python3 -m gemtide [config.yaml]
```

Or, if using a virtual environment
```bash
$ /opt/venv/gemtide/bin/gemtide [config.yaml]
```

## Custom Jetforce application

See Jetforce README section on [Virtual Hosting](https://github.com/michael-lazar/jetforce/blob/master/README.md#virtual-hosting) 

### Usage

```python
from jetforce import GeminiServer
from gemtide import GemTideApplication

app = GemTideApplication(api_key, station_prefix="location/")
server = GeminiServer(app)
server.run()
```

## Developing

Create a virtual environment
```bash
$ mkdir /opt/gemtide
$ python3 -m venv /opt/gemtide/venv
$ python3 -m pip install --upgrade pip
$ . /opt/gemtide/venv/bin/activate
```

Clone the repository
```bash
$ git clone git@git.sr.ht:~supergrizzlybear/gemtide
$ cd gemtide
```

Install requirements
```bash
$ pip install -r requrements.txt
```

Test
```bash
$ python3 test_gemtide.py
```

## License

This project is licensed under the [Floodgap Free Software License](https://www.floodgap.com/software/ffsl/license.html).

> The Floodgap Free Software License (FFSL) has one overriding mandate: that software
> using it, or derivative works based on software that uses it, must be free. By free
> we mean simply "free as in beer" -- you may put your work into open or closed source
> packages as you see fit, whether or not you choose to release your changes or updates
> publicly, but you must not ask any fee for it.

## Contact

* Email: supergrizzlybear@protonmail.com
* Mastodon: [@supergrizzlybear@fosstodon.org](https://fosstodon.org/@supergrizzlybear)
* Gemini: [super.grizzlybear.site](gemini://super.grizzlybear.site)
