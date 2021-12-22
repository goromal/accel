{ stdenv
, cleanSource
, cmake
, clang
, git
, eigen
, glog
, gflags
, suitesparse
, manif-geom-cpp 
, ceres-src
, python
, pybind11-src
}:
stdenv.mkDerivation {
    name = "pyceres";
    version = "1.0.0";
    src = cleanSource ./pyceres-src/.;
    nativeBuildInputs = [
        cmake
        clang
        git
        python
    ];
    buildInputs = [
        eigen
        manif-geom-cpp
        glog
        gflags
        suitesparse
    ];
    prePatch = ''
        mkdir pyceres-src
        mv *.cpp pyceres-src
        mv AddToCeres.cmake pyceres-src
        mkdir ceres-solver
        cp -r ${ceres-src}/* ceres-solver/
        mv pyceres-src ceres-solver/pyceres-src
        chmod -R 777 ceres-solver
        mkdir ceres-solver/pyceres-src/pybind11
        cp -r ${pybind11-src}/* ceres-solver/pyceres-src/pybind11/
        chmod -R 777 ceres-solver/pyceres-src/pybind11
    '';
    patches = [
        "ceres-build.patch"
    ];
    configurePhase = ''
        cd ceres-solver
        mkdir ceres-bin && cd ceres-bin
        cmake -DBUILD_TESTING=OFF -DBUILD_EXAMPLES=OFF -DBUILD_BENCHMARKS=OFF ..
    '';
    installPhase = ''
        mkdir -p $out/lib
        mv lib/pyceres* $out/lib
    '';
}
    