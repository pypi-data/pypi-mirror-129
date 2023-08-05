# RhubarbPy

**_A sweet and simple python package_**

This package is mainly a staging ground for testing different deployment and build methods for python projects, as well as versioning a project.

## Versioning with `setuptools_scm`

The package version string can be performed automatically using the package `setuptools_scm`. To do this, first configure `setuptools_scm` in your packages `pyproject.toml` folder, look at the packages [README](https://github.com/pypa/setuptools_scm) or look at this project for configuration. Once this is configured, whenever you want to release a new version you must create a new git release tag.  
For example...

```shell
> git tag -a v0.0.3 -m "Release Version 0.0.3"
```

After this, you need to push the tags to the remote using this command.

```shell
> git push --tags
```

At this point, you can check the version of your project using the `get_version()` function from the `setuptools_scm` package.

```shell
> python -c "from setuptools_scm import get_version; print(get_version())"
```
