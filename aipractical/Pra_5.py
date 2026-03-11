import itertools 
 
def solve_crypto(equation): 
    left, right = equation.replace(" ", "").split("=") 
    words = left.split("+") + [right] 
 
    letters = sorted(set("".join(words))) 
    if len(letters) > 10: 
        print("Too many letters (max 10)") 
        return 
 
    first_letters = set(word[0] for word in words) 
    digits = range(10) 
 
    for perm in itertools.permutations(digits, len(letters)): 
        mapping = dict(zip(letters, perm)) 
 
        # Leading letter cannot be zero 
        if any(mapping[ch] == 0 for ch in first_letters): 
            continue 
 
        def value(word): 
            return int("".join(str(mapping[c]) for c in word)) 
 
        if sum(value(w) for w in words[:-1]) == value(words[-1]): 
            print("Solution:") 
            for k in sorted(mapping): 
                print(k, "=", mapping[k]) 
            print("Verified:", equation) 
            return 
 
    print("No solution found") 
 
# Example usage 
solve_crypto("SEND + MORE = MONEY")