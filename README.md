# Canvas TUI

A simple TUI for [Canvas LMS](https://github.com/instructure/canvas-lms). It contains most of the important student features of the UI. This now means you can work directly from the TTY, no browser needed.

## Usage

This only works with student accounts. Attempting to access a course you have teacher in may break things.

Either clone the repo, install dependencies with `uv sync`, and run src/main.py, or download the prebuilt binaries from the releases tab and run them. Some distros do not like the binary for some reason and throw a libpython error, so you may need to run from source.

Follow the setup prompts and you are good to go!

## Features

- Browse modules and assignments
- Get your overall grade
- Get/reply to Canvas messages
- Submit assignments using text entry/URL/file upload
- View pages
- View announcements