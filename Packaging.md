# Linux Packaging #

## RPM Packages ##

Carcode includes automatic rpm package generation via setup.py script, you will need to have rpm building packages (such as rpm-build) this may vary from distribution to distribution.

To generate the package run the script with the following arguments:

```
 python setup.py bdist_rpm
```

Packages will be created inside the directory dist, usually with the name carcode-version-1.noarch.rpm.

Be sure of updating version numbers inside the setup.py script.

When adding new files to the project be sure of adding the to the MANIFEST file.

## DEB Packages ##

Carcode includes basic deb building structure and scripts to automatically package, you may need deb building packages such as debuild and its dependencies.

To generate the package run as root (or with sudo) the setup.py script with the following arguments:

```
 sudo python setup.py bdist_deb
```

The packages will be builded outside the carcode directory, with filename such as carcode\_version\_i386.deb.

When adding new files to the project be sure of adding the to the MANIFEST file, make sure that the files install with the command:

```
 python setup.py install
```