# Use ALSA backend?
%define alsa_backend      0

# Use system nspr/nss?
%define system_nss        1

# Use system hunspell?
%if 0%{?fedora} > 25
%define system_hunspell   1
%else
%define system_hunspell   0
%endif

# Use system sqlite?
%if 0%{?fedora} > 27
%define system_sqlite     1
%else
%define system_sqlite     0
%endif
%define system_ffi        1

# Use system cairo?
%define system_cairo      0

# Use system libvpx?
%define system_libvpx     1

# Use system libicu?
%if 0%{?fedora} > 27
%define system_libicu     1
%else
%define system_libicu     0
%endif

# Big endian platforms
%ifarch ppc64 s390x
# Javascript Intl API is not supported on big endian platforms right now:
# https://bugzilla.mozilla.org/show_bug.cgi?id=1322212
%define big_endian        1
%endif

# Hardened build?
%define hardened_build    1

%define system_jpeg       1

%ifarch %{ix86} x86_64
%define run_tests         0
%else
%define run_tests         0
%endif

# Build as a debug package?
%define debug_build       0

%define default_bookmarks_file  %{_datadir}/bookmarks/default-bookmarks.html
%define firefox_app_id  \{ec8030f7-c20a-464f-9b0e-13a3a9e97384\}
# Minimal required versions
%global cairo_version 1.13.1
%global freetype_version 2.1.9
%global libnotify_version 0.7.0
%if %{?system_libvpx}
%global libvpx_version 1.4.0
%endif

%if %{?system_nss}
%global nspr_version 4.10.10
# NSS/NSPR quite often ends in build override, so as requirement the version
# we're building against could bring us some broken dependencies from time to time.
%global nspr_build_version %{nspr_version}
#%global nspr_build_version %(pkg-config --silence-errors --modversion nspr 2>/dev/null || echo 65536)
%global nss_version 3.29.3
%global nss_build_version %{nss_version}
#%global nss_build_version %(pkg-config --silence-errors --modversion nss 2>/dev/null || echo 65536) echo 65536)
%endif

%if %{?system_sqlite}
%global sqlite_version 3.8.4.2
# The actual sqlite version (see #480989):
%global sqlite_build_version %(pkg-config --silence-errors --modversion sqlite3 2>/dev/null || echo 65536)
%endif

%global mozappdir     %{_libdir}/%{name}
%global mozappdirdev  %{_libdir}/%{name}-devel-%{version}
%global langpackdir   %{mozappdir}/langpacks
%global tarballdir    firefox-%{version}

%define official_branding       0
%define build_langpacks         0

%define enable_mozilla_crashreporter       0
%if !%{debug_build}
%ifarch %{ix86} x86_64
%define enable_mozilla_crashreporter       0
%endif
%endif

Summary:        Dapper Linux Hardened Browser
Name:           dapper-hardened-browser
Version:        55.0.2
Release:        2%{?pre_tag}%{?dist}
URL:            https://github.com/dapperlinux/dapper-hardened/browser
License:        MPLv1.1 or GPLv2+ or LGPLv2+
Group:          Applications/Internet
Source0:        https://archive.mozilla.org/pub/firefox/releases/%{version}%{?pre_version}/source/firefox-%{version}%{?pre_version}.source.tar.xz
%if %{build_langpacks}
#Source1: firefox-langpacks-%{version}%{?pre_version}-20170818.tar.xz
%endif
Source10:       firefox-mozconfig
Source12:       browser-redhat-default-prefs.js
Source20:       dapper-hardened-browser.desktop
Source21:       firefox.sh.in
Source23:       dapper-hardened-browser.1
Source24:       mozilla-api-key
Source25:       firefox-symbolic.svg
Source26:       distribution.ini

# Dapper Linux Additions
Source27:	mozilla.cfg
Source28:	distribution.tar.xz
Source29:	stylish.sqlite
Source30:	unofficial.tar.xz
Source31:	autoconfig.js

# Build patches
Patch0:         firefox-install-dir.patch
Patch3:         mozilla-build-arm.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=814879#c3
Patch18:        xulrunner-24.0-jemalloc-ppc.patch
# workaround linking issue on s390 (JSContext::updateMallocCounter(size_t) not found)
Patch19:        xulrunner-24.0-s390-inlines.patch
Patch20:        firefox-build-prbool.patch
Patch25:        rhbz-1219542-s390-build.patch
Patch26:        build-icu-big-endian.patch
Patch27:        mozilla-1335250.patch
Patch28:        build-1360521-missing-cheddar.patch
Patch29:        build-big-endian.patch
Patch30:        fedora-build.patch
Patch31:        build-ppc64-s390x-curl.patch
Patch32:        build-rust-ppc64le.patch
Patch33:        build-ppc-s390-dom.patch
Patch34:        build-cubeb-pulse-arm.patch
Patch35:        build-ppc-jit.patch

# Fedora specific patches
# Unable to install addons from https pages
Patch204:        rhbz-966424.patch
Patch215:        firefox-enable-addons.patch
Patch219:        rhbz-1173156.patch
Patch221:        firefox-fedora-ua.patch
Patch224:        mozilla-1170092.patch
Patch225:        mozilla-1005640-accept-lang.patch
#ARM run-time patch
Patch226:        rhbz-1354671.patch
Patch229:        firefox-nss-version.patch


