#!/bin/bash 
# To generate or update the .po files
# $ sh update_i18n.sh
# 
# To compile to .mo files for release
# sh update_i18n.sh mocompile

PRODUCT=$(sed -rn "s/^[[:space:]]*i18n_domain[[:space:]]*=[[:space:]]*[\"']?([^\"']*)[\"']?(.*)$/\1/p" configure.zcml)

# if you want to add new language, add the language
# to the following list (separated by space)
LANGUAGES='es'

if [ -z "$1" ]; then

    for lang in $LANGUAGES; do
        mkdir -p locales/$lang/LC_MESSAGES/
        touch locales/$lang/LC_MESSAGES/$PRODUCT.po
    done

    i18ndude rebuild-pot --pot locales/$PRODUCT.pot --create $PRODUCT ./


    # merge with manual manteined po files, if it exist
    if [ -f locales/manual-$PRODUCT.pot ]; then
       i18ndude merge --pot locales/$PRODUCT.pot --merge locales/manual-$PRODUCT.pot
    fi

    # filter out invalid PO file headers. i18ndude sync adds them to the file, 
    # but i18ntestcase fails if these headers are there
    for lang in $LANGUAGES; do
        i18ndude sync --pot locales/$PRODUCT.pot locales/$lang/LC_MESSAGES/$PRODUCT.po
        mv locales/$lang/LC_MESSAGES/$PRODUCT.po locales/$lang/LC_MESSAGES/$PRODUCT.potmp
        grep -vE "^\"(Language|Domain).*" locales/$lang/LC_MESSAGES/$PRODUCT.potmp  >locales/$lang/LC_MESSAGES/$PRODUCT.po
        rm  locales/$lang/LC_MESSAGES/$PRODUCT.potmp
    done

elif [ "$1" = "mocompile" ]; then

    for lang in $LANGUAGES; do
        PO_FILE=locales/$lang/LC_MESSAGES/$PRODUCT.po
        MO_FILE=locales/$lang/LC_MESSAGES/$PRODUCT.mo

        if [ -r "$PO_FILE" ]; then
            echo "Compiling ${MO_FILE}"
            msgfmt -o $MO_FILE $PO_FILE
        else
            echo "Warning: ${PO_FILE} not found"
        fi
    done

fi
