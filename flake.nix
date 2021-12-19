{
  description = "master-thesis";
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/release-21.11";
    flake-utils.url = "github:numtide/flake-utils";
  };
  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (
      system: with nixpkgs.legacyPackages.${system};
      {
        devShell =
          pkgs.mkShell {
            buildInputs = with pkgs; [
              gnumake
              pandoc
              haskellPackages.pandoc-crossref
              nodePackages.live-server
              yq-go
              (python3.withPackages (packages: with packages; [ pymupdf pyyaml ]))
            ];
          };
      }
    );
}
