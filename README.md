# CM3142

## Usage

### Requirements

sense-emu (at least on my setup) refused to work with any python version newer
than 3.11 so that is what this project runs on

To start working on the project, run

`python -m venv venv`

This virtual environment will need to be selected every time the project is
going to be ran

VSCode *should* automatically pick up on it. If it doesn't, open terminal and run

Windows
`venv\Scripts\activate`

MacOS/Linux
`source venv/bin/activate`

After that, to build/download all requirements, run

`pip install .`

### Project Structure

All tasks are split up between different modules contained within the `src` folder

Due to python's rules, every folder should contain a `__init__.py` file,
however that file doesn't need to contain anything though

Every directly runnable module should contain a `__main__.py` file

If there are any shared details between modules, they should go in `lib`

To use a module from a different folder, it can be accessed similarly to

`import lib.data_types`

If a change has been made to a module outside of the runnable one, you may need
to rebuild it. This can be done by running `pip install .` again

### Adding new modules

When adding a module via `pip install`, the module name should be added to
`requirements.txt` as to not make project setup annoying
