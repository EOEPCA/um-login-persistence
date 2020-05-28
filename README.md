<!--
***
*** To avoid retyping too much info. Do a search and replace for the following:
*** um-login-persistence
-->

<!-- PROJECT SHIELDS -->
<!--
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
![Build][build-shield]

<!-- PROJECT LOGO -->
<br />
<p align="center">

  <h3 align="center">um-login-persistence</h3>

  <p align="center">
    EOEPCA Persistence system for the Login Service Building Block
    <br />
    <a href="https://github.com/EOEPCA/um-login-persistence"><strong>Explore the docs »</strong></a>
    <br />
    <a href="https://github.com/EOEPCA/um-login-persistence">View Demo</a>
    ·
    <a href="https://github.com/EOEPCA/um-login-persistence/issues">Report Bug</a>
    ·
    <a href="https://github.com/EOEPCA/um-login-persistence/issues">Request Feature</a>
  </p>
</p>

## Table of Contents

- [Table of Contents](#table-of-contents)
- [About The Project](#about-the-project)
  - [Built With](#built-with)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Initializing Data](#initializing-data)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
- [Acknowledgements](#acknowledgements)

<!-- ABOUT THE PROJECT -->

## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

### Built With

- [Python](https://www.python.org//)
- [PyTest](https://docs.pytest.org)
- [YAML](https://yaml.org/)
- [Travis CI](https://travis-ci.com/)

<!-- GETTING STARTED -->

## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.

- [Docker](https://www.docker.com/)
- [Python](https://www.python.org//)

### Installation

1. Get into EOEPCA's development environment

```sh
vagrant ssh
```

3. Clone the repo

```sh
git clone https://github.com/EOEPCA/um-login-persistence.git
```

4. Change local directory

```sh
cd template-service
```

## Usage


The following environment variables are supported by the container:

- `GLUU_CONFIG_ADAPTER`: The config backend adapter, can be `consul` (default) or `kubernetes`.
- `GLUU_CONFIG_CONSUL_HOST`: hostname or IP of Consul (default to `localhost`).
- `GLUU_CONFIG_CONSUL_PORT`: port of Consul (default to `8500`).
- `GLUU_CONFIG_CONSUL_CONSISTENCY`: Consul consistency mode (choose one of `default`, `consistent`, or `stale`). Default to `stale` mode.
- `GLUU_CONFIG_CONSUL_SCHEME`: supported Consul scheme (`http` or `https`).
- `GLUU_CONFIG_CONSUL_VERIFY`: whether to verify cert or not (default to `false`).
- `GLUU_CONFIG_CONSUL_CACERT_FILE`: path to Consul CA cert file (default to `/etc/certs/consul_ca.crt`). This file will be used if it exists and `GLUU_CONFIG_CONSUL_VERIFY` set to `true`.
- `GLUU_CONFIG_CONSUL_CERT_FILE`: path to Consul cert file (default to `/etc/certs/consul_client.crt`).
- `GLUU_CONFIG_CONSUL_KEY_FILE`: path to Consul key file (default to `/etc/certs/consul_client.key`).
- `GLUU_CONFIG_CONSUL_TOKEN_FILE`: path to file contains ACL token (default to `/etc/certs/consul_token`).
- `GLUU_CONFIG_KUBERNETES_NAMESPACE`: Kubernetes namespace (default to `default`).
- `GLUU_CONFIG_KUBERNETES_CONFIGMAP`: Kubernetes configmaps name (default to `gluu`).
- `GLUU_CONFIG_KUBERNETES_USE_KUBE_CONFIG`: Load credentials from `$HOME/.kube/config`, only useful for non-container environment (default to `false`).
- `GLUU_SECRET_ADAPTER`: The secrets adapter, can be `vault` or `kubernetes`.
- `GLUU_SECRET_VAULT_SCHEME`: supported Vault scheme (`http` or `https`).
- `GLUU_SECRET_VAULT_HOST`: hostname or IP of Vault (default to `localhost`).
- `GLUU_SECRET_VAULT_PORT`: port of Vault (default to `8200`).
- `GLUU_SECRET_VAULT_VERIFY`: whether to verify cert or not (default to `false`).
- `GLUU_SECRET_VAULT_ROLE_ID_FILE`: path to file contains Vault AppRole role ID (default to `/etc/certs/vault_role_id`).
- `GLUU_SECRET_VAULT_SECRET_ID_FILE`: path to file contains Vault AppRole secret ID (default to `/etc/certs/vault_secret_id`).
- `GLUU_SECRET_VAULT_CERT_FILE`: path to Vault cert file (default to `/etc/certs/vault_client.crt`).
- `GLUU_SECRET_VAULT_KEY_FILE`: path to Vault key file (default to `/etc/certs/vault_client.key`).
- `GLUU_SECRET_VAULT_CACERT_FILE`: path to Vault CA cert file (default to `/etc/certs/vault_ca.crt`). This file will be used if it exists and `GLUU_SECRET_VAULT_VERIFY` set to `true`.
- `GLUU_SECRET_KUBERNETES_NAMESPACE`: Kubernetes namespace (default to `default`).
- `GLUU_SECRET_KUBERNETES_CONFIGMAP`: Kubernetes secrets name (default to `gluu`).
- `GLUU_SECRET_KUBERNETES_USE_KUBE_CONFIG`: Load credentials from `$HOME/.kube/config`, only useful for non-container environment (default to `false`).
- `GLUU_WAIT_MAX_TIME`: How long the startup "health checks" should run (default to `300` seconds).
- `GLUU_WAIT_SLEEP_DURATION`: Delay between startup "health checks" (default to `10` seconds).
- `GLUU_OXTRUST_CONFIG_GENERATION`: Whether to generate oxShibboleth configuration or not (default to `true`).
- `GLUU_CACHE_TYPE`: Supported values are `IN_MEMORY`, `REDIS`, `MEMCACHED`, and `NATIVE_PERSISTENCE` (default to `NATIVE_PERSISTENCE`).
- `GLUU_REDIS_URL`: URL of Redis server, format is host:port (optional; default to `localhost:6379`).
- `GLUU_REDIS_TYPE`: Redis service type, either `STANDALONE` or `CLUSTER` (optional; default to `STANDALONE`).
- `GLUU_MEMCACHED_URL`: URL of Memcache server, format is host:port (optional; default to `localhost:11211`).
- `GLUU_PERSISTENCE_TYPE`: Persistence backend being used (one of `ldap`, `couchbase`, or `hybrid`; default to `ldap`).
- `GLUU_PERSISTENCE_LDAP_MAPPING`: Specify data that should be saved in LDAP (one of `default`, `user`, `cache`, `site`, or `token`; default to `default`). Note this environment only takes effect when `GLUU_PERSISTENCE_TYPE` is set to `hybrid`.
- `GLUU_PERSISTENCE_SKIP_EXISTING`: skip initialization if backend already initialized (default to `True`).
- `GLUU_LDAP_URL`: Address and port of LDAP server (default to `localhost:1636`); required if `GLUU_PERSISTENCE_TYPE` is set to `ldap` or `hybrid`.
- `GLUU_COUCHBASE_URL`: Address of Couchbase server (default to `localhost`); required if `GLUU_PERSISTENCE_TYPE` is set to `couchbase` or `hybrid`.
- `GLUU_COUCHBASE_USER`: Username of Couchbase server (default to `admin`); required if `GLUU_PERSISTENCE_TYPE` is set to `couchbase` or `hybrid`.
- `GLUU_COUCHBASE_CERT_FILE`: Couchbase root certificate location (default to `/etc/certs/couchbase.crt`); required if `GLUU_PERSISTENCE_TYPE` is set to `couchbase` or `hybrid`.
- `GLUU_COUCHBASE_PASSWORD_FILE`: Path to file contains Couchbase password (default to `/etc/gluu/conf/couchbase_password`); required if `GLUU_PERSISTENCE_TYPE` is set to `couchbase` or `hybrid`.
- `GLUU_OXTRUST_API_ENABLED`: Enable oxTrust API (default to `false`).
- `GLUU_OXTRUST_API_TEST_MODE`: Enable oxTrust API test mode; not recommended for production (default to `false`). If set to `false`, UMA mode is activated. See [oxTrust API docs](https://gluu.org/docs/oxtrust-api/4.1/) for reference.
- `GLUU_CASA_ENABLED`: Enable Casa-related features; custom scripts, ACR, UI menu, etc. (default to `false`).
- `GLUU_PASSPORT_ENABLED`: Enable Passport-related features; custom scripts, ACR, UI menu, etc. (default to `false`).
- `GLUU_RADIUS_ENABLED`: Enable Radius-related features; UI menu, etc. (default to `false`).
- `GLUU_SAML_ENABLED`: Enable SAML-related features; UI menu, etc. (default to `false`).


## Initializing Data

kubectl run  --image=eoepca/um-login-persistence:latest persistence --env="GLUU_CONFIG_ADAPTER=kubernetes"     --env="GLUU_SECRET_ADAPTER=kubernetes"     --env="GLUU_OXTRUST_CONFIG_GENERATION=false"     --env="GLUU_LDAP_URL=opendj:1636"     --env="GLUU_PASSPORT_ENABLED=true" --env="GLUU_PERSISTENCE_TYPE=ldap"

The process may take a while, check the output of the `persistence` container log.

## Roadmap

See the [open issues](https://github.com/EOEPCA/um-login-persistence/issues) for a list of proposed features (and known issues).

<!-- CONTRIBUTING -->

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- LICENSE -->

## License

Distributed under the Apache-2.0 License. See `LICENSE` for more information.

## Contact

[EOEPCA mailbox](eoepca.systemteam@telespazio.com)

Project Link: [https://github.com/EOEPCA/um-login-persistence](https://github.com/EOEPCA/um-login-persistence)

## Acknowledgements

- README.md is based on [this template](https://github.com/othneildrew/Best-README-Template) by [Othneil Drew](https://github.com/othneildrew).


[contributors-shield]: https://img.shields.io/github/contributors/EOEPCA/um-login-persistence.svg?style=flat-square
[contributors-url]: https://github.com/EOEPCA/um-login-persistence/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/EOEPCA/um-login-persistence.svg?style=flat-square
[forks-url]: https://github.com/EOEPCA/um-login-persistence/network/members
[stars-shield]: https://img.shields.io/github/stars/EOEPCA/um-login-persistence.svg?style=flat-square
[stars-url]: https://github.com/EOEPCA/um-login-persistence/stargazers
[issues-shield]: https://img.shields.io/github/issues/EOEPCA/um-login-persistence.svg?style=flat-square
[issues-url]: https://github.com/EOEPCA/um-login-persistence/issues
[license-shield]: https://img.shields.io/github/license/EOEPCA/um-login-persistence.svg?style=flat-square
[license-url]: https://github.com/EOEPCA/um-login-persistence/blob/master/LICENSE
[build-shield]: https://www.travis-ci.com/EOEPCA/um-login-persistence.svg?branch=master
