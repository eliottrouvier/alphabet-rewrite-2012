import numpy as np

def simulate_h_sequence(iterations: int):
    """Simule l'expansion de la suite h = ache."""
    rules = {
        'h': 'ache',
        'a': 'a',
        'c': 'cé',
        'e': 'eu',
        'é': 'é',
        'u': 'u'
    }
    
    current_string = "h"
    print(f"Itération 0 (Longueur {len(current_string):2}) : {current_string}")
    
    for i in range(1, iterations + 1):
        # On applique la règle à chaque caractère
        next_string = "".join(rules[char] for char in current_string)
        current_string = next_string
        
        # On n'affiche la chaîne complète que pour les premières itérations pour garder le terminal lisible
        display_str = current_string if len(current_string) < 60 else current_string[:57] + "..."
        print(f"Itération {i} (Longueur {len(current_string):3}) : {display_str}")

def analyze_growth_rate():
    """Calcule le taux de croissance via la matrice de transition."""
    # Alphabet : ['h', 'a', 'c', 'e', 'é', 'u']
    # M[i, j] = nombre de fois que la lettre 'i' est produite par la lettre 'j'
    
    M = np.array([
        [1, 0, 0, 0, 0, 0],  # Ligne h : produite par h
        [1, 1, 0, 0, 0, 0],  # Ligne a : produite par h, a
        [1, 0, 1, 0, 0, 0],  # Ligne c : produite par h, c
        [1, 0, 0, 1, 0, 0],  # Ligne e : produite par h, e
        [0, 0, 1, 0, 1, 0],  # Ligne é : produite par c, é
        [0, 0, 0, 1, 0, 1]   # Ligne u : produite par e, u
    ])
    
    # Calcul des valeurs propres
    eigenvalues, _ = np.linalg.eig(M)
    
    print("\n--- Analyse Mathématique ---")
    print(f"Matrice de transition M :\n{M}")
    print(f"Valeurs propres : {np.real(eigenvalues)}")

if __name__ == "__main__":
    simulate_h_sequence(5)
    analyze_growth_rate()