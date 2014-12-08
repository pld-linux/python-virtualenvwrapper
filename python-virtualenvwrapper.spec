#
# Conditional build:
%bcond_with	tests	# requires network to install stuff from pypi

%define 	module	virtualenvwrapper
Summary:	Enhancements to virtualenv
Name:		python-%{module}
Version:	4.3.1
Release:	1
License:	MIT
Group:		Development/Languages
Source0:	http://pypi.python.org/packages/source/v/%{module}/%{module}-%{version}.tar.gz
# Source0-md5:	4327d04b0e65d4229352454ab8ce3f37
URL:		http://pypi.python.org/pypi/virtualenvwrapper
BuildRequires:	python-pbr
BuildRequires:	python-setuptools
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
%if %{with tests}
BuildRequires:	python-stevedore
BuildRequires:	python-virtualenv
BuildRequires:	python-virtualenv-clone
## Just for tests
BuildRequires:	ksh
BuildRequires:	python-tox
BuildRequires:	zsh
%endif
Requires:	python-stevedore
Requires:	python-virtualenv
Requires:	python-virtualenv-clone
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
virtualenvwrapper is a set of extensions to Ian Bicking's virtualenv
tool. The extensions include wrappers for creating and deleting
virtual environments and otherwise managing your development workflow,
making it easier to work on more than one project at a time without
introducing conflicts in their dependencies.

%prep
%setup -q -n %{module}-%{version}

%build
%{__python} setup.py build

%if %{with tests}
tox -e py27
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean

install -d $RPM_BUILD_ROOT/etc/profile.d
ln -s %{_bindir}/virtualenvwrapper.sh $RPM_BUILD_ROOT/etc/profile.d/virtualenvwrapper.sh

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc PKG-INFO docs
/etc/profile.d/virtualenvwrapper.sh
%attr(755,root,root) %{_bindir}/virtualenvwrapper.sh
%attr(755,root,root) %{_bindir}/virtualenvwrapper_lazy.sh
%{py_sitescriptdir}/virtualenvwrapper
%{py_sitescriptdir}/virtualenvwrapper-%{version}-py*-nspkg.pth
%{py_sitescriptdir}/virtualenvwrapper-%{version}-py*.egg-info
