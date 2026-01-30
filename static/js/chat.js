// Chat functionality
document.addEventListener('DOMContentLoaded', function() {
    const chatBody = document.getElementById('chatBody');
    const userInput = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');
    const typingIndicator = document.getElementById('typingIndicator');
    const clearChatButton = document.getElementById('clearChat');
    const toggleThemeButton = document.getElementById('toggleTheme');
    const chatHistoryBtn = document.getElementById('chatHistoryBtn');
    const historyModal = new bootstrap.Modal(document.getElementById('historyModal'));
    const historyModalBody = document.getElementById('historyModalBody');
    
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
        
        // Add message content
        const contentElement = document.createElement('div');
        contentElement.className = 'message-content';
        
        if (isUser) {
            contentElement.textContent = text;
        } else {
            contentElement.innerHTML = formatMessage(text);
            
            // Add feedback buttons for assistant messages
            const feedback = document.createElement('div');
            feedback.className = 'message-feedback';
            feedback.innerHTML = `
                <button class="btn-feedback"><i class="far fa-thumbs-up"></i></button>
                <button class="btn-feedback"><i class="far fa-thumbs-down"></i></button>
            `;
            contentElement.appendChild(feedback);
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
            // Add assistant message
            addMessage(data.answer, false, data.timestamp);
        })
        .catch(error => {
            console.error('Error:', error);
            addMessage('Sorry, there was an error processing your request. Please try again.', false);
        });
    }
    
    // Toggle between light and dark theme
    function toggleTheme() {
        isDarkTheme = !isDarkTheme;
        
        if (isDarkTheme) {
            // Switch to dark theme
            document.documentElement.style.setProperty('--dark-bg', '#0f172a');
            document.documentElement.style.setProperty('--body-bg', '#0a1122');
            document.documentElement.style.setProperty('--header-bg', '#0f172a');
            document.documentElement.style.setProperty('--footer-bg', '#0f172a');
            document.documentElement.style.setProperty('--dark-text', '#f8fafc');
            document.documentElement.style.setProperty('--dark-text-secondary', '#cbd5e1');
            document.documentElement.style.setProperty('--assistant-message-bg', '#1e293b');
            document.documentElement.style.setProperty('--input-bg', '#1e293b');
            document.documentElement.style.setProperty('--dark-border', '#475569');
            
            // Update icon
            toggleThemeButton.innerHTML = '<i class="fas fa-moon"></i>';
        } else {
            // Switch to light theme
            document.documentElement.style.setProperty('--dark-bg', '#f1f5f9');
            document.documentElement.style.setProperty('--body-bg', '#ffffff');
            document.documentElement.style.setProperty('--header-bg', '#ffffff');
            document.documentElement.style.setProperty('--footer-bg', '#f8fafc');
            document.documentElement.style.setProperty('--dark-text', '#1e293b');
            document.documentElement.style.setProperty('--dark-text-secondary', '#64748b');
            document.documentElement.style.setProperty('--assistant-message-bg', '#f1f5f9');
            document.documentElement.style.setProperty('--input-bg', '#ffffff');
            document.documentElement.style.setProperty('--dark-border', '#e2e8f0');
            
            // Update icon
            toggleThemeButton.innerHTML = '<i class="fas fa-sun"></i>';
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
                // Fade out current chat content
                chatBody.style.opacity = 0;
                
                setTimeout(() => {
                    // Clear all messages
                    chatBody.innerHTML = `
                        <div class="empty-state">
                            <div class="chatbot-label">AI PUBLICATIONS ASSISTANT</div>
                            <h3>Understanding Publication Content</h3>
                            <p>Ask me anything about the research papers in our dataset. I can summarize content, find specific information, or help you understand complex topics.</p>
                            <div class="example-questions">
                                <div class="example-question" onclick="useExample('What publications are about RAG?')">What publications are about RAG?</div>
                                <div class="example-question" onclick="useExample('Summarize recent publications on LLMs')">Summarize recent publications on LLMs</div>
                                <div class="example-question" onclick="useExample('What are the key findings in neural networks?')">What are the key findings in neural networks?</div>
                                <div class="example-question" onclick="useExample('Compare different forecasting models')">Compare different forecasting models</div>
                            </div>
                        </div>
                    `;
                    
                    // Re-add hidden typing indicator
                    const typingIndicator = document.createElement('div');
                    typingIndicator.className = 'typing-indicator';
                    typingIndicator.id = 'typingIndicator';
                    typingIndicator.innerHTML = `
                        <div class="message-avatar"><i class="fas fa-robot"></i></div>
                        <span></span><span></span><span></span>
                    `;
                    chatBody.appendChild(typingIndicator);
                    
                    // Fade back in
                    chatBody.style.opacity = 1;
                    scrollToBottom();
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
    
    // History Modal Logic
    function loadHistory() {
        historyModalBody.innerHTML = `
            <div class="text-center py-4">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </div>
        `;
        
        fetch('/history')
            .then(response => response.json())
            .then(data => {
                if (data.length === 0) {
                    historyModalBody.innerHTML = '<div class="text-center py-5"><i class="fas fa-history mb-3" style="font-size: 3rem; opacity: 0.3;"></i><p>No chat history found yet.</p></div>';
                    return;
                }
                
                let html = '<div class="history-list">';
                data.forEach(item => {
                    html += `
                        <div class="history-item mb-4 p-3" style="background: rgba(255,255,255,0.05); border-radius: 12px; border-left: 4px solid var(--user-message-bg);">
                            <div class="small text-muted mb-2"><i class="far fa-calendar-alt me-1"></i> ${item.timestamp}</div>
                            <div class="fw-bold mb-2">Q: ${item.question}</div>
                            <div class="message-content" style="opacity: 0.9;">A: ${formatMessage(item.answer)}</div>
                        </div>
                    `;
                });
                html += '</div>';
                historyModalBody.innerHTML = html;
            })
            .catch(error => {
                console.error('Error fetching history:', error);
                historyModalBody.innerHTML = '<div class="alert alert-danger">Error loading history. Please try again later.</div>';
            });
    }

    chatHistoryBtn.addEventListener('click', function() {
        loadHistory();
        historyModal.show();
    });
    
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