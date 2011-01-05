Introduction
============

raptus.article.images provides support for multiple images per article.

The following features for raptus.article are provided by this package:

Content
-------
    * Image - add your images in a article.

Dependencies
------------
    * archetypes.schemaextender
    * raptus.article.core
    * plone.app.imaging

Installation
============

Note if you install raptus.article.default you can skip this installation steps.

To install raptus.article.images into your Plone instance, locate the file
buildout.cfg in the root of your Plone instance directory on the file system,
and open it in a text editor.

Add the actual raptus.article.images add-on to the "eggs" section of
buildout.cfg. Look for the section that looks like this::

    eggs =
        Plone

This section might have additional lines if you have other add-ons already
installed. Just add the raptus.article.images on a separate line, like this::

    eggs =
        Plone
        raptus.article.images

Note that you have to run buildout like this::

    $ bin/buildout

Then go to the "Add-ons" control panel in Plone as an administrator, and
install or reinstall the "raptus.article.default" product.

Note that if you do not use the raptus.article.default package you have to
include the zcml of raptus.article.images either by adding it
to the zcml list in your buildout or by including it in another package's
configure.zcml.

Plone 3 compatibility
---------------------

This packages requires plone.app.imaging which requires two pins in buildout
when using Plone 3, which there are::

    Products.Archetypes = 1.5.16
    archetypes.schemaextender = 2.0.3
    plone.scale = 1.2

Usage
=====

Add image
---------
You may now add images in your article. Click the "Add new" menu and select "Image" in the pull down menu.
You get the standard plone form to add your image. 

Components
----------
The following packages provide components to display contained images:

    * `raptus.article.gallery <http://pypi.python.org/pypi/raptus.article.gallery>`_
    * `raptus.article.fader <http://pypi.python.org/pypi/raptus.article.fader>`_
    * `raptus.article.lightbox <http://pypi.python.org/pypi/raptus.article.lightbox>`_
    * `raptus.article.lightboxgallery <http://pypi.python.org/pypi/raptus.article.lightboxgallery>`_
    * `raptus.article.randomimage <http://pypi.python.org/pypi/raptus.article.randomimage>`_

Copyright and credits
=====================

raptus.article is copyrighted by `Raptus AG <http://raptus.com>`_ and licensed under the GPL. 
See LICENSE.txt for details.
