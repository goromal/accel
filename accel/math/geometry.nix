{ stdenv
, cleanSource
, manif-geom-cpp 
, python
, pybind11-src
, cmake
, clang
, git
, eigen
}:
stdenv.mkDerivation {
    name = "geometry";
    version = "1.0.0";
    src = cleanSource ./geometry-src/.;
    nativeBuildInputs = [
        cmake
        clang
        git
        python
    ];
    buildInputs = [
        eigen
        manif-geom-cpp
    ];
    prePatch = ''
        mkdir pybind11
        cp -r ${pybind11-src}/* pybind11/
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