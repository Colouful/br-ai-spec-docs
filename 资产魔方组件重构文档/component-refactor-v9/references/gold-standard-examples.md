# Gold-Standard Code Templates

> 这些是从已验证的 disposalTool2 页面提取的真实代码模板。
> 迁移时**严格对照**这些模板，不要凭记忆或凭规则"自由发挥"。

---

## 1. Tab 容器模板（index.vue）

来源: `src/views/disposalTool2/disposalManagement/index.vue`

```vue
<template>
  <Tabs
    v-model:active-key="tabIndex"
    type="line"
    lazy-load
    class="disposal-management-tabs"
  >
    <TabPane
      v-if="hasAuth('disposal_tools_outbound_list')"
      key="1"
      title="外呼"
    >
      <TodoList />
    </TabPane>
    <TabPane
      v-if="hasAuth('disposal_tools_AI_outbound_list')"
      key="2"
      title="AI外呼"
    >
      <CompletedList />
    </TabPane>
  </Tabs>
</template>

<script setup>
import { Tabs, TabPane } from '@arco-design/web-vue';
import { usePermission } from '@koi-design/vix-auth';
import { ref, provide, watch, nextTick } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import TodoList from './todoList.vue';
import CompletedList from './completedList.vue';

const route = useRoute();
const router = useRouter();
const { hasAuth } = usePermission();

// 从 query 参数获取 tab，默认为 '1'
const getDefaultTab = () => {
  if (route.query.tab) return route.query.tab;
  return '1';
};

const tabIndex = ref(getDefaultTab());
provide('tabIndex', tabIndex);  // ← 子组件通过 inject 获取

// 监听 tab 变化，更新路由 query 参数
watch(tabIndex, newVal => {
  if (route.name === 'DisposalManagement2') {
    router.replace({
      name: 'DisposalManagement2',
      query: { ...route.query, tab: newVal }
    });
  }
});

// 首次加载时如果 URL 没有 tab 参数，主动写入默认值
nextTick(() => {
  if (!route.query.tab && route.name === 'DisposalManagement2') {
    router.replace({
      name: 'DisposalManagement2',
      query: { ...route.query, tab: tabIndex.value }
    });
  }
});

// 监听路由 query 变化，更新 tab
watch(
  () => route.query.tab,
  newTab => {
    if (newTab && newTab !== tabIndex.value) {
      tabIndex.value = newTab;
    }
  },
  { immediate: true }
);
</script>
```

---

## 2. ProTable 列表模板（todoList.vue）

来源: `src/views/disposalTool2/disposalManagement/todoList.vue`

