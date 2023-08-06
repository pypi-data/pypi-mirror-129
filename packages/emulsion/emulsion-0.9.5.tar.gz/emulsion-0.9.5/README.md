EMuLSion - Quick Start
======================

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table of Contents**

- [EMuLSion - Quick Start](#emulsion---quick-start)
    - [Part A - General information](#part-a---general-information)
    - [Part B - Requirements](#part-b---requirements)
        - [1. Install [GIT](https://git-scm.com)](#1-install-githttpsgit-scmcom)
        - [2. Install a [Python 3](https://docs.python.org/3/) environment with required modules](#2-install-a-python-3httpsdocspythonorg3-environment-with-required-modules)
            - [Recommended: local Anaconda configuration](#recommended-local-anaconda-configuration)
            - [Alternative: regular Python3 install](#alternative-regular-python3-install)
        - [3. Install [Graphviz](http://www.graphviz.org) (**recommended**)](#3-install-graphvizhttpwwwgraphvizorg-recommended)
        - [4. Install [R](https://www.r-project.org) (**optional**)](#4-install-rhttpswwwr-projectorg-optional)
        - [5. Install [Doxygen](http://www.stack.nl/~dimitri/doxygen/) (**optional**)](#5-install-doxygenhttpwwwstacknldimitridoxygen-optional)
    - [Part C - Installation of the Emulsion framework](#part-c---installation-of-the-emulsion-framework)
        - [1. Clone the EMuLSion repository](#1-clone-the-emulsion-repository)
        - [2. Add the current repository to your `PYTHONPATH` environment variable](#2-add-the-current-repository-to-your-pythonpath-environment-variable)
    - [Part D - Test your installation](#part-d---test-your-installation)
    - [Part E - Generate the API documentation (optional)](#part-e---generate-the-api-documentation-optional)
    - [Part F - Content of the repository](#part-f---content-of-the-repository)

<!-- markdown-toc end -->


Part A - General information
----------------------------

EMuLSion is a framework with a _Domain-Specific Language_ to design
multi-level epidemiological models. Several classical paradigms are
encompassed within a multi-level agent-based approach. Knowledge and
expertise concerns are clearly separated from the procedural concerns,
so as to make all assumptions explicit and easily revisable, and to
automatize as much as possible their implementation.

- **Version 0.9.5**
- **Licence:** CeCILL B (to confirm)
- **Authors:**
  - Sébastien Picault (`sebastien.picault@oniris-nantes.fr`)
  - Yu-Lin Huang
  - Vianney Sicard
  - Pauline Ezanno (`pauline.ezanno@oniris-nantes.fr`)


Part B - Requirements
---------------------

### 1. Install [GIT](https://git-scm.com)

The current version of EMuLSion is available only through a GIT
repository.

```
sudo apt install git
```


### 2. Install a [Python 3](https://docs.python.org/3/) environment with required modules

#### Recommended: local Anaconda configuration

[Anaconda](https://www.anaconda.com) is a comprehensive distribution
for scientific computing and data science. Install the version
corresponding to your operating system.

For Linux, go to `https://repo.continuum.io/archive/` to get the
latest version of Anaconda. Update the `ANACONDA_VERSION` variable
below, then:

```
export ANACONDA_VERSION=5.0.1     # keep this up to date!
wget https://repo.continuum.io/archive/Anaconda3-$ANACONDA_VERSION-Linux-x86_64.sh
sh Anaconda3-$ANACONDA_VERSION-Linux-x86_64.sh
```

Accept the licence and default answers. Thus, Anaconda will be
installed in `~/anaconda3`

Ensure that your `PATH` variable is up to date:

```
source ~/.bashrc
```

Now install additional required modules:

```
pip install progressbar2 ggplot docopt textx utm

```

#### Alternative: regular Python3 install
In that case, you will have **many additional modules to install**!

```
sudo apt install python3 python3-tk
```

Install the required modules as shown below:

```
# first upgrade the module installer
python3 -m pip3 install --upgrade pip
# install the notebooks (jupyter)
python3 -m pip3 install jupyter
# install modules used by EMuLSion framework
sudo pip3 install numpy scipy matplotlib sympy pandas
sudo pip3 install docopt jinja2 textX
sudo pip3 install sortedcontainers progressbar2 pyyaml
sudo pip3 install cython setuptools
sudo pip3 install ggplot sqlalchemy utm
```

### 3. Install [Graphviz](http://www.graphviz.org) (**recommended**)

Graphviz is a flexible graph drawing tool, used by EMuLSion to draw
state machines. If you choose not to install Graphviz, some output
features will not be available.

```
sudo apt install graphviz
```

### 4. Install [R](https://www.r-project.org) (**optional**)

R is used with package `ggplot` for some visualization scripts.

```
sudo apt install r-base r-dev
sudo R --no-save -e 'install.packages("ggplot2", repos="http://cran.r-project.org")'
```

### 5. Install [Doxygen](http://www.stack.nl/~dimitri/doxygen/) (**optional**)

Doxygen is used for API documentation generation.

```
sudo apt install doxygen
pip install doxypypy # or sudo pip3 install doxypypy
```


Part C - Installation of the Emulsion framework
-----------------------------------------------

### 1. Clone the EMuLSion repository

First create a directory for GIT repositories.

```
export GIT_REPO=~/git    # choose any directory
mkdir -p "$GIT_REPO"
cd "$GIT_REPO"
git clone beorn:/git/EMuLSion
cd EMuLSion
```

### 2. Add the current repository to your `PYTHONPATH` environment variable

Type in the shell:

```
export PYTHONPATH=`pwd`/src
```

This allows Python to search for modules in the `src` directory of
EMuLSion repository. To make it persistent, add the line above to your
shell initialization file as follows:

```
echo "export PYTHONPATH=$(pwd)/src" >>~/.bashrc
```


Part D - Test your installation
-------------------------------

EMuLSion comes as an executable Python package. All possible commands
and options are documented through the `--help` option:


```
cd "$GIT_REPO/EMuLSion"
python3 -m emulsion --help

```

Of course you can define an **alias** for executing the package (and
you can also add this alias to your `.bashrc`):

```
alias emulsion='python3 -m emulsion'
```


The **Quickstart** model is aimed at verifying that the framework is
operational. Below are a few examples to test it.

```
# run a simulation, generate the graph of the state machines
emulsion run config/quickstart.yaml --view-machines \
	--output-dir outputs/quickstart --figure-dir img/quickstart

# check what you get in outputs
ls outputs/quickstart

# check what you get in img
ls img/quickstart

# plot figures for the last experiment
emulsion plot config/quickstart.yaml \
	--output-dir outputs/quickstart  --figure-dir img/quickstart

# show parameters
emulsion show config/quickstart.yaml

# run the simulation with other parameters
# only 10 steps per run
emulsion run config/quickstart.yaml --time 10 \
	--output-dir outputs/quickstart
# change time step to 28 days (instead of 7 in YAML file)
emulsion run config/quickstart.yaml \
	--output-dir outputs/quickstart -p delta_t=28
# change other parameter
emulsion run config/quickstart.yaml \
	--output-dir outputs/quickstart -p quarantine_size=50

# test the reproducibility of the simulations
emulsion run --seed 666 --output-dir outputs/quickstart
mv outputs/quickstart/counts.csv outputs/quickstart/counts1.csv
emulsion run --seed 666 --output-dir outputs/quickstart
diff -s outputs/quickstart/counts.csv outputs/quickstart/counts1.csv

```


Part E - Generate the API documentation (optional)
--------------------------------------------------

Using `doxygen`, type:

```
doxygen doxygen.config
```

Part F - Content of the repository
----------------------------------
- For Users

  | File name    | Role                                                          |
  |--------------|---------------------------------------------------------------|
  | `README.md`  | This file                                                     |
  | `src/`       | Sources of the Python framework (emulsion module)             |
  | `config/`    | Location of YAML model description files                      |
  | `notebooks/` | Location for Jupyter notebooks, used for tests                |
  | `data/`      | Location for model input data                                 |
  | `doc/`       | Location for technical report and framework API documentation |

- For Developers

  | File name        | Role                                                            |
  |------------------|-----------------------------------------------------------------|
  | `scripts/`       | Location for (shell/R) utility scripts and syntactic rules      |
  | `outputs/`       | Location for model outputs                                      |
  | `img/`           | Location for image files (plots, maps...)                       |
  | `lib/`           | Location for storing compiled libraries                         |
  | `TODO.org`       | A small short-term roadmap                                      |
  | `doxygen.config` | Configuration file for Doxygen                                  |
  | `SCHEMA.yaml`    | An experimental description of the YAML schema for valid models |
  | `setup.py`       | Configuration file for building a distribution (experimental)   |

-----
_Last update: 2018-03-09, S. Picault (`sebastien.picault@oniris-nantes.fr`)_
