{ local ? true,
}:
let
    pkgs = import (if local then <nixpkgs> else builtins.fetchGit (import ./src.nix)) {};
    pybind11-src = pkgs.fetchgit {
        fetchSubmodules = true;
        url = "https://github.com/pybind/pybind11.git";
        rev = "07e225932235ccb0db5271b0874d00f086f28423";
        sha256 = "1wb57ff1xnblg7m136226ihfv1v01q366d54l08wi8hky19jcfh0";
    };
    ceres-src = pkgs.fetchgit {
        fetchSubmodules = true;
        url = "https://github.com/ceres-solver/ceres-solver.git";
        rev = "31008453fe979f947e594df15a7e254d6631881b";
        sha256 = "1qbc21ivwy7vwfshh6iasyvbdri85inkwy3gnnxyvk8dkpw2m1vl";
    };
    stdenv = pkgs.clangStdenv;
    cmake = pkgs.cmake;
    clang = pkgs.clang;
    eigen = pkgs.eigen;
    git = pkgs.git;
    glog = pkgs.glog;
    gflags = pkgs.gflags;
    suitesparse = pkgs.suitesparse;
    cleanSource = pkgs.lib.cleanSource;
    manif-geom-cpp = import (builtins.fetchGit {
        url = "https://github.com/goromal/manif-geom-cpp.git";
        rev = "3ca0626df33139fb3a6a711008f9b7252c6577cb";
        ref = "master";
    } + "/manif-geom-cpp.nix") { 
        inherit stdenv;
        inherit cleanSource;
        inherit cmake;
        inherit clang;
        inherit git;
        inherit eigen;
        boost = pkgs.boost;
    };
    runCommand = pkgs.runCommand;
    python = pkgs.python37;
    buildPythonPackage = pkgs.python37.pkgs.buildPythonPackage;
    numpy = pkgs.python37.pkgs.numpy;
    requests = pkgs.python37.pkgs.requests;
    colorama = pkgs.python37.pkgs.colorama;
    ffmpeg-python = pkgs.python37.pkgs.ffmpeg-python;
    scipy = pkgs.python37.pkgs.scipy;
    networkx = pkgs.python37.pkgs.networkx;
    osqp = pkgs.python37.pkgs.osqp;
in import ./accel.nix {
    inherit pybind11-src;
    inherit ceres-src;
    inherit stdenv;
    inherit cmake;
    inherit clang;
    inherit eigen;
    inherit git;
    inherit glog;
    inherit gflags;
    inherit suitesparse;
    inherit cleanSource;
    inherit runCommand;
    inherit manif-geom-cpp;
    inherit python;
    inherit buildPythonPackage;
    inherit numpy;
    inherit requests;
    inherit colorama;
    inherit ffmpeg-python;
    inherit scipy;
    inherit networkx;
    inherit osqp;
}
