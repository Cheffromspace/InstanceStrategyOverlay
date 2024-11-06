#!/bin/bash
find . -type f -name "*:*" | while read file; do
    newname=$(echo "$file" | sed "s/:/ -/g")
    git mv "$file" "$newname"
done
