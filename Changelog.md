=== Version 3.1.1 ===
* Fixed reading import settings.
* Fixed showing tooltips if some fields are absent.

=== Version 3.1 ===
* Added possibility to convert names to upper/lower/camel cases.
* Added tooltips for waypoints.
* Several fixes.

=== Version 3.0 ===
* Ported to PyQt6.
* Moved to pyproject.toml instead of setup.py to configure setuptools.

=== Version 2.4.1 ===
* Fixed reading GPX files with millisecond accuracy.

=== Version 2.4 ===
* Added possibility to set bold or italic fonts for axes labels and point captions.
* Added options to convert waypoints to tracks and vice versa when exporting to GPX/KML files.
* Initial steps for compatibility with PyQt6.

=== Version 2.3 ===
* Added posibility to select multiple points in profile window.
* Added "go to main window" button in the profile window.
* Several fixes and performance improvements.

=== Version 2.2 ===
* Added possibility to get altitudes for waypoints and tracks from online SRTM data.
* Reading and writing KML files is now supported.
* Added possibility to open files by drag & drop from file manager.

=== Version 2.1 ===
* Improved user interactions in the profile window: dragging captions, changing selected markers and more.
* Added more actions in the context menu and shortcuts to them.
* Added possibility to change point name via point style dialog.

=== Version 2.0 ===
* Added detailed view for profile window. It allows one to view/modify all points and see their coordinates.
* Added possibility to zoom and drag the profile.
* Added detailed view to the main window with more columns (speed, slope, etc.).
* Added an option to sort imported points by time.
* Changed dependency to QCustomPlot2.

=== Version 1.2 ===
* Added possibility to show absolute date and time in the X axis labels.
* Added several new options to settings dialog and point properties dialog.
* Added support for dark color themes.
* Added arrow-like marker shapes.

=== Version 1.1 ===
* Added GPX Viewer archive format to store project along with all GPX files.
* Added possibility to choose columns to be copied to clipboard.

=== Version 1.0 ===
* Major improvement: use QCustomPlot instead of matplotlib to draw profiles.
* As a result some interactivity added to plot window (see help menu for details).
* Added possibility to rename several points at once.
* Added several new settings.
* Refactored several dialogs and menus.
* Added a lot of new icons and tooltips.

=== Version 0.9.3 ===
* Added possibility to revert point names to default values.
* Added possibility to choose from several online maps providers.

=== Version 0.9.2 ===
* Added an option to draw profiles using only selected points and tracks.

=== Version 0.9.1 ===
* Several fixes.

=== Version 0.9 ===
* Ask about new GPX file location if file not found.
* Added recent projects submenu.

=== Version 0.8 ===
* Possibility to select distance coefficient.

=== Version 0.7 ===
* Added possibility to edit names.
* Added possibility to show point location on Google maps.
* Total statistics in the statistics window is now shown for selected rows only.
* Read and write additional WPT fields: cmt, desc, sym.
* Added mime type for Linux version.

=== Version 0.6 ===
* Added full support for tracks in addition to waypoints.

=== Version 0.5 ===
* Added exporting non-skipped points to a GPX file.

=== Version 0.4 ===
* Added statistics by segments.
* Added support for time zones.

=== Version 0.3 ===
* Handle files without timestamps.
* Handle loading multiple GPX files.

=== Version 0.2 ===
* Windows installer now works properly.

=== Version 0.1 ===
* Basic functionality is ready.
