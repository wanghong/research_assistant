<template>
    <div class="chat-window">
      <div class="chat-messages">
        <div v-for="(message, index) in messages" :key="index" :class="message.sender === 'user' ? 'user-message' : 'ai-message'">
          <div class="message-content">
            {{ message.content }}
          </div>
        </div>
      </div>
      <div class="input-area">
        <el-input v-model="inputMessage" placeholder="输入消息" @keyup.enter="sendMessage"></el-input>
        <el-button @click="sendMessage">发送</el-button>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  
  const messages = ref([]);
  const inputMessage = ref('');
  
  const sendMessage = async() => {
    if (inputMessage.value.trim() === '') return;
    messages.value.push({ sender: 'user', content: inputMessage.value });
    //await sendRequest(inputMessage.value);
    fetchStream(inputMessage.value);
    inputMessage.value = '';
  };

  const fetchStream = (question) => {
    const eventSource = new EventSource('/api');

    eventSource.onmessage = function (event) {
      console.log(event.data)
      const lastMessageIndex = messages.value.length - 1;
      if (lastMessageIndex >= 0 && messages.value[lastMessageIndex].sender === 'ai') {
          messages.value[lastMessageIndex].content += event.data;
        } else {
          messages.value.push({ sender: 'ai', content: event.data});
        }
    };

    eventSource.onerror = function (error) {
      console.error('EventSource failed:', error);
    };
  }
  
  const sendRequest = async (message) => {
    try {
      const response = await fetch('api', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ input: message })
      });

      if (!response.ok) {
        throw new Error(`请求失败，状态码: ${response.status}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value, { stream: true });
        const lastMessageIndex = messages.value.length - 1;
        if (lastMessageIndex >= 0 && messages.value[lastMessageIndex].sender === 'ai') {
          messages.value[lastMessageIndex].content += chunk;
        } else {
          messages.value.push({ sender: 'ai', content: chunk});
        }
      }
    } catch (error) {
      console.error('请求出错:', error);
    }
  };
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
  </style>    