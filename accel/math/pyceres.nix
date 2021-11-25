{ pkgs
, ceres 
, python
, pybind11
}:
pkgs.clangStdenv.mkDerivation {
    name = "pyceres";
    version = "0.0.0";
    src = pkgs.lib.cleanSource ./.;
    
    nativeBuildInputs = [
        pkgs.cmake
        pkgs.clang
        pkgs.git
        python
    ];

    buildInputs = [
        pkgs.eigen
        pkgs.glog
        pkgs.gflags
        pkgs.suitesparse
    ];

    prePatch = ''
        mkdir ceres-solver
        cp -r ${ceres}/* ceres-solver
        chmod -R 777 ceres-solver
        mkdir pyceres-src/pybind11
        cp -r ${pybind11}/* pyceres-src/pybind11
        chmod -R 777 pyceres-src/pybind11
    '';

    patches = [
        "ceres-build.patch"
    ];

    configurePhase = ''
        cd ceres-solver
        ln -s ../pyceres-src
        mkdir ceres-bin && cd ceres-bin
        cmake -DBUILD_TESTING=OFF -DBUILD_EXAMPLES=OFF -DBUILD_BENCHMARKS=OFF ..
    '';

    installPhase = ''
        mkdir -p $out/bin
        mv lib/* $out/bin
    '';
}
    