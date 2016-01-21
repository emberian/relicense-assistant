#!/usr/bin/env bash

set -e

if grep -q $1 relicensed.txt bad-clone.txt unable.txt bad-fork.txt no-issue.txt bad-push.txt bad-pr.txt; then
    exit
else
    if [[ $1 == *google-apis-rs* ]]; then
        exit
    fi
fi

crate_uri=$1
repo_name=$(python3 repo_name.py $1)
dir_name=${repo_name}-$(uuidgen)
issue_link=$(python3 license_issue.py $1 || false)
if [ $status == 2 -o $status == 1 ]; then
    echo $crate_uri >> no-issue.txt
    exit
fi
git clone --depth 1 $1 $dir_name || (echo $crate_uri >> bad-clone.txt && exit)

echo $dir_name >> .gitignore
pushd $dir_name
if grep -q "Temporary Redirect" <(hub fork); then
    echo $crate_uri >> ../bad-fork.txt
    popd
    exit
fi
cp ../mit-template.txt LICENSE-MIT
cp ../pr-template.txt .

sed -i -e "s|{{project_name}}|$repo_name|" LICENSE-MIT pr-template.txt || (echo $crate_uri >> ../unable.txt && popd && exit)
sed -i -e "s|{{repo_id}}|$dir_name|" LICENSE-MIT pr-template.txt || (echo $crate_uri >> ../unable.txt && popd && exit)
sed -i -e "s|{{relicense_issue}}|$issue_link|" pr-template.txt || (echo $crate_uri >> ../unable.txt && popd && exit)
sed -i -e 's_^license =.*$_license = "MIT OR Apache-2.0"_' Cargo.toml || (echo $crate_uri >> ../unable.txt && popd && exit)
git rm --ignore-unmatch LICENSE LICENSE.md || (echo $crate_uri >> ../unable.txt && popd && exit)
cp ../LICENSE-APACHE .

if [ -e README.rst ]; then
    cat ../readme-junk.rst.txt >> README.rst
else
    cat ../readme-junk.md.txt >> README.md
fi

git add LICENSE-{MIT,APACHE} Cargo.toml README.*
git commit -m "Relicense to dual MIT/Apache-2.0

Closes $issue_link" --no-gpg-sign

git push -f cmr || (echo $crate_uri >> ../bad-push.txt && exit)
hub pull-request -F pr-template.txt || (echo $crate_uri >> ../bad-pr.txt && exit)

popd

echo $crate_uri >> relicensed.txt
#sleep 1m
