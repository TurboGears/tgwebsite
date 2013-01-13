TODO:
- Add search box on site template. Include doc page inventories for searching
- Cogbin issues: Those need to be fixed. It should be more obvious that the keywords are clickable links to get to the right tables. It's not, and that's bad styling, I admit.
- The color changes for the menu items: Support for :static and :hover is currently broken. Needs to be fixed.

README:

New directive: youtube. See documentation below.

YOUTUBE:

sphinxcontrib.youtube
=====================

This module defines a directive, `youtube`.  It takes a single, required
argument, a YouTube video ID::

    ..  youtube:: oHg5SJYRHA0

The referenced video will be embedded into HTML output.  By default, the
embedded video will be sized for 720p content.  To control this, the
parameters "aspect", "width", and "height" may optionally be provided::

    ..  youtube:: oHg5SJYRHA0
        :width: 640
        :height: 480

    ..  youtube:: oHg5SJYRHA0
        :aspect: 4:3

    ..  youtube:: oHg5SJYRHA0
        :width: 100%

    ..  youtube:: oHg5SJYRHA0
        :height: 200px
