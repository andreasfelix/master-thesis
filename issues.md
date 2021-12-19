# Issues

* [Firefox version 83 and above do not reset page counter correctly](https://bugzilla.mozilla.org/show_bug.cgi?id=1679712)
    * e.g. first page has the number 9, but the table of contents seems to be correct
    * Use Firefox 81 or Chromium to generate PDF from `print.html`
    * Install Firefox 81 with nix:

        ```console
        nix-env -i firefox-81.0 -f https://github.com/NixOS/nixpkgs/archive/2c162d49cd5b979eb66ff1653aecaeaa01690fcc.tar.gz
        ```