# Directories with a Home.md are bundled together

When the `smartdownpreview` Sublime Plugin is invoked upon a target file (i.e., the file being edited), the Plugin will detect whether there is a `Home.md` file in the same directory as the target file. If so, then the contents of the directory will be included in the output HTML. This includes common media types (PNG, GIF, SVG, JPG) that are located within the directory containing Home.md.

This behavior only occurs when a `Home.md` exists.

## Smartdown Tunnels

Using the syntax:

```markdown
[](:@Other)
```

we can build a Smartdown Tunnel to the card stored in file `Other.md`.

[Go to Other](:@Other)

## Hypercube SVG Remotely

![](/media/hypercube)

## Tickle example with Global mode Syntax

```P5JS/playable/autoplay
var message = "tickle",
  font,
  bounds, // holds x, y, w, h of the text's bounding box
  fontsize = 60,
  x, y; // x and y coordinates of the text

function preload() {
  font = loadFont('https://smartdown.site/gallery/resources/SourceSansPro-Regular.otf');
}

function setup() {
  createCanvas(410, 250);

  // set up the font
  textFont(font);
  textSize(fontsize);

  // get the width and height of the text so we can center it initially
  bounds = font.textBounds(message, 0, 0, fontsize);
  x = width / 2 - bounds.w / 2;
  y = height / 2 - bounds.h / 2;
}

function draw() {
  background(204, 120);

  // write the text in black and get its bounding box
  fill(0);
  text(message, x, y);
  bounds = font.textBounds(message,x,y,fontsize);

  // check if the mouse is inside the bounding box and tickle if so
  if ( mouseX >= bounds.x && mouseX <= bounds.x + bounds.w &&
    mouseY >= bounds.y && mouseY <= bounds.y + bounds.h) {
    x += random(-5, 5);
    y += random(-5, 5);
  }
}
```
