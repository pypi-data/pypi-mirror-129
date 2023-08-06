![Sphinx Bulma Theme](banner.png)
#
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/oAGoulart/sphinx-bulma?display_name=tag&sort=semver)
[![Build Sass](https://github.com/oAGoulart/sphinx-bulma/actions/workflows/sass.yml/badge.svg)](https://github.com/oAGoulart/sphinx-bulma/actions/workflows/sass.yml)
[![CodeQL](https://github.com/oAGoulart/sphinx-bulma/actions/workflows/codeql-analysis.yml/badge.svg?branch=master)](https://github.com/oAGoulart/sphinx-bulma/actions/workflows/codeql-analysis.yml)
[![GitHub Pages deploy](https://github.com/oAGoulart/sphinx-bulma/actions/workflows/gh-pages.yml/badge.svg)](https://github.com/oAGoulart/sphinx-bulma/actions/workflows/gh-pages.yml)

### A simple responsive theme for sphinx using **[Bulma]** featuring:
  1.  Built-in dark/light color themes using native _CSS_ and _JavaScript_
  2.  Sphinx built-in text search engine
  3.  Extended _Sass_ rulesets from **[Bulma]**
  4.  Support for user-defined favicon and logo (sphinx theme config)
  5.  Custom icon font made with **[Fontello]**
  6.  User-defined source repository/files reference
  7.  User-defined primary theme color (custom theme config)

<details>
  <summary><em>Screenshots (big images)</em></summary>
  
  ### YASL (_C++_) light palette
  ![Yasl Light](screenshots/yasl_light.png)
  
  ### YASL (_C++_) dark palette
  ![Yasl Dark](screenshots/yasl_dark.png)
  
  ### Markout (_Python_) light palette
  ![Markout Light](screenshots/markout_light.png)
  
  ### Markout (_Python_) dark palette
  ![Markout Dark](screenshots/markout_dark.png)
  
  ### Sphinx Bulma example light palette
  ![Sphinx Bulma Example Light](screenshots/structure_light.png)
  
  ### Sphinx Bulma example dark palette
  ![Sphinx Bulma Example Dark](screenshots/structure_dark.png)
  
  ### Sphinx Bulma test module light palette
  ![Sphinx Bulma Test Light](screenshots/module_light.png)
  
  ### Sphinx Bulma test module dark palette
  ![Sphinx Bulma Test Dark](screenshots/module_dark.png)
  
</details>

## Installing

Using pip to install this package (recommended using it within a [venv]):

```sh
pip install sphinx-bulma
```

...or alternatively, using [pipenv]:

```
pipenv install sphinx-bulma
```

## Configuration

The theme's project-wide options are defined in the `src/sphinx-bulma/theme.conf` file, and can be defined in your project's `conf.py` via `html_theme_options`. For example:

```py
html_theme_options = {
  'navigation_depth': 2,           # maximum depth of tree
  'includehidden': True,           # if true sidebar may include toctrees marked with hidden option
  'titles_only': False,            # if true removes headers within a page from the sidebar
  'display_git': False,            # if true all git_* options must be set
  'git_host': 'github.com',        # git host url
  'git_user': 'gh-user',           # your git host username
  'git_repo': 'doc-repo',          # doc repository
  'git_blob': 'blob',              # default for github
  'git_version': 'master/docs/',   # docs folder
  'git_icon': 'github',            # icon to show on docs
  'git_desc': 'Check the sources', # link description
  'default_palette': 'dark',       # default color palette (dark or light)
  'sidebar': True,                 # if true sidebar will be rendered
  'primary': '885bfb',             # primary color hex value (do not add preceding #)
  'primary_invert': 'fff'          # primary inverted color hex value (do not add preceding #)
}
```

## Using with Python packages

This example uses [pipenv] to setup everything easily, start by creating a Sphinx config file, here's an example:

path: `myproject/docs/config.py`
```py
import sys
import os
from datetime import datetime

sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath('.'))

extensions = [
  'sphinx.ext.autodoc',
  'sphinx.ext.mathjax',
  'sphinx.ext.viewcode',
]
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'

project = u'myproject'
year = datetime.now().year
copyright = u'%d Augusto Goulart' % year

exclude_patterns = ['_build']

html_theme = 'sphinx-bulma' # don't forget our theme

# this is the pipenv path to the site-packages
html_theme_path = [os.path.join(os.getenv('PIPENV_SITE_PACKAGES', '..').split('\r')[0], 'Lib', 'site-packages')]
```

After that, just run this in your project root dir

path: `myproject`
```sh
pipenv --site-packages --python 3.10
pipenv install sphinx sphinx-bulma
pipenv shell
export PIPENV_SITE_PACKAGES=$(pipenv --venv)
sphinx-build docs docs/_build
```

## Using to document **C++** with **[breathe]**

I mostly use Sphinx to document my C++ code and modules, here's an example of how I set it up, this is best suited for my own devenv (Win32/Win64) so it may not apply to your specific use case.

With that being said, make sure you have Python >= `3.10` and Doxygen >= `1.8` installed.

### Setting up Sphinx `config.py`

First create the sphinx config file in your docs folder (here `docs`):

path: `myproject/docs/config.py`
```py
import sys
import os
from datetime import datetime

sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath('.'))

project = 'myproject'
year = datetime.now().year
copyright = u'%d Augusto Goulart' % year
author = 'Augusto Goulart'
release = '0.1.0'

# don't forget to add breathe as an extension
extensions = ['breathe']

# now configure breathe
breathe_projects = {
  'myproject': 'doxyxml',  # specify where are the Doxygen generated xml files (relative to this dir)
}
breathe_default_project = 'myproject'

# paths config
templates_path = ['_templates']
exclude_patterns = ['_build']

# now configure the sphinx theme and visuals
html_favicon = 'static/favicon.ico'
html_logo = 'static/logo.png'
html_theme = 'sphinx-bulma'    # don't forget this
html_theme_options = {         # add all options you want to overwrite default values here
  'display_git': True,
  'git_host': 'github.com',
  'git_user': 'oAGoulart',
  'git_repo': 'yasl',
  'git_version': 'master/docs/',
  'git_icon': 'github-circled',
  'git_desc': 'Edit on GitHub',
}

# this config is very important so sphinx can find the theme (you'll see why it's that path in short)
html_theme_path = ["../_env/Lib/site-packages"]

# don't forget to specify your static files dir if you use it
html_static_path = ['static']

# some other configs
pygments_style = 'sphinx'
highlight_language = 'c++'
primary_domain = 'cpp'
```

### Setting up our Python build script

Now create another Python file on the same dir for our building script

path: `myproject/docs/build.py`
```py
#!/usr/bin/env python
# Build the documentation.

import errno, os, re, sys
from subprocess import check_call, CalledProcessError, Popen, PIPE, STDOUT

class Pip:
  def __init__(self):
    self.path = os.path.join('_env', 'Scripts', 'pip') # we will be using a venv to install everything

  def install(self, package, commit=None):
    "Install package using pip."
    if commit:
      package = 'git+https://github.com/{0}.git@{1}'.format(package, commit)
    print('Installing {0}'.format(package))
    check_call([self.path, 'install', package])

def install_packages():
  pip = Pip()
  pip.install('sphinx')         # we will need sphinx
  pip.install('breathe')        # ...and also breathe
  pip.install('sphinx-bulma')   # ...and finally our theme

def build_docs():
  doc_dir = os.path.dirname(os.path.realpath(__file__))
  work_dir = '.'
  include_dir = os.path.join(work_dir, 'include')
  # Build doxygen xml.
  cmd = ['.\doxygen.exe', '-']
  p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
  doxyxml_dir = os.path.join(doc_dir, 'doxyxml')
  
  # this is our Doxygen config, I just copy-pasted from one of my projects, change as you need (but keep the xml files)
  out, _ = p.communicate(input=r'''
      PROJECT_NAME      = YASL
      GENERATE_LATEX    = NO
      GENERATE_MAN      = NO
      GENERATE_RTF      = NO
      CASE_SENSE_NAMES  = NO
      INPUT             = {0}/base.h {0}/config.h {0}/memory.h {0}/script.h \
                          {0}/status.h {0}/yasl.h {0}/memory/data.h {0}/memory/patch.h \
                          {0}/memory/peformat.h {0}/memory/protection.h {0}/memory/trampoline.h
      QUIET             = YES
      JAVADOC_AUTOBRIEF = YES
      AUTOLINK_SUPPORT  = NO
      GENERATE_HTML     = NO
      GENERATE_XML      = YES
      XML_OUTPUT        = {1}
      ALIASES           = "rst=\verbatim embed:rst"
      ALIASES          += "endrst=\endverbatim"
      MACRO_EXPANSION   = YES
      PREDEFINED        = _WIN32=1 \
                          __cplusplus=1 \
                          _MSVC_LANG=202002L \
                          _DLL=1
    '''.format(include_dir, doxyxml_dir).encode('UTF-8'))
  out = out.decode('utf-8')
  print(out)
  if p.returncode != 0:
    raise CalledProcessError(p.returncode, cmd)
  
  # Build html docs.
  html_dir = os.path.join(work_dir, '_build')
  check_call([os.path.join(work_dir, '_env', 'Scripts', 'sphinx-build'),
              '-Dbreathe_projects.format=' + os.path.abspath(doxyxml_dir),
              '-b', 'html', doc_dir, html_dir])
  return html_dir

if __name__ == '__main__':
  install_packages()
  build_docs()
```

### Using a batch script to call our build

This step will make your life easier, create a batch script in your project root dir

path: `myproject/docs.bat`
```batch
@ECHO OFF

pushd %~dp0

REM Command file for building documentation

REM you can remove this if you already have doxygen
curl --output doxygen.zip https://www.doxygen.nl/files/doxygen-1.9.2.windows.x64.bin.zip
tar -x -k -f doxygen.zip

REM creates our python virtualenv (used by our build script)
py -m pip install --user virtualenv
py -m venv _env

py .\docs\build.py

popd
```

Now whenever you want to build your docs, just call `.\docs.bat` on terminal

But wait! There's one more thing that can help you, if you want to upload your docs to GitHub Pages, see the next step

### Deploying to GitHub Pages

All you need is to create a new action for your GitHub repo (in `.github/workflows`)

path: `myproject/.github/workflows/gh-pages.yml`
```yml
name: Deploy docs
on:
  push:
    branches: [ master ]

  workflow_dispatch:

jobs:
  build:
    runs-on: windows-latest

    steps:
    - name: Checkout
      uses: actions/checkout@v2
      
    - name: Setup python
      uses: actions/setup-python@v2
      with:
        python-version: 3.10.0
        architecture: x64

    - name: Build
      run: |
        ./docs.bat
        cd _build
        New-Item -Path '.\.nojekyll' -ItemType File
    
    - name: Push site
      uses: actions/upload-artifact@master
      with:
        name: site
        path: _build/
        
  deploy:
    runs-on: ubuntu-latest
    needs: build
    
    steps:
    - name: Pop site
      uses: actions/download-artifact@master
      with:
        name: site
        path: _build/
        
    - name: Deploy to GitHub Pages
      uses: Cecilapp/GitHub-Pages-deploy@v3
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      with:
        email: myemail@mail.org
        build_dir: _build/
```

---

### Contributions

Feel free to leave your contribution here, I would really appreciate it!
Also, if you have any doubts or troubles using this package just contact me or leave an issue.


[Bulma]: https://bulma.io/
[Fontello]: https://fontello.com/
[todo]: /#yet-to-be-done-aka-todo
[breathe]: https://github.com/michaeljones/breathe
[venv]: https://docs.python.org/3/library/venv.html
[pipenv]: https://pypi.org/project/pipenv/
[source]: https://github.com/oAGoulart/yasl
[site]: https://oagoulart.github.io/yasl/
