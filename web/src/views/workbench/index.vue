<template>
  <AppPage :show-footer="false">
    <div flex flex-col flex-1 gap-4>
      <!-- 用户信息卡片 -->
      <n-card rounded-10>
        <div flex items-center justify-between>
          <div flex items-center>
            <img rounded-full width="60" :src="userStore.avatar" />
            <div ml-10>
              <p text-20 font-semibold>
                {{ $t('views.workbench.text_hello', { username: userStore.name }) }}
              </p>
              <p mt-5 text-14 op-60>{{ $t('views.workbench.text_welcome') }}</p>
            </div>
          </div>
        </div>
      </n-card>

      <!-- 数据统计卡片 -->
      <n-grid x-gap="12" y-gap="12" cols="2 600:4">
        <n-gi>
          <n-card title="今日检测量" hoverable>
            <div text-24 font-bold>14</div>
          </n-card>
        </n-gi>
        <n-gi>
          <n-card title="敏感词总数" hoverable>
            <div text-24 font-bold>4,042</div>
          </n-card>
        </n-gi>
        <n-gi>
          <n-card title="检测准确率" hoverable>
            <div text-24 font-bold>99.5%</div>
          </n-card>
        </n-gi>
        <n-gi>
          <n-card title="系统健康度" hoverable>
            <div text-24 font-bold>100%</div>
          </n-card>
        </n-gi>
      </n-grid>

      <!-- 功能模块 -->
      <n-card title="快捷入口" hoverable>
        <n-grid x-gap="12" y-gap="12" cols="2 400:4">
          <n-gi>
            <n-button secondary block type="success" @click="$router.push('/web-crawler')">
              网页检测
            </n-button>
          </n-gi>
          <n-gi>
            <n-button secondary block type="info" @click="$router.push('/text-det')">
              文本/OCR检测
            </n-button>
          </n-gi>
          <n-gi>
            <n-button secondary block type="warning" @click="$router.push('/profile')">
              个人中心
            </n-button>
          </n-gi>
          <n-gi>
            <n-button secondary block type="error" @click="$router.push('/crawlers')">
              检测报告
            </n-button>
          </n-gi>
        </n-grid>
      </n-card>

      <!-- 开发时间线-->
      <n-card title="开发时间线" hoverable>
        <n-timeline horizontal>
          <n-timeline-item type="warning" title="建题" time="2025-02-03" />
          <n-timeline-item type="success" content="开发完成" time="2025-02-23" />
        </n-timeline>
      </n-card>
    </div>
  </AppPage>
</template>

<script setup>
import { useUserStore } from '@/store'
import { NGrid, NGi } from 'naive-ui'

const userStore = useUserStore()
</script>
