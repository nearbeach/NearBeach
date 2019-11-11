
1.1.1 / 2015-10-13
==================

  As of jQuery 1.12 and 2.2.0 the jQuery project is now using a completely different build process. As a result, this library no longer works, so I have hard capped the source downloader to jQuery 1.11.3 and 2.1.4, and removed support for jQuery 3.0 alphas until such a time that I can rewrite this builder for the newer versions.

1.1.0 / 2015-10-13
==================

  * jQuery Source is now downloaded via a postinstall script, rather than using sub-dependencies. This fixes errors caused by npm3's automatic de-duplication.
  * Added support for jQuery 3.
