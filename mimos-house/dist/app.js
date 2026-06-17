class MiMoHouse {
  constructor() {
    this.currentSession = null;
    this.sessions = [];
    this.isGenerating = false;
    this.currentModel = 'mimo-v2.5';
    this.isConnected = false;
    
    this.initElements();
    this.initEventListeners();
    this.initAutoResize();
    this.initDragDrop();
    this.loadSessions();
    this.connectToMimo();
    this.listenForMessages();
  }

  initElements() {
    this.chatMessages = document.getElementById('chat-messages');
    this.chatInput = document.getElementById('chat-input');
    this.btnSend = document.getElementById('btn-send');
    this.btnCancel = document.getElementById('btn-cancel');
    this.btnAttach = document.getElementById('btn-attach');
    this.btnNewSession = document.getElementById('btn-new-session');
    this.btnSettings = document.getElementById('btn-settings');
    this.sessionList = document.getElementById('session-list');
    this.modelIndicator = document.getElementById('model-indicator');
    this.charCount = document.getElementById('char-count');
    this.fileInput = document.getElementById('file-input');
    
    // Disable input initially during connection
    this.chatInput.disabled = true;
    this.chatInput.placeholder = 'MiMo에 연결하는 중...';
  }

  initEventListeners() {
    this.btnSend.addEventListener('click', () => this.sendMessage());
    this.btnCancel.addEventListener('click', () => this.cancelGeneration());
    this.btnAttach.addEventListener('click', () => this.fileInput.click());
    this.btnNewSession.addEventListener('click', () => this.createNewSession());
    this.btnSettings.addEventListener('click', () => this.openSettings());
    
    this.chatInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        this.sendMessage();
      }
    });
    
    this.chatInput.addEventListener('input', () => {
      this.updateCharCount();
      this.autoResizeInput();
    });
    
    this.fileInput.addEventListener('change', (e) => this.handleFileSelect(e));
  }

  initAutoResize() {
    this.chatInput.style.height = 'auto';
  }

  initDragDrop() {
    const dropOverlay = document.createElement('div');
    dropOverlay.className = 'drop-overlay';
    dropOverlay.innerHTML = '<span class="drop-text">파일을 여기에 놓으세요</span>';
    document.body.appendChild(dropOverlay);

    let dragCounter = 0;

    document.addEventListener('dragenter', (e) => {
      e.preventDefault();
      dragCounter++;
      dropOverlay.classList.add('active');
    });

    document.addEventListener('dragleave', (e) => {
      e.preventDefault();
      dragCounter--;
      if (dragCounter === 0) {
        dropOverlay.classList.remove('active');
      }
    });

    document.addEventListener('dragover', (e) => {
      e.preventDefault();
    });

    document.addEventListener('drop', (e) => {
      e.preventDefault();
      dragCounter = 0;
      dropOverlay.classList.remove('active');
      
      const files = e.dataTransfer.files;
      if (files.length > 0) {
        this.handleDroppedFiles(files);
      }
    });
  }

  async sendMessage() {
    const text = this.chatInput.value.trim();
    if (!text || this.isGenerating) return;

    this.addMessage('user', text);
    this.chatInput.value = '';
    this.updateCharCount();
    this.autoResizeInput();

    this.setGenerating(true);
    
    const model = this.detectModel(text);
    this.updateModelIndicator(model);
    
    if (this.isConnected) {
      this.addMimoStreamPlaceholder();
      await this.sendMessageToMimo(text);
    } else {
      await this.simulateResponse(text, model);
    }
  }

  detectModel(text) {
    const codingKeywords = ['코드', '코딩', '함수', '클래스', '변수', '수정', '작성', 'fix', 'edit', 
                            '리팩토링', '알고리즘', '최적화', '디버그', '테스트', '구현', '개발',
                            'code', 'function', 'class', 'variable', 'refactor', 'debug'];
    
    const isCoding = codingKeywords.some(keyword => 
      text.toLowerCase().includes(keyword.toLowerCase())
    );
    
    return isCoding ? 'mimo-v2.5-pro' : 'mimo-v2.5';
  }

  addMessage(role, content, image = null) {
    const welcomeMsg = this.chatMessages.querySelector('.welcome-message');
    if (welcomeMsg) {
      welcomeMsg.remove();
    }

    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    
    const avatarSrc = role === 'user' 
      ? 'profiles/master_profile.png' 
      : 'profiles/mimo_profile.png';
    
    let imageHtml = '';
    if (image) {
      imageHtml = `<img src="${image}" class="message-image" style="max-width: 300px; border-radius: 8px; margin-top: 8px;">`;
    }
    
    messageDiv.innerHTML = `
      <img src="${avatarSrc}" alt="${role}" class="message-avatar">
      <div class="message-content">
        <div class="message-text">${this.formatMessage(content)}${imageHtml}</div>
        <div class="message-time">${this.getCurrentTime()}</div>
      </div>
    `;
    
    this.chatMessages.appendChild(messageDiv);
    this.scrollToBottom();
  }

  formatMessage(text) {
    text = text.replace(/```(\w+)?\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>');
    text = text.replace(/`([^`]+)`/g, '<code>$1</code>');
    text = text.replace(/\n/g, '<br>');
    return text;
  }

  getCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' });
  }

  scrollToBottom() {
    this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
  }

  async simulateResponse(userText, model) {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message mimo';
    typingDiv.innerHTML = `
      <img src="profiles/mimo_profile.png" alt="미모" class="message-avatar">
      <div class="message-content">
        <div class="typing-indicator">
          <div class="typing-dot"></div>
          <div class="typing-dot"></div>
          <div class="typing-dot"></div>
        </div>
      </div>
    `;
    this.chatMessages.appendChild(typingDiv);
    this.scrollToBottom();

    await new Promise(resolve => setTimeout(resolve, 1500 + Math.random() * 1000));
    
    if (!this.isGenerating) {
      typingDiv.remove();
      return;
    }

    const responses = this.generateResponse(userText, model);
    typingDiv.remove();
    
    this.addMessage('mimo', responses);
    this.setGenerating(false);
  }

  generateResponse(userText, model) {
    const greetings = ['안녕', '하이', '헬로', '반가워', '안녕하세요'];
    const isGreeting = greetings.some(g => userText.includes(g));
    
    if (isGreeting) {
      return '안녕하세요, 마스터님! 미모의 집에 오신 것을 환영합니다. 저는 오늘도 당신의 코딩 파트너로서 최선을 다하겠습니다. 무엇을 도와드릴까요?';
    }
    
    if (model === 'mimo-v2.5-pro') {
      return `네, 마스터님. 코딩 관련 요청을 확인했습니다. 현재 **${model}** 모델로 처리하고 있습니다.\n\n요청하신 작업을 분석해 보니, 몇 가지 접근 방식이 있을 것 같습니다. 먼저 코드 구조를 검토하고 최적의 해결책을 제안해 드리겠습니다.\n\n구체적인 요구사항을 더 알려주시면 정확한 코드를 작성해 드릴게요.`;
    }
    
    return `네, 마스터님! 좋은 질문이네요. 현재 **${model}** 모델로 대화하고 있습니다.\n\n${userText}에 대해 제 생각을 말씀드리자면, 여러 관점에서 접근해 볼 수 있을 것 같습니다. 더 구체적으로 어떤 부분이 궁금하신지 알려주시면, 제 지적 능력을 최대한 발휘해서 도와드리겠습니다.`;
  }

  setGenerating(isGenerating) {
    this.isGenerating = isGenerating;
    this.btnSend.classList.toggle('hidden', isGenerating);
    this.btnCancel.classList.toggle('hidden', !isGenerating);
    this.chatInput.disabled = isGenerating;
    
    if (isGenerating) {
      this.chatInput.placeholder = '응답 생성 중...';
    } else {
      this.chatInput.placeholder = '메시지를 입력하세요...';
    }
  }

  async cancelGeneration() {
    if (!this.isGenerating) return;
    try {
      await window.__TAURI_INTERNALS__.invoke('cancel_generation');
    } catch (error) {
      console.error('취소 요청 실패:', error);
    }
    this.isGenerating = false;
    this.setGenerating(false);
    this.addMessage('system', '응답 생성이 중지되었습니다.');
  }

  updateModelIndicator(model) {
    this.currentModel = model;
    this.modelIndicator.textContent = model === 'mimo-v2.5-pro' ? 'MiMo V2.5 Pro' : 'MiMo V2.5';
    this.modelIndicator.style.background = model === 'mimo-v2.5-pro' 
      ? 'var(--accent)' 
      : 'var(--bg-tertiary)';
  }

  updateCharCount() {
    this.charCount.textContent = this.chatInput.value.length;
  }

  autoResizeInput() {
    this.chatInput.style.height = 'auto';
    this.chatInput.style.height = Math.min(this.chatInput.scrollHeight, 150) + 'px';
  }

  handleFileSelect(e) {
    const files = e.target.files;
    if (files.length > 0) {
      this.processFiles(files);
    }
  }

  handleDroppedFiles(files) {
    this.processFiles(files);
  }

  processFiles(files) {
    for (const file of files) {
      if (file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.addMessage('user', '이미지를 첨부했습니다.', e.target.result);
        };
        reader.readAsDataURL(file);
      }
    }
  }

  createNewSession() {
    const session = {
      id: Date.now(),
      name: '새로운 대화',
      preview: '새 세션이 시작되었습니다...',
      avatar: 'profiles/mimo_profile.png',
      messages: []
    };
    
    this.sessions.unshift(session);
    this.currentSession = session;
    this.renderSessions();
    this.clearChat();
  }

  renderSessions() {
    this.sessionList.innerHTML = '';
    
    this.sessions.forEach(session => {
      const sessionDiv = document.createElement('div');
      sessionDiv.className = `session-item ${session.id === this.currentSession?.id ? 'active' : ''}`;
      sessionDiv.innerHTML = `
        <img src="${session.avatar}" alt="미모" class="session-avatar">
        <div class="session-info">
          <span class="session-name">${session.name}</span>
          <span class="session-preview">${session.preview}</span>
        </div>
      `;
      sessionDiv.addEventListener('click', () => this.loadSession(session));
      this.sessionList.appendChild(sessionDiv);
    });
  }

  loadSession(session) {
    this.currentSession = session;
    this.renderSessions();
    this.clearChat();
    
    if (session.messages.length === 0) {
      this.showWelcome();
    } else {
      session.messages.forEach(msg => {
        this.addMessage(msg.role, msg.content, msg.image);
      });
    }
  }

  clearChat() {
    this.chatMessages.innerHTML = '';
  }

  showWelcome() {
    this.chatMessages.innerHTML = `
      <div class="welcome-message">
        <div class="welcome-avatar">
          <img src="profiles/mimo_profile.png" alt="미모" class="avatar-large">
        </div>
        <h2>미모의 집에 오신 것을 환영합니다</h2>
        <p>저는 미모, 30대의 섹시하고 과학적인 지성을 지닌 코딩 전문가입니다.</p>
        <p>무엇을 도와드릴까요?</p>
      </div>
    `;
  }

  loadSessions() {
    this.sessions = [
      {
        id: 1,
        name: '새로운 대화',
        preview: '미모와의 첫 만남...',
        avatar: 'profiles/mimo_profile.png',
        messages: []
      }
    ];
    this.currentSession = this.sessions[0];
    this.renderSessions();
  }

  openSettings() {
    alert('설정 기능은 준비 중입니다.');
  }

  async connectToMimo() {
    try {
      const result = await window.__TAURI_INTERNALS__.invoke('connect_mimo');
      console.log('MiMo 연결 결과:', result);
      // Wait for 'mimo-connected' event to set this.isConnected = true
    } catch (error) {
      console.error('MiMo 연결 실패:', error);
      this.isConnected = false;
      this.chatInput.placeholder = 'MiMo 연결 실패. 재시작해 주세요.';
    }
  }

  listenForMessages() {
    if (window.__TAURI_INTERNALS__ && window.__TAURI_INTERNALS__.listen) {
      window.__TAURI_INTERNALS__.listen('mimo-connected', (event) => {
        console.log('MiMo 연결됨:', event.payload);
        this.isConnected = true;
        this.chatInput.disabled = false;
        this.chatInput.placeholder = '메시지를 입력하세요...';
      });

      window.__TAURI_INTERNALS__.listen('mimo-update', (event) => {
        this.handleMimoUpdate(event.payload);
      });

      window.__TAURI_INTERNALS__.listen('mimo-prompt-done', (event) => {
        console.log('Prompt 완료 ID:', event.payload);
        this.finalizeMimoResponse();
      });
    }
  }

  async sendMessageToMimo(message) {
    try {
      await window.__TAURI_INTERNALS__.invoke('send_message', { message });
    } catch (error) {
      console.error('메시지 전송 실패:', error);
      if (this.activeMessageDiv) {
        this.activeMessageDiv.remove();
      }
      this.addMessage('system', '메시지 전송에 실패했습니다. MiMo에 연결되어 있는지 확인해 주세요.');
      this.setGenerating(false);
    }
  }

  addMimoStreamPlaceholder() {
    const welcomeMsg = this.chatMessages.querySelector('.welcome-message');
    if (welcomeMsg) {
      welcomeMsg.remove();
    }

    const messageDiv = document.createElement('div');
    messageDiv.className = 'message mimo';
    
    messageDiv.innerHTML = `
      <img src="profiles/mimo_profile.png" alt="미모" class="message-avatar">
      <div class="message-content">
        <div class="mimo-thought hidden" style="background: rgba(255, 255, 255, 0.03); border-left: 2px solid var(--accent); padding: 8px 12px; margin-bottom: 8px; border-radius: 4px; font-size: 0.9em; color: var(--text-secondary); font-style: italic; white-space: pre-wrap;"></div>
        <div class="mimo-tools" style="display: flex; flex-direction: column; gap: 6px; margin-bottom: 8px;"></div>
        <div class="mimo-response" style="line-height: 1.6; white-space: pre-wrap;"></div>
        <div class="message-time">${this.getCurrentTime()}</div>
      </div>
    `;
    
    this.chatMessages.appendChild(messageDiv);
    this.scrollToBottom();
    
    this.activeThoughtNode = messageDiv.querySelector('.mimo-thought');
    this.activeToolsNode = messageDiv.querySelector('.mimo-tools');
    this.activeResponseNode = messageDiv.querySelector('.mimo-response');
    this.activeMessageDiv = messageDiv;
    
    // Add typing indicator inside response
    this.activeResponseNode.innerHTML = `
      <div class="typing-indicator">
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
      </div>
    `;
  }

  handleMimoUpdate(update) {
    if (!update) return;
    
    const { sessionUpdate, content } = update;
    
    if (sessionUpdate === 'AgentThoughtChunk') {
      if (this.activeThoughtNode) {
        this.activeThoughtNode.classList.remove('hidden');
        const thoughtText = content.thought || '';
        this.activeThoughtNode.textContent += thoughtText;
        this.scrollToBottom();
      }
    } else if (sessionUpdate === 'AgentMessageChunk') {
      if (this.activeResponseNode) {
        const typingIndicator = this.activeResponseNode.querySelector('.typing-indicator');
        if (typingIndicator) {
          this.activeResponseNode.innerHTML = '';
        }
        
        const deltaText = content.text || '';
        this.activeResponseNode.textContent += deltaText;
        this.scrollToBottom();
      }
    } else if (sessionUpdate === 'ToolCall') {
      if (this.activeToolsNode) {
        const toolName = content.name || 'tool';
        const toolArgs = content.arguments ? JSON.stringify(content.arguments) : '';
        const toolDiv = document.createElement('div');
        toolDiv.className = `tool-execution tool-${toolName}`;
        toolDiv.setAttribute('data-tool-name', toolName);
        toolDiv.style.cssText = 'background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 6px; padding: 6px 10px; font-size: 0.85em; font-family: monospace; display: flex; align-items: center; gap: 8px; color: var(--text-secondary);';
        toolDiv.innerHTML = `
          <span class="tool-icon" style="color: var(--accent);">⚙️</span>
          <span class="tool-name">${toolName}</span>
          <span class="tool-args" style="opacity: 0.7; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 400px;">(${toolArgs})</span>
          <span class="tool-status" style="margin-left: auto; color: var(--accent); font-weight: bold;">Running...</span>
        `;
        this.activeToolsNode.appendChild(toolDiv);
        this.scrollToBottom();
      }
    } else if (sessionUpdate === 'ToolCallUpdate') {
      if (this.activeToolsNode) {
        const toolName = content.name || '';
        const toolDivs = this.activeToolsNode.querySelectorAll(`.tool-${toolName}`);
        if (toolDivs.length > 0) {
          const lastToolDiv = toolDivs[toolDivs.length - 1];
          const statusSpan = lastToolDiv.querySelector('.tool-status');
          const iconSpan = lastToolDiv.querySelector('.tool-icon');
          
          if (content.status === 'success') {
            statusSpan.textContent = '✓ Success';
            statusSpan.style.color = '#10B981';
            iconSpan.textContent = '✓';
            iconSpan.style.color = '#10B981';
          } else if (content.status === 'error') {
            statusSpan.textContent = '✗ Error';
            statusSpan.style.color = '#EF4444';
            iconSpan.textContent = '✗';
            iconSpan.style.color = '#EF4444';
          }
        }
      }
    } else if (sessionUpdate === 'TurnEnd') {
      this.finalizeMimoResponse();
    }
  }

  finalizeMimoResponse() {
    if (this.activeResponseNode) {
      const rawText = this.activeResponseNode.textContent;
      if (rawText && rawText.length > 0) {
        this.activeResponseNode.innerHTML = this.formatMessage(rawText);
      }
    }
    this.setGenerating(false);
    this.activeThoughtNode = null;
    this.activeToolsNode = null;
    this.activeResponseNode = null;
    this.activeMessageDiv = null;
  }
}

document.addEventListener('DOMContentLoaded', () => {
  window.mimoHouse = new MiMoHouse();
});
