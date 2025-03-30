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
            <v-md-preview :text="message.content"></v-md-preview>
          </div>
        </div>
      </div>
      <!-- 添加加载指示器 -->
      <div v-if="isLoading" class="ai-message">
        <div class="message-content loading-indicator">
          <div class="loading-spinner"></div>
        </div>
      </div>
    </div>
    <div class="input-area">
      <el-input v-model="inputMessage" placeholder="Please enter your question." @keyup.enter="sendMessage"></el-input>
      <el-button @click="sendMessage">Send</el-button>
    </div>
  </div>
</template>
  
  <script setup>
  import {ref, nextTick, watch} from 'vue'
  
  const messages = ref([]);
  const inputMessage = ref('');
  const isLoading = ref(false);
  const chatMessagesRef = ref(null);
  
  // 滚动到底部的方法
  const scrollToBottom = async () => {
    await nextTick();
    if (chatMessagesRef.value) {
      chatMessagesRef.value.scrollTop = chatMessagesRef.value.scrollHeight;
    }
  };
  
  // 监听消息变化，自动滚动到底部
  watch(() => [...messages.value], () => {
    scrollToBottom();
  }, { deep: true });
  
  // 监听加载状态变化，当加载指示器出现时也滚动到底部
  watch(() => isLoading.value, (newVal) => {
    if (newVal) {
      scrollToBottom();
    }
  });
  
  const sendMessage = async() => {
    if (inputMessage.value.trim() === '') return;
    messages.value.push({ sender: 'user', content: inputMessage.value });
    isLoading.value = true;
    fetchStream(inputMessage.value);
    inputMessage.value = '';
    // 发送消息后滚动到底部
    scrollToBottom();
  };

  const fetchStream = (question) => {
    const eventSource = new EventSource(`/api?question=${encodeURIComponent(question)}`);

    eventSource.onmessage = function (event) {
      if (event.data === '[DONE]') {
        eventSource.close();
        isLoading.value = false;
        scrollToBottom(); // 消息结束时滚动到底部
        return;
      }

      let data = JSON.parse(event.data);
      data = data.content;
      if (data === '') return;
      isLoading.value = false;
      
      const lastMessageIndex = messages.value.length - 1;
      if (lastMessageIndex >= 0 && messages.value[lastMessageIndex].sender === 'ai') {
          messages.value[lastMessageIndex].content += data;
        } else {
          messages.value.push({ sender: 'ai', content: data});
        }
      // 不需要在这里调用scrollToBottom，因为watch会处理
    };

    eventSource.onclose = function () {
      // 关闭 EventSource
      eventSource.close();
      isLoading.value = false;
      console.log('EventSource 已关闭');
    };

    eventSource.onerror = function (error) {
      console.error('EventSource 失败:', error);
      // 关闭 EventSource
      eventSource.close();
      isLoading.value = false;
    };
  }
  </script>
  
  <style scoped>
  .chat-window {
    max-width: 800px; /* 增大最大宽度 */
    margin: 0 auto;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 20px; /* 增大内边距 */
    height: 700px; /* 增大高度 */
    display: flex;
    flex-direction: column;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 16px;
  }
  
  .chat-messages {
    flex: 1;
    overflow-y: auto;
    margin-bottom: 20px; /* 增大底部边距 */
    padding-right: 10px; /* 增大右侧内边距 */
  }
  
  .user-message {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 15px; /* 增大消息之间的底部边距 */
  }
  
  .ai-message {
    display: flex;
    justify-content: flex-start;
    margin-bottom: 15px; /* 增大消息之间的底部边距 */
  }
  
  .message-content {
    padding: 15px 20px; /* 增大消息内容的内边距 */
    border-radius: 20px; /* 增大消息框的圆角 */
    max-width: 70%;
    line-height: 1.5;
    text-align: left;
  }
  
  .user-message .message-content {
    background-color: #007aff;
    color: white;
    box-shadow: 0 2px 4px rgba(0, 122, 255, 0.2);
  }
  
  .ai-message .message-content {
    background-color: #f0f0f0;
    color: #333;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  
  .input-area {
    display: flex;
    gap: 15px; /* 增大输入框和按钮之间的间距 */
  }
  
  .input-area .el-input__inner {
    border-radius: 25px; /* 增大输入框的圆角 */
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 16px;
    padding: 12px 15px; /* 增大输入框内文字的内边距 */
  }
  
  .input-area .el-button {
    border-radius: 25px; /* 增大按钮的圆角 */
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 16px;
    padding: 0 20px; /* 增大按钮内文字的左右内边距 */
  }
  
  /* 添加加载指示器样式 */
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