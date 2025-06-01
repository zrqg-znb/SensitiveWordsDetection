<script setup>
import { NButton, NPopconfirm } from 'naive-ui'
import { h, onMounted, ref, resolveDirective, withDirectives } from 'vue'
import { useCRUD } from '@/composables'
import api from '@/api'
import { renderIcon } from '@/utils'
import CommonPage from '@/components/page/CommonPage.vue'
import CrudTable from '@/components/table/CrudTable.vue'
import { useUserStore } from '@/store'
const userStore = useUserStore()
defineOptions({ name: '网页抓取' })
const $table = ref(null)
const queryItems = ref({
  user_id: userStore.userId,
})
const vPermission = resolveDirective('permission')
const { modalForm, handleDelete } = useCRUD({
  name: '爬虫',
  initForm: {},
  doCreate: api.createCrawler,
  doUpdate: api.updateCrawler,
  doDelete: api.deleteCrawler,
  refresh: () => $table.value?.handleSearch(),
})

function get_report(row) {
  window.open(row.result_url)
}

const columns = [
  {
    title: '网页地址',
    key: 'url',
    width: 'auto',
    align: 'center',
    ellipsis: { tooltip: true },
  },
  {
    title: '请求方法',
    key: 'method',
    align: 'center',
    width: 'auto',
    ellipsis: { tooltip: true },
  },
  {
    title: '请求时间',
    key: 'updated_at',
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
              type: 'success',
              style: 'margin-right: 8px;',
              onClick: () => {
                get_report(row)
                modalForm.value.roles = row.roles.map((e) => (e = e.id))
              },
            },
            {
              default: () => '获取报告',
              icon: renderIcon('material-symbols:book', { size: 16 }),
            }
          ),
          [[vPermission, 'post/api/v1/crawler/create']]
        ),
        h(
          NPopconfirm,
          {
            onPositiveClick: () => handleDelete({ crawler_id: row.id }, false),
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
                    default: () => '删除报告',
                    icon: renderIcon('material-symbols:delete-outline', { size: 16 }),
                  }
                ),
                [[vPermission, 'delete/api/v1/crawler/delete']]
              ),
            default: () => h('div', {}, '确定删除该分析记录吗?'),
          }
        ),
      ]
    },
  },
]
onMounted(() => {
  $table.value?.handleSearch()
})
</script>

<template>
  <!--业务页面-->
  <CommonPage title="爬虫列表">
    <!--表格-->
    <CrudTable
      ref="$table"
      v-model:query-items="queryItems"
      :get-data="api.getCrawlerList"
      :columns="columns"
    >
    </CrudTable>
  </CommonPage>
</template>
