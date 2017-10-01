#!/usr/bin/env bash
# Usage: gen-single.sh
#
# Run a single experiment

script="$0"
root="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"
notebooks="${root}/notebooks"
experiments="${root}/experiments"

main() {
    while :; do
        case $1 in
            -h|-\?|--help)
                cat "${script}" | tail -n +2 | while read l; do [[ "$l" =~ ^#\ ? ]] && echo "${l:2}" || break; done
                exit
                ;;
            *)
                break
        esac
        shift
    done

    experiment_dir="${experiments}/$(date "+%Y-%m-%d-%H-%M-%S")"
    mkdir -p "${experiment_dir}"
    old_dir=$(pwd)
    cd "${experiment_dir}"
    cp "${notebooks}/Circle.ipynb" .
    nohup jupyter nbconvert --to html --execute "Circle.ipynb" >"nbconvert.out" 2>"nbconvert.err" &
    cd "${old_dir}"
    [[ -L "${experiments}/latest" ]] && rm "${experiments}/latest"
    ln -s "${experiment_dir}" "${experiments}/latest"
    echo "Output will be written in ${experiment_dir}"
}

main "$@"