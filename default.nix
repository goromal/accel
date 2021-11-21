{ local ? true,
}:
let
    pkgs = import (if local then <nixpkgs> else builtins.fetchGit (import ./src.nix)) {};
    python = pkgs.python37;
    pypkgs = python.pkgs;
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
}
