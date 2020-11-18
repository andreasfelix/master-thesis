with import <nixpkgs> {};
mkShell {
    buildInputs = [
        gnumake
        pandoc
        haskellPackages.pandoc-crossref
        nodePackages.live-server
    ];
    shellHook = "
        echo Master-Thesis Shell
    ";
}