```vue
<template>
  <div class="page-wrapper">
    <ProTable
      search
      :action-ref="proTableActionRef"
      :columns="proColumns"
      :request="handleRequest"
      row-key="id"
      manual-request
      size="small"
      :search-tool-bar-actions="searchToolBarActions"
      :query-data="initQueryData"
      :default-page-size="10"
      :page-size-options="[10, 20, 30, 50, 100]"
      :form-props="{ originalToolbarIsShows: [false, false] }"
      :table-props="tableProps"
    >
      <template #cell-action="{ record }">
        <ProActions
          type="link"
          :max-visible-count="2"
          :is-open-dropdown="false"
          :items="getRowActions(record)"
          :comp-props="{ underline: false }"
        />
      </template>
    </ProTable>

    <!-- 弹窗组件 -->
    <Approve
      v-if="approveVisible"
      v-model:visible="approveVisible"
      :current-row="currentRow"
      @refresh-table="getList"
    />
  </div>
</template>

<script setup>
import { ref, reactive, computed, inject, watch, onMounted, nextTick } from 'vue';
import { ProTable, ProActions } from '@ex/ux-comp';
import { usePermission } from '@koi-design/vix-auth';
import AUTH from '@libs/const';
import { getCallListApi } from '@/api/disposalTool';
import Approve from './components/approve.vue';
import { todoColumnsSetting } from './setting';

const { hasAuth } = usePermission();
const proTableActionRef = reactive({});
const currentRow = ref({});
const approveVisible = ref(false);

// ========== 查询缓存（必须排除分页参数）==========
const STORAGE_QUERY_KEY = 'todo-list';

const getStoredQueryData = () => {
  const cache = sessionStorage.getItem(STORAGE_QUERY_KEY);
  if (!cache) return null;
  try {
    const { query } = JSON.parse(cache);
    return query || null;
  } catch {
    sessionStorage.removeItem(STORAGE_QUERY_KEY);
    return null;
  }
};

const saveQueryData = params => {
  try {
    sessionStorage.setItem(
      STORAGE_QUERY_KEY,
      JSON.stringify({ query: params })
    );
  } catch {
    // 存储满时静默失败
  }
};

const initQueryData = computed(() => getStoredQueryData());

// ========== 列配置（搜索字段 + 表格列合并）==========
const proColumns = computed(() => {
  const columns = [];

  // 搜索栏字段（hideInTable: true）
  columns.push({
    title: '机构编号',
    dataIndex: 'orgNo',
    valueType: 'input',
    hideInTable: true,
    fieldProps: { placeholder: '请输入机构编号', allowClear: true }
  });

  // 表格列（hideInSearch: true）
  todoColumnsSetting.forEach(col => {
    if (col.key === 'action') {
      columns.push({
        title: col.title,
        dataIndex: col.key,
        width: col.width,
        hideInSearch: true,
        slotName: 'cell-action'
      });
    } else {
      columns.push({
        title: col.title,
        dataIndex: col.key,
        width: col.width || col.minWidth,
        hideInSearch: true
      });
    }
  });

  return columns;
});

// ========== 请求处理 ==========
const buildRequestParams = params => {
  const { pageNo, pageSize, ...rest } = params || {};
  return {
    pageNum: pageNo,   // ← pageNo → pageNum 映射
    pageSize,
    ...rest
  };
};

const handleRequest = async params => {
  try {
    const requestParams = buildRequestParams(params);
    // ★ 关键：saveQueryData 必须排除分页参数
    const { pageNo, pageSize, ...queryOnly } = params || {};
    saveQueryData(queryOnly);
    const data = await getCallListApi(requestParams);
    return {
      data: data?.records || [],
      total: Number(data?.total || 0),
      success: true
    };
  } catch (error) {
    console.error('列表查询失败:', error);
    return { data: [], total: 0, success: false };
  }
};

// ★ 关键：tableProps 必须包含 scroll.y
const tableProps = {
  scroll: { x: 'max-content', y: 500 }
};

// ========== 行操作 ==========
const getRowActions = record => [
  {
    label: '编辑',
    accessible: hasAuth(AUTH.XXX.EDIT),
    onClick: () => handleOperate('edit', record)
  },
  {
    label: '查看',
    accessible: hasAuth(AUTH.XXX.VIEW),
    onClick: () => handleOperate('view', record)
  }
];

// ========== 刷新 ==========
const getList = () => {
  nextTick(() => {
    proTableActionRef.reload?.();
  });
};

// ========== 工具栏按钮 ==========
const searchToolBarActions = computed(() => [
  {
    key: 'create',
    text: '新增',
    type: 'primary',
    placement: 'suffix',
    auth: hasAuth(AUTH.XXX.ADD),
    onClick: () => handleOperate('create')
  }
]);

// ========== Tab 切换监听 ==========
const tabIndex = inject('tabIndex');
watch(
  () => tabIndex.value,
  val => {
    if (val === '1') {
      getList();
    }
  }
);

onMounted(() => {
  nextTick(() => {
    proTableActionRef.reload?.();
  });
});
</script>
```

---

## 3. ProModalForm 弹窗模板（approve.vue）

来源: `src/views/disposalTool2/disposalManagement/components/approve.vue`

**这是最容易出错的组件，19 个 bug 中有 12 个与此相关。严格对照！**

