# tcim - terminal commands in menus
An easy way to call hard to remember or complex terminal commands or scripts from a menu.

## supported menu systems
- dmenu
- xdg desktop menu

## files
`commands.tsv` contains your commands and is located in `~/.config/tcim`.
It can be edited using the menu (see usage) or manually using your favourite text editor.
Since it is a `.tsv` file, you could even use a spreadsheet program like libreoffice calc.

## file format
`commands.tsv` is a tab-separated values file:

    name <tab> comment <tab> command

**example:**

    list filesystems	report file system space usage	df -h

If you don't want to keep the terminal open after the command has finished, prepend the command with `[NOKEEP]`.
If you don't want to run the command in a terminal, prepend the command with `[NOTERM]`.

The command can't contain double quotes `"`.
If you need double quotes, move the command into a script file and use it in the command field.

## installation
    pip install tcim

## usage
### dmenu
Call `tcim-dmenu` to list the available commands in a dmenu.
Currently `xterm` is used to display the result of the command and it is expected to be installed.

### xdg desktop menu
Call `tcim-update-xdg-menu` to update your desktop menu, used by many desktop environments.
Once called, everything (e.g. editing the commands-file) is available from the menu.

## uninstall
`pip uninstall tcim` doesn't uninstall .desktop menu entries created by `tcim-update-xdg-menu`.
You can use this command to get rid of them:

    xdg-desktop-menu uninstall command-menu.directory ~/.local/share/applications/command-*

## todo
- new field for optional working directory
- support more menu systems (e.g. rofi, openbox)
