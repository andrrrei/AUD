# I've read about the symbols allowed in the user part of an email address here: https://habr.com/ru/articles/224623/ 
# and found out that symbols like '._+- are allowed. Based on this information, I created a variable named login_symbols.
# For the domain part, restrictions are slightly stricter: https://askdev.ru/q/kakie-simvoly-dopuskayutsya-v-adrese-elektronnoy-pochty-2149/
# Allowed symbols described in the variable domain_symbols.
# It's important to note that a domain cannot start or end with a hyphen or a dot, and a login cannot start with a punctuation mark.

def check_address(login, domain):
    if len(login) < 1 or len(domain) < 3:
        return False
    login_symbols = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890'._+-"
    domain_symbols = "qwertyuiopasdfghjklzxcvbnm1234567890-."
    if login[0] not in login_symbols[:login_symbols.find("'")]:
        return False
    if domain[0] in '-.' or domain[len(domain) - 1] in '-.':
        return False
    if domain.find('.') == -1:
        return False
    for symb in login[1:]:
        if symb not in login_symbols:
            return False
    for symb in domain:
        if symb not in domain_symbols:
            return False
    return True

s = input()
address_correct = True
if '@' in s:
    at = s.find('@')
    address_correct = check_address(s[:at], s[at + 1:])
else:
    address_correct = False

if address_correct:
    print('Correct email address')
else:
    print('Incorrect email address')
