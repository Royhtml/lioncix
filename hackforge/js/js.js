        // Update preview with sample content
        document.addEventListener('DOMContentLoaded', function() {
            const previewFrame = document.getElementById('preview-frame');
            const previewContent = `
                <!DOCTYPE html>
                <html>
                <head>
                    <style>
                        body { 
                            font-family: Arial, sans-serif; 
                            margin: 0; 
                            padding: 20px; 
                            background: #f5f5f5; 
                            color: #333;
                        }
                        header { 
                            background: #1a1a1a; 
                            color: #00ff41; 
                            padding: 20px; 
                            border-radius: 5px;
                            margin-bottom: 20px;
                        }
                        h1 { 
                            margin: 0; 
                            font-size: 24px; 
                        }
                        p { 
                            margin: 10px 0 0; 
                            color: #ccc; 
                        }
                        .feature { 
                            background: white; 
                            padding: 15px; 
                            margin-bottom: 10px; 
                            border-radius: 5px;
                            border-left: 3px solid #00ff41;
                        }
                    </style>
                </head>
                <body>
                    <header>
                        <h1>Welcome to HackForge</h1>
                        <p>Advanced Cyber Security Platform</p>
                    </header>
                    <div class="feature">
                        <h3>VS Code Editor</h3>
                        <p>Code directly in our browser-based editor with live preview.</p>
                    </div>
                    <div class="feature">
                        <h3>Security Testing</h3>
                        <p>Test your code for vulnerabilities with integrated tools.</p>
                    </div>
                    <div class="feature">
                        <h3>Live Collaboration</h3>
                        <p>Work together with your team in real-time.</p>
                    </div>
                </body>
                </html>
            `;
            
            // Set the iframe content
            previewFrame.contentDocument.open();
            previewFrame.contentDocument.write(previewContent);
            previewFrame.contentDocument.close();
        });

        // Tab switching functionality
        document.querySelectorAll('.editor-tab').forEach(tab => {
            tab.addEventListener('click', function() {
                document.querySelectorAll('.editor-tab').forEach(t => t.classList.remove('active'));
                this.classList.add('active');
                
                // In a real implementation, this would switch the code content
            });
        });

        // Sidebar icon functionality
        document.querySelectorAll('.sidebar-icon').forEach(icon => {
            icon.addEventListener('click', function() {
                document.querySelectorAll('.sidebar-icon').forEach(i => i.classList.remove('active'));
                this.classList.add('active');
                
                // In a real implementation, this would switch the sidebar view
            });
        });

        // Mobile navbar functionality
        document.querySelectorAll('.mobile-nav-item').forEach(item => {
            item.addEventListener('click', function(e) {
                e.preventDefault();
                document.querySelectorAll('.mobile-nav-item').forEach(i => i.classList.remove('active'));
                this.classList.add('active');
            });
        });