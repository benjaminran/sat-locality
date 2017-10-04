#!/usr/bin/env bash
# Usage: gen-single.sh
#
# Run a single experiment

script="$0"
root="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"
notebooks="${root}/notebooks"
experiments="${root}/experiments"

show_help() {
    cat "${script}" | tail -n +2 | while read l; do [[ "$l" =~ ^#\ ? ]] && echo "${l:2}" || break; done
}

link_latest() {
    experiment_dir="${1}"
    [[ -L "${experiment_dir}/../latest" ]] && rm "${experiment_dir}/../latest"
    ln -s "${experiment_dir}" "${experiment_dir}/../latest"
}

main() {
    while :; do
        case $1 in
            -h|-\?|--help)
                show_help
                exit
                ;;
            *)
                break
        esac
        shift
    done

    key="$(date "+%Y-%m-%d-%H-%M-%S")"
    experiment_dir="${experiments}/${key}"
    mkdir -p "${experiment_dir}"
    link_latest "${experiment_dir}"
    cp "${notebooks}/Circle.ipynb" "${experiment_dir}"
    nohup jupyter nbconvert --ExecutePreprocessor.timeout=None --to html --execute "${experiment_dir}/Circle.ipynb" <"/dev/null" >"${experiment_dir}/nbconvert.out" 2>"${experiment_dir}/nbconvert.err" &
    echo "Output will be written in ${experiment_dir}"
}

main "$@"