name: pylint

on: [push, pull_request]

jobs:
  PEP8:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Setup Python
        uses: actions/setup-python@v2.2.2
        with:
          python-version: 3.9

      - name: Install Python lint libraries
        run: |
          pip install autopep8 autoflake
      - name: Check for showstoppers
        run: |
          autopep8 --verbose --in-place --recursive --aggressive --aggressive . *.py
      - name: Remove unused imports and variables
        run: |
          autoflake --in-place --recursive --remove-all-unused-imports --remove-unused-variables --ignore-init-module-imports .
      # commit changes
      - uses: stefanzweifel/git-auto-commit-action@v4
        with:
          commit_message: 'pylint: auto fixes'
          commit_options: '--no-verify --signoff'
          repository: .
          commit_user_name: KENZO-404
          commit_user_email: latukolan404@gmail.com
          commit_author: KENZO-404 <latukolan404@gmail.com>
