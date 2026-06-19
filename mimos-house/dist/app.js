const tauriInvoke = async (cmd, args = {}) => {
  if (window.__TAURI__ && window.__TAURI__.core && window.__TAURI__.core.invoke) {
    return await window.__TAURI__.core.invoke(cmd, args);
  } else if (window.__TAURI_INTERNALS__ && window.__TAURI_INTERNALS__.invoke) {
    return await window.__TAURI_INTERNALS__.invoke(cmd, args);
  }
  throw new Error("Tauri invoke interface not found");
};

const tauriListen = async (event, callback) => {
  if (window.__TAURI__ && window.__TAURI__.event && window.__TAURI__.event.listen) {
    return await window.__TAURI__.event.listen(event, callback);
  } else if (window.__TAURI_INTERNALS__ && window.__TAURI_INTERNALS__.listen) {
    return await window.__TAURI_INTERNALS__.listen(event, callback);
  }
  throw new Error("Tauri listen interface not found");
};

class MiMoHouse {
  constructor() {
    this.currentSession = null;
    this.sessions = [];
    this.isGenerating = false;
    this.currentModel = 'mimo-v2.5';
    this.isConnected = false;
    this.selectedModelMode = 'auto'; // 'auto', 'v2.5', 'pro'
    
    // Silence detection and tool tracking for multi-turn prompts
    this.activeTools = new Set();
    this.mimoCompletionTimer = null;
    
    this.initElements();
    this.initEventListeners();
    this.initAutoResize();
    this.initDragDrop();
    this.loadSessions();
    this.initConnection();
  }

  async initConnection() {
    // 1. Register event listeners first to prevent race conditions
    await this.listenForMessages();
    // 2. Start connection sequence
    await this.connectToMimo();
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
    // Lock the input on initial load until the connection is established to prevent premature simulation fallback
    this.chatInput.disabled = true;
    this.chatInput.placeholder = 'MiMo 연결을 대기하는 중...';

    // Image preview and attachment variables
    this.imagePreviewContainer = document.getElementById('image-preview-container');
    this.imagePreview = document.getElementById('image-preview');
    this.btnRemoveImage = document.getElementById('btn-remove-image');
    this.attachedImage = null;
  }

