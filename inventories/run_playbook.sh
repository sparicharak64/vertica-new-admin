set -e
set -x

ansible-playbook -f 9 inventories/provisionaccess.yml \
    --extra-vars "group_vars/all" \
    --vault-password-file ./.vault-pw.txt