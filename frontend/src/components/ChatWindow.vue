<template>
  <div class="chat-window">
    <div class="chat-messages" ref="chatMessagesRef">
      <div v-for="(message, index) in messages" :key="index"
        :class="message.sender === 'user' ? 'user-message' : 'ai-message'">
        <div class="message-content">
          <div v-if="message.sender === 'user'">
            {{message.content}}
          </div>
          <div v-else>
            <div class="markdown-container">
              <v-md-preview :text="message.content"></v-md-preview>
              <div class="progress-container" v-if="index === messages.length - 1 && message.sender === 'ai' && isStreaming">
                <div class="progress-bar"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-if="isLoading" class="ai-message">
        <div class="message-content loading-indicator">
          <div class="loading-spinner"></div>
        </div>
      </div>
    </div>
    <div class="input-area">
      <el-input v-model="inputMessage" placeholder="Please enter your question." @keyup.enter="sendMessage" :disabled="isLoading || isStreaming"></el-input>
      <el-button @click="sendMessage" :disabled="isLoading || isStreaming">Send</el-button>
    </div>
  </div>
</template>
  
  <script setup>
  import {ref, nextTick, watch} from 'vue'
  
  // chat messages
  const messages = ref([]);
  // user input message
  const inputMessage = ref('');
  // loading state
  const isLoading = ref(false);
  const chatMessagesRef = ref(null);
  // streaming output state
  const isStreaming = ref(false);
  
  const scrollToBottom = async () => {
    await nextTick();
    if (chatMessagesRef.value) {
      chatMessagesRef.value.scrollTop = chatMessagesRef.value.scrollHeight;
    }
  };
  
  // watching messages, if messages changed, scroll to bottom
  watch(() => [...messages.value], () => {
    scrollToBottom();
  }, { deep: true });
  
  // watching isLoading, if isLoading changed, scroll to bottom
  watch(() => isLoading.value, (newVal, oldVal) => {
    if (newVal) {
      scrollToBottom();
    } else if (oldVal && !newVal) {
      const aiMessages = document.querySelectorAll('.ai-message .message-content');
      if (aiMessages.length > 0) {
        const lastAiMessage = aiMessages[aiMessages.length - 1];
        lastAiMessage.style.width = '80%';
      }
    }
  });
  
  const sendMessage = async() => {
    if (inputMessage.value.trim() === '') return;
    messages.value.push({ sender: 'user', content: inputMessage.value });
    isLoading.value = true;
    fetchStream(inputMessage.value);
    inputMessage.value = '';
    // scroll to bottom after sending message
    scrollToBottom();
  };

  const fetchStream = (question) => {
    const eventSource = new EventSource(`/api?question=${encodeURIComponent(question)}`);

    eventSource.onmessage = function (event) {
      if (event.data === '[DONE]') {
        eventSource.close();
        isLoading.value = false;
        isStreaming.value = false; 
        scrollToBottom(); 
        return;
      }

      let data = JSON.parse(event.data);
      data = data.content;
      if (data === '') return;
      isLoading.value = false;
      isStreaming.value = true;
      
      const lastMessageIndex = messages.value.length - 1;
      if (lastMessageIndex >= 0 && messages.value[lastMessageIndex].sender === 'ai') {
          messages.value[lastMessageIndex].content += data;
        } else {
          messages.value.push({ sender: 'ai', content: data});
        }
    };

    eventSource.onclose = function () {
      eventSource.close();
      isLoading.value = false;
      isStreaming.value = false;
      console.log('EventSource closed');
    };

    eventSource.onerror = function (error) {
      console.error('EventSource error:', error);
      eventSource.close();
      isLoading.value = false;
      isStreaming.value = false;
    };
  }
  </script>
  
  <style scoped>
  .chat-window {
    max-width: 800px;
    margin: 0 auto;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 20px;
    height: 700px;
    display: flex;
    flex-direction: column;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 16px;
  }
  
  .chat-messages {
    flex: 1;
    overflow-y: auto;
    margin-bottom: 20px;
    padding-right: 10px;
  }
  
  .user-message {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 15px;
  }
  
  .ai-message {
    display: flex;
    justify-content: flex-start;
    margin-bottom: 15px;
  }
  
  .message-content {
    border-radius: 20px;
    max-width: 80%;
    line-height: 1.5;
    text-align: left;
  }
  
  .user-message .message-content {
    background-color: #007aff;
    color: white;
    box-shadow: 0 2px 4px rgba(0, 122, 255, 0.2);
    padding: 14px 20px;
  }
  
  .ai-message .message-content {
    background-color: #f0f0f0;
    color: #333;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    width: auto;
    transition: width 0.3s ease;
  }
  
  .input-area {
    display: flex;
    gap: 15px;
  }
  
  .input-area .el-input__inner {
    border-radius: 25px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 16px;
    padding: 12px 15px; 
  }
  
  .input-area .el-button {
    border-radius: 25px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 16px;
    padding: 0 20px;
  }

  .progress-container {
    width: 90%;
    height: 3px;
    margin: 8px auto 0;
    overflow: hidden;
    position: relative;
    border-radius: 1.5px;
  }
  
  .progress-bar {
    position: absolute;
    width: 30%;
    height: 100%;
    background: linear-gradient(to right, transparent, #007aff, transparent);
    animation: shimmer 2s infinite;
  }
  
  @keyframes shimmer {
    0% {
      transform: translateX(-100%);
    }
    100% {
      transform: translateX(300%);
    }
  }
  
  @keyframes pulse {
    0%, 100% {
      transform: scale(1);
      opacity: 0.6;
    }
    50% {
      transform: scale(1.2);
      opacity: 1;
    }
  }
  
  .loading-indicator {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 40px;
    min-width: 60px;
  }
  
  .loading-spinner {
    width: 20px;
    height: 20px;
    border: 3px solid rgba(0, 0, 0, 0.1);
    border-radius: 50%;
    border-top-color: #007aff;
    animation: spin 1s ease-in-out infinite;
  }
  
  @keyframes spin {
    to { transform: rotate(360deg); }
  }
  </style>