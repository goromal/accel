{ pkgs
, manif-geom-cpp 
, ceres
, python
, pybind11
}:
pkgs.clangStdenv.mkDerivation {
    name = "pyceres";
    version = "1.0.0";
    src = pkgs.lib.cleanSource ./pyceres-src/.;
    nativeBuildInputs = [
        pkgs.cmake
        pkgs.clang
        pkgs.git
        python
    ];
    buildInputs = [
        pkgs.eigen
        pkgs.manif-geom-cpp
        pkgs.glog
        pkgs.gflags
        pkgs.suitesparse
    ];
    prePatch = ''
        mkdir pyceres-src
        mv *.cpp pyceres-src
        mv AddToCeres.cmake pyceres-src
        mkdir ceres-solver
        cp -r ${ceres}/* ceres-solver/
        mv pyceres-src ceres-solver/pyceres-src
        chmod -R 777 ceres-solver
        mkdir ceres-solver/pyceres-src/pybind11
        cp -r ${pybind11}/* ceres-solver/pyceres-src/pybind11/
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
    