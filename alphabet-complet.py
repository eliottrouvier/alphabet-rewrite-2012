def classify_alphabet_complexity():
    # Définition du dictionnaire phonétique complet (système fermé)
    rules = {
        'a': 'a', 'b': 'bé', 'c': 'cé', 'd': 'dé', 'e': 'eu',
        'f': 'effe', 'g': 'gé', 'h': 'ache', 'i': 'i', 'j': 'ji',
        'k': 'ka', 'l': 'elle', 'm': 'emme', 'n': 'enne', 'o': 'o',
        'p': 'pé', 'q': 'cu', 'r': 'erre', 's': 'esse', 't': 'té',
        'u': 'u', 'v': 'vé', 'w': 'doublevé', 'x': 'ixe', 'y': 'igrec',
        'z': 'zède', 'é': 'é', 'è': 'è'
    }
    
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    iterations = 10
    results = {}

    for letter in alphabet:
        current = letter
        lengths = [len(current)]
        
        # Simulation de l'expansion
        for _ in range(iterations):
            current = "".join(rules[char] for char in current)
            lengths.append(len(current))
            
        # Calcul des différences finies (dérivées discrètes)
        # d1 = vélocité (différence première)
        d1 = [lengths[i+1] - lengths[i] for i in range(len(lengths)-1)]
        # d2 = accélération (différence seconde)
        d2 = [d1[i+1] - d1[i] for i in range(len(d1)-1)]
        
        # Classification mathématique
        if all(l == lengths[0] for l in lengths):
            complexity = "O(1)   - Constante"
        # Si la vélocité finit par se stabiliser (constante sur les 3 derniers termes)
        elif d1[-1] == d1[-2] == d1[-3]:
            complexity = "O(n)   - Linéaire"
        # Si l'accélération finit par se stabiliser
        elif d2[-1] == d2[-2] == d2[-3]:
            complexity = "O(n²)  - Quadratique"
        else:
            complexity = "O(2^n) - Exponentielle"
            
        results[letter] = complexity

    # Affichage trié par complexité
    print("--- Complexité de l'alphabet français ---")
    sorted_results = sorted(results.items(), key=lambda x: x[1])
    for char, comp in sorted_results:
        print(f"Lettre {char.upper()} : {comp}")

if __name__ == "__main__":
    classify_alphabet_complexity()