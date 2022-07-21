%bcond_without java

%define major %(echo %{version} |cut -d. -f1)
%define libphonenumber %mklibname phonenumber %{major}
%define devphonenumber %mklibname -d phonenumber
%define libgeocoding %mklibname geocoding %{major}

Summary:	Library for parsing phone numbers
Name:		libphonenumber
Version:	8.12.52
Release:	1
Source0:	https://github.com/google/libphonenumber/archive/v%{version}/%{name}-%{version}.tar.gz
Patch0:		libphonenumber-8.12.7-no-underlinking.patch
Patch1:		libphonenumber-8.12.7-optional-static-libs.patch
Patch2:		libphonenumber-8.12.40-system-absl.patch
License:	Apache 2.0
BuildRequires:	cmake
BuildRequires:	pkgconfig(icu-uc)
BuildRequires:	boost-devel
BuildRequires:	pkgconfig(protobuf)
BuildRequires:	protobuf-compiler
BuildRequires:	pkgconfig(re2)
BuildRequires:	pkgconfig(gtest)
BuildRequires:	pkgconfig(absl_strings)
BuildRequires:	pkgconfig(absl_container_common)
%if %{with java}
BuildRequires:	jdk-current
BuildRequires:	ant
%endif

%description
Library for parsing, formatting, and validating international phone numbers.

%package -n %{libphonenumber}
Summary:	Library for parsing phone numbers
Group:		System/Libraries

%description -n %{libphonenumber}
Library for parsing phone numbers.

%package -n %{libgeocoding}
Summary:	Library for geo-coding phone numbers
Group:		System/Libraries

%description -n %{libgeocoding}
Library for geo-coding phone numbers.

%package -n %{devphonenumber}
Summary:	Development files for the library for parsing phone numbers
Group:		Development/C++ and C
Requires:	%{libphonenumber} = %{EVRD}
Requires:	%{libgeocoding} = %{EVRD}
Requires:	pkgconfig(protobuf)
Requires:	pkgconfig(absl_container_common)
Provides:	phonenumber-devel = %{EVRD}

%description -n %{devphonenumber}
Development files for the library for parsing phone numbers.

%package java
Summary:	The phone number parsing library for Java
Group:		Development/Java

%description java
The phone number parsing library for Java.

%prep
%autosetup -p1
cd cpp
LDFLAGS="%{build_ldflags} -L." %cmake \
	-DBUILD_STATIC_LIB:BOOL=OFF

%build
# Not using %%make_build because the Makefiles are broken.
# Protobuf-built source files aren't guaranteed to be built
# before they're used.
make -C cpp/build

%if %{with java}
# Unfortunately we can't module-ify this Java library because
# multiple jar files all try to export the same package name,
# com.google.i18n.phonenumbers
# If we want to make it a module at some point, we have to
# merge the jar files into one.
. %{_sysconfdir}/profile.d/90java.sh
cd java
ant jar
%endif

%install
%make_install -C cpp/build

mkdir -p %{buildroot}%{_datadir}/java
cp java/build/jar/*.jar %{buildroot}%{_datadir}/java

%files -n %{libphonenumber}
%{_libdir}/libphonenumber.so.%{major}*

%files -n %{libgeocoding}
%{_libdir}/libgeocoding.so.%{major}*

%files -n %{devphonenumber}
%{_includedir}/phonenumbers
%{_libdir}/libgeocoding.so
%{_libdir}/libphonenumber.so

%if %{with java}
%files java
%{_datadir}/java/*.jar
%endif
