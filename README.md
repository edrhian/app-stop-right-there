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

- **Name:** It must be unique, it helps you to know which rule is applied to your active window
- **Expression:** The regular expression of the rule, it will trigger the rule if it matches with active window title
- **Enabled:** Applies the rule if true, if not it will be ignored even if the expression matches with the active window title

Your **active window title** is the title of the window that is currently focused, the background windows doesn't count.

### Rule management

You can manage all rules from the **Main Screen**

#### Adding and editing rules

- To add a rule press the binding `a`, this will show a new screen where you will have to fill the fields of the rule.
- To edit a rule, select one and press the binding `e`, you can't edit the title
- You can disable and enable a rule easily by selecting it and pressing `d`, this will switch the state of the rule.

#### Removing rules

- To delete the rule, select one and press the binding `r`, this will popup a confirmation window:
  - Press `esc` to cancel
  - Press `r` again to confirm the deletion

### About Regular Expressions

> For users that doesn't know what Regular Expressions (RegEx) are I recommend these [resources](#resources)

The function that reads regular expressions uses `re.search()`. This method scans through the title looking for a match to the pattern.

For example, having a rule with the expression: **Youtube** will have the following effects on these titles:

- **Chrome**: It won't match
- **Youtube**: It will match
- **Youtube - Home**: It will match
- **Chrome - Youtube**: It will match
- **Chrome - youtube**: It won't match because of the lower case `y`

### Warning Screen

### Window Title Display Screen

### Configuration

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

## Resources

- [Zeeshan Ahmad - Learn Regex The Easy Way](https://github.com/ziishaned/learn-regex): A github repository that explains what is a regular expression and how to build them, it has translations to other languages.
- [Grant Skinner - RegExr](https://regexr.com/): A website that helps to build and test regular expressions.
- [python re library documentation](https://docs.python.org/3/library/re.html): Documentation of the python regular expression library, for developers.
