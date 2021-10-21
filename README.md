# Github Action Image Resizing

This is a Github Action for resizing images in your project.

In main.py you will find the implementation of the code to resize the images using the library `Pillow`.


# Inputs

| Input      | Description | Required | Default |
| ----------- | ----------- | ----------- |  ----------- |
| `DEBUG` | Will print debug messages (True/False) | `false` | False
| `IMAGES_MAX_WIDTH`      | Max width of the images       | `true`
| `IMAGES_QUALITY`   | Quality of the reized image 0-100        | `false` | 100
| `IMAGES_FORMATS`   | Formats we are going to resize (Comma separated)        | `true` | "jpg, jpge, png"
| `IMAGES_DIRECTORIES`   | Directories we are going to be looking the images in (Comma separated)         | `true` |
| `IMAGES_PREFIX`   | Prefix to add when renaming the images        | `false` |""
| `IMAGES_SUFFIX`   | Suffix  to add when renaming the images     | `false` |""



# Output

| Output      | Description | 
| ----------- | ----------- | 
| `result` | Images that were resized) |


# Example of Usage

This workflow could be used to re size the images on every `pull_request`. After this it will push the commit to the same PR.

```
name: Resize images

on: [pull_request]

jobs:
  build:
    name: Github Action Image Resizing
    runs-on: ubuntu-latest
    steps:

      - uses: actions/checkout@master

      - name: Resize Images
        id: resize-images

        # You can change the version as well
        uses: gonzalonaveira/gh-image-resizing@master
        with:
          IMAGES_MAX_WIDTH: "1500"
          IMAGES_QUALITY: "90"
          IMAGES_FORMATS: "jpg, jpge, png" 
          IMAGES_DIRECTORIES: "public/assets/blog/images"

      - name: Commit changes
        uses: EndBug/add-and-commit@v4
        with:
          add: 'public/'
          author_name: "github-actions[bot]"
          author_email: "github-actions@users.noreply.github.com"
          message: |
            Images Reszied by Github action
            ${{steps.resize-images.outputs.result}}
            
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```