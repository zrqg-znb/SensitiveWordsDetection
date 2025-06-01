<script setup>
import { h, onMounted, ref, resolveDirective, withDirectives } from 'vue'
import { NButton, NForm, NFormItem, NInput, NPopconfirm, NSelect, NSwitch } from 'naive-ui'

import CommonPage from '@/components/page/CommonPage.vue'
import QueryBarItem from '@/components/query-bar/QueryBarItem.vue'
import CrudModal from '@/components/table/CrudModal.vue'
import CrudTable from '@/components/table/CrudTable.vue'
import TheIcon from '@/components/icon/TheIcon.vue'

import { renderIcon } from '@/utils'
import { useCRUD } from '@/composables'
import api from '@/api'

defineOptions({ name: '敏感词管理' })

const $table = ref(null)
const queryItems = ref({})
const vPermission = resolveDirective('permission')

const addSensitiveWordRules = {
  word: [
    {
      required: true,
      message: '请输入敏感词',
      trigger: ['input', 'blur', 'change'],
    },
  ],
  level: [
    {
      required: true,
      message: '请输入敏感等级',
      // trigger: ['input', 'blur'],
    },
  ],
  category: [
    {
      required: true,
      message: '请输入分类',
      trigger: ['input', 'blur'],
    },
  ],
}

const {
  modalVisible,
  modalTitle,
  modalLoading,
  handleSave,
  modalForm,
  modalFormRef,
  handleEdit,
  handleDelete,
  handleAdd,
} = useCRUD({
  name: '敏感词',
  initForm: {},
  doCreate: api.createSensitiveWord,
  doUpdate: api.updateSensitiveWord,
  doDelete: api.deleteSensitiveWord,
  refresh: () => $table.value?.handleSearch(),
})
onMounted(() => {
  $table.value?.handleSearch()
})

async function handleUpdateHidden(row) {
  if (!row.id) return
  row.publishing = true
  await api.toggleSensitiveWord(row.id)
  $table.value?.handleSearch()
  row.publishing = false
  $message?.success(row.is_active ? '已失效' : '已激活')
}

const columns = [
  {
    title: '敏感词',
    key: 'word',
    width: 'auto',
    align: 'center',
    ellipsis: { tooltip: true },
  },
  {
    title: '分类',
    key: 'category',
    align: 'center',
    width: 'auto',
    ellipsis: { tooltip: true },
  },
  {
    title: '状态',
    key: 'is_active',
    width: 'auto',
    align: 'center',
    render(row) {
      return h(NSwitch, {
        size: 'small',
        rubberBand: false,
        value: row.is_active,
        onUpdateValue: () => handleUpdateHidden(row),
      })
    },
  },
  {
    title: '敏感等级',
    key: 'level',
    width: 'auto',
    align: 'center',
    ellipsis: { tooltip: true },
  },
  {
    title: '操作',
    key: 'actions',
    width: 'auto',
    align: 'center',
    fixed: 'right',
    render(row) {
      return [
        withDirectives(
          h(
            NButton,
            {
              size: 'small',
              type: 'primary',
              style: 'margin-right: 8px;',
              onClick: () => {
                handleEdit(row)
                modalForm.value.roles = row.roles.map((e) => (e = e.id))
              },
            },
            {
              default: () => '编辑',
              icon: renderIcon('material-symbols:edit', { size: 16 }),
            }
          ),
          [[vPermission, 'post/api/v1/sen_words/update']]
        ),
        h(
          NPopconfirm,
          {
            onPositiveClick: () => handleDelete({ word_id: row.id }, false),
            onNegativeClick: () => {},
          },
          {
            trigger: () =>
              withDirectives(
                h(
                  NButton,
                  {
                    size: 'small',
                    type: 'error',
                    style: 'margin-right: 8px;',
                  },
                  {
                    default: () => '删除',
                    icon: renderIcon('material-symbols:delete-outline', { size: 16 }),
                  }
                ),
                [[vPermission, 'delete/api/v1/sen_words/delete']]
              ),
            default: () => h('div', {}, '确定删除该敏感词吗?'),
          }
        ),
      ]
    },
  },
]
</script>
<template>
  <!--业务页面-->
  <CommonPage show-footer title="敏感词列表">
    <template #action>
      <div>
        <NButton
          v-permission="'post/api/v1/sen_words/create'"
          class="float-right mr-15"
          type="primary"
          @click="handleAdd"
        >
          <TheIcon icon="material-symbols:add" :size="18" class="mr-5" />
          新建敏感词
        </NButton>
      </div>
    </template>
    <!--表格-->
    <CrudTable
      ref="$table"
      v-model:query-items="queryItems"
      :columns="columns"
      :get-data="api.getSensitiveWordList"
    >
      <template #queryBar>
        <QueryBarItem label="敏感词" :label-width="60">
          <NInput
            v-model:value="queryItems.word"
            placeholder="请输入敏感词"
            clearable
            type="text"
            @keypress.enter="$table?.handleSearch()"
          />
        </QueryBarItem>
        <QueryBarItem label="分类" :label-width="40">
          <NInput
            v-model:value="queryItems.category"
            placeholder="请输入分类"
            clearable
            type="text"
            @keypress.enter="$table?.handleSearch()"
          />
        </QueryBarItem>
        <QueryBarItem label="敏感等级" :label-width="80">
          <NInput
            v-model:value="queryItems.level"
            placeholder="请输入敏感等级"
            clearable
            type="text"
          />
        </QueryBarItem>
        <QueryBarItem label="状态" :label-width="70">
          <NSelect
            v-model:value="queryItems.is_active"
            :options="[
              { label: '已激活', value: true },
              { label: '已失效', value: false },
            ]"
            style="width: 120px"
            placeholder="请选择状态"
            clearable
            @change="$table?.handleSearch()"
          />
        </QueryBarItem>
      </template>
    </CrudTable>
    <!-- 新增/编辑 弹窗 -->
    <CrudModal
      v-model:visible="modalVisible"
      :title="modalTitle"
      :loading="modalLoading"
      @save="handleSave"
    >
      <NForm
        ref="modalFormRef"
        :model="modalForm"
        :rules="addSensitiveWordRules"
        label-placement="left"
        label-align="left"
        :label-width="80"
      >
        <NFormItem label="敏感词" path="word">
          <NInput v-model:value="modalForm.word" placeholder="请输入敏感词" />
        </NFormItem>
        <NFormItem label="敏感等级" path="level">
          <NInput v-model:value="modalForm.level" placeholder="请输入敏感等级" />
        </NFormItem>
        <NFormItem label="分类" path="category">
          <NInput v-model:value="modalForm.category" placeholder="请输入分类" />
        </NFormItem>
      </NForm>
    </CrudModal>
  </CommonPage>
</template>
