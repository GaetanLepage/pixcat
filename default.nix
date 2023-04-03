{pkgs ? import <nixpkgs> {}}: let
  py = pkgs.python3Packages;
in
  py.buildPythonPackage {
    pname = "pixcat";
    version = "0.5";
    src = pkgs.lib.cleanSource ./.;

    format = "pyproject";

    nativeBuildInputs = [py.setuptools];

    propagatedBuildInputs = with py; [
      numpy
      matplotlib
      opencv4
    ];

    pythonImportsCheck = ["pixcat"];

    postPatch = ''
      substituteInPlace pyproject.toml --replace "opencv-python" "opencv"
    '';
  }