# Upstream patches
Patch304:        mozilla-1253216.patch
Patch402:        mozilla-1196777.patch
Patch406:        mozilla-256180.patch
Patch407:        mozilla-1348576.patch
Patch410:        mozilla-1321521.patch
Patch411:        mozilla-1321521-2.patch
Patch412:        mozilla-1337988.patch
Patch413:        mozilla-1353817.patch

# Debian patches
Patch500:        mozilla-440908.patch

%if %{?system_nss}
BuildRequires:  pkgconfig(nspr) >= %{nspr_version}
BuildRequires:  pkgconfig(nss) >= %{nss_version}
BuildRequires:  nss-static >= %{nss_version}
%endif
%if %{?system_cairo}
BuildRequires:  pkgconfig(cairo) >= %{cairo_version}
%endif
BuildRequires:  pkgconfig(libpng)
%if %{?system_jpeg}
BuildRequires:  libjpeg-devel
%endif
BuildRequires:  zip
BuildRequires:  bzip2-devel
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(libIDL-2.0)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(gtk+-2.0)
BuildRequires:  pkgconfig(krb5)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(freetype2) >= %{freetype_version}
BuildRequires:  pkgconfig(xt)
BuildRequires:  pkgconfig(xrender)
%if %{?system_hunspell}
BuildRequires:  pkgconfig(hunspell)
%endif
BuildRequires:  pkgconfig(libstartup-notification-1.0)
%if %{?alsa_backend}
BuildRequires:  pkgconfig(alsa)
%endif
BuildRequires:  pkgconfig(libnotify) >= %{libnotify_version}
BuildRequires:  pkgconfig(dri)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  dbus-glib-devel
%if %{?system_libvpx}
BuildRequires:  libvpx-devel >= %{libvpx_version}
%endif
BuildRequires:  autoconf213
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(icu-i18n)
BuildRequires:  pkgconfig(gconf-2.0)
BuildRequires:  yasm

Requires:       mozilla-filesystem
%if %{?system_nss}
Requires:       nspr >= %{nspr_build_version}
Requires:       nss >= %{nss_build_version}
%endif

%if 0%{?fedora} > 25
# For early testing of rhbz#1400293 mozbz#1324096 on F26 and Rawhide,
# temporarily require the specific NSS build with the backports.
# Can be removed after firefox is changed to require NSS 3.30.
BuildRequires:  nss-devel >= 3.29.1-2.1
Requires:       nss >= 3.29.1-2.1
%endif
BuildRequires:  python2-devel

%if 0%{?fedora} < 26
# Using Conflicts for p11-kit, not Requires, because on multi-arch
# systems p11-kit isn't yet available for secondary arches like
# p11-kit.i686 (fallback to libnssckbi.so from NSS).
# This build contains backports from p11-kit 0.23.4
Conflicts: p11-kit < 0.23.2-3
# Requires build with CKA_NSS_MOZILLA_CA_POLICY attribute
Requires: ca-certificates >= 2017.2.11-1.1
# Requires NSS build with backports from NSS 3.30
BuildRequires:  nss-devel >= 3.29.3-1.1
Requires:       nss >= 3.29.3-1.1
%endif

BuildRequires:  desktop-file-utils
BuildRequires:  system-bookmarks
%if %{?system_sqlite}
BuildRequires:  pkgconfig(sqlite3) >= %{sqlite_version}
Requires:       sqlite >= %{sqlite_build_version}
%endif

%if %{?system_ffi}
BuildRequires:  pkgconfig(libffi)
%endif

%if %{?run_tests}
BuildRequires:  xorg-x11-server-Xvfb
%endif
BuildRequires:  rust
BuildRequires:  cargo

Obsoletes:      mozilla <= 37:1.7.13
Provides:       webclient

%description
Dapper Hardened Browser is a hardened web browser based on Mozilla technologies,
and includes many preinstalled and configured addons to increase security and privacy.

%if %{enable_mozilla_crashreporter}
%global moz_debug_prefix %{_prefix}/lib/debug
%global moz_debug_dir %{moz_debug_prefix}%{mozappdir}
%global uname_m %(uname -m)
%global symbols_file_name %{name}-%{version}.en-US.%{_os}-%{uname_m}.crashreporter-symbols.zip
%global symbols_file_path %{moz_debug_dir}/%{symbols_file_name}
%global _find_debuginfo_opts -p %{symbols_file_path} -o debugcrashreporter.list
%global crashreporter_pkg_name mozilla-crashreporter-%{name}-debuginfo
%package -n %{crashreporter_pkg_name}
Summary: Debugging symbols used by Mozilla's crash reporter servers
Group: Development/Debug
%description -n %{crashreporter_pkg_name}
This package provides debug information for Firefox, for use by
Mozilla's crash reporter servers.  If you are trying to locally
debug %{name}, you want to install %{name}-debuginfo instead.
%files -n %{crashreporter_pkg_name} -f debugcrashreporter.list
%defattr(-,root,root)
%endif

%if %{run_tests}
%global testsuite_pkg_name mozilla-%{name}-testresults
%package -n %{testsuite_pkg_name}
Summary: Results of testsuite
Group: Development/Debug
%description -n %{testsuite_pkg_name}
This package contains results of tests executed during build.
%files -n %{testsuite_pkg_name}
/test_results
%defattr(-,root,root)
%endif

#---------------------------------------------------------------------

%prep
%setup -q -c
tar -xof %{SOURCE28}
tar -xof %{SOURCE30}
rm -rf %{tarballdir}/browser/branding/unofficial
%{__mv} unofficial %{tarballdir}/browser/branding/
cd %{tarballdir}

