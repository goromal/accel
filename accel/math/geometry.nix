{ pkgs
, manif-geom-cpp 
, python
, pybind11
}:
pkgs.clangStdenv.mkDerivation {
    name = "manif-geom-py";
    version = "1.0.0";
    src = pkgs.lib.cleanSource ./geometry-src/.;
    
    nativeBuildInputs = [
        pkgs.cmake
        pkgs.clang
        pkgs.git
        python
    ];
    
    buildInputs = [
        pkgs.eigen
    ];
    
    prePatch = ''
        mkdir pybind11
        mkdir manif-geom-cpp
        echo "--------"
        ls
        echo "--------"
    '';
    
    # TODO
}