        // Game Data dengan Level Tak Terbatas
        const gameData = {
            currentLevel: 1,
            score: 0,
            lives: 3,
            maxLives: 3,
            streak: 0,
            highestLevel: 1,
            startTime: null,
            timeLeft: 2 * 60 * 60 * 1000, // 2 jam dalam milidetik
            timerInterval: null,
            achievements: {
                5: { title: "Script Kiddie", description: "Mencapai Level 5" },
                10: { title: "Junior Hacker", description: "Mencapai Level 10" },
                25: { title: "Security Analyst", description: "Mencapai Level 25" },
                50: { title: "Pentester", description: "Mencapai Level 50" },
                100: { title: "Elite Hacker", description: "Mencapai Level 100" },
                150: { title: "Cyber Warrior", description: "Mencapai Level 150" },
                200: { title: "Digital Legend", description: "Mencapai Level 200" }
            },
            unlockedAchievements: new Set()
        };

        // Challenge Types dengan Generator Dinamis untuk 100+ Level
        const challengeTypes = {
            passwordCrack: {
                name: "Password Cracking",
                generator: (level) => {
                    const basePasswords = [
                        "password", "admin", "123456", "qwerty", "letmein", 
                        "monkey", "password1", "abc123", "welcome", "sunshine"
                    ];
                    const advancedPasswords = [
                        "P@ssw0rd!", "Admin123!", "Secure2023!", "Cyb3rS3cur1ty", "H@ckTh3Pl@net",
                        "M4st3rH4ck3r", "S3cur1tyF1rst!", "D3f3ndTh3N3t", "C0mp1ExP@ss", "L3v3lUp!"
                    ];
                    const expertPasswords = [
                        "K4l1L1nuxR0ck5!", "P3nT3st3r2023!", "Cyb3rS3cur1tyM4st3r!", "H4ckTh3G1b50n!",
                        "D3f3n51v3M34sur3s!", "0ff3n51v3S3cur1ty!", "N3tw0rkP3n3tr4t10n!", "Cl0udS3cur1ty2023!"
                    ];
                    
                    let passwordPool;
                    if (level <= 20) passwordPool = basePasswords;
                    else if (level <= 75) passwordPool = advancedPasswords;
                    else passwordPool = expertPasswords;
                    
                    let password = passwordPool[Math.floor(Math.random() * passwordPool.length)];
                    
                    // Untuk level tinggi, tambahkan kompleksitas
                    if (level > 50) {
                        const specialChars = ["!", "@", "#", "$", "%", "&", "*"];
                        password += specialChars[Math.floor(Math.random() * specialChars.length)];
                    }
                    if (level > 100) {
                        password += Math.floor(Math.random() * 1000);
                    }
                    
                    // Hash simulasi berdasarkan level
                    let hash = "";
                    if (level <= 30) {
                        // MD5 style (sederhana)
                        for (let i = 0; i < password.length; i++) {
                            hash += password.charCodeAt(i).toString(16);
                        }
                        hash = hash.padEnd(32, '0').substring(0, 32);
                    } else if (level <= 80) {
                        // SHA-1 style
                        for (let i = 0; i < password.length; i++) {
                            hash += (password.charCodeAt(i) * 2).toString(16);
                        }
                        hash = hash.padEnd(40, '0').substring(0, 40);
                    } else {
                        // SHA-256 style
                        for (let i = 0; i < password.length; i++) {
                            hash += (password.charCodeAt(i) * 3).toString(16);
                        }
                        hash = hash.padEnd(64, '0').substring(0, 64);
                    }
                    
                    const hashTypes = ["MD5", "SHA-1", "SHA-256"];
                    const hashType = level <= 30 ? hashTypes[0] : level <= 80 ? hashTypes[1] : hashTypes[2];
                    
                    return {
                        challenge: `Password Hash ${hashType}: ${hash}\n\nCrack password dari hash di atas.${level > 50 ? "\n\nPERINGATAN: Sistem mendeteksi enhanced encryption!" : ""}`,
                        answer: password,
                        hint: `Password terdiri dari ${password.length} karakter.${level <= 20 ? " Ini adalah password umum." : " Gunakan teknik advanced password cracking."}`
                    };
                }
            },
            
            sqlInjection: {
                name: "SQL Injection",
                generator: (level) => {
                    const basicPayloads = [
                        { input: "' OR '1'='1", description: "Bypass login form" },
                        { input: "admin'--", description: "Login sebagai admin" },
                        { input: "' OR 1=1--", description: "Universal truth condition" }
                    ];
                    
                    const advancedPayloads = [
                        { input: "' UNION SELECT 1,2,3--", description: "Extract database information" },
                        { input: "'; DROP TABLE users--", description: "Drop users table" },
                        { input: "' AND 1=CONVERT(int, (SELECT table_name FROM information_schema.tables))--", description: "Advanced SQLi" },
                        { input: "' OR EXISTS(SELECT * FROM users WHERE username='admin')--", description: "Conditional injection" }
                    ];
                    
                    const expertPayloads = [
                        { input: "' AND SUBSTRING((SELECT TOP 1 name FROM sysobjects WHERE xtype='U'),1,1)='a'--", description: "Blind SQL injection" },
                        { input: "'; EXEC xp_cmdshell('dir')--", description: "Command execution" },
                        { input: "' UNION SELECT 1,@@version,3--", description: "Database version extraction" },
                        { input: "' AND (SELECT COUNT(*) FROM users) > 10--", description: "Boolean-based blind injection" }
                    ];
                    
                    let payloadPool;
                    if (level <= 25) payloadPool = basicPayloads;
                    else if (level <= 90) payloadPool = advancedPayloads;
                    else payloadPool = expertPayloads;
                    
                    const payload = payloadPool[Math.floor(Math.random() * payloadPool.length)];
                    const complexity = level > 100 ? " (WAF Bypass Required)" : level > 60 ? " (Filter Evasion)" : "";
                    
                    return {
                        challenge: `[LEVEL ${level}] SQL Injection Challenge${complexity}:\n\nForm Login Rentan:\n\nUsername: [                 ]\nPassword: [                 ]\n\n[       Login       ]\n\nTujuan: ${payload.description}\n\nMasukkan payload SQL Injection:`,
                        answer: payload.input,
                        hint: `Gunakan karakter ' untuk mengakhiri string.${level > 40 ? " Perhatikan struktur UNION query." : ""}${level > 100 ? " WAF memblokir karakter umum, gunakan encoding." : ""}`
                    };
                }
            },
            
            cryptography: {
                name: "Cryptography",
                generator: (level) => {
                    const texts = [
                        "hello world", "secret message", "encrypt this", "cybersecurity", 
                        "hackthesystem", "penetration testing", "zero trust architecture",
                        "quantum cryptography", "blockchain security", "iot vulnerability"
                    ];
                    const text = texts[Math.floor(Math.random() * texts.length)];
                    
                    let encrypted, answer, hint;
                    
                    if (level <= 15) {
                        // Caesar Cipher
                        const shift = 3 + Math.floor(Math.random() * 10);
                        encrypted = text.split('').map(char => {
                            if (char >= 'a' && char <= 'z') {
                                return String.fromCharCode((char.charCodeAt(0) - 97 + shift) % 26 + 97);
                            } else if (char >= 'A' && char <= 'Z') {
                                return String.fromCharCode((char.charCodeAt(0) - 65 + shift) % 26 + 65);
                            }
                            return char;
                        }).join('');
                        
                        answer = text;
                        hint = `Caesar Cipher dengan pergeseran ${shift} posisi`;
                    } else if (level <= 50) {
                        // Base64
                        encrypted = btoa(text);
                        answer = text;
                        hint = "Ini adalah encoding Base64. Decode untuk mendapatkan teks asli.";
                    } else if (level <= 100) {
                        // Vigenère Cipher
                        const key = "HACK";
                        encrypted = text.split('').map((char, i) => {
                            if (char >= 'a' && char <= 'z') {
                                const shift = key[i % key.length].toLowerCase().charCodeAt(0) - 97;
                                return String.fromCharCode((char.charCodeAt(0) - 97 + shift) % 26 + 97);
                            } else if (char >= 'A' && char <= 'Z') {
                                const shift = key[i % key.length].toUpperCase().charCodeAt(0) - 65;
                                return String.fromCharCode((char.charCodeAt(0) - 65 + shift) % 26 + 65);
                            }
                            return char;
                        }).join('');
                        
                        answer = text;
                        hint = "Vigenère Cipher dengan kunci 4 karakter. Pola berulang setiap 4 karakter.";
                    } else {
                        // RSA Simulation (sederhana)
                        const p = 61, q = 53, n = p * q;
                        let numbers = [];
                        for (let i = 0; i < text.length; i++) {
                            numbers.push(text.charCodeAt(i) * 2);
                        }
                        encrypted = `RSA Encrypted [n=${n}]: ${numbers.join(' ')}`;
                        answer = text;
                        hint = "Simulasi RSA sederhana. Setiap karakter dikalikan 2 sebelum 'enkripsi'.";
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
                    const bufferSize = 64 + Math.floor(Math.random() * 64);
                    const offset = bufferSize + 8 + Math.floor(Math.random() * 32);
                    const architectures = ["x86", "x64", "ARM"];
                    const arch = level <= 50 ? architectures[0] : architectures[1];
                    
                    let exploitType;
                    if (level <= 30) exploitType = "Buffer Overflow";
                    else if (level <= 80) exploitType = "Return Oriented Programming";
                    else if (level <= 130) exploitType = "Format String Attack";
                    else exploitType = "Heap Exploitation";
                    
                    return {
                        challenge: `[${arch}] ${exploitType}:\n\n#include <stdio.h>\n#include <string.h>\n\nvoid vulnerable() {\n    char buffer[${bufferSize}];\n    gets(buffer);\n}\n\nint main() {\n    printf("Starting service...\\n");\n    vulnerable();\n    return 0;\n}\n\nOffset untuk meng-overwrite return address?`,
                        answer: offset.toString(),
                        hint: `Buffer: ${bufferSize} byte + Saved EBP/RFP: 8 byte + Padding: ${offset - bufferSize - 8} byte\nArchitecture: ${arch}`
                    };
                }
            },
            
            forensics: {
                name: "Digital Forensics",
                generator: (level) => {
                    const scenarios = [
                        { 
                            logs: [
                                "192.168.1.100 -> GET /malware.exe",
                                "10.0.0.50 -> POST /data_stealer.php", 
                                "172.16.254.1 -> CONNECT /backdoor:4444"
                            ],
                            answer: "192.168.1.100",
                            description: "IP mana yang mencurigakan?"
                        },
                        {
                            logs: [
                                "User: admin - Failed login: 15 times",
                                "User: guest - Failed login: 3 times", 
                                "User: root - Failed login: 23 times"
                            ],
                            answer: "root",
                            description: "User mana yang mengalami brute force attack?"
                        },
                        {
                            logs: [
                                "File: secret.txt - MD5: 5d41402abc4b2a76b9719d911017c592",
                                "File: backup.zip - MD5: 7d793037a0760186574b0286a2c6a3c3",
                                "File: malware.exe - MD5: 5d41402abc4b2a76b9719d911017c592"
                            ],
                            answer: "secret.txt",
                            description: "File mana yang memiliki hash sama dengan malware?"
                        }
                    ];
                    
                    const scenario = scenarios[Math.floor(Math.random() * scenarios.length)];
                    const complexity = level > 70 ? "\n\n[FORENSICS MODE: Advanced analysis required]" : "";
                    
                    return {
                        challenge: `Digital Forensics - Level ${level}:\n\nLog Analysis:\n${scenario.logs.join('\n')}${complexity}\n\n${scenario.description}`,
                        answer: scenario.answer,
                        hint: "Analisis pola dan anomali dalam log."
                    };
                }
            },
            
            webExploit: {
                name: "Web Exploitation",
                generator: (level) => {
                    const basicExploits = [
                        { vuln: "XSS", payload: "&lt;script&gt;alert('XSS')&lt;/script&gt;", description: "Lakukan XSS injection" },
                        { vuln: "CSRF", payload: "https://evil.com/transfer?amount=1000&to=attacker", description: "Buat URL CSRF exploit" }
                    ];
                    
                    const advancedExploits = [
                        { vuln: "LFI", payload: "../../../etc/passwd", description: "Eksploitasi Local File Inclusion" },
                        { vuln: "SSRF", payload: "http://localhost:8080/admin", description: "Server-Side Request Forgery" },
                        { vuln: "XXE", payload: "<?xml version='1.0'?><!DOCTYPE root [<!ENTITY test SYSTEM 'file:///etc/passwd'>]><root>&test;</root>", description: "XML External Entity injection" }
                    ];
                    
                    const expertExploits = [
                        { vuln: "SQLi Time-Based", payload: "' OR IF(1=1,SLEEP(5),0)--", description: "Time-based blind SQL injection" },
                        { vuln: "Template Injection", payload: "{{7*7}}", description: "Server-Side Template Injection" },
                        { vuln: "Deserialization", payload: "O:8:\"stdClass\":1:{s:3:\"cmd\";s:6:\"whoami\";}", description: "Insecure deserialization exploit" }
                    ];
                    
                    let exploitPool;
                    if (level <= 20) exploitPool = basicExploits;
                    else if (level <= 85) exploitPool = advancedExploits;
                    else exploitPool = expertExploits;
                    
                    const exploit = exploitPool[Math.floor(Math.random() * exploitPool.length)];
                    const waf = level > 110 ? " (WAF Active)" : "";
                    
                    return {
                        challenge: `Web Vulnerability: ${exploit.vuln}${waf}\n\n${exploit.description}\n\nMasukkan payload yang sesuai:`,
                        answer: exploit.payload,
                        hint: `Research tentang ${exploit.vuln} vulnerability.${level > 110 ? " WAF mendeteksi payload sederhana." : ""}`
                    };
                }
            },
            
            reverseEngineering: {
                name: "Reverse Engineering",
                generator: (level) => {
                    const programs = [
                        { code: "mov eax, 5\nadd eax, 3\nmul eax, 2", result: "16", description: "Hasil akhir dari operasi assembly?" },
                        { code: "x = 10\ny = 3\nresult = x % y", result: "1", description: "Output dari program sederhana?" },
                        { code: "str = 'hello'\nfor i in range(len(str)):\n    print(chr(ord(str[i]) + 1))", result: "ifmmp", description: "Output dari program Python?" }
                    ];
                    
                    const program = programs[Math.floor(Math.random() * programs.length)];
                    const complexity = level > 60 ? "\n\n[OBFUSCATED CODE: Analysis required]" : "";
                    
                    return {
                        challenge: `Reverse Engineering - Level ${level}:\n\nKode Program:\n${program.code}${complexity}\n\n${program.description}`,
                        answer: program.result,
                        hint: "Jalankan kode secara mental atau trace execution flow."
                    };
                }
            },
            
            networkSecurity: {
                name: "Network Security",
                generator: (level) => {
                    const protocols = ["TCP", "UDP", "ICMP", "HTTP", "HTTPS", "SSH", "FTP"];
                    const targetProtocol = protocols[Math.floor(Math.random() * protocols.length)];
                    
                    let port, service;
                    switch(targetProtocol) {
                        case "HTTP": port = 80; service = "Web Server"; break;
                        case "HTTPS": port = 443; service = "Secure Web"; break;
                        case "SSH": port = 22; service = "Secure Shell"; break;
                        case "FTP": port = 21; service = "File Transfer"; break;
                        default: port = Math.floor(Math.random() * 1000) + 1000; service = "Custom Service";
                    }
                    
                    return {
                        challenge: `Network Security Assessment:\n\nTarget: 192.168.1.${Math.floor(Math.random() * 255)}\nService: ${service}\nProtocol: ${targetProtocol}\n\nPort yang biasanya digunakan oleh service ini?`,
                        answer: port.toString(),
                        hint: `Research port standar untuk ${targetProtocol}`
                    };
                }
            }
        };

        // DOM Elements
        const levelDisplay = document.getElementById('level-display');
        const scoreDisplay = document.getElementById('score-display');
        const livesDisplay = document.getElementById('lives-display');
        const streakDisplay = document.getElementById('streak-display');
        const timerDisplay = document.getElementById('timer');
        const levelTitle = document.getElementById('level-title');
        const levelDescription = document.getElementById('level-description');
        const challengeArea = document.getElementById('challenge-area');
        const answerInput = document.getElementById('answer-input');
        const submitBtn = document.getElementById('submit-btn');
        const hintBtn = document.getElementById('hint-btn');
        const skipBtn = document.getElementById('skip-btn');
        const solveBtn = document.getElementById('solve-btn');
        const hintText = document.getElementById('hint-text');
        const successModal = document.getElementById('success-modal');
        const gameOverModal = document.getElementById('game-over-modal');
        const timeUpModal = document.getElementById('time-up-modal');
        const nextLevelBtn = document.getElementById('next-level-btn');
        const restartBtn = document.getElementById('restart-btn');
        const continueBtn = document.getElementById('continue-btn');
        const newGameBtn = document.getElementById('new-game-btn');
        const difficultyBadge = document.getElementById('difficulty-badge');
        const difficultyFill = document.getElementById('difficulty-fill');
        const complexityIndicators = document.getElementById('complexity-indicators');
        const achievementNotification = document.getElementById('achievement-notification');
        const achievementTitle = document.getElementById('achievement-title');
        const achievementDescription = document.getElementById('achievement-description');
        const highestLevelSpan = document.getElementById('highest-level');
        const finalScoreSpan = document.getElementById('final-score');
        const timeUpLevelSpan = document.getElementById('time-up-level');
        const timeUpScoreSpan = document.getElementById('time-up-score');
        const scoreEarnedSpan = document.getElementById('score-earned');
        const streakCountSpan = document.getElementById('streak-count');
        const timeBonusEarnedSpan = document.getElementById('time-bonus-earned');
        const successTitle = document.getElementById('success-title');
        const timeBonusDisplay = document.getElementById('time-bonus');
        const gameOverMessage = document.getElementById('game-over-message');

        // Initialize Game
        function initGame() {
            gameData.startTime = Date.now();
            startTimer();
            updateGameStats();
            generateLevel();
            updateMilestones();
        }

        // Timer Functions
        function startTimer() {
            gameData.timerInterval = setInterval(() => {
                gameData.timeLeft -= 1000;
                
                if (gameData.timeLeft <= 0) {
                    clearInterval(gameData.timerInterval);
                    gameData.timeLeft = 0;
                    showTimeUpModal();
                }
                
                updateTimerDisplay();
            }, 1000);
        }

        function updateTimerDisplay() {
            const hours = Math.floor(gameData.timeLeft / (1000 * 60 * 60));
            const minutes = Math.floor((gameData.timeLeft % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((gameData.timeLeft % (1000 * 60)) / 1000);
            
            timerDisplay.textContent = 
                `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
            
            // Warning when less than 5 minutes
            if (gameData.timeLeft < 5 * 60 * 1000) {
                timerDisplay.classList.add('timer-warning');
            }
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
            if (level <= 10) return { name: "MUDAH", class: "difficulty-easy", value: 1 };
            if (level <= 30) return { name: "MENENGAH", class: "difficulty-medium", value: 2 };
            if (level <= 60) return { name: "SULIT", class: "difficulty-hard", value: 3 };
            if (level <= 100) return { name: "EXPERT", class: "difficulty-expert", value: 4 };
            if (level <= 150) return { name: "MASTER", class: "difficulty-master", value: 5 };
            return { name: "LEGEND", class: "difficulty-legend", value: 6 };
        }

        // Generate Random Level
        function generateLevel() {
            const level = gameData.currentLevel;
            const difficulty = calculateDifficulty(level);
            
            // Update difficulty display
            difficultyBadge.textContent = difficulty.name;
            difficultyBadge.className = `difficulty-badge ${difficulty.class}`;
            difficultyFill.style.width = `${Math.min(100, (level % 50) * 2)}%`;
            difficultyFill.style.backgroundColor = getComputedStyle(document.documentElement)
                .getPropertyValue(`--difficulty-${difficulty.class.split('-')[1]}`);
            
            // Update complexity indicators
            updateComplexityIndicators(level);
            
            // Select challenge type based on level
            const availableTypes = Object.keys(challengeTypes);
            let selectedType;
            
            if (level <= 25) {
                selectedType = availableTypes[level % 4];
            } else if (level <= 75) {
                selectedType = availableTypes[4 + (level % 3)];
            } else {
                selectedType = availableTypes[Math.floor(Math.random() * availableTypes.length)];
            }
            
            const challengeType = challengeTypes[selectedType];
            const challenge = challengeType.generator(level);
            
            // Update UI
            levelTitle.textContent = `Level ${level}: ${challengeType.name}`;
            levelDescription.textContent = `${getRandomScenario(level)} - [${difficulty.name}]`;
            challengeArea.textContent = challenge.challenge;
            hintText.textContent = challenge.hint;
            answerInput.value = '';
            answerInput.focus();
            
            // Store current challenge data
            gameData.currentChallenge = challenge;
            gameData.levelStartTime = Date.now();
            
            // Update time bonus display
            updateTimeBonusDisplay();
            
            // Check for achievements
            checkAchievements();
        }

        // Update complexity indicators
        function updateComplexityIndicators(level) {
            complexityIndicators.innerHTML = '';
            const dots = Math.min(10, Math.floor(level / 15) + 1);
            
            for (let i = 0; i < 10; i++) {
                const dot = document.createElement('div');
                dot.className = `complexity-dot ${i < dots ? 'active' : ''}`;
                complexityIndicators.appendChild(dot);
            }
        }

        // Update time bonus display
        function updateTimeBonusDisplay() {
            const baseBonus = Math.max(0, Math.floor((2 * 60 * 1000 - (Date.now() - gameData.levelStartTime)) / 1000));
            const bonusPoints = Math.floor(baseBonus / 10) * 5;
            timeBonusDisplay.textContent = `Time Bonus: +${bonusPoints} points`;
        }

        // Get Random Scenario
        function getRandomScenario(level) {
            const basicScenarios = [
                "Perusahaan fintech mengalami breach data",
                "Sistem pemerintah disusupi hacker",
                "Infrastruktur kritis dalam bahaya"
            ];
            
            const advancedScenarios = [
                "APT group menargetkan infrastruktur nasional",
                "Zero-day exploit terdeteksi dalam wild",
                "Ransomware mengancam rumah sakit",
                "IoT botnet melakukan DDoS attack"
            ];
            
            const expertScenarios = [
                "Quantum computing threat terhadap enkripsi",
                "AI-powered cyber attack terdeteksi",
                "Supply chain compromise pada software update",
                "Critical infrastructure zero-day exploitation"
            ];
            
            if (level <= 30) return basicScenarios[Math.floor(Math.random() * basicScenarios.length)];
            if (level <= 80) return advancedScenarios[Math.floor(Math.random() * advancedScenarios.length)];
            return expertScenarios[Math.floor(Math.random() * expertScenarios.length)];
        }

        // Check Answer
        function checkAnswer() {
            const userAnswer = answerInput.value.trim().toLowerCase();
            const correctAnswer = gameData.currentChallenge.answer.toLowerCase();
            
            if (userAnswer === correctAnswer) {
                // Correct answer
                const timeSpent = Date.now() - gameData.levelStartTime;
                const timeBonus = Math.max(0, Math.floor((2 * 60 * 1000 - timeSpent) / 1000));
                const bonusPoints = Math.floor(timeBonus / 10) * 5;
                
                const baseScore = 100;
                const difficulty = calculateDifficulty(gameData.currentLevel);
                const scoreEarned = baseScore * difficulty.value + (gameData.streak * 10) + bonusPoints;
                
                gameData.score += scoreEarned;
                gameData.streak++;
                
                // Show success modal
                scoreEarnedSpan.textContent = scoreEarned;
                streakCountSpan.textContent = gameData.streak;
                timeBonusEarnedSpan.textContent = bonusPoints;
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
                    finalScoreSpan.textContent = gameData.score;
                    gameOverMessage.textContent = `Nyawa Anda telah habis pada Level ${gameData.currentLevel}. Mulai dari awal?`;
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
                finalScoreSpan.textContent = gameData.score;
                gameOverMessage.textContent = `Nyawa Anda telah habis pada Level ${gameData.currentLevel}. Mulai dari awal?`;
                gameOverModal.style.display = 'flex';
            } else {
                generateLevel();
            }
        }

        // Solve Level (for testing)
        function solveLevel() {
            answerInput.value = gameData.currentChallenge.answer;
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

        // Update milestones
        function updateMilestones() {
            for (let i = 5; i <= 200; i *= 2) {
                const milestone = document.getElementById(`milestone-${i}`);
                if (milestone) {
                    if (gameData.currentLevel >= i) {
                        milestone.classList.add('reached');
                    }
                }
            }
        }

        // Next Level
        function nextLevel() {
            successModal.style.display = 'none';
            gameData.currentLevel++;
            updateGameStats();
            updateMilestones();
            generateLevel();
        }

        // Restart Game
        function restartGame() {
            gameOverModal.style.display = 'none';
            gameData.currentLevel = 1;
            gameData.score = 0;
            gameData.lives = gameData.maxLives;
            gameData.streak = 0;
            gameData.timeLeft = 2 * 60 * 60 * 1000;
            gameData.unlockedAchievements.clear();
            clearInterval(gameData.timerInterval);
            initGame();
        }

        // Show Time Up Modal
        function showTimeUpModal() {
            timeUpLevelSpan.textContent = gameData.currentLevel;
            timeUpScoreSpan.textContent = gameData.score;
            timeUpModal.style.display = 'flex';
        }

        // Continue without timer
        function continueWithoutTimer() {
            timeUpModal.style.display = 'none';
            clearInterval(gameData.timerInterval);
            timerDisplay.textContent = "∞";
            timerDisplay.classList.remove('timer-warning');
        }

        // Event Listeners
        submitBtn.addEventListener('click', checkAnswer);
        hintBtn.addEventListener('click', () => {
            hintText.style.display = 'block';
        });
        skipBtn.addEventListener('click', skipLevel);
        solveBtn.addEventListener('click', solveLevel);
        nextLevelBtn.addEventListener('click', nextLevel);
        restartBtn.addEventListener('click', restartGame);
        continueBtn.addEventListener('click', continueWithoutTimer);
        newGameBtn.addEventListener('click', restartGame);

        answerInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                checkAnswer();
            }
        });

        // Update time bonus every second
        setInterval(() => {
            if (gameData.levelStartTime) {
                updateTimeBonusDisplay();
            }
        }, 1000);

        // Initialize the game
        initGame();