#
# Conditional build:
%bcond_with	tests		# tests require networking

Summary:	Generate rpm specfiles from gems
Name:		gem2rpm
Version:	0.10.1
Release:	1
License:	GPL v2+
Group:		Development/Languages
Source0:	https://github.com/fedora-ruby/gem2rpm/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	a22be828b4aeff0387a735daae969c5c
Source2:	pld.spec.erb
Patch0:		gems.patch
Patch1:		pld.patch
Patch2:		style.patch
URL:		https://github.com/fedora-ruby/gem2rpm
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.656
%if %{with tests}
%if %(locale -a | grep -q '^en_US$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
%endif
Requires:	ruby-rubygems
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Generate source rpms and rpm spec files from a Ruby Gem. The spec file
tries to follow the gem as closely as possible, and be compliant with
the Fedora rubygem packaging guidelines

%package doc
Summary:	Documentation for %{name}
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description doc
Documentation for %{name}.

%prep
%setup -q
%{__sed} -i -e '1 s,#!.*ruby,#!%{__ruby},' bin/*
%patch0 -p1
%patch1 -p1
%patch2 -p1
cp -p %{SOURCE2} templates

# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%build
%if %{with tests}
# tests need UTF-8 locale
LC_ALL=en_US.UTF-8 \
testrb -Itest test/
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_rubylibdir},%{_bindir}}

cp -a bin/* $RPM_BUILD_ROOT%{_bindir}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_rubylibdir}

install -d $RPM_BUILD_ROOT%{_datadir}/ruby/templates
cp -a templates/* $RPM_BUILD_ROOT%{_datadir}/ruby/templates

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README AUTHORS
%attr(755,root,root) %{_bindir}/gem2rpm
%{ruby_rubylibdir}/gem2rpm.rb
%{ruby_rubylibdir}/gem2rpm
%{_datadir}/ruby/templates
