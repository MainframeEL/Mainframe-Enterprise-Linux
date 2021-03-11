Name:           mos-release
Version:        1.0.0
Release:        1%{?dist}
Summary:        Contains the os-release files for Mainframe/OS

License:        FRL
#URL:            
Source0:        %{name}-%{version}.tar.gz

#BuildRequires:  
Requires:       bash

%description
OS Release for Mainframe/OS and for systems transfering from any EL distrobution (OS)

%global debug_package %{nil}

%prep
%setup -q

%build


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
cp mos-release-1.0.0/* $RPM_BUILD_ROOT%{_sysconfdir}


%files
%{_sysconfdir}

%changelog
* Thu Mar 11 2021 Abdon Morales <abdonmoralesjr@icloud.com.
- First version being packaged
