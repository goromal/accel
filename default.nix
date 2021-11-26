{ local ? true,
}:
let
    pkgs = import (if local then <nixpkgs> else builtins.fetchGit (import ./src.nix)) {};
    python = pkgs.python37;
    pypkgs = python.pkgs;
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
      rev = "90a35f640baa66764165d9e2221e0c985ca1541e";
      ref = "master";
    }) { inherit pkgs; };
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
    preConfigure = ''
      mkdir -p $out/mgc
      cp -r ${manif-geom-cpp}/* $out/mgc/
      chmod -R 777 $out/mgc
      ls $out
    '';
    postInstall = ''
      echo $out
      ls $out
      echo "----------"
      ls $out/bin
      echo "----------"
      ls $out/bin/accel
      echo "----------"
      ls $out/lib
      echo "----------"
      ls $out/lib/python3.7/site-packages
      echo "----------"
      ls $out/lib/python3.7/site-packages/accel
      echo "----------"
      ls $out/mgc
      echo "----------"
    '';
}
