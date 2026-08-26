import urllib.request
import re
import matplotlib.pyplot as plt
import numpy as np
import ssl

# Ignore SSL verification
ssl._create_default_https_context = ssl._create_unverified_context

# 1. Dictionary and rules
rules = {
    'a': 'a', 'b': 'bé', 'c': 'cé', 'd': 'dé', 'e': 'eu',
    'f': 'effe', 'g': 'gé', 'h': 'ache', 'i': 'i', 'j': 'ji',
    'k': 'ka', 'l': 'elle', 'm': 'emme', 'n': 'enne', 'o': 'o',
    'p': 'pé', 'q': 'cu', 'r': 'erre', 's': 'esse', 't': 'té',
    'u': 'u', 'v': 'vé', 'w': 'doublevé', 'x': 'ixe', 'y': 'igrec',
    'z': 'zède', 'é': 'é', 'è': 'è'
}

def strip_accents(s):
    import unicodedata
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    return s.lower()

explosive_letters = set(['f', 'l', 'm', 'n', 'r', 's', 'w', 'y'])
safe_letters = set('abcdefghijklmnopqrstuvwxyz') - explosive_letters

# URL from Daniel Miessler SecLists (French words)
url = "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Miscellaneous/lang-french-full.txt"
try:
    print(f"Downloading wordlist from {url}...")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(req)
    words = response.read().decode('utf-8').splitlines()
    print(f"Downloaded {len(words)} words.")
except Exception as e:
    print(f"Could not download French dict: {e}")
    words = ["bonjour", "au", "revoir", "cacao", "caduc", "boutique", "paquebot", "capuche", "bagage", "cabotage", "objectif"]

longest_safe_words = []
max_len = 0

for w in words:
    clean_w = strip_accents(w).strip()
    if not clean_w.isalpha():
        continue
    if any(c in explosive_letters for c in clean_w):
        continue
    if len(clean_w) > max_len:
        max_len = len(clean_w)
        longest_safe_words = [clean_w]
    elif len(clean_w) == max_len:
        longest_safe_words.append(clean_w)

longest_safe_words = list(set(longest_safe_words))
print(f"Longest safe words (length {max_len}): {longest_safe_words}")
with open("longest_safe_words.txt", "w") as f:
    f.write(f"Longest safe words (length {max_len}): {', '.join(longest_safe_words)}\n")

# 2. Game of Life visualization
def generate_history(word, iterations=15):
    history = [word]
    current = word
    for _ in range(iterations):
        current = "".join(rules.get(char, char) for char in current)
        history.append(current)
    return history

def plot_history(history, filename, title):
    alphabet_ext = "abcdefghijklmnopqrstuvwxyzéè "
    char_to_int = {c: i for i, c in enumerate(alphabet_ext)}
    
    max_len = max(len(h) for h in history)
    matrix = np.zeros((len(history), max_len))
    
    for i, h in enumerate(history):
        pad_left = (max_len - len(h)) // 2
        for j, char in enumerate(h):
            matrix[i, pad_left + j] = char_to_int.get(char, char_to_int[' '])
            
    matrix_masked = np.ma.masked_where(matrix == char_to_int[' '], matrix)
    
    plt.figure(figsize=(12, 10))
    plt.imshow(matrix_masked, cmap='tab20', aspect='auto', interpolation='nearest')
    plt.title(title)
    plt.xlabel('Position dans la chaîne')
    plt.ylabel('Génération (Itération)')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()

if longest_safe_words:
    safe_word = longest_safe_words[0]
    hist_safe = generate_history(safe_word, iterations=15)
    plot_history(hist_safe, 'game_of_life_safe.png', f"Évolution du mot stable '{safe_word}'")

hist_explosive = generate_history("ouf", iterations=12)
plot_history(hist_explosive, 'game_of_life_explosive.png', "Évolution du mot 'ouf' (Explosion due au 'f')")

print("Generated game of life visualizations.")
