#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class AbseilConan(ConanFile):
    name = "abseil"
    version = "20180223"
    commit_id = "0d40cb771eec8741f44e5979cfccf1eeeedb012a"
    url = "https://github.com/bincrafters/conan-abseil"
    description = "Abseil Common Libraries (C++) from Google"
    license = "Apache-2.0"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    # short_paths = True
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    source_subfolder = "source_subfolder"
    requires = "cctz/2.2@bincrafters/stable"
    
    def source(self):
        source_url = "https://github.com/abseil/abseil-cpp"
        tools.get("{0}/archive/{1}.zip".format(source_url, self.commit_id))
        extracted_dir = "abseil-cpp-" + self.commit_id
        os.rename(extracted_dir, self.source_subfolder)

    def configure(self):
        if self.settings.os == 'Linux':
            compiler = self.settings.compiler
            version = float(self.settings.compiler.version.value)
            libcxx = compiler.libcxx
            if compiler == 'gcc' and version > 5 and libcxx != 'libstdc++11':
                raise ConanException(
                    'Using abseil with GCC > 5 on Linux requires "compiler.libcxx=libstdc++11"'
                    'but was passed: ' + str(self.settings.compiler.libcxx))
                    
    def build(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_TESTING"] = False
        cmake.definitions["ABSL_CCTZ_TARGET"] = "CONAN_PKG::cctz"
        cmake.configure()
        cmake.build()
                    
    def package(self):
        self.copy("LICENSE", dst="licenses", src=self.source_subfolder)
        self.copy("*.h", dst="include", src=self.source_subfolder)
        self.copy("*.inc", dst="include", src=self.source_subfolder)
        self.copy("*.a", dst="lib", src=".", keep_path=False)
        self.copy("*.lib", dst="lib", src=".", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")
