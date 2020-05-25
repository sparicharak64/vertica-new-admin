set -e
set -x

ansible-playbook -f 10 -f 9 $1 "${@:2}" \
    --extra-vars "@group_vars/all" \
    --vault-password-file ./.vault-pw.txt \
    --limit master