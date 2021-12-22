{ pybind11-src
, ceres-src
, stdenv
, cmake
, clang
, eigen
, git
, glog
, gflags
, suitesparse
, manif-geom-cpp
, cleanSource
, runCommand
, python
, buildPythonPackage
, numpy
, requests
, colorama
, ffmpeg-python
, scipy
, networkx
, osqp
}:
let
    pythonLibDir = "lib/python${python.passthru.pythonVersion}/site-packages";
    geometry = import ./accel/math/geometry.nix {
        inherit stdenv;
        inherit cleanSource;
        inherit manif-geom-cpp;
        inherit python;
        inherit pybind11-src;
        inherit cmake;
        inherit clang;
        inherit git;
        inherit eigen;
    };
    pyceres = import ./accel/math/pyceres.nix {
        inherit stdenv;
        inherit cleanSource;
        inherit cmake;
        inherit clang;
        inherit git;
        inherit eigen;
        inherit glog;
        inherit gflags;
        inherit suitesparse;
        inherit manif-geom-cpp;
        inherit ceres-src;
        inherit python;
        inherit pybind11-src;
    };
    getVersion = root: builtins.fromJSON (builtins.readFile (
        runCommand "get_accel_version" { buildInputs = [ python ]; } ''
        python ${root}/scripts/make_manifest.py > $out
        ''));
    versionInfo = getVersion ./.;
in buildPythonPackage rec {
    pname = versionInfo.pname;
    version = versionInfo.version;
    src = cleanSource ./.;
    propagatedBuildInputs = [
        numpy
        requests
        colorama
	    ffmpeg-python
	    scipy
	    networkx
	    osqp
    ];
    doCheck = false;
    postInstall = ''
        cp -r ${geometry}/lib/geometry* $out/${pythonLibDir}/accel/math/
        cp -r ${pyceres}/lib/pyceres* $out/${pythonLibDir}/accel/math/
        chmod -R 777 $out/${pythonLibDir}
    '';
}
