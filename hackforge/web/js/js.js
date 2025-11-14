        // Game Data
        const gameData = {
            currentLevel: 1,
            score: 0,
            lives: 3,
            maxLives: 3,
            levels: [
                {
                    title: "Level 1: Password Cracking Dasar",
                    description: "Sebuah perusahaan kecil menjadi korban serangan siber. Anda harus memecahkan password administrator untuk mengamankan sistem. Password tersimpan dalam format hash MD5: 5f4dcc3b5aa765d61d8327deb882cf99",
                    challenge: "Hash MD5: 5f4dcc3b5aa765d61d8327deb882cf99\n\nPassword ini adalah salah satu yang paling umum digunakan di dunia. Terdiri dari 8 karakter huruf kecil.",
                    answer: "password",
                    hint: "Ini adalah password default yang sering tidak diubah oleh pengguna. Terdiri dari 8 karakter: p-a-s-s-w-o-r-d",
                    type: "text"
                },
                {
                    title: "Level 2: SQL Injection",
                    description: "Sebuah situs web e-commerce memiliki kerentanan SQL Injection pada form login. Gunakan teknik SQL Injection untuk melewati authentication.",
                    challenge: "Form Login:\n\nUsername: [                 ]\nPassword: [                 ]\n\n[       Login       ]\n\nMasukkan payload SQL Injection pada field username untuk melewati login.",
                    answer: "' OR '1'='1",
                    hint: "Gunakan karakter ' untuk mengakhiri string dan tambahkan kondisi yang selalu benar.",
                    type: "text"
                },
                {
                    title: "Level 3: Enkripsi Caesar Cipher",
                    description: "Anda menemukan pesan rahasia yang dienkripsi menggunakan Caesar Cipher dengan pergeseran 3. Dekripsi pesan berikut: khoor zruog",
                    challenge: "Pesan terenkripsi: khoor zruog\n\nCaesar Cipher: Setiap huruf digeser 3 posisi ke kanan dalam alfabet.\nDekripsi dengan menggeser 3 posisi ke kiri.",
                    answer: "hello world",
                    hint: "k -> h, h -> e, o -> l, dst. Pergeseran 3 huruf ke kiri.",
                    type: "text"
                },
                {
                    title: "Level 4: Binary Exploitation",
                    description: "Sebuah program sederhana memiliki buffer overflow vulnerability. Analisis kode berikut dan temukan cara untuk mengeksekusi shellcode.",
                    challenge: "Kode C:\n\n#include <stdio.h>\n#include <string.h>\n\nvoid vulnerable_function(char *input) {\n    char buffer[64];\n    strcpy(buffer, input);\n}\n\nint main(int argc, char *argv[]) {\n    if(argc > 1) {\n        vulnerable_function(argv[1]);\n    }\n    return 0;\n}\n\nBerapa byte input yang diperlukan untuk mencapai return address?",
                    answer: "76",
                    hint: "Buffer 64 byte + saved frame pointer 4 byte + return address 8 byte = 76 byte",
                    type: "number"
                },
                {
                    title: "Level 5: Steganografi",
                    description: "Seorang agen menyembunyikan pesan rahasia dalam gambar. Ekstrak pesan tersembunyi dari gambar berikut.",
                    challenge: "File: secret_image.jpg\n\nGunakan tool steghide untuk mengekstrak pesan. Password yang diperlukan adalah nama kota ibukota Indonesia.",
                    answer: "jakarta",
                    hint: "Ibukota Indonesia adalah Jakarta. Gunakan steghide extract -sf secret_image.jpg",
                    type: "text"
                }
            ]
        };

        // DOM Elements
        const levelDisplay = document.getElementById('level-display');
        const scoreDisplay = document.getElementById('score-display');
        const livesDisplay = document.getElementById('lives-display');
        const levelTitle = document.getElementById('level-title');
        const levelDescription = document.getElementById('level-description');
        const challengeArea = document.getElementById('challenge-area');
        const answerInput = document.getElementById('answer-input');
        const submitBtn = document.getElementById('submit-btn');
        const hintBtn = document.getElementById('hint-btn');
        const hintText = document.getElementById('hint-text');
        const successModal = document.getElementById('success-modal');
        const gameOverModal = document.getElementById('game-over-modal');
        const nextLevelBtn = document.getElementById('next-level-btn');
        const restartBtn = document.getElementById('restart-btn');
        const levelSelector = document.getElementById('level-selector');
        const progressFill = document.getElementById('progress-fill');

        // Initialize Game
        function initGame() {
            updateGameStats();
            loadLevel(gameData.currentLevel);
            generateLevelSelector();
        }

        // Update Game Stats
        function updateGameStats() {
            levelDisplay.textContent = gameData.currentLevel;
            scoreDisplay.textContent = gameData.score;
            livesDisplay.textContent = gameData.lives;
            
            // Update lives display
            for (let i = 1; i <= gameData.maxLives; i++) {
                const lifeElement = document.getElementById(`life-${i}`);
                if (lifeElement) {
                    if (i <= gameData.lives) {
                        lifeElement.classList.remove('lost');
                    } else {
                        lifeElement.classList.add('lost');
                    }
                }
            }
            
            // Update progress bar
            const progress = ((gameData.currentLevel - 1) / gameData.levels.length) * 100;
            progressFill.style.width = `${progress}%`;
        }

        // Load Level
        function loadLevel(levelNumber) {
            const levelIndex = levelNumber - 1;
            if (levelIndex < 0 || levelIndex >= gameData.levels.length) return;
            
            const level = gameData.levels[levelIndex];
            levelTitle.textContent = level.title;
            levelDescription.textContent = level.description;
            challengeArea.textContent = level.challenge;
            hintText.textContent = level.hint;
            answerInput.value = '';
            answerInput.focus();
            
            // Update current level in game data
            gameData.currentLevel = levelNumber;
            updateGameStats();
            
            // Update level selector
            const levelButtons = levelSelector.querySelectorAll('.level-btn');
            levelButtons.forEach((btn, index) => {
                btn.classList.remove('current');
                if (index === levelIndex) {
                    btn.classList.add('current');
                }
            });
        }

        // Generate Level Selector
        function generateLevelSelector() {
            levelSelector.innerHTML = '';
            gameData.levels.forEach((level, index) => {
                const levelBtn = document.createElement('div');
                levelBtn.className = 'level-btn';
                levelBtn.textContent = index + 1;
                levelBtn.addEventListener('click', () => {
                    if (index + 1 <= gameData.currentLevel) {
                        loadLevel(index + 1);
                    }
                });
                levelSelector.appendChild(levelBtn);
            });
        }

        // Check Answer
        function checkAnswer() {
            const levelIndex = gameData.currentLevel - 1;
            const level = gameData.levels[levelIndex];
            const userAnswer = answerInput.value.trim().toLowerCase();
            const correctAnswer = level.answer.toLowerCase();
            
            if (userAnswer === correctAnswer) {
                // Correct answer
                gameData.score += 100 * gameData.currentLevel;
                successModal.style.display = 'flex';
                document.getElementById('success-message').textContent = `Selamat! Jawaban benar. Skor +${100 * gameData.currentLevel}`;
            } else {
                // Wrong answer
                gameData.lives--;
                updateGameStats();
                
                if (gameData.lives <= 0) {
                    // Game over
                    gameOverModal.style.display = 'flex';
                } else {
                    // Show error and shake animation
                    challengeArea.classList.add('glitch');
                    setTimeout(() => {
                        challengeArea.classList.remove('glitch');
                    }, 500);
                    
                    answerInput.value = '';
                    answerInput.focus();
                }
            }
        }

        // Show Hint
        function showHint() {
            hintText.style.display = 'block';
        }

        // Next Level
        function nextLevel() {
            successModal.style.display = 'none';
            
            if (gameData.currentLevel < gameData.levels.length) {
                loadLevel(gameData.currentLevel + 1);
            } else {
                // All levels completed
                alert('Selamat! Anda telah menyelesaikan semua level HackForge!');
                loadLevel(1);
                gameData.score = 0;
                gameData.lives = gameData.maxLives;
                updateGameStats();
            }
        }

        // Restart Game
        function restartGame() {
            gameOverModal.style.display = 'none';
            gameData.currentLevel = 1;
            gameData.score = 0;
            gameData.lives = gameData.maxLives;
            initGame();
        }

        // Event Listeners
        submitBtn.addEventListener('click', checkAnswer);
        hintBtn.addEventListener('click', showHint);
        nextLevelBtn.addEventListener('click', nextLevel);
        restartBtn.addEventListener('click', restartGame);

        answerInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                checkAnswer();
            }
        });

        // Initialize the game
        initGame();