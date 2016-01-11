#!/usr/bin/env bash

set -x
set -e

if grep -q $1 relicensed.txt; then
    exit
fi

crate_uri=$1
repo_name=$(python3 repo_name.py $1)
if [ $? = 2 ]; then
    exit
fi
dir_name=${repo_name}-$(uuidgen)
issue_link=$(python3 license_issue.py $1)
git clone --depth 1 $1 $dir_name
pushd $dir_name
hub fork
cp ../mit-template.txt LICENSE-MIT
cp ../pr-template.txt .

sed -i -e "s|{{project_name}}|$repo_name|" LICENSE-MIT pr-template.txt
sed -i -e "s|{{repo_id}}|$dir_name|" LICENSE-MIT pr-template.txt
sed -i -e "s|{{relicense_issue}}|$issue_link|" pr-template.txt
sed -i -e 's_^license =.*$_license = "MIT OR Apache-2.0"_' Cargo.toml
git rm LICENSE LICENSE.md
cp ../LICENSE-APACHE .

if [ -e README.rst ];
    cat ../readme-junk.rst.txt >> README.rst
else
    cat ../readme-junk.md.txt >> README.md
fi

git add LICENSE-{MIT,APACHE} Cargo.toml README.md
git commit -m "Relicense to dual MIT/Apache-2.0

Closes $issue_link" --no-gpg-sign

git push -f cmr
hub pull-request -F pr-template.txt
popd

echo $crate_uri >> relicensed.txt
sleep 1m
