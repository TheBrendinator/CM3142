# CM3142

## Important

It appears sense-emu doesn't work under Windows

MacOS has not been tested yet

It works fine under Linux (Which the pi's run on)

## Usage

### Requirements

Sense-emu has issues with certain versions of python packages

The tested and confirmed working setup uses Python 3.11.15

### Setup

Clone the project as usual

Open a terminal window inside the project directory and run

`python -m venv venv`

This will create a folder where the project can be built and ran

This is necessary due to how the modules have been broken up, otherwise it
would mess up the global python installation

VSCode should automatically pick up on the virtual environment, however if it doesn't:

Open a terminal and run:

Windows
`venv\Scripts\activate`

MacOS/Linux
`source venv/bin/activate`

After that, run

`pip install .`

### Project Structure

All tasks are split up between different modules contained within the `src` folder

Due to python's build rules, every folder should contain a `__init__.py` file,
however that file doesn't need to contain anything though. This might be
outdated information but it worked after I did it so I'm leaving it

Every directly runnable module should contain a `__main__.py` file

If there are any shared details between modules, they should go in `lib`

To use a module from a different folder, it can be accessed like so:

`import lib.data_types`

If a change has been made to a module outside of the runnable one, you may need
to rebuild it. This can be done by running `pip install .` again

### Adding new modules

If any modules need to be installed, add them to the dependency list in `pyproject.toml`

## Commit Formatting

This isn't necessary to follow but I enjoy a clean commit history

docs: Documentation only changes
feat: A new feature
fix: A bug fix
perf: A code change that improves performance
refactor: A code change that neither fixes a bug nor adds a feature
style: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
chore: Any changes unrelated to code
