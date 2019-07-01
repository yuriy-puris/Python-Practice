
logins_map = {"Kseniia": "ksu", "Alexey": "alex74"}


def get_from_dict(name):
    if name in logins_map:
        return logins_map[name]
    else:
        return "default value"


print(get_from_dict("Kseniia"))
print(get_from_dict("Vitaly"))

print(logins_map.get("Kseniia"))
print(logins_map.get("Vitaly", "default value"))
