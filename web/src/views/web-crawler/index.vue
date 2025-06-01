<template>
  <AppPage :show-footer="false">
    <n-card>
      <n-form
        ref="formRef"
        :model="formValue"
        :rules="rules"
        label-placement="left"
        label-width="auto"
        require-mark-placement="right-hanging"
        size="medium"
      >
        <!-- 请求方法选择 -->
        <n-form-item label="请求方法" path="method">
          <n-select
            v-model:value="formValue.method"
            :options="httpMethods"
            placeholder="请选择请求方法"
          />
        </n-form-item>

        <!-- URL输入框 -->
        <n-form-item label="目标URL" path="url">
          <n-input v-model:value="formValue.url" placeholder="请输入目标URL" />
        </n-form-item>

        <!-- Headers配置 -->
        <n-form-item label="请求头Headers">
          <n-dynamic-input
            v-model:value="formValue.headers"
            :on-create="onCreateHeader"
            placeholder="请添加Header"
          >
            <template #create-button-default> 添加Header</template>
            <template #default="{ value }">
              <div style="display: flex; align-items: center; width: 100%">
                <n-input v-model:value="value.key" placeholder="Key" style="margin-right: 12px" />
                <n-input v-model:value="value.value" placeholder="Value" />
              </div>
            </template>
          </n-dynamic-input>
        </n-form-item>

        <!-- 参数配置 -->
        <n-form-item label="请求参数params">
          <n-dynamic-input
            v-model:value="formValue.params"
            :on-create="onCreateParam"
            placeholder="请添加参数"
          >
            <template #create-button-default> 添加参数</template>
            <template #default="{ value }">
              <div style="display: flex; align-items: center; width: 100%">
                <n-checkbox v-model:checked="value.enabled" style="margin-right: 12px" />
                <n-input v-model:value="value.key" placeholder="Key" style="margin-right: 12px" />
                <n-input v-model:value="value.value" placeholder="Value" />
              </div>
            </template>
          </n-dynamic-input>
        </n-form-item>

        <!-- 发送按钮 -->
        <n-form-item>
          <n-button type="primary" :loading="loading" @click="handleSubmit"> 发送请求</n-button>
        </n-form-item>
      </n-form>
    </n-card>
  </AppPage>
</template>

<script setup>
import { ref, reactive } from 'vue'
import {
  NCard,
  NForm,
  NFormItem,
  NInput,
  NButton,
  NDynamicInput,
  NCheckbox,
  NSelect,
  useMessage,
} from 'naive-ui'
import api from '@/api'
import { useUserStore } from '@/store'
const userStore = useUserStore()
const message = useMessage()
const loading = ref(false)
const formRef = ref(null)
const $table = ref(null)
onMounted(() => {
  $table.value?.handleSearch()
})
const formValue = reactive({
  url: '',
  method: 'GET',
  headers: [
    {
      key: 'user-agent',
      value:
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    },
  ],
  params: [],
})

const httpMethods = [
  { label: 'GET', value: 'GET' },
  { label: 'POST', value: 'POST' },
  { label: 'PUT', value: 'PUT' },
  { label: 'DELETE', value: 'DELETE' },
  { label: 'PATCH', value: 'PATCH' },
  { label: 'HEAD', value: 'HEAD' },
  { label: 'OPTIONS', value: 'OPTIONS' },
]

const rules = {
  url: {
    required: true,
    message: '请输入目标URL',
    trigger: ['blur', 'input'],
  },
  method: {
    required: true,
    message: '请选择请求方法',
    trigger: ['blur', 'change'],
  },
}

function onCreateHeader() {
  return {
    key: '',
    value: '',
  }
}

function onCreateParam() {
  return {
    key: '',
    value: '',
    enabled: true,
  }
}

async function handleSubmit() {
  try {
    await formRef.value?.validate()
    loading.value = true

    // 构建请求参数
    const requestData = {
      url: formValue.url,
      result_url: '',
      user_id: userStore.userId,
      method: formValue.method,
      headers: formValue.headers.reduce((acc, curr) => {
        if (curr.key && curr.value) {
          acc[curr.key] = curr.value
        }
        return acc
      }, {}),
      params: formValue.params.reduce((acc, curr) => {
        if (curr.enabled && curr.key && curr.value) {
          acc[curr.key] = curr.value
        }
        return acc
      }, {}),
    }

    // TODO: 发送请求到后端
    const response = await api.doCrawler(requestData)
    if (response.code === 200) {
      message.success('网页分析完成，请在分析历史中查看详细报告')
    }
  } catch (error) {
    if (error?.message) {
      message.error(error.message)
    }
  } finally {
    loading.value = false
  }
}
</script>
