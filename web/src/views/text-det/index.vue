<script setup>
import { CloudUpload } from '@vicons/ionicons5'
import api from '@/api'
import { useMessage } from 'naive-ui'
const message = useMessage()
const sentence = ref(null)
const handleSearch = () => {
  const request_sentences = { sentences: [sentence.value] }
  api.checkText(request_sentences).then((res) => {
    if (res.code === 200) {
      message.success(res.msg)
      // 右侧区域显示res.data.report_url的地址的内容
      const iframe = document.createElement('iframe')
      iframe.style.width = '100%'
      iframe.style.height = '100%'
      iframe.style.border = 'none'
      iframe.src = res.data.report_url
      // 清空原有内容
      document.getElementById('det_res').innerHTML = ''
      document.getElementById('det_res').appendChild(iframe)
    } else {
      message.error(res.msg)
    }
  })
}
// 处理文件变化
const handleChange = ({ file }) => {
  // 读取文件并转换为 Base64
  const reader = new FileReader()
  reader.onload = (e) => {
    const fullBase64 = e.target.result

    // 去掉 Base64 前缀
    const base64WithoutPrefix = fullBase64.split(',')[1] || fullBase64

    // 构建请求对象
    const request_base = { base64_data: base64WithoutPrefix }
    api.getBase64(request_base).then((res) => {
      if (res.code === 200) {
        for (let i = 0; i < res.data.sentences.length; i++) {
          sentence.value += res.data.sentences[i]
        }
      } else {
        message.error(res.msg)
      }
    })
  }
  reader.readAsDataURL(file.file)
}
</script>
<template>
  <AppPage>
    <n-grid x-gap="12" :cols="2">
      <n-gi>
        <div class="light-green">
          <n-upload multiple directory-dnd accept="image/*" :max="1" @change="handleChange">
            <n-upload-dragger>
              <div style="margin-bottom: 12px">
                <n-icon size="48" :depth="3">
                  <CloudUpload />
                </n-icon>
              </div>
              <n-text style="font-size: 16px"> 点击或者拖动文件到该区域来上传 </n-text>
              <n-p depth="3" style="margin: 8px 0 0 0">
                请上传待检测的图片数据，仅支持jpg、png、jpeg格式，且不超过2M
              </n-p>
            </n-upload-dragger>
          </n-upload>
          <n-input
            v-model:value="sentence"
            mt-10
            :autosize="{
              minRows: 8,
              maxRows: 15,
            }"
            type="textarea"
            placeholder="请输入待检测的文字,且不少于100字"
          />
          <n-button mt-10 type="primary" @click="handleSearch"> 开始检测 </n-button>
        </div>
      </n-gi>
      <n-gi>
        <div id="det_res" class="green">
          <h2 class="right-text">请先上传文字或图片进行检测</h2>
        </div>
      </n-gi>
    </n-grid>
  </AppPage>
</template>
<style scoped>
.light-green {
  height: 80vh;
  box-shadow: 0 0 10px rgba(193, 210, 241, 0.5);
  padding: 2rem;
  text-align: center;
}
.green {
  height: 80vh;
  box-shadow: 0 0 10px rgba(193, 210, 241, 0.5);
  display: flex;
}
.right-text {
  margin: auto;
}
</style>