```vue
<template>
  <ProModalForm
    v-model:visible="visible"
    title="编辑配置"
    :width="600"
    :fields="formFields"
    :loading="loading"
    validate-mode="both"
    :on-finish="handleFinish"
    :action-ref="modalFormAction"
    :form-props="formLayoutProps"
    :modal-props="{
      okText: '提交',
      cancelText: '取消',
      maskClosable: false,
      titleAlign: 'start'       // ★ 必须
    }"
    :on-open-change="onOpenChange"
  />
</template>

<script setup>
import { computed, reactive, ref, watch } from 'vue';
import { ProModalForm } from '@ex/ux-comp';
import { Message as message } from '@arco-design/web-vue';

const props = defineProps({
  visible: { type: Boolean, default: true },
  currentRow: { type: Object, default: () => ({}) }
});
const emit = defineEmits(['update:visible', 'refreshTable']);

// ★ 必须：model ref 用于表单数据
const model = ref({
  orgNo: '',
  orgName: '',
  fieldName: ''
});

const visible = computed({
  get: () => props.visible,
  set: value => emit('update:visible', value)
});

const modalFormAction = reactive({});

// ★ 必须：formLayoutProps 配置
const formLayoutProps = {
  layout: {
    mode: 'grid',
    columns: [24, 24, 24, 24],
    totalColumns: 24,
    gutter: 16
  },
  bordered: false
};

// ★ 必须：所有字段 takeFullRow: true
const formFields = computed(() => [
  {
    label: '机构编号',
    field: 'orgNo',
    valueType: 'input',
    fieldProps: { disabled: true },    // ★ 只读字段：input + disabled
    takeFullRow: true                   // ★ 必须
  },
  {
    label: '机构名称',
    field: 'orgName',
    valueType: 'input',
    fieldProps: { disabled: true },
    takeFullRow: true
  },
  {
    label: '选择字段',
    field: 'fieldName',
    valueType: 'select',
    rules: [{ required: true, message: '请选择', trigger: 'change' }],
    fieldProps: { placeholder: '请选择', allowClear: true },
    options: () => someApi().then(data => data.map(d => ({ value: d.code, label: d.name }))),
    // ★ onChange 必须同步 model + Event 守卫
    onChange: val => {
      if (val instanceof Event) return;  // ★ Event 守卫
      model.value.fieldName = val;        // ★ 同步 model
    },
    takeFullRow: true
  }
]);

const loading = ref(false);

const resetForm = () => {
  model.value = { orgNo: '', orgName: '', fieldName: '' };
};

// ★ 必须：fillFormValues 用 setTimeout 确保表单就绪
const fillFormValues = () => {
  setTimeout(() => {
    if (modalFormAction.setFieldsValue) {
      modalFormAction.setFieldsValue({
        orgNo: model.value.orgNo,
        orgName: model.value.orgName,
        fieldName: model.value.fieldName
      });
    }
  }, 100);
};

// 监听弹窗打开和 currentRow 变化，回显数据
watch(
  [() => props.visible, () => props.currentRow],
  ([newVisible, newCurrentRow]) => {
    if (newVisible && newCurrentRow && newCurrentRow.id) {
      model.value = {
        orgNo: newCurrentRow.orgNo || '',
        orgName: newCurrentRow.orgName || '',
        fieldName: newCurrentRow.fieldName || ''
      };
      fillFormValues();
    }
  },
  { immediate: true }
);

const onOpenChange = open => {
  if (!open) resetForm();
};

// ★★★ 最关键：handleFinish 成功路径必须 emit 关闭 ★★★
const handleFinish = async values => {
  loading.value = true;
  try {
    await updateApi({ ...model.value, id: props.currentRow.id });
    message.success('操作成功');
    emit('update:visible', false);   // ★★★ 必须！Bug #1,5,6 的根因
    emit('refreshTable', true);
  } catch (err) {
    message.error(err);
    return false;
  } finally {
    loading.value = false;
  }
};
</script>
```

---

## 4. ProDescriptions 详情模板（outboundDetail.vue）

来源: `src/views/disposalTool2/disposalManagement/components/outboundDetail.vue`

