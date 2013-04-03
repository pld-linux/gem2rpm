Summary:	Generate rpm specfiles from gems
Name:		gem2rpm
Version:	0.8.1
Release:	0.1
License:	GPL v2+
Group:		Development/Languages
Source0:	http://rubygems.org/gems/%{name}-%{version}.gem
# Source0-md5:	d3c9416f225ae944fd195e69e122d46e
# git clone https://github.com/lutter/gem2rpm.git && cd gem2rpm && git checkout v0.8.1
# tar czvf gem2rpm-0.8.1-tests.tgz test/
Source1:	%{name}-%{version}-tests.tgz
# Source1-md5:	d7d8bc231dc405bbce00f570c89f530e
URL:		https://github.com/lutter/gem2rpm/
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.656
Requires:	ruby
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

%build
%if %{with tests}
testrb -Itest test/
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_rubylibdir},%{_bindir}}

cp -a bin/* $RPM_BUILD_ROOT%{_bindir}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_rubylibdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README AUTHORS
%attr(755,root,root) %{_bindir}/gem2rpm
%{ruby_rubylibdir}/gem2rpm.rb
%{ruby_rubylibdir}/gem2rpm

%if 0
%files doc
%defattr(644,root,root,755)
%doc %{gem_docdir}
%doc %{gem_instdir}/README
%doc %{gem_instdir}/AUTHORS
%endif
