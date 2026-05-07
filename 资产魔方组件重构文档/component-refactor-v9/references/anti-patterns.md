# Anti-Patterns: 19 Bugs, 10 Rules

> 来源: `docs/component-refactor/bugfix-log.md`（19 条真实 bug）
> 这不是"建议"，是**硬性停止规则**。命中任一条必须修复后才能继续。

---

## AP-01: ProModalForm onFinish 缺少 emit('update:visible', false)

**严重级别**: 🔴 BLOCKER
**命中 Bug**: #1, #5, #6
**频率**: 3/19

### 错误代码
```js
const handleFinish = async values => {
  await updateApi(values);
  message.success('操作成功');
  // ❌ 缺少关闭弹窗
  emit('refreshTable', true);
};
```

### 正确代码
```js
const handleFinish = async values => {
  await updateApi(values);
  message.success('操作成功');
  emit('update:visible', false);  // ★ 必须！
  emit('refreshTable', true);
};
```

### 检测方法
搜索所有 ProModalForm 子组件的 `handleFinish` / `handleSubmit`，检查成功路径是否包含 `emit('update:visible', false)`。

---

## AP-02: ProModalForm initFormModel 覆盖用户输入

**严重级别**: 🔴 BLOCKER
**命中 Bug**: #10, #12, #13, #14, #16
**频率**: 5/19（最高频）

### 根因
ProModalForm 内部 `watch(() => props.fields, initFormModel)` 在 `formFields` computed 重计算时触发，执行 `formModel.value = props.formModel`，用父组件 model 的旧值覆盖用户已填值。

### 触发条件
`formFields` computed 依赖动态 ref（如选项列表），当选项加载完成时触发重计算。

### 防御措施
1. **onChange 必须在异步操作前同步 model**
```js
onChange: async val => {
  model.value.vendorId = val;  // ★ 先同步
  const options = await getOptions(val);  // 再异步
  subOptions.value = options;
}
```

2. **如果 formFields 依赖动态数据，考虑用 watch + setFieldsValue 替代 onChange 驱动**

### 检测方法
检查 `formFields` computed 是否引用了动态 ref（`xxxOptions.value`），如果有则必须检查所有 onChange 是否同步 model。

---

## AP-03: ProModalForm 字段缺少 takeFullRow: true

**严重级别**: 🟡 HIGH
**命中 Bug**: #11
**频率**: 1/19

### 错误代码
```js
{ label: '机构编号', field: 'orgNo', valueType: 'input' }
// ❌ 缺少 takeFullRow: true
```

### 正确代码
```js
{ label: '机构编号', field: 'orgNo', valueType: 'input', takeFullRow: true }
```

### 检测方法
搜索所有 ProModalForm 的 `formFields` / `fields`，检查每个字段对象是否包含 `takeFullRow: true`。

---

## AP-04: onChange 中异步操作前未同步 model

**严重级别**: 🔴 BLOCKER
**命中 Bug**: #9, #12, #13, #14
**频率**: 4/19

### 错误代码
```js
onChange: async val => {
  // ❌ 异步操作可能触发 formFields 重计算 → initFormModel 覆盖
  const options = await getSubOptions(val);
  subOptions.value = options;
  model.value.vendorId = val;  // 太晚了
}
```

### 正确代码
```js
onChange: async val => {
  model.value.vendorId = val;  // ★ 先同步
  const options = await getSubOptions(val);  // 再异步
  subOptions.value = options;
}
```

### 检测方法
检查所有 ProModalForm 字段的 `onChange`，确保 `model.xxx = val` 在任何 `await` 之前。

---

## AP-05: onChange Event 对象泄漏

**严重级别**: 🟡 HIGH
**命中 Bug**: #15
**频率**: 1/19

### 症状
选择字段后回显 `[object Event]`。

### 错误代码
```js
onChange: val => {
  model.value.template = val;  // ❌ val 可能是 Event 对象
}
```

### 正确代码
```js
onChange: val => {
  if (val instanceof Event) return;  // ★ Event 守卫
  model.value.template = val;
}
```

### 检测方法
搜索所有 `onChange` 回调，检查是否有 `instanceof Event` 守卫。

---

## AP-06: ProTable 缺少 scroll.y

**严重级别**: 🟡 HIGH
**命中 Bug**: #18
**频率**: 14 个文件受影响

