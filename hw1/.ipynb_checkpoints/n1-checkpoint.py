# Прочитал, какие символы могут быть записаны в пользовательской части адреса эл. почты: https://habr.com/ru/articles/224623/
# Выяснил, что в том числе допустимы символы '._+-, на основе этой информации создал переменную login_symbols
# Для доменной части ограничения чуть жестче: https://askdev.ru/q/kakie-simvoly-dopuskayutsya-v-adrese-elektronnoy-pochty-2149/
# Допустимые символы описаны в переменной domain_symbols
# Важно, что домен не может начинаться и заканчиваться дефисом или точкой, логин не может начинаться со знака препинания


def check_adress(login, domain):
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
adress_correct = True
if '@' in s:
    at = s.find('@')
    adress_correct = check_adress(s[:at], s[at + 1:])
else:
    adress_correct = False

if adress_correct:
    print('Correct email adress')
else:
    print('Incorrect email adress')
