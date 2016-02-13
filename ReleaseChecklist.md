## Step 1: Choose the Right Version Name ##

Currently, carcode has an X.Y version number (e.g. 3.0), and an optional "alphaX" or "betaX" afterwards. Alpha versions are meant only for developers, while beta versions are meant to be testable by non-developers. Release without an "alpha" or "beta" are meant to be major public releases of stable, polished code.

For example, the first two alpha releases of carcode 3.0 were named like this:

> carcode\_v3.0\_alpha1

> carcode\_v3.0\_alpha2

## Step 2: Copy the release to the tags folder ##

If the release version name is, say, carcode\_v3.7\_beta19, then copy it to the SVN folder `tags/carcode_v3.7_beta19`. Thus we will have a history of all releases.

For example, if we had our main code in `trunk/carcode3` and we decide to do the release v3.1 alpha 1, we create a tag with the following subversion command:

```
svn copy https://carcode.googlecode.com/svn/trunk/carcode3 https://carcode.googlecode.com/svn/tags/carcode_v3.1_alpha1
```


## Step 3: Add a version tag labs to the issue tracker and wiki web ##

This way we can tag issues and documentation to specific versions. New labels  can be added via the admin interface http://code.google.com/p/carcode/adminIssues