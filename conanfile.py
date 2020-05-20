from conans import ConanFile, tools, Meson, VisualStudioBuildEnvironment
import glob
import os
import shutil



def get_plugins():
    return get_internal_plugins() + get_plugins_with_external_deps()

def get_plugin_libs_by_plugin(plugin_name):
    libs = {
        "aalib": ["aasink"],
        "alpha": ["alpha", "alphacolor"],
        "debugutils": ["navigationtest", "debug"],
        "flx": ["flxdec"],
        "gdk-pixbuf": ["gdkpixbuf"],
        "gtk3": ["gtk"],
        "law": ["alaw", "mulaw"],
        "libcaca": ["cacasink"],
        "oss": ["ossaudio"],
        "pulse": ["pulsesink"],
        "qt": ["qmlgl"],
        "raw1394": ["1394"],
        "y4m": ["y4menc"]
    }

    if plugin_name in libs:
        return libs[plugin_name]
    else:
        return [plugin_name]

def get_internal_plugins():
    return [
        "alpha",
        "apetag",
        "audiofx",
        "audioparsers",
        "auparse",
        "autodetect",
        "avi",
        "cutter",
        "debugutils",
        "deinterlace",
        "dtmf",
        "effectv",
        "equalizer",
        "flv",
        "flx",
        "goom",
        "goom2k1",
        "icydemux",
        "id3demux",
        "imagefreeze",
        "interleave",
        "isomp4",
        "law",
        "level",
        "matroska",
        "monoscope",
        "multifile",
        "multipart",
        "replaygain",
        "rtp",
        "rtpmanager",
        "rtsp",
        "shapewipe",
        "smpte",
        "spectrum",
        "udp",
        "videobox",
        "videocrop",
        "videofilter",
        "videomixer",
        "wavenc",
        "wavparse",
        "y4m"
    ]

# Feature options for plugins with external deps
def get_plugins_with_external_deps():
    return get_plugins_with_external_deps_with_conan_package() + \
        get_plugins_with_external_system_deps() + \
        get_plugins_with_external_deps_without_conan_package()

def get_plugins_with_external_deps_with_conan_package():
    return [
        "cairo",
        "flac",
        "gdk-pixbuf",
        "gtk3",
        "jpeg",
        "lame",
        "mpg123",
        "png"
    ]

def get_plugins_with_external_system_deps():
    return [
        "directsound",
        "osxaudio",
        "osxvideo"
    ]

def get_plugins_with_external_deps_without_conan_package():
    return [
        "aalib",
        "dv",
        "dv1394",
        "jack",
        "libcaca",
        "oss",
        "oss4",
        "pulse",
        "qt5",
        "shout2",
        "soup",
        "speex",
        "taglib",
        "twolame",
        "vpx",
        "waveform",
        "wavpack",
        "ximagesrc",
        "v4l2"
    ]








