{
  description = "LVM Project Dependencies";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
    utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, utils, ... }:
  utils.lib.eachDefaultSystem(
    system:
    let
      pkgs = import nixpkgs { inherit system; };
    in
    {
      devShells.default = pkgs.mkShell {
        buildInputs = with pkgs; [
          (python311.withPackages (ps: [
                                   ps.seaborn
                                   ps.pandas
                                   ps.numpy
                                   ps.jupyter
                                   ps.z3
          ]))
        ];
      };
    }
  );
}
