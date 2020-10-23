with import <nixpkgs> {};
mkShell {
    buildInputs = [
        gnumake
        pandoc
        haskellPackages.pandoc-crossref
        haskellPackages.pandoc-citeproc
        nodePackages.live-server
    ];
    shellHook = "
        echo Master-Thesis Shell
    ";
}