  initEventListeners() {
    this.btnSend.addEventListener('click', () => this.sendMessage());
    this.btnCancel.addEventListener('click', () => this.cancelGeneration());
    this.btnAttach.addEventListener('click', () => this.fileInput.click());
    this.btnNewSession.addEventListener('click', () => this.createNewSession());
    this.btnSettings.addEventListener('click', () => this.openSettings());
    
    this.btnRemoveImage.addEventListener('click', () => this.removeAttachedImage());
    
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

    // Event listeners for model toggle buttons
    document.querySelectorAll('.toggle-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const mode = e.target.getAttribute('data-mode');
        this.selectedModelMode = mode;
        
        document.querySelectorAll('.toggle-btn').forEach(b => b.classList.remove('active'));
        e.target.classList.add('active');
        
        this.setModelOverride(mode);
        
        if (mode === 'auto') {
          const text = this.chatInput.value.trim();
          this.updateModelIndicator(this.detectModel(text));
        } else if (mode === 'v2.5') {
          this.updateModelIndicator('mimo-v2.5');
        } else if (mode === 'pro') {
          this.updateModelIndicator('mimo-v2.5-pro');
        }
      });
    });
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
    const image = this.attachedImage;
    if ((!text && !image) || this.isGenerating) return;

    this.addMessage('user', text, image);
    this.chatInput.value = '';
    this.updateCharCount();
    this.autoResizeInput();

    if (image) {
      this.removeAttachedImage();
    }

    this.setGenerating(true);
    
    let model = 'mimo-v2.5';
    if (this.selectedModelMode === 'auto') {
      model = this.detectModel(text);
    } else if (this.selectedModelMode === 'v2.5') {
      model = 'mimo-v2.5';
    } else if (this.selectedModelMode === 'pro') {
      model = 'mimo-v2.5-pro';
    }
    this.updateModelIndicator(model);
    
    if (this.isConnected) {
      this.addMimoStreamPlaceholder();
      await this.setModelOverride(this.selectedModelMode);
      await this.sendMessageToMimo(text, image);
    } else {
      await this.simulateResponse(text, model);
    }
  }

  async setModelOverride(mode) {
    try {
      const response = await fetch('http://127.0.0.1:1984/override_model', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ mode })
      });
      const data = await response.json();
      console.log('Model override success:', data);
    } catch (error) {
      console.error('Failed to set model override on proxy:', error);
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
      imageHtml = `<img src="${image}" class="message-image" style="max-width: 120px; max-height: 120px; object-fit: contain; border-radius: 6px; margin-top: 8px; display: block; border: 1px solid rgba(255,255,255,0.08); cursor: pointer;">`;
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
    if (this.mimoCompletionTimer) {
      clearTimeout(this.mimoCompletionTimer);
      this.mimoCompletionTimer = null;
    }
    this.activeTools.clear();
    try {
      await tauriInvoke('cancel_generation');
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
    
    if (this.selectedModelMode === 'auto') {
      if (model === 'mimo-v2.5-pro') {
        this.modelIndicator.style.background = 'var(--accent)';
        this.modelIndicator.style.color = '#ffffff';
        this.modelIndicator.style.boxShadow = 'none';
      } else {
        this.modelIndicator.style.background = 'var(--bg-tertiary)';
        this.modelIndicator.style.color = 'var(--text-secondary)';
        this.modelIndicator.style.boxShadow = 'none';
      }
    } else if (this.selectedModelMode === 'v2.5') {
      this.modelIndicator.style.background = 'linear-gradient(135deg, #10b981, #059669)';
      this.modelIndicator.style.color = '#ffffff';
      this.modelIndicator.style.boxShadow = '0 0 8px rgba(16, 185, 129, 0.3)';
    } else if (this.selectedModelMode === 'pro') {
      this.modelIndicator.style.background = 'linear-gradient(135deg, #9333ea, #7c3aed)';
      this.modelIndicator.style.color = '#ffffff';
      this.modelIndicator.style.boxShadow = '0 0 8px rgba(147, 51, 234, 0.3)';
    }
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
          this.attachedImage = e.target.result;
          this.imagePreview.style.backgroundImage = `url(${e.target.result})`;
          this.imagePreviewContainer.classList.remove('hidden');
        };
        reader.readAsDataURL(file);
        break;
      }
    }
  }

  removeAttachedImage() {
    this.attachedImage = null;
    this.imagePreviewContainer.classList.add('hidden');
    this.imagePreview.style.backgroundImage = 'none';
    this.fileInput.value = '';
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
        <button class="delete-session-btn" title="대화 삭제">×</button>
      `;
      sessionDiv.addEventListener('click', () => this.loadSession(session));
      
      const deleteBtn = sessionDiv.querySelector('.delete-session-btn');
      deleteBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        this.deleteSession(session.id);
      });

      this.sessionList.appendChild(sessionDiv);
    });
  }

  deleteSession(sessionId) {
    if (this.sessions.length <= 1) {
      alert('최소 하나의 세션은 유지되어야 합니다.');
      return;
    }
    
    const index = this.sessions.findIndex(s => s.id === sessionId);
    if (index === -1) return;
    
    this.sessions.splice(index, 1);
    
    if (this.currentSession?.id === sessionId) {
      this.currentSession = this.sessions[0];
    }
    
    this.renderSessions();
    this.loadSession(this.currentSession);
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
      const result = await tauriInvoke('connect_mimo');
      console.log('MiMo 연결 결과:', result);
      
      const isConnected = await tauriInvoke('get_connection_status');
      if (result === '이미 연결되어 있습니다.' || isConnected) {
        this.isConnected = true;
        this.chatInput.disabled = false;
        this.chatInput.placeholder = '메시지를 입력하세요...';
      }
    } catch (error) {
      console.error('MiMo 연결 실패:', error);
      this.isConnected = false;
      this.chatInput.disabled = false;
      this.chatInput.placeholder = 'MiMo 연결 실패. 시뮬레션 모드로 작동합니다.';
    }
  }

  async listenForMessages() {
    try {
      await tauriListen('mimo-connected', (event) => {
        console.log('MiMo 연결됨:', event.payload);
        this.isConnected = true;
        this.chatInput.disabled = false;
        this.chatInput.placeholder = '메시지를 입력하세요...';
      });

      await tauriListen('mimo-update', (event) => {
        this.handleMimoUpdate(event.payload);
      });

      await tauriListen('mimo-prompt-done', (event) => {
        const payload = event.payload;
        const thoughtTokens = payload && payload.thoughtTokens ? payload.thoughtTokens : 0;
        // Store for use by usage_update handler
        this.lastThoughtTokens = thoughtTokens;
        console.log('Prompt 완료 ID:', payload && payload.id, '/ 사고 토큰:', thoughtTokens);
        // We do not finalize here because in multi-turn runs (with tools), 
        // the response is returned at the end of the turn, but the agent 
        // automatically continues generating notifications in subsequent turns.
        // Finalization is handled by usage_update events.
      });
    } catch (error) {
      console.warn('Tauri event listener registration failed:', error);
    }
  }

  async sendMessageToMimo(message, imageData = null) {
    try {
      await tauriInvoke('send_message', { message, imageData });
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
        <div class="mimo-thought-container hidden" style="margin-bottom: 8px; border-radius: 4px; overflow: hidden; border: 1px solid rgba(255,255,255,0.05);">
          <div class="mimo-thought-header" style="background: rgba(255,255,255,0.03); padding: 6px 12px; font-size: 0.85em; color: var(--text-secondary); cursor: pointer; display: flex; align-items: center; gap: 6px; user-select: none;">
            <span style="color: var(--accent);">🧠</span>
            <span class="mimo-thought-title">미모의 생각 (클릭해서 보기)</span>
            <span class="mimo-thought-arrow" style="margin-left: auto; transition: transform 0.2s ease; font-size: 0.8em;">▼</span>
          </div>
          <div class="mimo-thought-body" style="display: none; background: rgba(255, 255, 255, 0.01); border-top: 1px solid rgba(255,255,255,0.05); border-left: 2px solid var(--accent); padding: 8px 12px; font-size: 0.9em; color: var(--text-secondary); font-style: italic; white-space: pre-wrap;"></div>
        </div>
        <div class="mimo-tools" style="display: flex; flex-direction: column; gap: 6px; margin-bottom: 8px;"></div>
        <div class="mimo-response" style="line-height: 1.6; white-space: pre-wrap;"></div>
        <div class="message-time">${this.getCurrentTime()}</div>
      </div>
    `;
    
    this.chatMessages.appendChild(messageDiv);
    this.scrollToBottom();
    
    const thoughtContainer = messageDiv.querySelector('.mimo-thought-container');
    const thoughtHeader = messageDiv.querySelector('.mimo-thought-header');
    const thoughtBody = messageDiv.querySelector('.mimo-thought-body');
    const thoughtArrow = messageDiv.querySelector('.mimo-thought-arrow');
    const thoughtTitle = messageDiv.querySelector('.mimo-thought-title');

    thoughtHeader.addEventListener('click', () => {
      if (thoughtBody.style.display === 'none') {
        thoughtBody.style.display = 'block';
        thoughtArrow.style.transform = 'rotate(180deg)';
        thoughtTitle.textContent = '미모의 생각 (클릭해서 접기)';
      } else {
        thoughtBody.style.display = 'none';
        thoughtArrow.style.transform = 'rotate(0deg)';
        thoughtTitle.textContent = '미모의 생각 (클릭해서 보기)';
      }
      this.scrollToBottom();
    });

    this.activeThoughtContainerNode = thoughtContainer;
    this.activeThoughtNode = thoughtBody;
    this.activeToolsNode = messageDiv.querySelector('.mimo-tools');
    this.activeResponseNode = messageDiv.querySelector('.mimo-response');
    this.activeMessageDiv = messageDiv;
    this.currentResponseText = ''; // 텍스트 누적 변수 초기화
    
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
    console.log('[MiMo Update]', sessionUpdate, update);

    // usage_update = LLM 1회 추론 완료 신호.
    // 툴 사용 시 여러 번 올 수 있으므로, 실제 텍스트가 쌓인 경우에만 finalize.
    if (sessionUpdate === 'usage_update') {
      if (this.isGenerating) {
        const hasText = this.currentResponseText && this.currentResponseText.trim().length > 0;
        if (hasText) {
          // 텍스트가 있을 때만 → 마지막 usage_update이므로 finalize
          const reasoningTokens = this.lastThoughtTokens || 0;
          if (reasoningTokens > 0 && this.activeThoughtContainerNode && this.activeThoughtNode) {
            this.activeThoughtContainerNode.classList.remove('hidden');
            if (!this.activeThoughtNode.textContent.trim()) {
              this.activeThoughtNode.textContent = `(미모가 ${reasoningTokens} 토큰 동안 내부적으로 사고했습니다.)`;
            }
          }
          console.log('MiMo usage_update (with text) — finalizing response');
          this.finalizeMimoResponse();
        } else {
          // 텍스트 없음 → 툴 사용 중간 usage_update. 무시하고 대기.
          console.log('MiMo usage_update (no text yet) — still waiting for response text');
        }
      }
      return;
    }

    // Reset completion timer on content-bearing updates only
    if (this.mimoCompletionTimer) {
      clearTimeout(this.mimoCompletionTimer);
      this.mimoCompletionTimer = null;
    }
    
    if (sessionUpdate === 'AgentThoughtChunk' || sessionUpdate === 'agent_thought_chunk') {
      if (this.activeThoughtNode && content) {
        if (this.activeThoughtContainerNode) {
          this.activeThoughtContainerNode.classList.remove('hidden');
        }
        const thoughtText = content.text || content.thought || '';
        this.activeThoughtNode.textContent += thoughtText;
        this.scrollToBottom();
      }
    } else if (sessionUpdate === 'AgentMessageChunk' || sessionUpdate === 'agent_message_chunk') {
      if (this.activeResponseNode && content) {
        // 타이핑 인디케이터 제거 (최초 1회)
        const typingIndicator = this.activeResponseNode.querySelector('.typing-indicator');
        if (typingIndicator) {
          this.activeResponseNode.innerHTML = '';
        }
        
        const deltaText = content.text || '';
        if (deltaText) {
          // 누적 변수에 추가
          this.currentResponseText = (this.currentResponseText || '') + deltaText;
          // DOM에 직접 텍스트 노드 추가 (기존 내용 유지)
          this.activeResponseNode.appendChild(document.createTextNode(deltaText));
        }
        this.scrollToBottom();
      }
    } else if (sessionUpdate === 'ToolCall' || sessionUpdate === 'tool_call') {
      const toolCallId = update.toolCallId || '';
      if (toolCallId) {
        this.activeTools.add(toolCallId);
      }

      if (this.activeToolsNode) {
        const toolName = update.title || 'tool';
        const toolArgs = update.rawInput ? JSON.stringify(update.rawInput) : '';
        
        // Check if this tool is already rendered
        let toolDiv = this.activeToolsNode.querySelector(`[data-tool-id="${toolCallId}"]`);
        if (!toolDiv) {
          toolDiv = document.createElement('div');
          toolDiv.className = `tool-execution tool-${toolName}`;
          toolDiv.setAttribute('data-tool-id', toolCallId);
          toolDiv.style.cssText = 'background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 6px; padding: 6px 10px; font-size: 0.85em; font-family: monospace; display: flex; align-items: center; gap: 8px; color: var(--text-secondary); margin-bottom: 4px;';
          toolDiv.innerHTML = `
            <span class="tool-icon" style="color: var(--accent);">⚙️</span>
            <span class="tool-name">${toolName}</span>
            <span class="tool-args" style="opacity: 0.7; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 400px;">(${toolArgs})</span>
            <span class="tool-status" style="margin-left: auto; color: var(--accent); font-weight: bold;">Running...</span>
          `;
          this.activeToolsNode.appendChild(toolDiv);
        }
        this.scrollToBottom();
      }
    } else if (sessionUpdate === 'ToolCallUpdate' || sessionUpdate === 'tool_call_update') {
      const toolCallId = update.toolCallId || '';
      const status = update.status || '';
      if (toolCallId && (status === 'completed' || status === 'success' || status === 'failed' || status === 'error')) {
        this.activeTools.delete(toolCallId);
      }

      if (this.activeToolsNode) {
        const toolDiv = this.activeToolsNode.querySelector(`[data-tool-id="${toolCallId}"]`);
        
        if (toolDiv) {
          const statusSpan = toolDiv.querySelector('.tool-status');
          const iconSpan = toolDiv.querySelector('.tool-icon');
          
          if (status === 'completed' || status === 'success') {
            statusSpan.textContent = '✓ Success';
            statusSpan.style.color = '#10B981';
            iconSpan.textContent = '✓';
            iconSpan.style.color = '#EF4444';
          } else if (status === 'failed' || status === 'error') {
            statusSpan.textContent = '✗ Error';
            statusSpan.style.color = '#EF4444';
            iconSpan.textContent = '✗';
            iconSpan.style.color = '#EF4444';
          } else if (status === 'in_progress') {
            statusSpan.textContent = 'Running...';
            statusSpan.style.color = 'var(--accent)';
          }
        }
      }
    } else if (sessionUpdate === 'TurnEnd' || sessionUpdate === 'turn_end') {
      this.finalizeMimoResponse();
      return;
    } else {
      console.log('[MiMo] Unhandled sessionUpdate type:', sessionUpdate);
    }

    // Fallback silence detection: finalize if no updates for 3 seconds and no tools active
    if (this.activeTools.size === 0 && this.isGenerating) {
      this.mimoCompletionTimer = setTimeout(() => {
        console.log('MiMo response completed due to silence (3s timeout)');
        this.finalizeMimoResponse();
      }, 3000);
    }
  }

  finalizeMimoResponse() {
    if (this.mimoCompletionTimer) {
      clearTimeout(this.mimoCompletionTimer);
      this.mimoCompletionTimer = null;
    }
    this.activeTools.clear();

    if (this.activeResponseNode && this.currentResponseText && this.currentResponseText.trim().length > 0) {
      // 누적된 텍스트를 HTML 포맷으로 변환하여 최종 렌더링
      this.activeResponseNode.innerHTML = this.formatMessage(this.currentResponseText);
    }
    this.setGenerating(false);
    this.activeThoughtContainerNode = null;
    this.activeThoughtNode = null;
    this.activeToolsNode = null;
    this.activeResponseNode = null;
    this.activeMessageDiv = null;
    this.currentResponseText = '';
    this.lastThoughtTokens = 0;
  }
}

document.addEventListener('DOMContentLoaded', () => {
  window.mimoHouse = new MiMoHouse();
});
