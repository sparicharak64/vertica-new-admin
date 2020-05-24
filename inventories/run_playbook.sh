ansible-playbook -f 9 provisionaccess.yml \
    --extra-vars "@group_vars/all" \
    --vault-password-file ./.vault-pw.txt