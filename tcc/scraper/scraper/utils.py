def strip_nbsp(string_list: list[str]) -> list[str]:
    return [item.strip().strip("\xa0") for item in string_list if item]