### 错误代码
```js
const tableProps = {
  scroll: { x: 'max-content' }  // ❌ 缺少 y
};
```

### 正确代码
```js
const tableProps = {
  scroll: { x: 'max-content', y: 500 }  // ★ 必须包含 y
};
// 详情页用 y: 400
```

### 检测方法
搜索所有 `tableProps`，检查 `scroll` 是否包含 `y` 属性。

---

## AP-07: saveQueryData 包含分页参数

**严重级别**: 🔴 BLOCKER
**命中 Bug**: #19
**频率**: 9 个文件受影响

### 死循环
`saveQueryData(params)` → sessionStorage 存入含 `pageSize: 20` → `initQueryData` 读取 → ProTable `formModel.pageSize = 20` 覆盖 `pagination.pageSize = 10` → 切换分页无效。

### 错误代码
```js
saveQueryData(params);  // ❌ params 包含 pageNo, pageSize
```

### 正确代码
```js
const { pageNo, pageSize, ...queryOnly } = params || {};
saveQueryData(queryOnly);  // ★ 只保存搜索条件
```

### 检测方法
搜索所有 `saveQueryData` 调用，检查传入参数是否已排除分页字段。

---

## AP-08: 列配置包含多余列（死代码）

**严重级别**: 🟡 MEDIUM
**命中 Bug**: #2, #3, #7, #8
**频率**: 4/19

### 症状
表格多出"附件名称"、"审批状态"等列，参考文件中不存在。

### 根因
从旧版模板复制了多余 slot 模板，在 `proColumns` computed 中额外 `push` 了列定义。

### 正确做法
严格对照参考文件（如 `setting.js` 中的 `xxxColumnsSetting`），不从旧版复制多余列。

### 检测方法
对比 `proColumns` computed 中的列与参考文件的列配置，移除多余列。

---

## AP-09: GET API 使用 data 而非 params

**严重级别**: 🔴 BLOCKER
**命中 Bug**: #17
**频率**: 1/19

### 根因
axios GET 请求的 `data` 是 request body，服务器通常忽略。分页参数必须用 `params` 才会作为 query string 发送。

### 错误代码
```js
export const getPageListApi = data => request({ url: '/api/list', method: 'get', data });
// ❌ GET 请求用 data
```

### 正确代码
```js
export const getPageListApi = params => request({ url: '/api/list', method: 'get', params });
// ★ GET 请求用 params
```

### 检测方法
搜索所有 `method: 'get'` 的 API 定义，检查是否使用 `params` 而非 `data`。

---

## AP-10: 只读字段使用 valueType: 'text'

**严重级别**: 🟡 MEDIUM
**命中 Bug**: 经验总结
**频率**: 常见

### 错误代码
```js
{ label: '机构编号', field: 'orgNo', valueType: 'text' }
// ❌ valueType: 'text' 渲染异常
```

### 正确代码
```js
{ label: '机构编号', field: 'orgNo', valueType: 'input', fieldProps: { disabled: true } }
// ★ 用 input + disabled
```

### 检测方法
搜索所有 `valueType: 'text'`，替换为 `valueType: 'input'` + `fieldProps: { disabled: true }`。

---

## 附录：Prettier/ESLint 格式问题

**严重级别**: 🔴 BLOCKER
**命中 Bug**: #4
**频率**: 1/19

每次编辑 Vue 文件后必须运行格式化：
```bash
npx prettier --write <file>
```

ESLint 检查：
```bash
python3 scripts/check_changed_eslint.py
```

---

## 快速检查命令

```bash
# AP-01: 检查 onFinish 是否有 emit('update:visible', false)
grep -rn "handleFinish\|handleSubmit" src/views/disposalTool2/<page>/ --include="*.vue" -A 10 | grep -c "update:visible"

# AP-06: 检查 tableProps.scroll 是否有 y
grep -rn "scroll.*x.*max-content" src/views/disposalTool2/<page>/ --include="*.vue" | grep -v "y:"

# AP-07: 检查 saveQueryData 是否排除分页
grep -rn "saveQueryData(" src/views/disposalTool2/<page>/ --include="*.vue" -B 2

# AP-09: 检查 GET API 是否用 data
grep -rn "method.*get.*data" src/api/ --include="*.js"
```
