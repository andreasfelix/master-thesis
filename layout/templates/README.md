<h1 align="center">$title$</h1>

- **Author:** $author$
- **Supervisors:** $supervisor-1st$ and $supervisor-2nd$
- **Institution:** [$department$, $faculty$, $university$]($department-website$)
- **Date:** $date$

<div align="center">

| [![Screen](https://api.iconify.design/carbon:screen.svg) Web](https://$github$.github.io/$repository$/) | [![PDF](https://api.iconify.design/carbon:document-pdf.svg) PDF](https://$github$.github.io/$repository$/thesis.pdf) |
| - | - |

</div>

## Abstract

$abstract$


## Build Instructions

1. Start development shell

    ```console
    nix develop
    ```

1. Render web version

    ```console
    make html
    ```

1. Render printable HTML

    ```console
    make print
    ```
1. Serve `dist` folder and save `print.html` from Google Chrome as `dist/thesis.pdf`

    ```console
    live-server dist
    ```

1. Add bookmarks and metadata to PDF

    ```console
    python layout/bookmarks.py
    ```

1. (Optional) Render README.md from template `layout/templates/README.md`

    ```console
    make README.md
    ```

1. Deploy `dist` folder to GitHub Pages

    ```console
    make deploy
    ```