# Build patches, can't change backup suffix from default because during build
# there is a compare of config and js/config directories and .orig suffix is
# ignored during this compare.
%patch0  -p1

%patch18 -p1 -b .jemalloc-ppc
#%patch19 -p2 -b .s390-inlines
%patch20 -p1 -b .prbool
%ifarch s390
%patch25 -p1 -b .rhbz-1219542-s390
%endif
#%patch28 -p2 -b .1360521-missing-cheddar
%patch29 -p1 -b .big-endian
%patch30 -p1 -b .fedora-build
%patch31 -p1 -b .ppc64-s390x-curl
%patch32 -p1 -b .rust-ppc64le
%patch33 -p1 -b .ppc-s390-dom
%patch34 -p1 -b .cubeb-pulse-arm
%ifarch ppc ppc64 ppc64le
%patch35 -p1 -b .ppc-jit
%endif

%patch3  -p1 -b .arm

# For branding specific patches.

# Fedora patches
#%patch204 -p2 -b .966424
%patch215 -p1 -b .addons
%patch219 -p2 -b .rhbz-1173156
%patch221 -p2 -b .fedora-ua
%patch224 -p1 -b .1170092
%patch225 -p1 -b .1005640-accept-lang
#ARM run-time patch
%ifarch aarch64
%patch226 -p1 -b .1354671
%endif

%patch304 -p1 -b .1253216
%patch402 -p1 -b .1196777
%patch406 -p1 -b .256180

%ifarch %{arm}
%if 0%{?fedora} < 26
# Workaround for mozbz#1337988
%patch412 -p1 -b .1337988
%endif
%endif
%patch413 -p1 -b .1353817

# Debian extension patch
%patch500 -p1 -b .440908

# Patch for big endian platforms only
%if 0%{?big_endian}
%patch26 -p1 -b .icu
%endif


%{__rm} -f .mozconfig
%{__cp} %{SOURCE10} .mozconfig
%if %{official_branding}
echo "ac_add_options --enable-official-branding" >> .mozconfig
%endif
%{__cp} %{SOURCE24} mozilla-api-key

%if %{?system_nss}
echo "ac_add_options --with-system-nspr" >> .mozconfig
echo "ac_add_options --with-system-nss" >> .mozconfig
%else
echo "ac_add_options --without-system-nspr" >> .mozconfig
echo "ac_add_options --without-system-nss" >> .mozconfig
%endif

%if %{?system_sqlite}
echo "ac_add_options --enable-system-sqlite" >> .mozconfig
%else
echo "ac_add_options --disable-system-sqlite" >> .mozconfig
%endif

%if %{?system_cairo}
echo "ac_add_options --enable-system-cairo" >> .mozconfig
%else
echo "ac_add_options --disable-system-cairo" >> .mozconfig
%endif

%if %{?system_ffi}
echo "ac_add_options --enable-system-ffi" >> .mozconfig
%endif

%ifarch %{arm}
echo "ac_add_options --disable-elf-hack" >> .mozconfig
%endif

%if %{?alsa_backend}
echo "ac_add_options --enable-alsa" >> .mozconfig
%endif

%if %{?system_hunspell}
echo "ac_add_options --enable-system-hunspell" >> .mozconfig
%else
echo "ac_add_options --disable-system-hunspell" >> .mozconfig
%endif

%if %{?debug_build}
echo "ac_add_options --enable-debug" >> .mozconfig
echo "ac_add_options --disable-optimize" >> .mozconfig
%else
%define optimize_flags "none"
# Fedora 26 (gcc7) needs to disable default build flags (mozbz#1342344)
%if 0%{?fedora} > 25
%ifnarch s390 s390x
%define optimize_flags "-g -O2"
%endif
%endif
%ifarch armv7hl
# ARMv7 need that (rhbz#1426850)
%define optimize_flags "-g -O2 -fno-schedule-insns"
%endif
%ifarch ppc64le aarch64
%define optimize_flags "-g -O2"
%endif
%if %{?optimize_flags} != "none"
echo 'ac_add_options --enable-optimize=%{?optimize_flags}' >> .mozconfig
%else
echo 'ac_add_options --enable-optimize' >> .mozconfig
%endif
echo "ac_add_options --disable-debug" >> .mozconfig
%endif

# s390(x) fails to start with jemalloc enabled
%ifarch s390 s390x
echo "ac_add_options --disable-jemalloc" >> .mozconfig
%endif

%ifnarch %{ix86} x86_64
echo "ac_add_options --disable-webrtc" >> .mozconfig
%endif

%if !%{enable_mozilla_crashreporter}
echo "ac_add_options --disable-crashreporter" >> .mozconfig
%endif

%if %{?run_tests}
echo "ac_add_options --enable-tests" >> .mozconfig
%endif

%if !%{?system_jpeg}
echo "ac_add_options --without-system-jpeg" >> .mozconfig
%else
echo "ac_add_options --with-system-jpeg" >> .mozconfig
%endif

%if %{?system_libvpx}
echo "ac_add_options --with-system-libvpx" >> .mozconfig
%else
echo "ac_add_options --without-system-libvpx" >> .mozconfig
%endif

%if %{?system_libicu}
echo "ac_add_options --with-system-icu" >> .mozconfig
%else
echo "ac_add_options --without-system-icu" >> .mozconfig
%endif

