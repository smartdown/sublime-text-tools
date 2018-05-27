# sublime-text-tools

## Sublime Text 3 plugin for manipulating and previewing Smartdown

[Sublime Text 3](https://www.sublimetext.com/3) is a code and text editor with a Python-based [API](https://www.sublimetext.com/docs/3/api_reference.html) that can be used to extend functionality via plugins. can be extended via *plugins*.

This repository contains a plugin and supporting files to enable the editing and previewing of [Smartdown](http://smartdown.site/) content. The Smartdown Preview command takes the currently edited Smartdown file and generates a standalone HTML file containing the Smartdown content and the appropriate Smartdown initialization and library code.

## Installation:

Your Sublime Text 3 installation has a `Packages` directory that contains directories for each installed plugin. You will need to install a copy of the `sublime-text-tools` into the Packages directory.

- Using the `Tools` menu command `Command Palette...`, type in the string `Browse Packages` and select the `Preferences: Browse Packages` option. This will reveal the directory containing your Sublime Text plugins.
- For example, on my MacOSX, the above technique reveals the path: `~/Library/Application\ Support/Sublime\ Text\ 3/Packages`.
- Clone, symlink, or otherwise copy, this `sublime-text-tools` repo into your Sublime Text `packages` directory. Make sure that the name of the directory is `sublime-text-tools`.
- Quit and restart Sublime Text (this step may not be necessary).

## Usage

- While viewing a Markdown or Smartdown file, use the `Smartdown/Preview` command via the `Tools` menu or via the default shortcut (`command-option-O` for MacOSX).
- Note that you must use the `Save` command prior to invoking the Smartdown Preview command; the plugin doesn't perform this Save operation automatically (although that feature could be easily added).

### Customization

The key binding that invokes the Smartdown Preview command is specified in the following files:

 - Default (Linux).sublime-keymap
 - Default (OSX).sublime-keymap
 - Default (Windows).sublime-keymap

If the default key binding needs to be changed, edit the appropriate platform-specific file. More info at [Key Bindings](http://docs.sublimetext.info/en/latest/reference/key_bindings.html).

## How it Works

- Detect the currently edited file using Sublime's Plugin API.
- Look in the current file's directory for sibling Smartdown files with a `.md` extension.
- Look in the current file's directory for sibling media files with extensions `.png`, `.jpg`, `.gif`, etc.
- Generate an HTML file into a `~/tmp` directory. This file will contain HTML `<script>` elements of type `application/x-smartdown` for each of the discovered `.md` files.
- These script elements will contain HTML-escaped Smartdown text.
- Encode any discovered media files using `base64` encoding.
- Add Javascript to the generated HTML file. This code will ensure that the encoded script corresponding to the current edited file will be rendered via Smartdown.
- The Javascript will also manage the loading of different encoded Smartdown elements as the user navigates via Smartdown's navigation buttons.

