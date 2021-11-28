{ pkgs
, manif-geom-cpp 
, python
, pybind11
}:
pkgs.clangStdenv.mkDerivation {
    name = "geometry";
    version = "1.0.0";
    src = pkgs.lib.cleanSource ./geometry-src/.;
    nativeBuildInputs = [
        pkgs.cmake
        pkgs.clang
        pkgs.git
        python
    ];
    buildInputs = [
        pkgs.eigen
        manif-geom-cpp
    ];
    prePatch = ''
        mkdir pybind11
        cp -r ${pybind11}/* pybind11/
        chmod -R 777 pybind11
    '';
    configurePhase = ''
        mkdir build && cd build
        cmake ..
    '';
    installPhase = ''
        mkdir -p $out/lib
        cp -r geometry* $out/lib
    '';
}