#---------------------------------------------------------------------

%build
%if %{?system_sqlite}
# Do not proceed with build if the sqlite require would be broken:
# make sure the minimum requirement is non-empty, ...
sqlite_version=$(expr "%{sqlite_version}" : '\([0-9]*\.\)[0-9]*\.') || exit 1
# ... and that major number of the computed build-time version matches:
case "%{sqlite_build_version}" in
  "$sqlite_version"*) ;;
  *) exit 1 ;;
esac
%endif

cd %{tarballdir}

echo "Generate big endian version of config/external/icu/data/icud58l.dat"
%if 0%{?big_endian}
  ./mach python intl/icu_sources_data.py .
  ls -l config/external/icu/data
  rm -f config/external/icu/data/icudt*l.dat
%endif

# Update the various config.guess to upstream release for aarch64 support
find ./ -name config.guess -exec cp /usr/lib/rpm/config.guess {} ';'

# -fpermissive is needed to build with gcc 4.6+ which has become stricter
#
# Mozilla builds with -Wall with exception of a few warnings which show up
# everywhere in the code; so, don't override that.
#
# Disable C++ exceptions since Mozilla code is not exception-safe
#
MOZ_OPT_FLAGS=$(echo "$RPM_OPT_FLAGS" | %{__sed} -e 's/-Wall//')
#rhbz#1037063
# -Werror=format-security causes build failures when -Wno-format is explicitly given
# for some sources
# Explicitly force the hardening flags for Firefox so it passes the checksec test;
# See also https://fedoraproject.org/wiki/Changes/Harden_All_Packages
MOZ_OPT_FLAGS="$MOZ_OPT_FLAGS -Wformat-security -Wformat -Werror=format-security"
%if 0%{?fedora} > 23
# Disable null pointer gcc6 optimization in gcc6 (rhbz#1328045)
MOZ_OPT_FLAGS="$MOZ_OPT_FLAGS -fno-delete-null-pointer-checks"
%endif
# Use hardened build?
%if %{?hardened_build}
MOZ_OPT_FLAGS="$MOZ_OPT_FLAGS -fPIC -Wl,-z,relro -Wl,-z,now"
%endif
%if %{?debug_build}
MOZ_OPT_FLAGS=$(echo "$MOZ_OPT_FLAGS" | %{__sed} -e 's/-O2//')
%endif
%ifarch s390
MOZ_OPT_FLAGS=$(echo "$MOZ_OPT_FLAGS" | %{__sed} -e 's/-g/-g1/')
# If MOZ_DEBUG_FLAGS is empty, firefox's build will default it to "-g" which
# overrides the -g1 from line above and breaks building on s390
# (OOM when linking, rhbz#1238225)
export MOZ_DEBUG_FLAGS=" "
%endif
%ifarch s390 %{arm} ppc aarch64
MOZ_LINK_FLAGS="-Wl,--no-keep-memory -Wl,--reduce-memory-overheads"
%endif
export CFLAGS=$MOZ_OPT_FLAGS
export CXXFLAGS=$MOZ_OPT_FLAGS
export LDFLAGS=$MOZ_LINK_FLAGS

export PREFIX='%{_prefix}'
export LIBDIR='%{_libdir}'

MOZ_SMP_FLAGS=-j1
# On x86 architectures, Mozilla can build up to 4 jobs at once in parallel,
# however builds tend to fail on other arches when building in parallel.
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le aarch64
[ -z "$RPM_BUILD_NCPUS" ] && \
     RPM_BUILD_NCPUS="`/usr/bin/getconf _NPROCESSORS_ONLN`"
[ "$RPM_BUILD_NCPUS" -ge 2 ] && MOZ_SMP_FLAGS=-j2
[ "$RPM_BUILD_NCPUS" -ge 4 ] && MOZ_SMP_FLAGS=-j4
[ "$RPM_BUILD_NCPUS" -ge 8 ] && MOZ_SMP_FLAGS=-j8
%endif

make -f client.mk build STRIP="/bin/true" MOZ_MAKE_FLAGS="$MOZ_SMP_FLAGS" MOZ_SERVICES_SYNC="1"

# create debuginfo for crash-stats.mozilla.com
%if %{enable_mozilla_crashreporter}
#cd %{moz_objdir}
make -C objdir buildsymbols
%endif

%if %{?run_tests}
%if %{?system_nss}
ln -s /usr/bin/certutil objdir/dist/bin/certutil
ln -s /usr/bin/pk12util objdir/dist/bin/pk12util

%endif
mkdir test_results
./mach --log-no-times check-spidermonkey &> test_results/check-spidermonkey || true
./mach --log-no-times check-spidermonkey &> test_results/check-spidermonkey-2nd-run || true
./mach --log-no-times cppunittest &> test_results/cppunittest || true
xvfb-run ./mach --log-no-times crashtest &> test_results/crashtest || true
./mach --log-no-times gtest &> test_results/gtest || true
xvfb-run ./mach --log-no-times jetpack-test &> test_results/jetpack-test || true
# not working right now ./mach marionette-test &> test_results/marionette-test || true
xvfb-run ./mach --log-no-times mochitest-a11y &> test_results/mochitest-a11y || true
xvfb-run ./mach --log-no-times mochitest-browser &> test_results/mochitest-browser || true
xvfb-run ./mach --log-no-times mochitest-chrome &> test_results/mochitest-chrome || true
xvfb-run ./mach --log-no-times mochitest-devtools &> test_results/mochitest-devtools || true
xvfb-run ./mach --log-no-times mochitest-plain &> test_results/mochitest-plain || true
xvfb-run ./mach --log-no-times reftest &> test_results/reftest || true
xvfb-run ./mach --log-no-times webapprt-test-chrome &> test_results/webapprt-test-chrome || true
xvfb-run ./mach --log-no-times webapprt-test-content &> test_results/webapprt-test-content || true
./mach --log-no-times webidl-parser-test &> test_results/webidl-parser-test || true
xvfb-run ./mach --log-no-times xpcshell-test &> test_results/xpcshell-test || true
%if %{?system_nss}
rm -f  objdir/dist/bin/certutil
rm -f  objdir/dist/bin/pk12util
%endif

