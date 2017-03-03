# dapper-hardened-browser

##About
The dapper-hardened-browser package contains the latest version of dapper-hardened-browser, a web browser based on Mozilla technologies, customised to provide a hardened browsing experience. Settings (those that reside in about:config) have been tweaked to prevent tracking and information leakage, such as crash reporting, preloading dns and Google safebrowing service.

Many addons are shipped with this browser by default to aid both security, privacy and user interface. Security minded addons includes NoScript, RequestPolicy, uBlock, Disconnect, Ghostery, HTTPS Everywhere, Random Agent Spoofer and Self Destructing Cookies. User experience addons shipped are Stylish, HTitle, Mozilla Labs: Prospector - Oneliner.

## Files in Repo
This version of dapper-hardened-browser is built and configured from a distro maintainer or enterprise standpoint. Some settings can be changed by the user, and some cannot. The following are the more interesting files:

```
autoconfig.js - Settings file which tells the browser to load custom mozilla.cfg
distribution.tar.xz - Archive containing addon archives
dapper-hardened-browser.desktop - Application definition for desktop environments
mozilla.cfg - All internal settings modifications, can be seen in about:config
stylish.sqlite - Stylish database containing browser theme
unofficial.tar.xz - Folder containing Dapper Linux branding
```


##Building Dapper Hardened Browser
To build this package, first install an RPM development chain:

```bash
$ sudo dnf install fedora-packager fedora-review

```

Next, setup rpmbuild directories with

```bash
$ rpmdev-setuptree
```
And place the file dapper-hardened-browser.spec in the SPECS directory, and all the rest of the files in the SOURCES directory like so: Note, you will need to compress the distribution and unofficial folders.
```bash
$ mv dapper-hardened-browser.spec ~/rpmbuild/SPECS/
$ mv * ~/rpmbuild/SOURCES/
$ tar -cvJf distribution.tar.xz distribution
$ tar -cvJf unofficial.tar.xz unofficial
```

and finally, you can build RPMs and SRPMs with:
```bash
$ cd ~/rpmbuild/SPECS
$ rpmbuild -ba dapper-hardened-browser.spec
```
