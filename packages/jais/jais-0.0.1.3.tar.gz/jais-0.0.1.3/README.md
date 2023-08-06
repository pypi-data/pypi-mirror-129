# Just Artificial Intelligence Stuff (JAIS)

# [TODO NEXT]
* add base tests
Before these:
    * init docs
    * update README
Do this:
    * Add confusion matrix visualization at the end of training and validation. Maybe save somewhere?
    * add model saving script
    * add learning rate warmup
    * add learning rate finder
    * automatic batch size finder
    * IMPLEMENT SWA MODEL AND LR_SCHEDULER, see https://pytorch.org/docs/stable/optim.html (GOTO section: Stochastic Weight Averaging)
    * ## FIND THE HYPERPARAMETERS AUTOMATICALLY AND SAVE THEM IN FILE FOR LATER USE

## How to Install (added on 3 Nov 2021, rewrite the README)
### Prerequisites to install Python 3.8 virtual env
```bash
apt update
apt install software-properties-common
add-apt-repository ppa:deadsnakes/ppa
apt update
apt install python3.8 python3.8-venv python3.8-dev
```
### Create a virtual env
```bash
make make_venv
```

## Start here (copy-paste these commands):
1. create a virtual env and install base packages

    Running `make` command will create, install requirements from `requirements_base.txt` file, and install this project in editable mode
```bash
    make
    source venv/bin/activate
```

2. Use sphinx to make documentation. The base template files are given in the `docs` folder. Refer them. Some sources for errors in sphinx - [sphinx-docs](https://www.sphinx-doc.org/en/master/tutorial/index.html), [fix 1](https://stackoverflow.com/questions/13516404/sphinx-error-unknown-directive-type-automodule-or-autoclass).

    * create docs:
    ```bash
        sphinx-quickstart docs
    ```
    * say yes to this: `> Separate source and build directories (y/n) [n]: y`
    * Then
    ```bash
        cd docs
        sphinx-build -b html source/ build/html
        sphinx-apidoc -o source/ ../myproj --force
        make html
    ```
    * Add these to `docs/source/conf.py` for Google style documentation. See example [here](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html).
    ```python
        extensions = [
            'sphinx.ext.duration',
            'sphinx.ext.autodoc',
            'sphinx.ext.napoleon'
        ]
        # Napoleon settings
        napoleon_google_docstring = True
        napoleon_numpy_docstring = False
        napoleon_include_init_with_doc = False
        napoleon_include_private_with_doc = False
        napoleon_include_special_with_doc = True
        napoleon_use_admonition_for_examples = False
        napoleon_use_admonition_for_notes = False
        napoleon_use_admonition_for_references = False
        napoleon_use_ivar = False
        napoleon_use_param = True
        napoleon_use_rtype = True
        napoleon_preprocess_types = False
        napoleon_type_aliases = None
        napoleon_attr_annotations = True

        # Documentation theme
        html_theme = 'furo'
    ```

3. Add any other specification command to Makefile.