%endif
#---------------------------------------------------------------------

%install
cd %{tarballdir}

# set up our default bookmarks
%{__cp} -p %{default_bookmarks_file} objdir/dist/bin/browser/chrome/en-US/locale/browser/bookmarks.html

# Make sure locale works for langpacks
%{__cat} > objdir/dist/bin/browser/defaults/preferences/firefox-l10n.js << EOF
pref("general.useragent.locale", "chrome://global/locale/intl.properties");
EOF

DESTDIR=$RPM_BUILD_ROOT make -C objdir install

%{__mkdir_p} $RPM_BUILD_ROOT{%{_libdir},%{_bindir},%{_datadir}/applications}

desktop-file-install --dir $RPM_BUILD_ROOT%{_datadir}/applications %{SOURCE20}

# set up the firefox start script
%{__rm} -rf $RPM_BUILD_ROOT%{_bindir}/firefox
%{__cat} %{SOURCE21} > $RPM_BUILD_ROOT%{_bindir}/%{name}
%{__chmod} 755 $RPM_BUILD_ROOT%{_bindir}/%{name}

%{__install} -p -D -m 644 %{SOURCE23} $RPM_BUILD_ROOT%{_mandir}/man1/dapper-hardened-browser.1

%{__rm} -f $RPM_BUILD_ROOT/%{mozappdir}/firefox-config
%{__rm} -f $RPM_BUILD_ROOT/%{mozappdir}/update-settings.ini

