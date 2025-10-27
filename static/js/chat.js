// Chat functionality
document.addEventListener('DOMContentLoaded', function() {
    const chatBody = document.getElementById('chatBody');
    const userInput = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');
    const typingIndicator = document.getElementById('typingIndicator');
    const clearChatButton = document.getElementById('clearChat');
    const toggleThemeButton = document.getElementById('toggleTheme');
    
    // Theme state (dark theme is default)
    let isDarkTheme = true;
    
    // Scroll to bottom of chat
    function scrollToBottom() {
        chatBody.scrollTop = chatBody.scrollHeight;
    }
    
    // Initialize
    scrollToBottom();
    
    // Process and format the message (convert markdown to HTML)
    function formatMessage(text) {
        // Check if marked is available
        if (typeof marked !== 'undefined') {
            return marked.parse(text);
        }
        return text;
    }
    
    // Add a message to the chat
    function addMessage(text, isUser, timestamp) {
        // Remove empty state if it exists
        const emptyState = document.querySelector('.empty-state');
        if (emptyState) {
            emptyState.remove();
        }
        
        const message = document.createElement('div');
        message.className = `message ${isUser ? 'user-message' : 'assistant-message'}`;
        
        // Add message header with avatar and sender name
        const messageHeader = document.createElement('div');
        messageHeader.className = 'message-header';
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.innerHTML = isUser ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';
        
        const sender = document.createElement('div');
        sender.className = 'message-sender';
        sender.textContent = isUser ? 'You' : 'Assistant';
        
        messageHeader.appendChild(avatar);
        messageHeader.appendChild(sender);
        message.appendChild(messageHeader);
        
        // Add message content
        const contentElement = document.createElement('div');
        contentElement.className = 'message-content';
        
        if (isUser) {
            contentElement.textContent = text;
        } else {
            contentElement.innerHTML = formatMessage(text);
        }
        
        message.appendChild(contentElement);
        
        // Add timestamp
        const timeElement = document.createElement('div');
        timeElement.className = 'message-time';
        timeElement.textContent = timestamp || new Date().toLocaleString();
        message.appendChild(timeElement);
        
        // Add to chat
        chatBody.appendChild(message);
        
        // Add animation class
        setTimeout(() => {
            message.classList.add('visible');
        }, 100);
        
        scrollToBottom();
    }
    
    // Send message function
    function sendMessage() {
        const text = userInput.value.trim();
        if (!text) return;
        
        // Add user message to chat
        addMessage(text, true);
        
        // Clear input
        userInput.value = '';
        
        // COMPLETELY REVISED TYPING INDICATOR IMPLEMENTATION
        // First, make sure it's properly positioned in the chat
        typingIndicator.style.display = 'flex';
        typingIndicator.style.opacity = '1';
        
        // Force a reflow to ensure the browser renders the indicator
        void typingIndicator.offsetWidth;
        
        // Make sure it's visible by scrolling to it
        scrollToBottom();
        
        // Add a pulsing effect to make it more noticeable
        typingIndicator.classList.add('pulsing');
        
        // Make the indicator more visible with a stronger style
        typingIndicator.style.border = '3px solid #6e8efb';
        typingIndicator.style.boxShadow = '0 0 20px rgba(110, 142, 251, 0.8)';
        
        // Log to console to verify it's being shown
        console.log("Showing typing indicator - " + new Date().toISOString());
        
        // Send to backend
        fetch('/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question: text }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Keep the typing indicator visible for a moment before hiding
            // This ensures users can see it even with fast responses
            setTimeout(() => {
                // Remove the pulsing effect
                typingIndicator.classList.remove('pulsing');
                
                // Start fading out the typing indicator
                typingIndicator.style.opacity = '0';
                
                // After a short fade-out, hide it completely and show the response
                setTimeout(() => {
                    typingIndicator.style.display = 'none';
                    
                    // Add assistant message
                    addMessage(data.answer, false, data.timestamp);
                    
                    // Log to console to verify it's being hidden
                    console.log("Hiding typing indicator and showing response - " + new Date().toISOString());
                }, 300);
            }, 500); // Keep visible for at least 500ms
        })
        .catch(error => {
            console.error('Error:', error);
            typingIndicator.classList.remove('pulsing');
            typingIndicator.style.display = 'none';
            addMessage('Sorry, there was an error processing your request. Please try again.', false);
        });
    }
    
    // Toggle between light and dark theme
    function toggleTheme() {
        isDarkTheme = !isDarkTheme;
        
        if (isDarkTheme) {
            // Switch to dark theme
            document.documentElement.style.setProperty('--primary-gradient', 'linear-gradient(135deg, #6e8efb, #a777e3)');
            document.documentElement.style.setProperty('--secondary-gradient', 'linear-gradient(135deg, #a777e3, #6e8efb)');
            document.documentElement.style.setProperty('--dark-bg', '#0f172a');
            document.documentElement.style.setProperty('--darker-bg', '#0a1122');
            document.documentElement.style.setProperty('--dark-surface', '#1e293b');
            document.documentElement.style.setProperty('--dark-card', '#334155');
            document.documentElement.style.setProperty('--dark-border', '#475569');
            document.documentElement.style.setProperty('--dark-text', '#f8fafc');
            document.documentElement.style.setProperty('--dark-text-secondary', '#cbd5e1');
            document.documentElement.style.setProperty('--user-message-gradient', 'linear-gradient(135deg, #6e8efb, #a777e3)');
            document.documentElement.style.setProperty('--assistant-message-bg', 'rgba(30, 41, 59, 0.8)');
            
            // Update background
            document.body.style.backgroundImage = `
                radial-gradient(circle at 10% 20%, rgba(110, 142, 251, 0.1) 0%, transparent 20%),
                radial-gradient(circle at 90% 80%, rgba(167, 119, 227, 0.1) 0%, transparent 20%),
                radial-gradient(circle at 50% 50%, rgba(30, 41, 59, 0.05) 0%, transparent 100%)
            `;
            
            // Update icon
            toggleThemeButton.innerHTML = '<i class="fas fa-sun"></i>';
        } else {
            // Switch to light theme
            document.documentElement.style.setProperty('--primary-gradient', 'linear-gradient(135deg, #0ea5e9, #3b82f6)');
            document.documentElement.style.setProperty('--secondary-gradient', 'linear-gradient(135deg, #3b82f6, #0ea5e9)');
            document.documentElement.style.setProperty('--dark-bg', '#f8fafc');
            document.documentElement.style.setProperty('--darker-bg', '#f1f5f9');
            document.documentElement.style.setProperty('--dark-surface', '#ffffff');
            document.documentElement.style.setProperty('--dark-card', '#f1f5f9');
            document.documentElement.style.setProperty('--dark-border', '#e2e8f0');
            document.documentElement.style.setProperty('--dark-text', '#0f172a');
            document.documentElement.style.setProperty('--dark-text-secondary', '#64748b');
            document.documentElement.style.setProperty('--user-message-gradient', 'linear-gradient(135deg, #0ea5e9, #3b82f6)');
            document.documentElement.style.setProperty('--assistant-message-bg', 'rgba(255, 255, 255, 0.8)');
            
            // Update background
            document.body.style.backgroundImage = `
                radial-gradient(circle at 10% 20%, rgba(14, 165, 233, 0.05) 0%, transparent 20%),
                radial-gradient(circle at 90% 80%, rgba(59, 130, 246, 0.05) 0%, transparent 20%),
                radial-gradient(circle at 50% 50%, rgba(255, 255, 255, 0.05) 0%, transparent 100%)
            `;
            
            // Update icon
            toggleThemeButton.innerHTML = '<i class="fas fa-moon"></i>';
        }
    }
    
    // Event listeners
    sendButton.addEventListener('click', sendMessage);
    
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    toggleThemeButton.addEventListener('click', toggleTheme);
    
    clearChatButton.addEventListener('click', function() {
        fetch('/clear_history', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // Clear chat UI with animation
                chatBody.style.opacity = 0;
                
                setTimeout(() => {
                    // Clear chat UI
                    chatBody.innerHTML = `
                        <div class="empty-state">
                            <i class="fas fa-robot empty-state-icon"></i>
                            <h3>Welcome to RAG Publications Assistant</h3>
                            <p>Ask questions about the publications dataset and get answers powered by AI. I'm here to help you find the information you need from our collection of research papers.</p>
                            <div class="example-questions">
                                <div class="example-question" onclick="useExample('What publications are about RAG?')">What publications are about RAG?</div>
                                <div class="example-question" onclick="useExample('Summarize recent publications on LLMs')">Summarize recent publications on LLMs</div>
                                <div class="example-question" onclick="useExample('What is RAG?')">What is RAG?</div>
                                <div class="example-question" onclick="useExample('How do I add memory to a chatbot?')">How do I add memory to a chatbot?</div>
                            </div>
                        </div>
                    `;
                    
                    // Fade back in
                    chatBody.style.opacity = 1;
                }, 300);
            }
        })
        .catch(error => {
            console.error('Error clearing chat:', error);
        });
    });
    
    // Add animation to send button
    sendButton.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-2px) scale(1.05)';
        this.style.boxShadow = 'var(--neon-shadow)';
    });
    
    sendButton.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0) scale(1)';
        this.style.boxShadow = '0 4px 10px rgba(0, 0, 0, 0.2)';
    });
    
    // Auto-focus the input field
    userInput.focus();
    
    // Add placeholder animation
    let placeholders = [
        "Ask me about publications...",
        "How can I help with your research?",
        "What would you like to know?",
        "Ask a question about RAG...",
        "Type your question here..."
    ];
    
    let currentPlaceholder = 0;
    
    // Change placeholder text every 3 seconds
    setInterval(() => {
        currentPlaceholder = (currentPlaceholder + 1) % placeholders.length;
        userInput.setAttribute('placeholder', placeholders[currentPlaceholder]);
    }, 3000);
    
    // Add input animation
    userInput.addEventListener('focus', function() {
        document.querySelector('.input-container').style.boxShadow = 'var(--neon-shadow)';
        document.querySelector('.input-container').style.borderColor = 'rgba(110, 142, 251, 0.5)';
    });
    
    userInput.addEventListener('blur', function() {
        document.querySelector('.input-container').style.boxShadow = '0 4px 15px rgba(0, 0, 0, 0.1)';
        document.querySelector('.input-container').style.borderColor = 'var(--glass-border)';
    });
    
    // Create floating particles
    function createParticles() {
        const particlesContainer = document.getElementById('particles');
        if (!particlesContainer) return;
        
        const particleCount = 20;
        
        for (let i = 0; i < particleCount; i++) {
            const particle = document.createElement('div');
            particle.classList.add('particle');
            
            // Random size between 2 and 6px
            const size = Math.random() * 4 + 2;
            particle.style.width = `${size}px`;
            particle.style.height = `${size}px`;
            
            // Random position
            const posX = Math.random() * 100;
            const posY = Math.random() * 100;
            particle.style.left = `${posX}%`;
            particle.style.top = `${posY}%`;
            
            // Random opacity
            particle.style.opacity = Math.random() * 0.3 + 0.1;
            
            // Add to container
            particlesContainer.appendChild(particle);
            
            // Animate particle
            animateParticle(particle);
        }
    }
    
    function animateParticle(particle) {
        const duration = Math.random() * 60 + 30;
        const newPosX = Math.random() * 100;
        const newPosY = Math.random() * 100;
        
        particle.style.transition = `all ${duration}s linear`;
        particle.style.left = `${newPosX}%`;
        particle.style.top = `${newPosY}%`;
        
        // Continue animation
        setTimeout(() => {
            animateParticle(particle);
        }, duration * 1000);
    }
    
    // Initialize particles
    createParticles();
    
    // Function to use example questions
    window.useExample = function(text) {
        if (userInput) {
            userInput.value = text;
            userInput.focus();
        }
    };

    // Add glow effect following mouse
    document.addEventListener('mousemove', function(e) {
        const glowTop = document.querySelector('.glow-top');
        const glowBottom = document.querySelector('.glow-bottom');
        
        if (glowTop && glowBottom) {
            // Calculate position based on mouse movement
            const x = e.clientX;
            const y = e.clientY;
            
            // Move glows slightly based on mouse position
            glowTop.style.transform = `translate(${x * 0.02}px, ${y * 0.01}px)`;
            glowBottom.style.transform = `translate(${-x * 0.01}px, ${-y * 0.02}px)`;
        }
    });
});

// Function to use example questions
function useExample(text) {
    const userInput = document.getElementById('userInput');
    userInput.value = text;
    userInput.focus();
    
    // Automatically send the example question
    document.getElementById('sendButton').click();
}