```vue
<template>
  <div class="relative flex flex-col items-start flex-1 bg-white p-8 rounded-xl overflow-auto">
    <div class="flex justify-end items-center w-full">
      <a-button @click="goBack">返回</a-button>
    </div>
    <a-spin
      class="absolute inset-0 z-10"
      :loading="loading"
      tip=""
      style="width: 100%; height: 100%"
    />
    <div class="pl-4 w-full">
      <ProDescriptions :columns="descColumns" :data="model" />
      <div class="mt-4 flex-1 w-full">
        <ProTable
          :action-ref="proTableActionRef"
          :columns="proColumns"
          :request="handleRequest"
          row-key="id"
          manual-request
          :default-page-size="10"
          :page-size-options="[10, 20, 30, 50, 100]"
          :form-props="{ originalToolbarIsShows: [false, false] }"
          :table-props="tableProps"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { ProDescriptions, ProTable } from '@ex/ux-comp';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();
const loading = ref(false);

const model = reactive({
  orgNo: '',
  orgName: '',
  orgCodeType: ''
});

// ★ ProDescriptions 列定义
const descColumns = [
  { title: '机构编号', dataIndex: 'orgNo' },
  { title: '机构名称', dataIndex: 'orgName' },
  { title: '机构代码', dataIndex: 'orgCodeType' }
];

const proTableActionRef = reactive({});
const tableProps = {
  scroll: { x: 'max-content', y: 400 }  // 详情页 y: 400
};

const goBack = () => {
  const tab = route.query.tab || '1';
  router.push({ name: 'DisposalManagement2', query: { tab } });
};
</script>
```

---

## 5. 带自定义 slot 的 ProModalForm 模板（createAI.vue）

来源: `src/views/disposalTool2/disposalManagement/components/createAI.vue`

用于弹窗内嵌套表格等复杂场景：

```vue
<ProModalForm
  v-model:visible="visible"
  :title="isEdit ? '编辑' : '新增'"
  :width="700"
  :fields="formFields"
  :loading="loading"
  validate-mode="both"
  :on-finish="handleFinish"
  :action-ref="modalFormAction"
  :form-props="formLayoutProps"
  :modal-props="{
    okText: '提交',
    cancelText: '取消',
    maskClosable: false,
    titleAlign: 'start'
  }"
  :on-open-change="onOpenChange"
>
  <!-- 自定义 slot -->
  <template #fieldSlot_fieldDetail>
    <div class="field-detail-wrapper">
      <a-form ref="aFormRef" :model="model">
        <a-table
          :columns="fieldDetailColumns"
          :data="model.fieldDetail"
          row-key="id"
          :pagination="false"
          size="small"
        >
          <template #code="{ record, rowIndex }">
            <!-- 内嵌表单项 -->
          </template>
        </a-table>
      </a-form>
      <a-button type="text" long @click="handleAddEnum">添加</a-button>
    </div>
  </template>
</ProModalForm>
```

对应字段定义中使用 `slotName`:
```js
fields.push({
  label: ' ',
  field: 'fieldDetail',
  slotName: 'fieldSlot_fieldDetail',  // ← 匹配 template #fieldSlot_xxx
  takeFullRow: true,
  formItemProps: { hideAsterisk: true }
});
```

---

## 6. edit + add 双模式 ProModalForm 关键模式

来源: `createAI.vue`

```js
// isLoadingData 守卫：编辑回显期间不触发副作用
const isLoadingData = ref(false);

// 监听字段变化，编辑回显期间跳过
watch(
  () => model.orgName,
  newVal => {
    if (isLoadingData.value) return;  // ★ 编辑回显守卫
    // ... 正常逻辑
  }
);

// 编辑回显
const loadFormData = async row => {
  isLoadingData.value = true;
  try {
    // 1. 设置基础字段
    model.value = { ...row };
    // 2. 加载选项
    await loadOptions();
    // 3. 回显表单值（每次异步操作后都要 setFieldsValue）
    setTimeout(() => {
      modalFormAction.setFieldsValue({ ...model.value });
    }, 100);
  } finally {
    isLoadingData.value = false;
  }
};
```

---

## 使用方法

迁移时：
1. 确定目标文件类型（Tab 容器 / 列表 / 弹窗 / 详情）
2. 打开对应的模板
3. 逐行对照，确保不遗漏关键点
4. 特别注意标有 ★ 的行
