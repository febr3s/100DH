# Build your MOREL website from a Zotero collection in 10 simple steps
1. **Check if you have the requirements**
  - A [Zotero account](https://www.zotero.org/user/register/)
  - A [GitHub account](https://github.com/signup)
2. **Prepare the Zotero Fields** for a MOREL website. MOREL items are added in the same way that items are added in any [Zotero library](https://www.zotero.org/support/adding_items_to_zotero). In its current version, MOREL can only process items of type `book`. Since not all the fields needed for MOREL are available for the `book` content type, some considerations must be made:
  - Excerpt: the fragment from each MOREL record corresponds to the `notes` of Zotero (see the [documentation](https://www.zotero.org/support/notes) about Zotero notes). In its current version, MOREL *only accepts one excerpt per book*.
  - Cover: the cover is a jpg file that is added as an `attachment` to the Zotero item (see the Zotero attachments [documentation](https://www.zotero.org/support/attaching_files)).
3. **[Fork](https://github.com/morelrep/morel-no-code-generator/fork) this repository** — that is, [create a copy](https://github.com/morelrep/morel-no-code-generator/fork) in your [GitHub](https://github.com) account.
4. **Go to the `actions` tab** and enable workflows.
5. **Open `_config.yml`** and change:
   - The `title` to your site's.
   - The `tagline` to your site's.
   - The `email` and/or social media accounts to your site's.
   - The `jotform` link (create your free account at https://www.jotform.com/). 
  > The Jorform account is to receive contributions from users
6. **Wait for the site to build**. Go to the `actions` tab, and wait for the workflow icon run to turn green. Sometimes GitHub gets slow. If it takes too long to build, or it fails, wait a couple of hours and edit the `_config.yml` file again to trigger the process.

![alt text](assets/img/tema/workflow.png)

7. **Replace or add to `assets/img/tema`** your preferred:
   - logo.png
   - pattern.png
   - avatar.png
8. **Go to the `settings` tab**, open the `pages` section, and select `gh-pages` as the branch that will build the site.

9. **Open the file `_abouts/site-description.md`** and write a description for your site. The `<!-- more -->` line separates what appears in the footer across all pages from the longer description that appears on the `about` page only.
10. **Generate the content from Zotero** by [exporting a collection](https://forums.zotero.org/discussion/5286/can-one-export-a-collection-and-not-the-entire-library), subcollection or library as a `csv` file, and replacing the content of `assets/data/books_zotero.csv`.
# Other features
To add cover images to your MOREL site, follow these steps:
1. Add a cover image to your item in your Zotero library by dragging it as an attachment
2. Clone the repository in a local folder
3. Create a Python environment from the root of the folder using ```python3 -m venv assets/env```
4. Run ```source assets/env/bin/activate```
5. Run ```pip install r requirements.txt``
6. Export your library or collection from Zotero as .csv file, and save it as `assets/data/books_zotero.csv`. Remember to check the "add notes" option to add excerpts.
7. Run ```python3 assets/env/src/morel-generate.py```
8. Commit your changes **adding ```[skip ci]``` to the commit message**.
9. Push your changes to GitHub.
# To add cover images with no code
For a MOREL no-code generator with cover images drawn from a Zotero library you can:

- [Request an invoice](mailto:proyectomorel@gmail.com) for a customized service
- [Promote this project](https://www.addtoany.com/share#url=http%3A%2F%2F127.0.0.1%3A4000%2Fmorel-no-code-generator%2F&title=%7C%20MOREL%20no-code%20website%20generator) to find code contributors that help develping this feature.