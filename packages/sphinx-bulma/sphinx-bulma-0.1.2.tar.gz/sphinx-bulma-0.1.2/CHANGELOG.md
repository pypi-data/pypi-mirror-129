# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]


## [0.1.2] - 2021/12/02

### Changed

- Edit required Python version

## [0.1.1] - 2021/11/11

### Updated

- Bump sass from 1.43.3 to 1.43.4
- Bump nodemon from 2.0.14 to 2.0.15
- Bump sphinx from 4.2.0 to 4.3.0

## [0.1.0] - 2021/10/31

### Updated

- All **npm** dev dependencies into new versions without security issues
- Main font family now is **Josefin Sans** and **Courier Prime** for code highlights
- Main theme layout now is mostly `Bulma` classes (or `@extend` ones)

### Removed

- All `sass` files from project `scss/module` folder (new components on `scss/components`)
- Many deprecated tags from **Sphinx** template generation
- Old **GitHub** action file

### Changed

- Fontello icons font uses new and different icons now (including custom **Sphinx** and **Bulma** icons)
- Moved from deprecated `node-sass` npm package into **Dart** `sass` package
- Use of deprecated and outdated `cpy` npm package for npm commands, now using `copyfiles` package
- No longer uses `KarmaCSS` package, changed to `Bulma` styles
- Project name from `sphinx_karma_theme` to `sphinx-bluma`

### Added

- Dark and light color palettes using native **CSS** and **JavaScript**
- Custom code highlights styling
- Support for favicon and `navbar` logo
- New theme options `display_git`, `git_host`, `git_user`, `git_repo`, `git_blob`, `git_version`, `git_icon`, `git_desc`, `default_palette`, `sidebar`, `primary`, and `primary_invert`
- Appended new copyright notice (under same license)
- Use examples

[Unreleased]: https://github.com/oAGoulart/sphinx-bulma/compare/v0.1.1...master
[0.1.1]: https://github.com/oAGoulart/sphinx-bulma/releases/tag/v0.1.1
[0.1.0]: https://github.com/oAGoulart/sphinx-bulma/releases/tag/v0.1.0
