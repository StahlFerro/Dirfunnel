#!/usr/bin/env bash

input=""

function show_menu {
    title="Dirclone"
    version="0.0.1"
    echo "=============================== $title v$version ==============================="
    echo "1. List target directories"
    echo "2. List save directory"
    echo "3. Add/update target directory"
    echo "4. Remove target directory"
    echo "5. Add/update save directory"
    echo "6. Copy target directories into save directory (existing overwrite)"
    echo "7. Show python version"
}

until [[ $input == "q" ]]
do {
    source venv/bin/activate
    show_menu
    echo -n "Please enter a number. Enter q to quit "
    read input
    echo ""
    case $input in
        "1") python main.py list ;;
        "2") python main.py save-info ;;
        "3")
            echo -n "Enter designation name: "
            read name
            echo -n "Enter target directory path: "
            read path
            if [[ $name != "" ]] && [[ $path != "" ]]; then
                python main.py add $name $path
            else
                echo "Please do not leave one or more of the arguments blank!"
            fi
            ;;
        "4")
            echo -n "Enter designation name: "
            read name
            if [[ $name != "" ]]; then
                python main.py remove $name
            else
                echo "Please do not leave one or more of the arguments blank!"
            fi
            ;;
        "5")
            echo -n "Enter save directory: "
            read name
            if [[ $name != "" ]]; then
                python main.py set-save $name
            else
                echo "Please do not leave one or more of the arguments blank!"
            fi
            ;;
        "6") python main.py clone ;;
        "7") python --version ;;
        "q") deactivate return ;;
        *)
    esac
    echo ""
    read -p "Press any key to continue...: "
}
done