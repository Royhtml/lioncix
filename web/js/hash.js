        // Game Data dengan Level Tak Terbatas
        const gameData = {
            currentLevel: 1,
            score: 0,
            lives: 3,
            maxLives: 3,
            streak: 0,
            highestLevel: 1,
            achievements: {
                5: { title: "Script Kiddie", description: "Mencapai Level 5" },
                10: { title: "Junior Hacker", description: "Mencapai Level 10" },
                25: { title: "Security Analyst", description: "Mencapai Level 25" },
                50: { title: "Pentester", description: "Mencapai Level 50" },
                100: { title: "Elite Hacker", description: "Mencapai Level 100" }
            },
            unlockedAchievements: new Set()
        };

        // Challenge Types dengan Generator Dinamis
        const challengeTypes = {
            passwordCrack: {
                name: "Password Cracking",
                generator: (level) => {
                    const passwords = [
                        "password", "admin", "123456", "qwerty", "letmein", 
                        "monkey", "password1", "abc123", "welcome", "sunshine"
                    ];
                    const advancedPasswords = [
                        "P@ssw0rd!", "Admin123!", "Secure2023!", "Cyb3rS3cur1ty", "H@ckTh3Pl@net"
                    ];
                    
                    const basePassword = level <= 10 ? 
                        passwords[Math.floor(Math.random() * passwords.length)] :
                        advancedPasswords[Math.floor(Math.random() * advancedPasswords.length)];
                    
                    // Untuk level tinggi, tambahkan variasi
                    let password = basePassword;
                    if (level > 20) {
                        password += Math.floor(Math.random() * 100);
                    }
                    
                    // Hash MD5 sederhana (simulasi)
                    let hash = "";
                    for (let i = 0; i < password.length; i++) {
                        hash += password.charCodeAt(i).toString(16);
                    }
                    
                    return {
                        challenge: `Password Hash MD5: ${hash}\n\nCrack password dari hash di atas.`,
                        answer: password,
                        hint: `Password terdiri dari ${password.length} karakter.${level <= 10 ? " Ini adalah password umum." : ""}`
                    };
                }
            },
            
            sqlInjection: {
                name: "SQL Injection",
                generator: (level) => {
                    const payloads = [
                        { input: "' OR '1'='1", description: "Bypass login form" },
                        { input: "' UNION SELECT 1,2,3--", description: "Extract database information" },
                        { input: "'; DROP TABLE users--", description: "Drop users table" },
                        { input: "' AND 1=CONVERT(int, (SELECT table_name FROM information_schema.tables))--", description: "Advanced SQLi" }
                    ];
                    
                    const payload = level <= 15 ? 
                        payloads[Math.floor(Math.random() * Math.min(level, 2))] :
                        payloads[Math.floor(Math.random() * payloads.length)];
                    
                    return {
                        challenge: `Form Login Rentan SQL Injection:\n\nUsername: [                 ]\nPassword: [                 ]\n\n[       Login       ]\n\nMasukkan payload SQL Injection untuk: ${payload.description}`,
                        answer: payload.input,
                        hint: `Gunakan karakter ' untuk mengakhiri string.${level > 10 ? " Perhatikan struktur UNION query." : ""}`
                    };
                }
            },
            
            cryptography: {
                name: "Cryptography",
                generator: (level) => {
                    const texts = ["hello world", "secret message", "encrypt this", "cybersecurity", "hackthesystem"];
                    const text = texts[Math.floor(Math.random() * texts.length)];
                    
                    let encrypted, answer, hint;
                    
                    if (level <= 10) {
                        // Caesar Cipher
                        const shift = 3 + Math.floor(Math.random() * 5);
                        encrypted = text.split('').map(char => {
                            if (char >= 'a' && char <= 'z') {
                                return String.fromCharCode((char.charCodeAt(0) - 97 + shift) % 26 + 97);
                            }
                            return char;
                        }).join('');
                        
                        answer = text;
                        hint = `Caesar Cipher dengan pergeseran ${shift} posisi`;
                    } else if (level <= 25) {
                        // Base64
                        encrypted = btoa(text);
                        answer = text;
                        hint = "Ini adalah encoding Base64. Decode untuk mendapatkan teks asli.";
                    } else {
                        // XOR Cipher
                        const key = Math.floor(Math.random() * 10) + 1;
                        encrypted = text.split('').map(char => 
                            String.fromCharCode(char.charCodeAt(0) ^ key)
                        ).join('');
                        // Convert to hex for display
                        encrypted = encrypted.split('').map(char => 
                            char.charCodeAt(0).toString(16).padStart(2, '0')
                        ).join(' ');
                        
                        answer = text;
                        hint = `XOR Cipher dengan key ${key}. Konversi dari hex ke text lalu XOR dengan key.`;
                    }
                    
                    return {
                        challenge: `Teks Terenkripsi: ${encrypted}\n\nDekripsi teks di atas.`,
                        answer: answer,
                        hint: hint
                    };
                }
            },
            
            binaryExploit: {
                name: "Binary Exploitation",
                generator: (level) => {
                    const bufferSize = 64 + Math.floor(Math.random() * 32);
                    const offset = bufferSize + 8 + Math.floor(Math.random() * 16);
                    
                    return {
                        challenge: `Buffer Overflow Analysis:\n\n#include <stdio.h>\n#include <string.h>\n\nvoid vulnerable() {\n    char buffer[${bufferSize}];\n    gets(buffer);\n}\n\nint main() {\n    vulnerable();\n    return 0;\n}\n\nBerapa byte yang diperlukan untuk mencapai return address?`,
                        answer: offset.toString(),
                        hint: `Buffer: ${bufferSize} byte + Saved EBP: 8 byte + Padding: ${offset - bufferSize - 8} byte`
                    };
                }
            },
            
            steganography: {
                name: "Steganography",
                generator: (level) => {
                    const messages = [
                        "secret", "hidden message", "confidential", "top secret", "classified"
                    ];
                    const password = [
                        "password", "secret", "hidden", "stego", "cyber"
                    ];
                    
                    const message = messages[Math.floor(Math.random() * messages.length)];
                    const pass = level <= 10 ? "password" : password[Math.floor(Math.random() * password.length)];
                    
                    return {
                        challenge: `Steganography Challenge:\n\nFile: secret_image.jpg\n\nPesan tersembunyi dalam gambar. Password: ${'*'.repeat(pass.length)}\n\nEkstrak pesan tersembunyi.`,
                        answer: message,
                        hint: `Gunakan steghide: steghide extract -sf secret_image.jpg -p ${pass}`
                    };
                }
            },
            
            forensics: {
                name: "Digital Forensics",
                generator: (level) => {
                    const ips = [
                        "192.168.1.100", "10.0.0.50", "172.16.254.1", "203.0.113.45"
                    ];
                    const domains = [
                        "malicious.com", "evil.org", "hacker.net", "suspicious.io"
                    ];
                    
                    const ip = ips[Math.floor(Math.random() * ips.length)];
                    const domain = domains[Math.floor(Math.random() * domains.length)];
                    
                    return {
                        challenge: `Analisis Jejak Digital:\n\nLog Network:\n- ${ip} -> GET /malware.exe\n- ${domain} -> POST /data_stealer.php\n- ${ip} -> CONNECT /backdoor:4444\n\nIP address mana yang mencurigakan?`,
                        answer: ip,
                        hint: `Perhatikan IP yang mengakses file mencurigakan dan membuka koneksi backdoor.`
                    };
                }
            },
            
            webExploit: {
                name: "Web Exploitation",
                generator: (level) => {
                    const exploits = [
                        { vuln: "XSS", payload: "&lt;script&gt;alert('XSS')&lt;/script&gt;", description: "Lakukan XSS injection" },
                        { vuln: "CSRF", payload: "https://evil.com/transfer?amount=1000&to=attacker", description: "Buat URL CSRF exploit" },
                        { vuln: "LFI", payload: "../../../etc/passwd", description: "Eksploitasi Local File Inclusion" }
                    ];
                    
                    const exploit = exploits[Math.floor(Math.random() * exploits.length)];
                    
                    return {
                        challenge: `Web Vulnerability: ${exploit.vuln}\n\n${exploit.description}\n\nMasukkan payload yang sesuai:`,
                        answer: exploit.payload,
                        hint: `Research tentang ${exploit.vuln} vulnerability.`
                    };
                }
            }
        };

        // DOM Elements
        const levelDisplay = document.getElementById('level-display');
        const scoreDisplay = document.getElementById('score-display');
        const livesDisplay = document.getElementById('lives-display');
        const streakDisplay = document.getElementById('streak-display');
        const levelTitle = document.getElementById('level-title');
        const levelDescription = document.getElementById('level-description');
        const challengeArea = document.getElementById('challenge-area');
        const answerInput = document.getElementById('answer-input');
        const submitBtn = document.getElementById('submit-btn');
        const hintBtn = document.getElementById('hint-btn');
        const skipBtn = document.getElementById('skip-btn');
        const hintText = document.getElementById('hint-text');
        const successModal = document.getElementById('success-modal');
        const gameOverModal = document.getElementById('game-over-modal');
        const nextLevelBtn = document.getElementById('next-level-btn');
        const restartBtn = document.getElementById('restart-btn');
        const difficultyBadge = document.getElementById('difficulty-badge');
        const difficultyFill = document.getElementById('difficulty-fill');
        const achievementNotification = document.getElementById('achievement-notification');
        const achievementTitle = document.getElementById('achievement-title');
        const achievementDescription = document.getElementById('achievement-description');
        const highestLevelSpan = document.getElementById('highest-level');
        const scoreEarnedSpan = document.getElementById('score-earned');
        const streakCountSpan = document.getElementById('streak-count');
        const successTitle = document.getElementById('success-title');

        // Initialize Game
        function initGame() {
            updateGameStats();
            generateLevel();
        }

        // Update Game Stats
        function updateGameStats() {
            levelDisplay.textContent = gameData.currentLevel;
            scoreDisplay.textContent = gameData.score;
            livesDisplay.textContent = gameData.lives;
            streakDisplay.textContent = gameData.streak;
            
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
            
            // Update highest level
            if (gameData.currentLevel > gameData.highestLevel) {
                gameData.highestLevel = gameData.currentLevel;
            }
        }

        // Calculate Difficulty
        function calculateDifficulty(level) {
            if (level <= 5) return { name: "MUDAH", class: "difficulty-easy", value: 1 };
            if (level <= 15) return { name: "MENENGAH", class: "difficulty-medium", value: 2 };
            if (level <= 30) return { name: "SULIT", class: "difficulty-hard", value: 3 };
            if (level <= 50) return { name: "EXPERT", class: "difficulty-expert", value: 4 };
            return { name: "MASTER", class: "difficulty-master", value: 5 };
        }

        // Generate Random Level
        function generateLevel() {
            const level = gameData.currentLevel;
            const difficulty = calculateDifficulty(level);
            
            // Update difficulty display
            difficultyBadge.textContent = difficulty.name;
            difficultyBadge.className = `difficulty-badge ${difficulty.class}`;
            difficultyFill.style.width = `${(level % 20) * 5}%`;
            difficultyFill.style.backgroundColor = getComputedStyle(document.documentElement)
                .getPropertyValue(`--difficulty-${difficulty.class.split('-')[1]}`);
            
            // Select challenge type based on level
            const availableTypes = Object.keys(challengeTypes);
            let selectedType;
            
            if (level <= 10) {
                selectedType = availableTypes[level % 3];
            } else if (level <= 25) {
                selectedType = availableTypes[3 + (level % 3)];
            } else {
                selectedType = availableTypes[Math.floor(Math.random() * availableTypes.length)];
            }
            
            const challengeType = challengeTypes[selectedType];
            const challenge = challengeType.generator(level);
            
            // Update UI
            levelTitle.textContent = `Level ${level}: ${challengeType.name}`;
            levelDescription.textContent = `Tantangan ${difficulty.name.toLowerCase()} - ${getRandomScenario(level)}`;
            challengeArea.textContent = challenge.challenge;
            hintText.textContent = challenge.hint;
            answerInput.value = '';
            answerInput.focus();
            
            // Store current challenge data
            gameData.currentChallenge = challenge;
            
            // Check for achievements
            checkAchievements();
        }

        // Get Random Scenario
        function getRandomScenario(level) {
            const scenarios = [
                "Perusahaan fintech mengalami breach data",
                "Sistem pemerintah disusupi hacker",
                "Infrastruktur kritis dalam bahaya",
                "Data pelanggan dicuri oleh ransomware group",
                "Server web terkena serangan DDoS",
                "Aplikasi mobile mengandung backdoor",
                "Jaringan korporat diinfiltrasi APT",
                "Database berisi informasi sensitif terekspos"
            ];
            
            return scenarios[Math.floor(Math.random() * scenarios.length)];
        }

        // Check Answer
        function checkAnswer() {
            const userAnswer = answerInput.value.trim().toLowerCase();
            const correctAnswer = gameData.currentChallenge.answer.toLowerCase();
            
            if (userAnswer === correctAnswer) {
                // Correct answer
                const baseScore = 100;
                const difficulty = calculateDifficulty(gameData.currentLevel);
                const scoreEarned = baseScore * difficulty.value + (gameData.streak * 10);
                
                gameData.score += scoreEarned;
                gameData.streak++;
                
                // Show success modal
                scoreEarnedSpan.textContent = scoreEarned;
                streakCountSpan.textContent = gameData.streak;
                successTitle.textContent = `LEVEL ${gameData.currentLevel} BERHASIL!`;
                successModal.style.display = 'flex';
            } else {
                // Wrong answer
                gameData.lives--;
                gameData.streak = 0;
                updateGameStats();
                
                if (gameData.lives <= 0) {
                    // Game over
                    highestLevelSpan.textContent = gameData.highestLevel;
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

        // Skip Level
        function skipLevel() {
            gameData.lives--;
            gameData.streak = 0;
            updateGameStats();
            
            if (gameData.lives <= 0) {
                highestLevelSpan.textContent = gameData.highestLevel;
                gameOverModal.style.display = 'flex';
            } else {
                generateLevel();
            }
        }

        // Check Achievements
        function checkAchievements() {
            if (gameData.achievements[gameData.currentLevel] && 
                !gameData.unlockedAchievements.has(gameData.currentLevel)) {
                
                const achievement = gameData.achievements[gameData.currentLevel];
                gameData.unlockedAchievements.add(gameData.currentLevel);
                
                // Show achievement notification
                achievementTitle.textContent = achievement.title;
                achievementDescription.textContent = achievement.description;
                achievementNotification.classList.add('show');
                
                setTimeout(() => {
                    achievementNotification.classList.remove('show');
                }, 3000);
            }
        }

        // Next Level
        function nextLevel() {
            successModal.style.display = 'none';
            gameData.currentLevel++;
            updateGameStats();
            generateLevel();
        }

        // Restart Game
        function restartGame() {
            gameOverModal.style.display = 'none';
            gameData.currentLevel = 1;
            gameData.score = 0;
            gameData.lives = gameData.maxLives;
            gameData.streak = 0;
            initGame();
        }

        // Event Listeners
        submitBtn.addEventListener('click', checkAnswer);
        hintBtn.addEventListener('click', () => {
            hintText.style.display = 'block';
        });
        skipBtn.addEventListener('click', skipLevel);
        nextLevelBtn.addEventListener('click', nextLevel);
        restartBtn.addEventListener('click', restartGame);

        answerInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                checkAnswer();
            }
        });

        // Initialize the game
        initGame();