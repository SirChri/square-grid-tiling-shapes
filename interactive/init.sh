#https://github.com/Semantic-Org/Semantic-UI/issues/7073
CHECK_OS="`uname -s`"
if [[ "$CHECK_OS" = "Darwin" ]]; then
    sed -i '' 's/;;/;/g' node_modules/semantic-ui-css/semantic.min.css
    sed -i '' 's/;;/;/g' node_modules/semantic-ui-css/semantic.css
else 
    sed -i 's/;;/;/g' node_modules/semantic-ui-css/semantic.min.css
    sed -i 's/;;/;/g' node_modules/semantic-ui-css/semantic.css
fi