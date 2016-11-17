%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

%global gem_name loofah

Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 2.0.3
Release: 3%{?dist}
Summary: Manipulate and transform HTML/XML documents and fragments
Group: Development/Languages
License: MIT
URL: https://github.com/flavorjones/loofah
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
Patch0001: 0001-Updating-test-to-support-libxml-2.9.3-behavior.patch

Requires: %{?scl_prefix_ruby}ruby(release)
Requires: %{?scl_prefix_ruby}ruby(rubygems)
Requires: %{?scl_prefix}rubygem(nokogiri) >= 1.6.6.2
BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildRequires: %{?scl_prefix}rubygem(nokogiri) >= 1.6.6.2
BuildRequires: %{?scl_prefix_ruby}rubygem(minitest)
BuildRequires: %{?scl_prefix}rubygem(rr)
BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}

# Explicitly require runtime subpackage, as long as older scl-utils do not generate it
Requires: %{?scl_prefix}runtime

%description
Loofah is a general library for manipulating and transforming HTML/XML
documents and fragments. It's built on top of Nokogiri and libxml2, so
it's fast and has a nice API.
Loofah excels at HTML sanitization (XSS prevention). It includes some
nice HTML sanitizers, which are based on HTML5lib's whitelist, so it
most likely won't make your codes less secure.

%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{pkg_name}

%prep
%setup -n %{pkg_name}-%{version} -q -c -T
%{?scl:scl enable %{scl} - << \EOF}
%gem_install -n %{SOURCE0}
%{?scl:EOF}

pushd .%{gem_instdir}
%patch0001 -p1
popd

%build


%install
mkdir -p %{buildroot}%{gem_dir}
cp -a  .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
%{?scl:scl enable %{scl} - << \EOF}
  ruby -I"lib:test" -e \
    'Dir.glob "./test/**/test_*.rb", &method(:require)'
%{?scl:EOF}
popd

%files
%dir %{gem_instdir}
%{gem_instdir}/MIT-LICENSE.txt
%doc %{gem_instdir}/README.rdoc
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
%exclude %{gem_instdir}/.*

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/Manifest.txt
%doc %{gem_instdir}/CHANGELOG.rdoc
%{gem_instdir}/Rakefile
%{gem_instdir}/Gemfile
%exclude %{gem_instdir}/benchmark
%exclude %{gem_instdir}/test

%changelog
* Thu Jul 28 2016 Pavel Valena <pvalena@redhat.com> - 2.0.3-3
- Include Gemfile and Rakefile in -doc subpackage
- Do not use %%license macro
- Explicitly require runtime subpackage

* Mon Feb 22 2016 Pavel Valena <pvalena@redhat.com> - 2.0.3-3
- Add scl macros

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 11 2016 Ken Dreyer <ktdreyer@ktdreyer.com> - 2.0.3-1
- Update to loofah 2.0.3 (rhbz#1256165)
- Use %%autosetup macro
- Drop macros for Fedora 20 (it is now EOL)
- Drop unneeded %%license definition

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 25 2015 Ken Dreyer <ktdreyer@ktdreyer.com> - 2.0.2-1
- Update to loofah 2.0.2 (rhbz#1218819)
- Drop patch to skip failing test (it works now, with Nokogiri 1.6.6.2)
- Drop Fedora 19 support
- Use %%license macro

* Thu Sep 11 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 2.0.1-1
- Update to loofah 2.0.1 (RHBZ #1132898)
- Drop upstreamed RR patch

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 12 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 2.0.0-1
- Update to loofah 2.0.0 (RHBZ #1096760)
- Adjustments for https://fedoraproject.org/wiki/Changes/Ruby_2.1

* Sat Dec 28 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.2.1-1
- Initial package
