import random
import hashlib
import string
import base64
import math
from datetime import datetime
import time
import sys

class CyberSecurityPuzzle:
    def __init__(self):
        self.current_level = 1
        self.score = 0
        self.hints_used = 0
        
    def loading_animation(self, duration=2, message="Memuat teka-teki"):
        """Animasi loading yang keren"""
        animation_chars = ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"]
        end_time = time.time() + duration
        
        print(f"\n{message}", end="")
        
        while time.time() < end_time:
            for char in animation_chars:
                print(f"\r{message} {char}", end="", flush=True)
                time.sleep(0.1)
        
        print(f"\r{message} ✓ Selesai!   ")
    
    def show_level_up_animation(self, level):
        """Menampilkan animasi dan ASCII art untuk level up"""
        ascii_arts = [
            """
            ╔══════════════════════════════╗
                    LEVEL {} LULUS!       
            ║       🎉 SELAMAT! 🎉        ║
            ║                              ║
                ➤ Melanjutkan tantangan   
            ╚══════════════════════════════╝
            """,
            """
            ████████████████████████████████
            ██                            ██
                 ⚡ LEVEL {} BERHASIL! ⚡ 
            ██                            ██
                 ➤ Naik level!           
            ████████████████████████████████
            """,
            """
            ┌──────────────────────────────┐
                 💀 LEVEL {} TERKUAK! 💀   
            │                              │
                ➤ Menuju tantangan lebih  
            │      menantang!              │
            └──────────────────────────────┘
            """,
            """
            ✨⋆｡‧˚ʚ🍃ɞ˚‧｡⋆✨⋆｡‧˚ʚ🍃ɞ˚‧｡⋆✨
                  LEVEL {} TERSELESAIKAN!
            ✨⋆｡‧˚ʚ🍃ɞ˚‧｡⋆✨⋆｡‧˚ʚ🍃ɞ˚‧｡⋆✨
                ➤ Lanjut ke level berikutnya!
            """,
            """
            ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
            ░░                            ░░
                 🔓 LEVEL {} TERBUKA! 🔓 
            ░░                            ░░
               ➤ Persiapan tantangan   
            ░░      selanjutnya!          ░░
            ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
            """
        ]
        
        art = random.choice(ascii_arts).format(level)
        print("\n" + "="*50)
        print(art)
        
        # Animasi countdown untuk level berikutnya
        print("\nMelanjutkan ke level {} dalam:".format(level + 1))
        for i in range(3, 0, -1):
            print(f"⏰ {i}...", end=" ", flush=True)
            time.sleep(1)
        print("GO! 🚀")
        print("="*50 + "\n")
    
    def show_welcome_animation(self):
        """Animasi pembuka yang keren"""
        welcome_text = """
        ╔══════════════════════════════════════════════╗
        ║              CYBER SECURITY PUZZLE           ║
                          🛡️ WELCOME 🛡️               
        ║                                              ║
        ║   Siap menjadi ahli keamanan cyber?          ║
        ║   Pecahkan semua teka-teki dan naik level!   ║
        ╚══════════════════════════════════════════════╝
        """
        print(welcome_text)
        
        # Animasi loading awal
        self.loading_animation(3, "Mempersiapkan sistem keamanan")
        
    def show_game_over_animation(self):
        """Animasi game over"""
        game_over_text = """
        ╔══════════════════════════════════════════════╗
        ║                 GAME OVER                    ║
                      🎯 FINAL SCORE 🎯              
        ║                                              ║
        ║   Level Tertinggi: {:2d}                     ║
        ║   Skor Akhir:     {:3d}                      ║
        ║   Hint Digunakan: {:2d}                      ║
        ║                                              ║
        ║   Terima kasih telah bermain!                ║
        ║   Tingkatkan skill keamanan cyber Anda!      ║
        ╚══════════════════════════════════════════════╝
        """.format(self.current_level, self.score, self.hints_used)
        print(game_over_text)

    def generate_puzzle(self, level):
        """Menghasilkan teka-teki berdasarkan level"""
        self.loading_animation(1, "Membuat tantangan keamanan")
        
        puzzle_types = [
            self.password_cracking,
            self.caesar_cipher,
            self.xor_encryption,
            self.hash_cracking,
            self.base64_decoding,
            self.rail_fence_cipher,
            self.vigenere_cipher,
            self.rsa_simple,
            self.binary_decoding,
            self.steganography_simple
        ]
        
        # Untuk level tinggi, kombinasikan beberapa metode
        if level > len(puzzle_types):
            # Pilih beberapa metode acak untuk dikombinasi
            num_methods = min(level // 5 + 2, len(puzzle_types))
            selected_methods = random.sample(puzzle_types, num_methods)
            
            # Gabungkan teka-teki
            combined_puzzle = {
                'type': 'combined',
                'methods': selected_methods,
                'level': level,
                'description': f"Teka-teki kombinasi level {level} - {num_methods} metode"
            }
            return combined_puzzle
        else:
            return puzzle_types[level % len(puzzle_types)](level)
    
    def password_cracking(self, level):
        """Teka-teki cracking password dengan kompleksitas meningkat"""
        length = min(5 + level // 2, 20)
        complexity = min(level // 3, 4)
        
        chars = string.ascii_lowercase
        if complexity >= 1:
            chars += string.digits
        if complexity >= 2:
            chars += string.punctuation
        if complexity >= 3:
            chars += string.ascii_uppercase
            
        password = ''.join(random.choice(chars) for _ in range(length))
        hint = f"Password terdiri dari {length} karakter"
        
        if complexity == 0:
            hint += " (hanya huruf kecil)"
        elif complexity == 1:
            hint += " (huruf dan angka)"
        elif complexity == 2:
            hint += " (huruf, angka, dan simbol)"
        else:
            hint += " (semua karakter)"
            
        return {
            'type': 'password',
            'question': f"Crack password berikut: {password}",
            'answer': password,
            'hint': hint,
            'level': level
        }
    
    def caesar_cipher(self, level):
        """Teka-teki Caesar cipher dengan shift yang semakin kompleks"""
        shift_range = min(5 + level * 2, 26)
        shift = random.randint(-shift_range, shift_range)
        
        text = self.generate_random_text(level)
        encrypted = self.caesar_encrypt(text, shift)
        
        return {
            'type': 'caesar',
            'question': f"Decode pesan Caesar cipher: {encrypted}",
            'answer': text,
            'hint': f"Shift antara -{shift_range} dan {shift_range}",
            'level': level
        }
    
    def xor_encryption(self, level):
        """Teka-teki XOR encryption dengan kunci yang semakin panjang"""
        key_length = min(1 + level // 3, 10)
        key = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(key_length))
        
        text = self.generate_random_text(level)
        encrypted = self.xor_encrypt(text, key)
        
        # Encode dalam base64 untuk tampilan yang lebih bersih
        encrypted_b64 = base64.b64encode(encrypted.encode()).decode()
        
        return {
            'type': 'xor',
            'question': f"Decode pesan XOR (base64): {encrypted_b64}",
            'answer': text,
            'hint': f"Kunci XOR memiliki {key_length} karakter",
            'level': level
        }
    
    def hash_cracking(self, level):
        """Teka-teki hash cracking dengan algoritma yang semakin sulit"""
        algorithms = ['md5', 'sha1', 'sha256', 'sha512']
        algo_index = min(level // 3, len(algorithms) - 1)
        algorithm = algorithms[algo_index]
        
        # Untuk level rendah, gunakan kata sederhana
        if level < 5:
            word_list = ["password", "admin", "hello", "secret", "cyber", "security", "hacker", "python", "code", "game"]
            word = random.choice(word_list)
        else:
            # Untuk level tinggi, gunakan kata acak
            word = self.generate_random_text(level // 2)
        
        if algorithm == 'md5':
            hash_value = hashlib.md5(word.encode()).hexdigest()
        elif algorithm == 'sha1':
            hash_value = hashlib.sha1(word.encode()).hexdigest()
        elif algorithm == 'sha256':
            hash_value = hashlib.sha256(word.encode()).hexdigest()
        else:  # sha512
            hash_value = hashlib.sha512(word.encode()).hexdigest()
        
        return {
            'type': 'hash',
            'question': f"Crack hash {algorithm.upper()}: {hash_value}",
            'answer': word,
            'hint': f"Gunakan teknik {algorithm.upper()} hashing. Kata mungkin dalam wordlist umum",
            'level': level
        }
    
    def base64_decoding(self, level):
        """Teka-teki decoding base64 dengan multiple encoding di level tinggi"""
        text = self.generate_random_text(level)
        encoded = text
        
        # Untuk level tinggi, lakukan encoding berulang
        iterations = min(1 + level // 5, 5)
        for i in range(iterations):
            encoded = base64.b64encode(encoded.encode()).decode()
        
        return {
            'type': 'base64',
            'question': f"Decode Base64 (diencode {iterations} kali): {encoded}",
            'answer': text,
            'hint': f"Perlu decode Base64 sebanyak {iterations} kali",
            'level': level
        }
    
    def rail_fence_cipher(self, level):
        """Teka-teki Rail Fence cipher dengan rails yang semakin banyak"""
        rails = min(2 + level // 4, 8)
        text = self.generate_random_text(level)
        encrypted = self.rail_fence_encrypt(text, rails)
        
        return {
            'type': 'rail_fence',
            'question': f"Decode Rail Fence cipher: {encrypted}",
            'answer': text,
            'hint': f"Menggunakan {rails} rails",
            'level': level
        }
    
    def vigenere_cipher(self, level):
        """Teka-teki Vigenere cipher dengan kunci yang semakin panjang"""
        key_length = min(2 + level // 3, 15)
        key = ''.join(random.choice(string.ascii_uppercase) for _ in range(key_length))
        
        text = self.generate_random_text(level).upper()
        encrypted = self.vigenere_encrypt(text, key)
        
        return {
            'type': 'vigenere',
            'question': f"Decode Vigenere cipher: {encrypted}",
            'answer': text,
            'hint': f"Kunci memiliki {key_length} karakter (huruf besar)",
            'level': level
        }
    
    def rsa_simple(self, level):
        """Teka-teki RSA sederhana dengan bilangan yang semakin besar"""
        # Untuk level rendah, gunakan bilangan kecil
        max_prime = min(50 + level * 10, 1000)
        
        # Pilih dua bilangan prima
        primes = [i for i in range(2, max_prime) if self.is_prime(i)]
        if len(primes) < 2:
            primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]  # Fallback primes
        
        p, q = random.sample(primes, 2)
        
        n = p * q
        phi = (p - 1) * (q - 1)
        
        # Pilih e (public exponent)
        e = 65537 if 65537 < phi else 3
        
        # Hitung d (private exponent)
        d = self.mod_inverse(e, phi)
        
        # Encode pesan sederhana
        message = str(random.randint(1, 100))
        encrypted = pow(int(message), e, n)
        
        return {
            'type': 'rsa',
            'question': f"Decrypt RSA: n={n}, e={e}, ciphertext={encrypted}",
            'answer': message,
            'hint': f"Faktorisasi n menjadi dua bilangan prima. n = p * q dimana p dan q adalah bilangan prima",
            'level': level
        }
    
    def binary_decoding(self, level):
        """Teka-teki decoding biner dengan kompleksitas meningkat"""
        text = self.generate_random_text(level)
        
        # Untuk level tinggi, tambahkan encoding lain
        if level > 10:
            # Konversi ke hex dulu, lalu ke biner
            hex_text = text.encode().hex()
            binary = ''.join(format(ord(c), '08b') for c in hex_text)
        else:
            binary = ''.join(format(ord(c), '08b') for c in text)
        
        # Format binary untuk readability
        formatted_binary = ' '.join([binary[i:i+8] for i in range(0, len(binary), 8)])
        
        return {
            'type': 'binary',
            'question': f"Decode biner: {formatted_binary}",
            'answer': text,
            'hint': "Setiap 8 bit mewakili satu karakter ASCII",
            'level': level
        }
    
    def steganography_simple(self, level):
        """Teka-teki steganografi sederhana"""
        # Buat pesan tersembunyi dalam teks
        hidden_message = self.generate_random_text(min(level, 10))
        
        # Buat teks pembungkus
        wrapper_text = " ".join([self.generate_random_word() for _ in range(10 + level)])
        
        # Sembunyikan pesan (untuk kesederhanaan, kita beri tahu posisinya)
        positions = random.sample(range(len(wrapper_text.split())), len(hidden_message.split()))
        words = wrapper_text.split()
        
        for i, pos in enumerate(positions):
            if pos < len(words):
                words[pos] = hidden_message.split()[i % len(hidden_message.split())]
        
        stego_text = " ".join(words)
        
        return {
            'type': 'steganography',
            'question': f"Temukan pesan tersembunyi: {stego_text}",
            'answer': hidden_message,
            'hint': f"Pesan tersembunyi terdiri dari {len(hidden_message.split())} kata",
            'level': level
        }
    
    # Helper methods
    def generate_random_text(self, length_factor):
        """Menghasilkan teks acak dengan panjang berdasarkan level"""
        length = max(3, min(3 + length_factor, 15))  # Batasi panjang teks
        words = [self.generate_random_word() for _ in range(length)]
        return " ".join(words)
    
    def generate_random_word(self):
        """Menghasilkan kata acak"""
        length = random.randint(3, 8)
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))
    
    def caesar_encrypt(self, text, shift):
        """Enkripsi Caesar cipher"""
        result = ""
        for char in text:
            if char.isalpha():
                ascii_offset = ord('a') if char.islower() else ord('A')
                result += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
            else:
                result += char
        return result
    
    def xor_encrypt(self, text, key):
        """Enkripsi XOR"""
        result = ""
        for i, char in enumerate(text):
            result += chr(ord(char) ^ ord(key[i % len(key)]))
        return result
    
    def rail_fence_encrypt(self, text, rails):
        """Enkripsi Rail Fence cipher"""
        # Hapus spasi untuk penyederhanaan
        text = text.replace(" ", "")
        
        fence = [[] for _ in range(rails)]
        rail = 0
        direction = 1
        
        for char in text:
            fence[rail].append(char)
            rail += direction
            if rail == 0 or rail == rails - 1:
                direction = -direction
        
        return ''.join(''.join(rail) for rail in fence)
    
    def vigenere_encrypt(self, text, key):
        """Enkripsi Vigenere cipher"""
        result = ""
        key_index = 0
        
        for char in text:
            if char.isalpha():
                ascii_offset = ord('A')
                shift = ord(key[key_index % len(key)]) - ascii_offset
                result += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
                key_index += 1
            else:
                result += char
        
        return result
    
    def is_prime(self, n):
        """Cek apakah bilangan prima"""
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
            
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            if n % i == 0:
                return False
        return True
    
    def mod_inverse(self, a, m):
        """Hitung modular inverse"""
        for d in range(1, m):
            if (d * a) % m == 1:
                return d
        return 1
    
    def solve_combined_puzzle(self, puzzle, user_answer):
        """Menyelesaikan puzzle kombinasi"""
        # Untuk kombinasi, kita perlu memeriksa setiap metode
        correct = True
        for method in puzzle['methods']:
            # Buat puzzle individual untuk setiap metode
            individual_puzzle = method(puzzle['level'])
            # Periksa apakah jawaban user mengandung jawaban yang benar
            if individual_puzzle['answer'].lower() not in user_answer.lower():
                correct = False
                break
        return correct
    
    def play(self):
        """Main game loop"""
        self.show_welcome_animation()
        
        print("\n" + "="*50)
        print("Selamat datang! di HackForge Selesaikan teka-teki untuk naik level.")
        print("Ketik 'hint' untuk bantuan, 'quit' untuk keluar.")
        print("="*50 + "\n")
        
        while True:
            puzzle = self.generate_puzzle(self.current_level)
            
            print(f"=== LEVEL {self.current_level} ===")
            print(f"Skor: {self.score} | Hint digunakan: {self.hints_used}")
            print(f"Tipe: {puzzle['type']}")
            print(f"Pertanyaan: {puzzle['question']}")
            
            while True:
                user_input = input("\nJawaban Anda: ").strip()
                
                if user_input.lower() == 'quit':
                    self.show_game_over_animation()
                    return
                
                elif user_input.lower() == 'hint':
                    self.hints_used += 1
                    print(f"💡 Hint: {puzzle['hint']}")
                    # Kurangi skor untuk penggunaan hint
                    self.score = max(0, self.score - 5)
                    print(f"Skor dikurangi 5 poin. Skor sekarang: {self.score}")
                
                else:
                    # Animasi pengecekan jawaban
                    self.loading_animation(1, "Memverifikasi jawaban")
                    
                    # Periksa jawaban
                    if puzzle['type'] == 'combined':
                        is_correct = self.solve_combined_puzzle(puzzle, user_input)
                    else:
                        is_correct = (user_input.lower() == puzzle['answer'].lower())
                    
                    if is_correct:
                        points_earned = puzzle['level'] * 10
                        self.score += points_earned
                        
                        print(f"\n🎯 BENAR! +{points_earned} poin")
                        print(f"💰 Skor sekarang: {self.score}")
                        
                        # Tampilkan animasi level up
                        self.show_level_up_animation(self.current_level)
                        
                        self.current_level += 1
                        break
                    else:
                        print("❌ SALAH! Coba lagi atau minta 'hint'")
        
        self.show_game_over_animation()

# Jalankan game
if __name__ == "__main__":
    game = CyberSecurityPuzzle()
    game.play()