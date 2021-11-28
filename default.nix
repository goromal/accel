{ local ? true,
}:
let
    pkgs = import (if local then <nixpkgs> else builtins.fetchGit (import ./src.nix)) {};
    python = pkgs.python37;
    pypkgs = python.pkgs;
    pythonLibDir = "lib/python${python.passthru.pythonVersion}/site-packages";
    pybind11 = pkgs.fetchgit {
        fetchSubmodules = true;
        url = "https://github.com/pybind/pybind11.git";
        rev = "07e225932235ccb0db5271b0874d00f086f28423";
        sha256 = "1wb57ff1xnblg7m136226ihfv1v01q366d54l08wi8hky19jcfh0";
    };
    ceres = pkgs.fetchgit {
        fetchSubmodules = true;
        url = "https://github.com/ceres-solver/ceres-solver.git";
        rev = "31008453fe979f947e594df15a7e254d6631881b";
        sha256 = "1qbc21ivwy7vwfshh6iasyvbdri85inkwy3gnnxyvk8dkpw2m1vl";
    };
    manif-geom-cpp = import (builtins.fetchGit {
        url = "https://github.com/goromal/manif-geom-cpp.git";
        rev = "c2514789a97c473760723b99b121af3de13ddcc3";
        ref = "dev/se3-run";
    }) { inherit pkgs; };
    geometry = import ./accel/math/geometry.nix {
        inherit pkgs;
        inherit manif-geom-cpp;
        inherit python;
        inherit pybind11;
    };
in python.pkgs.buildPythonPackage rec {
    pname = "accel";
    version = "0.0.0";
    src = pkgs.lib.cleanSource ./.;
    propagatedBuildInputs = [
        pypkgs.numpy
        pypkgs.requests
        pypkgs.colorama
	    pypkgs.ffmpeg-python
	    pypkgs.scipy
	    pypkgs.networkx
    ];
    doCheck = false;
    postInstall = ''
        cp -r ${geometry}/lib/geometry* $out/${pythonLibDir}/accel/math/
        chmod -R 777 $out/${pythonLibDir}
    '';
}
