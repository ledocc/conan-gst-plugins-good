from conans import ConanFile, CMake, tools
import os


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = ("cmake", "virtualrunenv")

    def build(self):
        cmake = CMake(self)

        options = []
        for name, value in self.options["gst-plugins-good"].items():
            if name.startswith("with_") and value:
                options.append( name.upper().replace("-","_") )
        cmake.definitions["GST_PLUGINS_GOOD_OPTIONS"] = ";".join(options)

        cmake.configure()
        cmake.build()

    def test(self):
        if not tools.cross_building(self.settings):
            bin_path = os.path.join("bin", "test_package")
            self.run(bin_path, run_environment=True)
