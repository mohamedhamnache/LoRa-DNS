def reverse_endian(hexastring):
    return "".join(
        reversed([hexastring[i : i + 2] for i in range(0, len(hexastring), 2)])
    )
