# Stop Right There

## About

Stop Right There is a Desktop App for Windows to stop distractions based in your active window title and regular expressions (regex).

## Screenshots

## Table of Contents

## Main Features

- A terminal user interface (TUI) made with Textual framework
- Blacklist windows by writing a regular expression to detect the title of your active window

## Installation

Install the zip and run the StopRightThereApp.exe

## Usage

### Main Screen

The main screens shows your blacklist, a list of rules.

A rule is just a item that determines which windows have to be blacklisted. Each rule has the following attributes:

- Name: It must be unique, it helps you to know which rule is applied to your active window
- Expression: The regular expression of the rule, it will trigger the rule if it matches with active window title
- Enabled: Applies the rule if true, else it will be ignored even if the expression matches with the active window title

### Rule management

- Adding, editing and removing rules
- About expressions
- Warning Screen
- Window title display
- Configuration

## Architecture

- TUI
- File based
- Window Manager

## Building

- Python Version
- Textual Version
- requirements.txt
- .spec

## Contributing

## License
