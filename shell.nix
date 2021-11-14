{ local ? true,
}:
let
    pkgs = import (if local then <nixpkgs> else builtins.fetchGit (import ./src.nix)) { };
    python = pkgs.python37;
    accel = import ./default.nix { inherit local; };
in with pkgs;
with python.pkgs;
mkShell rec {
    buildInputs = [
        accel
        virtualenv
	ffmpeg
	scipy
	networkx
#        black
#        flake8
#        mypy
    ];
    shellHook = ''
        virtualenv --no-setuptools venv
        export PATH="$PWD/venv/bin:$PATH"
        export PYTHONPATH=venv/lib/python3.7/site-packages/:$PYTHONPATH
    '';
    postShellHook = ''
        ln -sf PYTHONPATH/* ${virtualenv}/lib/python3.7/site-packages
    '';
}
