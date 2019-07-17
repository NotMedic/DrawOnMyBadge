// Variables for referencing the canvas and 2dcanvas context
var canvas,ctx;

// Variables to keep track of the mouse position and left-button status
var mouseX,mouseY,mouseDown=0;

// Variables to keep track of the touch position
var touchX,touchY;

var scale=10;

var exampleSocket;

// Draws a dot at a specific position on the supplied canvas name
// Parameters are: A canvas context, the x position, the y position, the size of the dot
function drawDot(ctx,x,y,size) {
    // Let's use black by setting RGB values to 0, and 255 alpha (completely opaque)
    //    r=0; g=0; b=0; a=255;

    //	console.log($(".color").val())

    // ctx.fillStyle = $(".color").val();

    // Select a fill style
    //ctx.fillStyle = "rgba("+r+","+g+","+b+","+(a/255)+")";
    var convertedColor = convertColorToRGB565($(".color").val());

    //	console.log(convertedColor);


    x = Math.floor(x / scale);
    y = Math.floor(y / scale);

    // Draw a filled circle
    // ctx.beginPath();
    // ctx.arc(x, y, size, 0, Math.PI*2, true);
    // ctx.closePath();
    // ctx.fill();
    ////ctx.fillRect(x,y,1,1);

    var jsMessage = {
        CMD: "DRAW",
        DATA: [x, y, `0x${convertedColor}`]
    };

    var message = JSON.stringify(jsMessage);

    console.log(message);

    exampleSocket.send(message);
}

// Clear the canvas context using the canvas width and height
function clearCanvas(canvas,ctx) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    message = 'CLEAR';
    exampleSocket.send(message);
}

function getFrame(){
    message = "FRAME";
    exampleSocket.send(message);
}

// Keep track of the mouse button being pressed and draw a dot at current location
function sketchpad_mouseDown() {
    mouseDown=1;
    drawDot(ctx,mouseX,mouseY,1);
}

// Keep track of the mouse button being released
function sketchpad_mouseUp() {
    mouseDown=0;
}

// Keep track of the mouse position and draw a dot if mouse button is currently pressed
function sketchpad_mouseMove(e) {
    // Update the mouse co-ordinates when moved
    getMousePos(e);

    // Draw a dot if the mouse button is currently being pressed
    if (mouseDown==1) {
        drawDot(ctx,mouseX,mouseY,1);
    }
}

// Get the current mouse position relative to the top-left of the canvas
function getMousePos(e) {
    if (!e)
        var e = event;

    if (e.offsetX) {
        mouseX = e.offsetX;
        mouseY = e.offsetY;
    }
    else if (e.layerX) {
        mouseX = e.layerX;
        mouseY = e.layerY;
    }
}

// Draw something when a touch start is detected
function sketchpad_touchStart() {
    // Update the touch co-ordinates
    getTouchPos();

    drawDot(ctx,touchX,touchY,1);

    // Prevents an additional mousedown event being triggered
    event.preventDefault();
}

// Draw something and prevent the default scrolling when touch movement is detected
function sketchpad_touchMove(e) {
    // Update the touch co-ordinates
    getTouchPos(e);

    // During a touchmove event, unlike a mousemove event, we don't need to check if the touch is engaged, since there will always be contact with the screen by definition.
    drawDot(ctx,touchX,touchY,1);

    // Prevent a scrolling action as a result of this touchmove triggering.
    event.preventDefault();
}

// Get the touch position relative to the top-left of the canvas
// When we get the raw values of pageX and pageY below, they take into account the scrolling on the page
// but not the position relative to our target div. We'll adjust them using "target.offsetLeft" and
// "target.offsetTop" to get the correct values in relation to the top left of the canvas.
function getTouchPos(e) {
    if (!e)
        var e = event;

    if(e.touches) {
        if (e.touches.length == 1) { // Only deal with one finger
            var touch = e.touches[0]; // Get the information for finger #1
            touchX=touch.pageX-touch.target.offsetLeft;
            touchY=touch.pageY-touch.target.offsetTop;
        }
    }
}

function rgb2to3(rgb2) {
    color = parseInt(rgb2, 16);
    var r = ((color >> 11) & 0x1F)*0xff/0x1F;
    var g = ((color >> 5) & 0x3F)*0xff/0x3F;
    var b = ((color) & 0x1F)*0xff/0x1F;

    var rgb = {
        r: Math.round(r),
        g: Math.round(g),
        b: Math.round(b)
    }

    return rgb;
}

function componentToHex(c) {
    var hex = c.toString(16);
    return hex.length == 1 ? "0" + hex : hex;
}

function convertColorToRGB565(color) {
    var match = color.match(/rgba?\((\d{1,3}), ?(\d{1,3}), ?(\d{1,3})\)?(?:, ?(\d(?:\.\d?))\))?/);
    var rgb = {
        r: match[1],
        g: match[2],
        b: match[3]
    }

    var r = (0x1f * rgb.r / 0xff) & 0x1f;
    var g = (0x3f * rgb.g / 0xff) & 0x3f;
    var b = (0x1f * rgb.b / 0xff) & 0x1f;

    var result = b & 0x1f;
    result += ((g & 0x3f) << 5);
    result += (r & 0x1f) << 11;

    return (componentToHex((result >> 8) & 0xff) + componentToHex(result & 0xff)).toUpperCase();
}

function sendWebsocketMessage(element, colourVal) {
    var xCord = $(element).data('xcord');
    var yCord = $(element).parent().data('ycord');
    console.log('xCord: ' + xCord);
    console.log('yCord: ' + yCord);
    var convertedColour = convertColourToRGB565(colourVal);
    console.log('convertedColour: ' + convertedColour);

    var jsMessage = {
        CMD: "DRAW",
        DATA: [
            xCord,
            yCord,
            `0x${convertedColour}`
        ]
    }
    var message = JSON.stringify(jsMessage);
    exampleSocket.send(message);
}