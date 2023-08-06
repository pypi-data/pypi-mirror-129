# Sistamapy

> Simple statuses Mastodon for Python

This package is compatible with [Pylint](https://www.pylint.org).

# Install 

``` bash
# apt install -y python3 python3-pip python3-setuptools python3-wheel python3-venv python3-dev
```

``` bash
$ python3 -m venv env
$ source ./env/bin/activate
$ pip install sepbit.sistamapy
```

# Credentials

In the [Mastodon](https://joinmastodon.org) account, create an app with `write:statuses` permission

## Usage

This is minimal example, see [statuses](https://docs.joinmastodon.org/methods/statuses).

``` python
from sepbit.sistamapy.statuses import Statuses

self.toot = Statuses(
    'mastodon.social',
    'TOKEN'
)
post = toot.post({
    'status': 'test ',
    'language': 'por',
    'visibility': 'public'
})

print(post)
```

## Tests

Execução de testes e verificar a cobertura de código

``` bash
$ source ./env/bin/activate
$ pip install -r requeriments.txt
$ tox 
```

## Change log 

Please see the [CHANGELOG](CHANGELOG.md) file for more information.

## Contributing 

Pull Requests not accepted.

## Security 

If you discover any security related issues, please email `contato@sepbit.com` instead of using the issue tracker.

## License 

GPL-3.0-or-later, please see [COPYING](COPYING) file for more information.
