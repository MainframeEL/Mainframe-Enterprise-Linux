%define debug_package %{nil}
%define product_family Mainframe Enterprise Linux
%define variant_titlecase Server
%define variant_lowercase server
%define release_name Red Fox
%define contentdir melinux
%define infra_var stock
%define base_release_version 8
%define full_release_version 8.3
%define dist_release_version 8
%define upstream_rel_long 8.3-1
%define upstream_rel 8.3
%define mel_rel 4
%define dist .el%{dist_release_version}

# The anaconda scripts in %%{_libexecdir} can create false requirements
%global __requires_exclude_from %{_libexecdir}

Name:           mel-release
Version:        %{upstream_rel}
Release:        %{mel_rel}%{?dist}
Summary:        %{product_family} release file
Group:          System Environment/Base
License:        GPLv2
Provides:       mel-release = %{version}-%{release}
Provides:       centos-release = %{version}-%{release}
Provides:       mel-release(upstream) = %{upstream_rel}
Provides:       centos-release(upstream) = %{upstream_rel}
Provides:       redhat-release = %{upstream_rel_long}
Provides:       system-release = %{upstream_rel_long}
Provides:       system-release(releasever) = %{base_release_version}
Provides:       base-module(platform:el%{base_release_version})

Provides:       mel-release-eula
Provides:       centos-release-eula
Provides:       redhat-release-eula

Source1:        85-display-manager.preset
Source2:        90-default.preset
Source3:        99-default-disable.preset
Source10:       RPM-GPG-KEY-sunOSLinux

##Source100:      rootfs-expand

Source200:      EULA
Source201:      FRL
##Source202:      Contributors

Source300:      mel.repo

%description
%{product_family} release files

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
echo "%{product_family} release %{full_release_version}%{?beta: %{beta}} (%{release_name})" > %{buildroot}/etc/mel-release
echo "Derived from Red Hat Enterprise Linux %{upstream_rel} (Source)" > %{buildroot}/etc/mel-release-upstream
ln -s mel-release %{buildroot}/etc/system-release
ln -s mel-release %{buildroot}/etc/redhat-release
ln -s mel-release %{buildroot}/etc/centos-release

# Create the os-release file
cat << EOF >>%{buildroot}%{_prefix}/lib/os-release
NAME="%{product_family}"
VERSION="%{full_release_version} (%{release_name})"
ID="mel"
ID_LIKE="rhel centos sunoslinux"
VERSION_ID="%{full_release_version}"
PLATFORM_ID="platform:el%{base_release_version}"
PRETTY_NAME="%{product_family} %{full_release_version}%{?beta: %{beta}} (%{release_name})"
ANSI_COLOR="0;34"
CPE_NAME="cpe:/o:mel:mel:%{full_release_version}:%{?beta:%(echo %{beta} | tr [A-Z] [a-z])}%{?!beta:GA}"
HOME_URL="https://github.com/SunOS-Linux"
BUG_REPORT_URL="https://github.com/SunOS-Linux/SunOS-Linux/issues"

MEL_MANTISBT_PROJECT="Mainframe Enterprise Linux-%{base_release_version}"
MEL_MANTISBT_PROJECT_VERSION="%{full_release_version}"

EOF

# Create the symlink for /etc/os-release
ln -s ../usr/lib/os-release %{buildroot}%{_sysconfdir}/os-release

# write cpe to /etc/system-release-cpe
echo "cpe:/o:mel:mel:%{full_release_version}:%{?beta:%{beta}}%{?!beta:ga}" | tr [A-Z] [a-z] > %{buildroot}/etc/system-release-cpe

# create /etc/issue and /etc/issue.net
echo '\S' > %{buildroot}/etc/issue
echo 'Kernel \r on an \m' >> %{buildroot}/etc/issue
cp %{buildroot}/etc/issue %{buildroot}/etc/issue.net
echo >> %{buildroot}/etc/issue

# copy GPG keys
mkdir -p -m 755 %{buildroot}/etc/pki/rpm-gpg
install -m 644 %{SOURCE10} %{buildroot}/etc/pki/rpm-gpg

# copy yum repos
mkdir -p -m 755 %{buildroot}/etc/yum.repos.d
install -m 644 %{SOURCE300} %{buildroot}/etc/yum.repos.d

mkdir -p -m 755 %{buildroot}/etc/dnf/vars
echo "%{infra_var}" > %{buildroot}/etc/dnf/vars/infra
echo "%{contentdir}" >%{buildroot}/etc/dnf/vars/contentdir

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
mkdir -p -m 755 %{buildroot}/%{_datadir}/mel-release
ln -s mel-release %{buildroot}/%{_datadir}/redhat-release
install -m 644 %{SOURCE200} %{buildroot}/%{_datadir}/mel-release

# use unbranded docdir
mkdir -p -m 755 %{buildroot}/%{_docdir}/mel-release
ln -s mel-release %{buildroot}/%{_docdir}/redhat-release
install -m 644 %{SOURCE201} %{buildroot}/%{_docdir}/mel-release

# copy systemd presets
mkdir -p %{buildroot}/%{_prefix}/lib/systemd/system-preset/
install -m 0644 %{SOURCE1} %{buildroot}/%{_prefix}/lib/systemd/system-preset/
install -m 0644 %{SOURCE2} %{buildroot}/%{_prefix}/lib/systemd/system-preset/
install -m 0644 %{SOURCE3} %{buildroot}/%{_prefix}/lib/systemd/system-preset/


%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
/etc/redhat-release
/etc/system-release
/etc/centos-release
##/etc/centos-release-upstream
/etc/mel-release
/etc/mel-release-upstream
/etc/dnf/
/etc/pki/rpm-gpg/RPM-GPG-KEY-sunOSLinux
%config(noreplace) /etc/yum.repos.d/mel.repo
%config(noreplace) /etc/os-release
%config /etc/system-release-cpe
%config(noreplace) /etc/issue
%config(noreplace) /etc/issue.net
/etc/rpm/macros.dist
%{_docdir}/redhat-release
%{_docdir}/mel-release/*
%{_datadir}/redhat-release
%{_datadir}/mel-release/*
%{_prefix}/lib/os-release
%{_prefix}/lib/systemd/system-preset/*

%changelog
* Wed Mar 24 2021 Abdon Morales <abdon.morales13_2022@outlook.com> - 8.3-rc1
- 8.3 rc release

