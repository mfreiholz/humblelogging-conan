from conan import ConanFile
from conan.tools.scm import Git
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout

class HumbleLoggingConanfile(ConanFile):
	name = "humblelogging"
	version = "0.0.0"
	description = "C++ Logging Library"
	license = "THE BEER-WARE LICENSE"
	homepage = "https://github.com/mfreiholz/humblelogging"

	git_url = "https://github.com/mfreiholz/humblelogging.git"
	git_tag = "main"

	settings = "os", "compiler", "build_type", "arch"
	options = {"shared": [True, False], "fPIC": [True, False]}
	default_options = {"shared": False, "fPIC": True}

	def source(self):
		git = Git(self)
		git.clone(url=self.git_url, target=".")
		git.checkout(self.git_tag)

	def config_options(self):
		if self.settings.os == "Windows":
			del self.options.fPIC

	def layout(self):
		cmake_layout(self)

	# The requirements method allows you to define the dependencies of your recipe
	def requirements(self):
		pass

	def build_requirements(self):
		self.requires("cmake/[>=3.14]")
		pass

	def generate(self):
		tc = CMakeToolchain(self)
		tc.variables["BuildShared"] = "ON" if self.options.shared else "OFF"
		tc.variables["BuildTests"] = "OFF"
		tc.variables["BuildApps"] = "OFF"
		tc.generate()

	# This method is used to build the source code of the recipe using the desired commands.
	def build(self):
		cmake = CMake(self)
		cmake.configure()
		cmake.build()

	# The actual creation of the package, once it's built, is done in the package() method.
	# Using the copy() method from tools.files, artifacts are copied
	# from the build folder to the package folder
	def package(self):
		cmake = CMake(self)
		cmake.install()
		# copy(self, "*.h", self.source_folder, join(self.package_folder, "include"), keep_path=False)

	def package_info(self):
		self.cpp_info.libs = ["humblelogging"]