class GStPluginsGoodConan(ConanFile):
    name = "gst-plugins-good"
    description = "GStreamer is a development framework for creating applications like media players, video editors, " \
                  "streaming media broadcasters and so on"
    topics = ("conan", "gstreamer", "multimedia", "video", "audio", "broadcasting", "framework", "media")
    url = "https://github.com/bincrafters/conan-gst-plugins-good"
    homepage = "https://gstreamer.freedesktop.org/"
    license = "GPL-2.0-only"
    settings = "os", "arch", "compiler", "build_type"

    options = dict({
        "shared": [True, False],
        "fPIC": [True, False],
        "with_bz2": [True, False],
        "ximagesrc-xshm": [True, False],
        "ximagesrc-xfixes": [True, False],
        "ximagesrc-xdamage": [True, False],
        "v4l2-probe": [True, False],
        "v4l2-libv4l2": [True, False],
        "v4l2-gudev": [True, False]},
        **{"with_"+plugin: [True, False] for plugin in get_plugins()},
    )
    default_options = dict({
        "shared": True,
        "fPIC": True,
        "with_bz2": True,
        "ximagesrc-xshm": True,
        "ximagesrc-xfixes": True,
        "ximagesrc-xdamage": True,
        "v4l2-probe": True,
        "v4l2-libv4l2": True,
        "v4l2-gudev": False},
        **{"with_"+plugin: True for plugin in get_internal_plugins()},
        **{"with_"+plugin: True for plugin in get_plugins_with_external_deps_with_conan_package()},
        **{"with_"+plugin: True for plugin in get_plugins_with_external_system_deps()},
        **{"with_"+plugin: False for plugin in get_plugins_with_external_deps_without_conan_package()}
    )

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"
    exports_sources = ["patches/*.patch"]

    requires = ("gstreamer/1.16.0@bincrafters/stable", "gst-plugins-base/1.16.0@bincrafters/stable")
    generators = "pkg_config"

    @property
    def _is_msvc(self):
        return self.settings.compiler == "Visual Studio"

    def configure(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd
        self.options['gstreamer'].shared = self.options.shared
        self.options['gst-plugins-base'].shared = self.options.shared

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

        if self.settings.os != 'Windows':
            del self.options.with_directsound
        if self.settings.os != 'Linux':
            del self.options.with_oss
            del self.options.with_oss4
            del self.options.with_pulse
            del self.options.ximagesrc
            del self.options["ximagesrc-xshm"]
            del self.options["ximagesrc-xfixes"]
            del self.options["ximagesrc-xdamage"]
            del self.options.v4l2
            del self.options["v4l2-probe"]
            del self.options["v4l2-libv4l2"]
            del self.options["v4l2-gudev"]
        if self.settings.os != 'Macos':
            del self.options.with_osxaudio
            del self.options.with_osxvideo

    def requirements(self):
        if self.options.with_bz2:
            self.requires("bzip2/1.0.8@")
        if self.options.with_cairo:
            self.requires("cairo/1.17.2@bincrafters/stable")
        if self.options.with_flac:
            self.requires("flac/1.3.3@")
        if self.options["gdk-pixbuf"]:
            self.requires("gdk-pixbuf/2.40.0@bincrafters/stable")
        if self.options.with_gtk3:
            self.requires("gtk/3.24.18@bincrafters/stable")
        if self.options.with_jpeg:
            self.requires("libjpeg/9c@")
        if self.options.with_lame:
            self.requires("libmp3lame/3.100")
        if self.options.with_mpg123:
            self.requires("libmpg123/1.25.13@bincrafters/stable")
        if self.options.with_png:
            self.requires("libpng/1.6.37@")

    def build_requirements(self):
        self.build_requires("meson/0.54.1")
        if not tools.which("pkg-config"):
            self.build_requires("pkg-config_installer/0.29.2@bincrafters/stable")
        self.build_requires("bison_installer/3.3.2@bincrafters/stable")
        self.build_requires("flex_installer/2.6.4@bincrafters/stable")

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        os.rename("%s-%s" % (self.name, self.version), self._source_subfolder)

    def _apply_patches(self):
        for patch in self.conan_data["patches"][self.version]:
            tools.patch(**patch)

    def _configure_meson(self):
        defs = dict()

        def add_flag(name, value):
            if name in defs:
                defs[name] += " " + value
            else:
                defs[name] = value

        def add_compiler_flag(value):
            add_flag("c_args", value)
            add_flag("cpp_args", value)

        def add_linker_flag(value):
            add_flag("c_link_args", value)
            add_flag("cpp_link_args", value)

        def add_bool_option(option):
            defs[option] = "true" if self.options.get_safe(option) else "false"
        def add_feature_option(option):
            defs[option] = "enabled" if self.options.get_safe(option) else "disabled"

        meson = Meson(self)
        if self.settings.compiler == "Visual Studio":
            add_linker_flag("-lws2_32")
            add_compiler_flag("-%s" % self.settings.compiler.runtime)
            if int(str(self.settings.compiler.version)) < 14:
                add_compiler_flag("-Dsnprintf=_snprintf")
        if self.settings.get_safe("compiler.runtime"):
            defs["b_vscrt"] = str(self.settings.compiler.runtime).lower()

        for plugin in get_plugins():
            add_feature_option("with_"+plugin)
        add_feature_option("with_bz2")
        if self.options.get_safe("with_ximagesrc"):
            add_feature_option("ximagesrc-xshm")
            add_feature_option("ximagesrc-xfixes")
            add_feature_option("ximagesrc-xdamage")
        if self.options.get_safe("with_v4l2"):
            add_bool_option("v4l2-probe")
            add_feature_option("v4l2-libv4l2")
            add_feature_option("v4l2-gudev")

        defs["examples"] = "disabled"
        defs["tests"] = "disabled"
        defs["nls"] = "disabled"
        defs["orc"] = "disabled"
        defs["doc"] = "disabled"
        meson.configure(build_folder=self._build_subfolder,
                        source_folder=self._source_subfolder,
                        defs=defs)
        return meson

    def _copy_pkg_config(self, name):
        root = self.deps_cpp_info[name].rootpath
        pc_dir = os.path.join(root, 'lib', 'pkgconfig')
        pc_files = glob.glob('%s/*.pc' % pc_dir)
        if not pc_files:  # zlib store .pc in root
            pc_files = glob.glob('%s/*.pc' % root)
        for pc_name in pc_files:
            new_pc = os.path.basename(pc_name)
            self.output.warn('copy .pc file %s' % os.path.basename(pc_name))
            shutil.copy(pc_name, new_pc)
            prefix = tools.unix_path(root) if self.settings.os == 'Windows' else root
            tools.replace_prefix_in_pc_file(new_pc, prefix)

    def build(self):
        self._apply_patches()
        self._copy_pkg_config("cairo")
        self._copy_pkg_config("glib")
        self._copy_pkg_config("gstreamer")
        self._copy_pkg_config("gst-plugins-base")
        with tools.environment_append(VisualStudioBuildEnvironment(self).vars) if self._is_msvc else tools.no_op():
            meson = self._configure_meson()
            meson.build()

    def _fix_library_names(self, path):
        # regression in 1.16
        if self.settings.compiler == "Visual Studio":
            with tools.chdir(path):
                for filename_old in glob.glob("*.a"):
                    filename_new = filename_old[3:-2] + ".lib"
                    self.output.info("rename %s into %s" % (filename_old, filename_new))
                    shutil.move(filename_old, filename_new)

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        with tools.environment_append(VisualStudioBuildEnvironment(self).vars) if self._is_msvc else tools.no_op():
            meson = self._configure_meson()
            meson.install()

        self._fix_library_names(os.path.join(self.package_folder, "lib"))
        self._fix_library_names(os.path.join(self.package_folder, "lib", "gstreamer-1.0"))

    def package_info(self):
        gst_plugin_path = os.path.join(self.package_folder, "lib", "gstreamer-1.0")
        if self.options.shared:
            self.output.info("Appending GST_PLUGIN_PATH env var : %s" % gst_plugin_path)
            self.env_info.GST_PLUGIN_PATH.append(gst_plugin_path)
        else:
            self.cpp_info.defines.append("GST_PLUGINS_GOOD_STATIC")
            self.cpp_info.libdirs.append(gst_plugin_path)
            for plugin in get_plugins():
                if self.options.get_safe("with_{}".format(plugin)):
                    for lib in get_plugin_libs_by_plugin(plugin):
                        self.cpp_info.libs.append("gst{}".format(lib))



