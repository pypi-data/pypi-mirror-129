# {portion_name} portion of {namespace_name} namespace package

[![GitLab develop](https://img.shields.io/gitlab/pipeline/{namespace_name}-group/{package_name}/develop?logo=python)](
    {repo_url})
[![GitLab release](https://img.shields.io/gitlab/pipeline/{namespace_name}-group/{package_name}/release?logo=python)](
    {repo_url}/-/tree/release)
[![PyPIVersion](https://img.shields.io/pypi/v/{package_name})](
    {pypi_url}/#history)

>this portion belongs to the `Application Environment for Python` - the `{namespace_name}` namespace, which provides
useful classes and helper methods to develop full-featured applications with Python, running on multiple platforms.

[![Coverage]({repo_pages}/{package_name}/coverage.svg)](
    {repo_pages}/{package_name}/coverage/{package_name}_py.html)
[![MyPyPrecision]({repo_pages}/{package_name}/mypy.svg)](
    {repo_pages}/{package_name}/lineprecision.txt)
[![PyLintScore]({repo_pages}/{package_name}/pylint.svg)](
    {repo_pages}/{package_name}/pylint.log)

[![PyPIImplementation](https://img.shields.io/pypi/implementation/{package_name})](
    {pypi_url}/)
[![PyPIPyVersions](https://img.shields.io/pypi/pyversions/{package_name})](
    {pypi_url}/)
[![PyPIWheel](https://img.shields.io/pypi/wheel/{package_name})](
    {pypi_url}/)
[![PyPIFormat](https://img.shields.io/pypi/format/{package_name})](
    {pypi_url}/)
[![PyPIStatus](https://img.shields.io/pypi/status/{package_name})](
    https://libraries.io/pypi/{pip_name})
[![PyPIDownloads](https://img.shields.io/pypi/dm/{package_name})](
    {pypi_url}/#files)


## installation

{TEMPLATE_PLACEHOLDER_ID_PREFIX}{TEMPLATE_INCLUDE_FILE_PLACEHOLDER_ID}{TEMPLATE_PLACEHOLDER_ID_SUFFIX}
    de_icl_README_pre_install.md
{TEMPLATE_PLACEHOLDER_ARGS_SUFFIX}
execute the following command to use the {import_name} {project_type} in your application. it will install {import_name}
into your python (virtual) environment:
 
```shell script
pip install {pip_name}
```

if you want to contribute to this portion then first fork
[the {package_name} repository at GitLab]({repo_url} "{import_name} code repository"). after that pull
it to your machine and finally execute the following command in the root folder of this repository ({package_name}):

```shell script
pip install -e .[dev]
```

the last command will install this {project_type} portion into your virtual environment, along with the tools you need
to develop and run tests or to extend the portion documentation. to contribute to the unit tests or to the documentation
of this portion, replace the setup extras key `dev` in the above command with `tests` or `docs` respectively.


## namespace portion documentation

detailed info on the features and usage of this portion is available at
[ReadTheDocs](https://{namespace_name}.readthedocs.io/en/latest/_autosummary/{import_name}.html#module-{import_name}
"{package_name} documentation").
