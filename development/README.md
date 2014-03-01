# Gittip Development Environment

Gittip aims to provide multiplatform support for development via
Vagrant.

## Requirements

While specific versions may not be required, they have been vetted as
working.

  * Vagrant X.Y.Z
  * Virtualbox X.Y.Z

## First-time setup

You should only need to run these commands once, when you first start
using this Vagrant environment.

```
vagrant plugin install vagrant-omnibus
vagrant plugin install vagrant-librarian-chef
```

## Recommended plugins

While not strictly necessary, they will make working with Vagrant a bit
simpler and/or standardized.

  * [vagrant-cachier]() plugin: `vagrant plugin install vagrant-cachier`
