%define product_family Mainframe Enterprise Linux OS
%define release_name Red Sox
%define contentdir sunoslinux
%define base_release_version 6
%define full_release_version 6.0
%define dist_release_version 6
%define upstream_rel_long 6.0-1
%define upstream_rel 6.0
%define sunoslinux_rel 1
%define dist .el%{dist_release_version}
Name:           sunos-linux-release
Version:        %{upstream_rel}
Release:        %{sunoslinux_rel}%{?dist}.mel
Summary:        Contains the os-release files for Mainframe Enterprise Linux 6
Group:		System Environment/Base
License:        FRL
Provides:       mainframeos-el-release = %{version}-%{release}
Provides:       centos-release = %{version}-%{release}
Provides:       mainframeos-el-release(upstream) = %{upstream_rel}
Provides:       centos-release(upstream) = %{upstream_rel}
Provides:       redhat-release = %{upstream_rel_long}
Provides:       system-release = %{upstream_rel_long}
Provides:       system-release(releasever) = %{base_release_version}
Provides:       base-module(platform:el%{base_release_version})

Provides:       mainframeos-el-release-eula
Provides:       centos-release-eula
Provides:       redhat-release-eula

Source200:      EULA
Source201:      FRL
##Source202:      Contributors

%description
OS Release for Mainframe/OS Enterprise Linux

%global debug_package %{nil}

%prep
echo OK

%build
echo OK

%install
rm -rf %{buildroot}

# create skeleton
mkdir -p %{buildroot}/etc
mkdir -p %{buildroot}%{_prefix}/lib

# create /etc/system-release and /etc/redhat-release
echo "%{product_family} release %{full_release_version} (%{release_name})" > %{buildroot}/etc/sunos-linux-release
echo "Derived from Red Hat Enterprise Linux %{upstream_rel} (Source)" > %{buildroot}/etc/mainframeos-el-release-upstream
ln -s sunos-linux-release %{buildroot}/etc/system-release
ln -s sunos-linux-release %{buildroot}/etc/redhat-release
ln -s sunos-linux-release %{buildroot}/etc/centos-release

# Create the os-release file
cat << EOF >>%{buildroot}%{_prefix}/lib/os-release
NAME="%{product_family}"
VERSION="%{full_release_version} (%{release_name})"
ID="mel"
ID_LIKE="rhel fedora"
VERSION_ID="%{full_release_version}"
PLATFORM_ID="platform:el%{base_release_version}"
PRETTY_NAME="%{product_family} %{full_release_version} (%{release_name})"
ANSI_COLOR="0;34"
HOME_URL="https://almalinux.org/"


SUN/OSLINUX_MANTISBT_PROJECT="Mainframe/OSEL-%{base_release_version}"
SUN/OSLINUX_MANTISBT_PROJECT_VERSION="%{full_release_version}"

EOF

# Create the symlink for /etc/os-release
ln -s ../usr/lib/os-release %{buildroot}%{_sysconfdir}/os-release

# write cpe to /etc/system-release-cpe
echo "cpe:/o:mainframeel:mainframeel:%{full_release_version}:" | tr [A-Z] [a-z] > %{buildroot}/etc/system-release-cpe

# create /etc/issue and /etc/issue.net
echo '\S' > %{buildroot}/etc/issue
echo 'Kernel \r on an \m' >> %{buildroot}/etc/issue
cp %{buildroot}/etc/issue %{buildroot}/etc/issue.net
echo >> %{buildroot}/etc/issue

# set up the dist tag macros
install -d -m 755 %{buildroot}/etc/rpm
cat >> %{buildroot}/etc/rpm/macros.dist << EOF
# dist macros.

%%almalinux_ver %{base_release_version}
%%almalinux %{base_release_version}
%%centos_ver %{base_release_version}
%%centos %{base_release_version}
%%rhel %{base_release_version}
%%dist .el%{base_release_version}
%%el%{base_release_version} 1
EOF

# use unbranded datadir
mkdir -p -m 755 %{buildroot}/%{_datadir}/mainframeos-el-release
ln -s sunos-linux-release %{buildroot}/%{_datadir}/redhat-release
install -m 644 %{SOURCE200} %{buildroot}/%{_datadir}/mainframeos-el-release

# use unbranded docdir
mkdir -p -m 755 %{buildroot}/%{_docdir}/mainframeos-el-release
ln -s sunos-linux-release %{buildroot}/%{_docdir}/redhat-release
install -m 644 %{SOURCE201} %{buildroot}/%{_docdir}/mainframeos-el-release


%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
/etc/redhat-release
/etc/system-release
/etc/centos-release
##/etc/centos-release-upstream
/etc/sunos-linux-release
/etc/sunos-linux-release-upstream
# add config(noreplace) for Mainframe Enterprise Linux after 6.0 release
%config(noreplace) /etc/os-release
%config /etc/system-release-cpe
%config(noreplace) /etc/issue
%config(noreplace) /etc/issue.net
/etc/rpm/macros.dist
%{_docdir}/redhat-release
%{_docdir}/mainframeos-el-release/*
%{_datadir}/redhat-release
%{_datadir}/mainframeos-el-release/*
%{_prefix}/lib/os-release


%changelog
* Tue Mar 30 2021 Abdon Morales <abdonmoralesjr@icloud.com>
- First version being packaged
