<template>
  <AppPage :show-footer="true" bg-cover :style="{ backgroundImage: `url(${bgImg})` }">
    <div
      style="transform: translateY(25px)"
      class="m-auto max-w-1500 min-w-345 f-c-c rounded-10 bg-white bg-opacity-70 p-15 card-shadow"
      dark:bg-dark
    >
      <div hidden w-380 px-20 py-35 md:block>
        <icon-custom-front-page pt-10 text-300 color-primary></icon-custom-front-page>
      </div>

      <div w-320 flex-col px-20 py-35>
        <h5 f-c-c text-24 font-normal color="#6a6a6a">
          <icon-custom-newlogo style="width: 50px; height: 50px;" mr-10 text-50 color-primary />敏感词检测系统
        </h5>
        <div mt-30>
          <n-input
            v-model:value="loginInfo.username"
            autofocus
            class="h-50 items-center pl-10 text-16"
            placeholder="请输入账户名"
            :maxlength="20"
          />
        </div>
        <div mt-30>
          <n-input
            v-model:value="loginInfo.password"
            class="h-50 items-center pl-10 text-16"
            type="password"
            show-password-on="mousedown"
            placeholder="请输入密码"
            :maxlength="20"
            @keypress.enter="handleLogin"
          />
        </div>

        <div mt-20>
          <n-button
            h-50
            w-full
            rounded-5
            text-16
            type="primary"
            :loading="loading"
            @click="handleLogin"
          >
            {{ $t('views.login.text_login') }}
          </n-button>
        </div>
        <div mt-10 text-center>
          <n-button text type="primary" @click="showRegister = true">注册新账号</n-button>
        </div>
      </div>
    </div>

    <!-- 注册弹窗 -->
    <n-modal v-model:show="showRegister" preset="dialog" title="注册新账号">
      <n-form
        ref="registerFormRef"
        :model="registerForm"
        :rules="registerRules"
        label-placement="left"
        label-width="80"
        require-mark-placement="right-hanging"
      >
        <n-form-item label="用户名" path="username">
          <n-input v-model:value="registerForm.username" placeholder="请输入用户名" />
        </n-form-item>
        <n-form-item label="邮箱" path="email">
          <n-input v-model:value="registerForm.email" placeholder="请输入邮箱" />
        </n-form-item>
        <n-form-item label="密码" path="password">
          <n-input
            v-model:value="registerForm.password"
            type="password"
            show-password-on="mousedown"
            placeholder="请输入密码"
          />
        </n-form-item>
        <n-form-item label="确认密码" path="confirmPassword">
          <n-input
            v-model:value="registerForm.confirmPassword"
            type="password"
            show-password-on="mousedown"
            placeholder="请再次输入密码"
          />
        </n-form-item>
      </n-form>
      <template #action>
        <n-button type="primary" :loading="registerLoading" @click="handleRegister">注册</n-button>
      </template>
    </n-modal>
  </AppPage>
</template>

<script setup>
import { lStorage, setToken } from '@/utils'
import bgImg from '@/assets/images/loginbg.jpeg'
import api from '@/api'
import { addDynamicRoutes } from '@/router'
import { useI18n } from 'vue-i18n'
import { NModal, NForm, NFormItem, NInput } from 'naive-ui'

const router = useRouter()
const { query } = useRoute()
const { t } = useI18n({ useScope: 'global' })

const loginInfo = ref({
  username: '',
  password: '',
})

const showRegister = ref(false)
const registerLoading = ref(false)
const registerForm = ref({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  role: '2',      // 默认角色为普通用户
  status: 1,         // 默认状态为启用
  department: '', // 默认部门为根部门
})

const registerRules = {
  username: [
    {
      required: true,
      message: '请输入用户名称',
      trigger: ['input', 'blur'],
    },
  ],
  email: [
    {
      required: true,
      message: '请输入邮箱地址',
      trigger: ['input', 'change'],
    },
    {
      trigger: ['blur'],
      validator: (rule, value, callback) => {
        const re = /^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/
        if (!re.test(registerForm.value.email)) {
          callback('邮箱格式错误')
          return
        }
        callback()
      },
    },
  ],
  password: [
    {
      required: true,
      message: '请输入密码',
      trigger: ['input', 'blur', 'change'],
    },
  ],
  confirmPassword: [
    {
      required: true,
      message: '请再次输入密码',
      trigger: ['input'],
    },
    {
      trigger: ['blur'],
      validator: (rule, value, callback) => {
        if (value !== registerForm.value.password) {
          callback('两次密码输入不一致')
          return
        }
        callback()
      },
    },
  ],
}

initLoginInfo()

function initLoginInfo() {
  const localLoginInfo = lStorage.get('loginInfo')
  if (localLoginInfo) {
    loginInfo.value.username = localLoginInfo.username || ''
    loginInfo.value.password = localLoginInfo.password || ''
  }
}

const loading = ref(false)
async function handleLogin() {
  const { username, password } = loginInfo.value
  if (!username || !password) {
    $message.warning(t('views.login.message_input_username_password'))
    return
  }
  try {
    loading.value = true
    $message.loading(t('views.login.message_login_success'))
    const res = await api.login({ username, password: password.toString() })
    $message.success(t('views.login.message_login_success'))
    setToken(res.data.access_token)
    await addDynamicRoutes()
    if (query.redirect) {
      const path = query.redirect
      console.log('path', { path, query })
      Reflect.deleteProperty(query, 'redirect')
      router.push({ path, query })
    } else {
      router.push('/')
    }
  } catch (e) {
    console.error('login error', e.error)
  }
  loading.value = false
}

async function handleRegister() {
  try {
    registerLoading.value = true
    await api.createUser({
      username: registerForm.value.username,
      email: registerForm.value.email,
      password: registerForm.value.password,
      role_ids: [registerForm.value.role],
      is_active: registerForm.value.status,
      // department: registerForm.value.department,
    })
    $message.success('注册成功，请登录')
    showRegister.value = false
    // 清空注册表单
    registerForm.value = {
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
    }
  } catch (error) {
    console.error('register error', error)
    $message.error('注册失败：' + error.message)
  } finally {
    registerLoading.value = false
  }
}
</script>