for s in 16 22 24 32 48 256; do
    %{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${s}x${s}/apps
    %{__cp} -p browser/branding/official/default${s}.png \
               $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${s}x${s}/apps/dapper-hardened-browser.png
done

# Register as an application to be visible in the software center
#
# NOTE: It would be *awesome* if this file was maintained by the upstream
# project, translated and installed into the right place during `make install`.
#
# See http://www.freedesktop.org/software/appstream/docs/ for more details.
#
mkdir -p $RPM_BUILD_ROOT%{_datadir}/appdata
cat > $RPM_BUILD_ROOT%{_datadir}/appdata/%{name}.appdata.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!-- Copyright 2014 Richard Hughes <richard@hughsie.com> -->
<!--
BugReportURL: https://bugzilla.mozilla.org/show_bug.cgi?id=1071061
SentUpstream: 2014-09-22
-->
<application>
  <id type="desktop">dapper-hardened-browser.desktop</id>
  <metadata_license>CC0-1.0</metadata_license>
  <description>
    <p>
      Bringing together all kinds of awesomeness to make browsing better for you.
      Get to your favorite sites quickly – even if you don’t remember the URLs.
      Type your term into the location bar (aka the Awesome Bar) and the autocomplete
      function will include possible matches from your browsing history, bookmarked
      sites and open tabs.
    </p>
    <!-- FIXME: Needs another couple of paragraphs -->
  </description>
  <url type="homepage">http://www.mozilla.org/</url>
  <screenshots>
    <screenshot type="default">https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/firefox/a.png</screenshot>
    <screenshot>https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/firefox/b.png</screenshot>
    <screenshot>https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/firefox/c.png</screenshot>
  </screenshots>
  <!-- FIXME: change this to an upstream email address for spec updates
  <updatecontact>someone_who_cares@upstream_project.org</updatecontact>
   -->
</application>
EOF

echo > ../%{name}.lang
%if %{build_langpacks}
# Extract langpacks, make any mods needed, repack the langpack, and install it.
%{__mkdir_p} $RPM_BUILD_ROOT%{langpackdir}
%{__tar} xf %{SOURCE1}
for langpack in `ls firefox-langpacks/*.xpi`; do
  language=`basename $langpack .xpi`
  extensionID=langpack-$language@firefox.mozilla.org
  %{__mkdir_p} $extensionID
  unzip -qq $langpack -d $extensionID
  find $extensionID -type f | xargs chmod 644

  cd $extensionID
  zip -qq -r9mX ../${extensionID}.xpi *
  cd -

  %{__install} -m 644 ${extensionID}.xpi $RPM_BUILD_ROOT%{langpackdir}
  language=`echo $language | sed -e 's/-/_/g'`
  echo "%%lang($language) %{langpackdir}/${extensionID}.xpi" >> ../%{name}.lang
done
%{__rm} -rf firefox-langpacks

# Install langpack workaround (see #707100, #821169)
function create_default_langpack() {
language_long=$1
language_short=$2
cd $RPM_BUILD_ROOT%{langpackdir}
ln -s langpack-$language_long@firefox.mozilla.org.xpi langpack-$language_short@firefox.mozilla.org.xpi
cd -
echo "%%lang($language_short) %{langpackdir}/langpack-$language_short@firefox.mozilla.org.xpi" >> ../%{name}.lang
}

# Table of fallbacks for each language
# please file a bug at bugzilla.redhat.com if the assignment is incorrect
create_default_langpack "bn-IN" "bn"
create_default_langpack "es-AR" "es"
create_default_langpack "fy-NL" "fy"
create_default_langpack "ga-IE" "ga"
create_default_langpack "gu-IN" "gu"
create_default_langpack "hi-IN" "hi"
create_default_langpack "hy-AM" "hy"
create_default_langpack "nb-NO" "nb"
create_default_langpack "nn-NO" "nn"
create_default_langpack "pa-IN" "pa"
create_default_langpack "pt-PT" "pt"
create_default_langpack "sv-SE" "sv"
create_default_langpack "zh-TW" "zh"
%endif # build_langpacks


%{__mkdir_p} $RPM_BUILD_ROOT/%{mozappdir}/browser/defaults/preferences

# System config dir
%{__mkdir_p} $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/pref

# System extensions
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/mozilla/extensions/%{firefox_app_id}
%{__mkdir_p} $RPM_BUILD_ROOT%{_libdir}/mozilla/extensions/%{firefox_app_id}

# Copy over the LICENSE
%{__install} -p -c -m 644 LICENSE $RPM_BUILD_ROOT/%{mozappdir}

# Copy over all Firefox files to new package
cp -r ${RPM_BUILD_ROOT}/usr/lib64/firefox/* $RPM_BUILD_ROOT%{mozappdir}

# Use the system hunspell dictionaries
%{__rm} -rf ${RPM_BUILD_ROOT}%{mozappdir}/dictionaries
ln -s %{_datadir}/myspell ${RPM_BUILD_ROOT}%{mozappdir}/dictionaries

# Enable crash reporter for Firefox application
%if %{enable_mozilla_crashreporter}
sed -i -e "s/\[Crash Reporter\]/[Crash Reporter]\nEnabled=1/" $RPM_BUILD_ROOT%{mozappdir}/application.ini
# Add debuginfo for crash-stats.mozilla.com
%{__mkdir_p} $RPM_BUILD_ROOT/%{moz_debug_dir}
%{__cp} objdir/dist/%{symbols_file_name} $RPM_BUILD_ROOT/%{moz_debug_dir}
%endif

%if %{run_tests}
# Add debuginfo for crash-stats.mozilla.com
%{__mkdir_p} $RPM_BUILD_ROOT/test_results
%{__cp} test_results/* $RPM_BUILD_ROOT/test_results
%endif

# Default
%{__cp} %{SOURCE12} ${RPM_BUILD_ROOT}%{mozappdir}/browser/defaults/preferences

# Add distribution.ini
%{__mkdir_p} ${RPM_BUILD_ROOT}%{mozappdir}/distribution
%{__cp} %{SOURCE26} ${RPM_BUILD_ROOT}%{mozappdir}/distribution

# Remove copied libraries to speed up build
rm -f ${RPM_BUILD_ROOT}%{mozappdirdev}/sdk/lib/libmozjs.so
rm -f ${RPM_BUILD_ROOT}%{mozappdirdev}/sdk/lib/libmozalloc.so
rm -f ${RPM_BUILD_ROOT}%{mozappdirdev}/sdk/lib/libxul.so

# Add Dapper Linux additions
%{__mkdir_p} $RPM_BUILD_ROOT%{mozappdir}/defaults/profile
%{__cp} %{SOURCE31} $RPM_BUILD_ROOT%{mozappdir}/defaults/pref/
%{__cp} %{SOURCE27} $RPM_BUILD_ROOT%{mozappdir}
cp -r $RPM_BUILD_DIR/%{name}-%{version}/distribution $RPM_BUILD_ROOT%{mozappdir}
chmod -R +755 $RPM_BUILD_ROOT%{mozappdir}/distribution
%{__cp} %{SOURCE29} $RPM_BUILD_ROOT%{mozappdir}/defaults/profile/
%{__mv} $RPM_BUILD_ROOT%{mozappdir}/firefox $RPM_BUILD_ROOT%{mozappdir}/%{name}
%{__mv} $RPM_BUILD_ROOT%{mozappdir}/firefox-bin $RPM_BUILD_ROOT%{mozappdir}/%{name}-bin

# Remove Firefox directory
rm -rf ${RPM_BUILD_ROOT}/usr/lib64/firefox

#---------------------------------------------------------------------

# Moves defaults/preferences to browser/defaults/preferences
%pretrans -p <lua>
require 'posix'
require 'os'
if (posix.stat("%{mozappdir}/browser/defaults/preferences", "type") == "link") then
  posix.unlink("%{mozappdir}/browser/defaults/preferences")
  posix.mkdir("%{mozappdir}/browser/defaults/preferences")
  if (posix.stat("%{mozappdir}/defaults/preferences", "type") == "directory") then
    for i,filename in pairs(posix.dir("%{mozappdir}/defaults/preferences")) do
      os.rename("%{mozappdir}/defaults/preferences/"..filename, "%{mozappdir}/browser/defaults/preferences/"..filename)
    end
    f = io.open("%{mozappdir}/defaults/preferences/README","w")
    if f then
      f:write("Content of this directory has been moved to %{mozappdir}/browser/defaults/preferences.")
      f:close()
    end
  end
end


%preun
# is it a final removal?
if [ $1 -eq 0 ]; then
  %{__rm} -rf %{mozappdir}/components
  %{__rm} -rf %{mozappdir}/extensions
  %{__rm} -rf %{mozappdir}/plugins
  %{__rm} -rf %{langpackdir}
fi

%post
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{mozappdir}/%{name}
%{mozappdir}/%{name}-bin
%doc %{_mandir}/man1/*
%dir %{_sysconfdir}/%{name}/*
%dir %{_datadir}/mozilla/extensions/*
%dir %{_libdir}/mozilla/extensions/*
%{_datadir}/appdata/*.appdata.xml
%{_datadir}/applications/*.desktop
%dir %{mozappdir}
%doc %{mozappdir}/LICENSE
%{mozappdir}/browser/chrome
%{mozappdir}/browser/chrome.manifest
%{mozappdir}/browser/defaults/preferences/browser-redhat-default-prefs.js
%{mozappdir}/browser/features/*.xpi
%{mozappdir}/distribution/distribution.ini
# That's Windows only
%ghost %{mozappdir}/browser/features/aushelper@mozilla.org.xpi
%attr(644, root, root) %{mozappdir}/browser/blocklist.xml
%dir %{mozappdir}/browser/extensions
%{mozappdir}/browser/extensions/*
%if %{build_langpacks}
%dir %{langpackdir}
%endif
%{mozappdir}/browser/omni.ja
%{mozappdir}/browser/icons
%{mozappdir}/chrome.manifest
%{mozappdir}/run-mozilla.sh
%{mozappdir}/application.ini
%{mozappdir}/pingsender
%exclude %{mozappdir}/removed-files
%{_datadir}/icons/hicolor/16x16/apps/dapper-hardened-browser.png
%{_datadir}/icons/hicolor/22x22/apps/dapper-hardened-browser.png
%{_datadir}/icons/hicolor/24x24/apps/dapper-hardened-browser.png
%{_datadir}/icons/hicolor/256x256/apps/dapper-hardened-browser.png
%{_datadir}/icons/hicolor/32x32/apps/dapper-hardened-browser.png
%{_datadir}/icons/hicolor/48x48/apps/dapper-hardened-browser.png
%if %{enable_mozilla_crashreporter}
%{mozappdir}/crashreporter
%{mozappdir}/crashreporter.ini
%{mozappdir}/minidump-analyzer
%{mozappdir}/Throbber-small.gif
%{mozappdir}/browser/crashreporter-override.ini
%endif
%{mozappdir}/*.so
%{mozappdir}/gtk2/*.so
%{mozappdir}/defaults/pref/channel-prefs.js
%{mozappdir}/defaults/pref/autoconfig.js
%{mozappdir}/defaults/profile/stylish.sqlite
%{mozappdir}/dependentlibs.list
%{mozappdir}/dictionaries
%{mozappdir}/distribution/*
%{mozappdir}/mozilla.cfg
%{mozappdir}/omni.ja
%{mozappdir}/platform.ini
%{mozappdir}/plugin-container
%{mozappdir}/gmp-clearkey
%{mozappdir}/fonts/EmojiOneMozilla.ttf
%if !%{?system_libicu}
%{mozappdir}/icudt*.dat
%endif
%if !%{?system_nss}
%{mozappdir}/libfreeblpriv3.chk
%{mozappdir}/libnssdbm3.chk
%{mozappdir}/libsoftokn3.chk
%endif

#---------------------------------------------------------------------

%changelog
* Tue Aug 22 2017 Matthew Ruffell <msr50@uclive.ac.nz> - 55.0.2-2
- Dapper Hardened Browser Rebranded and Built

* Fri Aug 18 2017 Martin Stransky <stransky@redhat.com> - 55.0.2-1
- Updated to 55.0.2

* Mon Aug 14 2017 Jan Horak <jhorak@redhat.com> - 55.0.1-1
- Update to 55.0.1

* Fri Aug 11 2017 Jan Horak <jhorak@redhat.com> - 55.0-6
- Do not require nss and nspr which we build package against

* Tue Aug 8 2017 Martin Stransky <stransky@redhat.com> - 55.0-5
- Rebuild

* Mon Aug 7 2017 Martin Stransky <stransky@redhat.com> - 55.0-2
- Updated to 55.0 (B3)

* Wed Aug 2 2017 Martin Stransky <stransky@redhat.com> - 55.0-1
- Updated to 55.0 (B1)

* Tue Jul 25 2017 Jan Horak <jhorak@redhat.com> - 54.0.1-1
- Update to 54.0.1

* Tue Jun 13 2017 Jan Horak <jhorak@redhat.com> - 54.0-2
- Update to 54.0 (B3)

* Thu Jun  8 2017 Jan Horak <jhorak@redhat.com> - 54.0-1
- Update to 54.0

* Wed May 31 2017 Jan Horak <jhorak@redhat.com> - 53.0.3-2
- Added patch for big endian platforms
- Do not restrict architectures in older Fedoras

* Fri May 26 2017 Jan Horak <jhorak@redhat.com> - 53.0.3-1
- Update to 53.0.3

* Wed May 24 2017 Martin Stransky <stransky@redhat.com> - 53.0.2-8
- Disabled Rust on ppc64 ppc64le s390x

* Wed May 24 2017 Martin Stransky <stransky@redhat.com> - 53.0.2-7
- Enabled aarch64 on all Fedoras
- Enabled Rust on all arches

* Wed May 24 2017 Martin Stransky <stransky@redhat.com> - 53.0.2-6
- Added aarch64 patch (mozbz#1353817)

* Tue May 16 2017 Martin Stransky <stransky@redhat.com> - 53.0.2-5
- Arm gcc6 build fix (mozbz#1337988)

* Fri May 12 2017 Martin Stransky <stransky@redhat.com> - 53.0.2-4
- Enabled rust on ix86

* Thu May 11 2017 Martin Stransky <stransky@redhat.com> - 53.0.2-3
- Enabled Rust on Arm builds

* Thu May 11 2017 Martin Stransky <stransky@redhat.com> - 53.0.2-2
- Enabled Arm builds

* Fri May  5 2017 Jan Horak <jhorak@redhat.com> - 53.0.2-1
- Update to 53.0.2
- Cannot use disable-skia for any architecture now

* Thu Apr 27 2017 Jan Horak <jhorak@redhat.com> - 53.0-4
- Added patch from rhbz#1400293

* Thu Apr 20 2017 Martin Stransky <stransky@redhat.com> - 53.0-3
- Enabled second arches

* Tue Apr 18 2017 Martin Stransky <stransky@redhat.com> - 53.0-2
- Disable system hunspell library when necessary

* Tue Apr 18 2017 Jan Horak <jhorak@redhat.com> - 52.0.2-3
- Do not use color management until it is fixed for some broken profiles,
  ie. don't set gfx.color_management.enablev4 to true (rhbz#1403970).
- Added distribution.ini file to fix mozbz#1354489

* Tue Apr 18 2017 Martin Stransky <stransky@redhat.com> - 53.0-1
- Updated to 53.0 (B6)

* Fri Mar 31 2017 Martin Stransky <stransky@redhat.com> - 52.0.2-2
- Added patch for mozbz#1348576 - enable e10s by default
- Added patch for mozbz#1158076 - enable dark theme by pref

* Wed Mar 29 2017 Jan Horak <jhorak@redhat.com> - 52.0.2-1
- Update to 52.0.2

* Mon Mar 27 2017 Martin Stransky <stransky@redhat.com> - 52.0-7
- Reverted mozbz#1158076 due to rhbz#1435964

* Wed Mar 22 2017 Martin Stransky <stransky@redhat.com> - 52.0-6
- Added fix for CVE-2017-5428
- Added fix for mozbz#1158076

* Mon Mar 13 2017 Martin Stransky <stransky@redhat.com> - 52.0-5
- Enable ALSA backend behind pref (rhbz#1431371)

* Fri Mar 10 2017 Martin Stransky <stransky@redhat.com> - 52.0-2
- Fixed e10s enablement (rhbz#1398717)

* Tue Mar  7 2017 Jan Horak <jhorak@redhat.com> - 52.0-3
- Added s390x to big endian platforms

* Tue Mar  7 2017 Jan Horak <jhorak@redhat.com> - 52.0-2
- Added fix for libicu on big endian platforms

* Fri Mar 3 2017 Martin Stransky <stransky@redhat.com> - 52.0-1
- Update to 52.0 (B2)

* Thu Mar 02 2017 Kai Engert <kaie@redhat.com> - 51.0.1-11
- Enable upstream fix for rhbz#1400293 mozbz#1324096 on F26 and Rawhide.
  Keep the old workaround on F24/F25, required base packages aren't
  available yet.

* Thu Mar 2 2017 Martin Stransky <stransky@redhat.com> - 51.0.1-10
- Test another ARMv7 build setup (rhbz#1426850)

* Mon Feb 27 2017 Martin Stransky <stransky@redhat.com> - 51.0.1-9
- Disabled ARMv7 due to build failures (rhbz#1426850)

* Mon Feb 27 2017 Martin Stransky <stransky@redhat.com> - 51.0.1-8
- Enabled ARMv7 (rhbz#1426850)

* Mon Feb 27 2017 Martin Stransky <stransky@redhat.com> - 51.0.1-7
- Added fix for rhbz#1414535

* Thu Feb 23 2017 Martin Stransky <stransky@redhat.com> - 51.0.1-6
- Added fix for mozbz#1321579

* Thu Feb 23 2017 Martin Stransky <stransky@redhat.com> - 51.0.1-5
- Disabled -O3 optimization on rawhide to make FF usable (rhbz#1422532)

* Wed Feb 15 2017 Jan Horak <jhorak@redhat.com> - 51.0.1-4
- Fixed bug 1421334 - translations for "New window"

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 51.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 25 2017 Jan Horak <jhorak@redhat.com> - 51.0.1-2
- Update to 51.0.1

* Tue Jan 24 2017 Martin Stransky <stransky@redhat.com> - 51.0-3
- Added fix for aarch64 crashes (rhbz#1354671)

* Thu Jan 19 2017 Martin Stransky <stransky@redhat.com> - 51.0-2
- Update to 51.0 (B2)

* Wed Jan 18 2017 Martin Stransky <stransky@redhat.com> - 51.0-1
- Update to 51.0 (B1)

* Tue Jan 17 2017 Jan Horak <jhorak@redhat.com> - 50.1.0-4
- Enable telemetry (rhbz#1412971)

* Mon Jan 16 2017 Martin Stransky <stransky@redhat.com> - 50.1.0-3
- Added patch for nss 3.28.1 (mozbz#1290037)

