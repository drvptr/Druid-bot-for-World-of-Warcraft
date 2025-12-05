#include <X11/Xlib.h>
#include <stdio.h>
#include <stdlib.h>
/******************************

 DOES NOT MAKE SENSE!

 IT NOT WORKED!
 
*****************************/


void draw_border(Display *display, Window target_window, int x, int y, int width, int height) {
    XWindowAttributes window_attributes;
    if (XGetWindowAttributes(display, target_window, &window_attributes) == 0) {
        return;
    }
    Window overlay_window = XCreateWindow(display, DefaultRootWindow(display),
                                          0, 0, window_attributes.width, window_attributes.height,
                                          0, CopyFromParent, InputOutput, CopyFromParent, CWOverrideRedirect, NULL);
    XRaiseWindow(display, overlay_window);
    XSetWindowAttributes attributes;
    attributes.override_redirect = True;
    attributes.background_pixel = 0;
    XChangeWindowAttributes(display, overlay_window, CWOverrideRedirect | CWBackPixel, &attributes);
    XClearWindow(display, overlay_window);
    GC gc = XCreateGC(display, overlay_window, 0, NULL);
    if (!gc) {
        return;
    }
    XSetForeground(display, gc, 0xFF0000);
    XDrawRectangle(display, overlay_window, gc, x, y, width, height);
    XFreeGC(display, gc);
    XMapWindow(display, overlay_window);
    XFlush(display);
    sleep(5);
    XDestroyWindow(display, overlay_window);
}

int main(int argc, char *argv[]) {
    if (argc != 6) {
        return 1;
    }
    Window target_window = strtoul(argv[1], NULL, 16);
    int x = atoi(argv[2]);
    int y = atoi(argv[3]);
    int width = atoi(argv[4]);
    int height = atoi(argv[5]);
    Display *display = XOpenDisplay(NULL);
    if (!display) {
        return 1;
    }
    draw_border(display, target_window, x, y, width, height);
    XCloseDisplay(display);

    return 0;
}
