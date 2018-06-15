# Directories with a Home.md are bundled together

When the `smartdownpreview` Sublime Plugin is invoked upon a target file (i.e., the file being edited), the Plugin will detect whether there is a `Home.md` file in the same directory as the target file. If not, then the other `.md` files in the directory will be included in the output HTML. However, without a `Home.md`, the co-located media files (PNG, GIF, SVG, JPG) in the same directory will be ignored, and not bundled with the output.


## Smartdown Tunnels

Using the syntax:

```markdown
[](:@Filename-With-Spaces)
```

we can build a Smartdown Tunnel to the card stored in file `Filename With Spaces.md`.

[Go to Filename-With-Spaces](:@Filename-With-Spaces)
