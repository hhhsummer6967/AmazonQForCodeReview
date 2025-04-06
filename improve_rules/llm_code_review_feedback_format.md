# 大语言模型代码审核反馈格式规范

## 1. 反馈结构总览

大语言模型进行代码审核时，应遵循以下结构化反馈格式：

```
# 代码审核报告: [文件名]

## 总体评估
[总体质量评价，包括需要改进的关键领域]

## 问题清单
[按严重程度排序的问题列表]

## 改进建议
[不属于具体问题但可以提升代码质量的建议]
```

## 2. 问题报告格式

每个发现的问题应使用以下格式报告：

```
### [问题ID]: [简短问题描述]

**严重程度**: [阻塞/严重/一般/建议]
**类型**: [功能/安全/性能/可维护性/风格/...]
**位置**: [文件名:行号] 或 [函数/方法名]
**描述**: [详细问题描述]
**原因**: [问题产生的原因或潜在影响]
**修复建议**: 
[具体的修复建议，最好包含代码示例]

```

## 3. 严重程度分类标准

- **阻塞 (Blocker)**: 必须修复才能合并的问题
  - 导致程序崩溃或无法运行
  - 严重的安全漏洞
  - 数据损坏或丢失风险
  - 违反核心业务规则

- **严重 (Critical)**: 应该在当前开发周期修复的问题
  - 影响主要功能但有临时解决方案
  - 中等安全风险
  - 严重性能问题
  - 可能导致未来维护困难的架构问题

- **一般 (Regular)**: 应该修复但优先级较低的问题
  - 次要功能问题
  - 代码质量问题
  - 轻微性能问题
  - 可改进的错误处理

- **建议 (Suggestion)**: 可选的改进点
  - 代码风格改进
  - 可读性增强
  - 小的重构建议
  - 文档完善

## 4. 问题类型分类

- **功能 (Functionality)**: 与代码功能实现相关的问题
- **安全 (Security)**: 与安全漏洞或安全最佳实践相关的问题
- **性能 (Performance)**: 与代码执行效率相关的问题
- **可维护性 (Maintainability)**: 与代码可读性、可扩展性相关的问题
- **风格 (Style)**: 与代码格式、命名约定相关的问题
- **测试 (Testing)**: 与测试覆盖或测试质量相关的问题
- **文档 (Documentation)**: 与代码注释或文档相关的问题
- **依赖 (Dependencies)**: 与外部依赖或库使用相关的问题
- **兼容性 (Compatibility)**: 与跨平台、向后兼容性相关的问题
- **错误处理 (Error Handling)**: 与异常处理或错误管理相关的问题

## 5. 反馈语言指南

- 使用专业但易于理解的语言
- 保持客观，关注代码而非开发者
- 提供具体而非模糊的反馈
- 解释"为什么"而不仅仅是"什么"
- 使用建设性而非批判性的语言
- 提供可行的解决方案
- 在适当情况下引用相关标准或最佳实践

## 6. 代码示例格式

提供修复建议时，使用以下格式：

```
**修复建议**:

```[语言]
// 原代码
function example() {
  // 有问题的代码
}
```

可以修改为:

```[语言]
// 修改后的代码
function example() {
  // 改进的代码
}
```

修改说明: [解释为什么这个修改解决了问题]
```

## 7. 具体用例示例

### 用例1: JavaScript 函数中的安全漏洞

```
### SEC-001: SQL注入漏洞

**严重程度**: 阻塞
**类型**: 安全
**位置**: database.js:42, executeQuery函数
**描述**: 函数直接将用户输入拼接到SQL查询中，没有进行参数化或转义，存在SQL注入风险。
**原因**: 直接字符串拼接创建SQL查询会允许攻击者注入恶意SQL代码，可能导致未授权数据访问、数据泄露或数据损坏。

**修复建议**:

```javascript
// 原代码
function executeQuery(userId) {
  const query = `SELECT * FROM users WHERE id = ${userId}`;
  return db.execute(query);
}
```

可以修改为:

```javascript
// 修改后的代码
function executeQuery(userId) {
  const query = `SELECT * FROM users WHERE id = ?`;
  return db.execute(query, [userId]);
}
```

修改说明: 使用参数化查询代替字符串拼接，防止SQL注入攻击。参数化查询会确保用户输入被视为数据而非代码执行。
```

### 用例2: Python 性能优化建议

```
### PERF-003: 低效的列表操作

**严重程度**: 一般
**类型**: 性能
**位置**: data_processor.py:78, process_items函数
**描述**: 在循环中频繁使用列表的append方法，然后将列表转换为字符串，这在处理大量数据时效率低下。
**原因**: 字符串连接操作在Python中是昂贵的，因为字符串是不可变的，每次连接都会创建新对象。对于大型列表，这会导致显著的性能下降。

**修复建议**:

```python
# 原代码
def process_items(items):
    result = []
    for item in items:
        processed = transform(item)
        result.append(processed)
    return ','.join(result)
```

可以修改为:

```python
# 修改后的代码
def process_items(items):
    return ','.join(transform(item) for item in items)
```

修改说明: 使用生成器表达式直接创建结果，避免了中间列表的创建和多次内存分配，提高了性能和内存效率。对于大型数据集，这种优化尤为重要。
```

### 用例3: Java 代码可维护性问题

```
### MAINT-007: 过长方法需要重构

**严重程度**: 严重
**类型**: 可维护性
**位置**: OrderProcessor.java:120, processOrder方法
**描述**: processOrder方法超过200行，包含多个责任和抽象级别，难以理解和维护。
**原因**: 过长的方法违反了单一责任原则，增加了认知负担，使代码难以测试、调试和修改。

**修复建议**:

将方法拆分为多个职责明确的小方法:

```java
// 原方法结构
public void processOrder(Order order) {
    // 验证订单 (30行)
    ...
    
    // 计算价格 (50行)
    ...
    
    // 应用折扣 (40行)
    ...
    
    // 处理支付 (45行)
    ...
    
    // 更新库存 (35行)
    ...
}
```

可以重构为:

```java
// 重构后的结构
public void processOrder(Order order) {
    validateOrder(order);
    calculatePrice(order);
    applyDiscounts(order);
    processPayment(order);
    updateInventory(order);
}

private void validateOrder(Order order) {
    // 验证逻辑
}

private void calculatePrice(Order order) {
    // 计算价格逻辑
}

private void applyDiscounts(Order order) {
    // 应用折扣逻辑
}

private void processPayment(Order order) {
    // 处理支付逻辑
}

private void updateInventory(Order order) {
    // 更新库存逻辑
}
```

修改说明: 将大方法分解为多个小方法，每个方法负责单一功能，提高了代码的可读性、可测试性和可维护性。这种方法还使每个功能更容易独立修改和扩展。
```

### 用例4: Go 错误处理改进

```
### ERR-002: 未处理的错误返回

**严重程度**: 严重
**类型**: 错误处理
**位置**: file_handler.go:56, ReadConfig函数
**描述**: 函数忽略了文件操作返回的错误，可能导致静默失败和难以诊断的问题。
**原因**: 在Go中，忽略错误返回会导致程序在出现问题时继续执行，可能导致数据不一致或程序崩溃。

**修复建议**:

```go
// 原代码
func ReadConfig(path string) Config {
    file, _ := os.Open(path)
    defer file.Close()
    
    var config Config
    decoder := json.NewDecoder(file)
    decoder.Decode(&config)
    
    return config
}
```

可以修改为:

```go
// 修改后的代码
func ReadConfig(path string) (Config, error) {
    var config Config
    
    file, err := os.Open(path)
    if err != nil {
        return config, fmt.Errorf("failed to open config file: %w", err)
    }
    defer file.Close()
    
    decoder := json.NewDecoder(file)
    if err := decoder.Decode(&config); err != nil {
        return config, fmt.Errorf("failed to decode config: %w", err)
    }
    
    return config, nil
}
```

修改说明: 修改后的代码正确处理并传播错误，使用错误包装提供更多上下文信息，并确保调用者能够适当地响应错误情况。
```

### 用例5: TypeScript 类型安全改进

```
### TYPE-004: 缺少类型定义

**严重程度**: 一般
**类型**: 可维护性
**位置**: user-service.ts:23, updateUserPreferences函数
**描述**: 函数参数和返回值缺少类型定义，降低了代码的类型安全性和自文档能力。
**原因**: 在TypeScript中，缺少类型定义会失去编译时类型检查的好处，增加运行时错误的风险，并使代码更难理解和维护。

**修复建议**:

```typescript
// 原代码
function updateUserPreferences(userId, preferences) {
  const user = getUser(userId);
  const updatedUser = {
    ...user,
    preferences: {
      ...user.preferences,
      ...preferences
    }
  };
  saveUser(updatedUser);
  return updatedUser;
}
```

可以修改为:

```typescript
// 修改后的代码
interface UserPreferences {
  theme: string;
  notifications: boolean;
  language: string;
}

interface User {
  id: string;
  name: string;
  email: string;
  preferences: UserPreferences;
}

function updateUserPreferences(userId: string, preferences: Partial<UserPreferences>): User {
  const user = getUser(userId);
  const updatedUser: User = {
    ...user,
    preferences: {
      ...user.preferences,
      ...preferences
    }
  };
  saveUser(updatedUser);
  return updatedUser;
}
```

修改说明: 添加了明确的接口定义和类型注解，提高了代码的类型安全性和自文档能力。使用`Partial<UserPreferences>`允许更新部分偏好设置，增加了灵活性的同时保持类型安全。
```

## 8. 总体评估示例

```
# 代码审核报告: user-authentication.js

## 总体评估

这个文件实现了用户认证功能，总体质量中等。代码结构清晰，功能完整，但存在几个安全问题和性能优化空间。主要关注点应该是修复身份验证中的安全漏洞和改进错误处理。

**需要改进的关键领域:**
- 密码处理安全性
- 错误处理和日志记录
- 输入验证
- 性能优化

共发现 12 个问题:
- 阻塞: 2个
- 严重: 3个
- 一般: 5个
- 建议: 2个
```

## 9. 改进建议示例

```
## 改进建议

1. **考虑添加缓存机制**: 对于频繁访问但很少变化的数据，如用户权限，可以实现缓存以提高性能。

2. **增加更多日志记录**: 在关键操作点添加结构化日志，将有助于问题诊断和性能监控。

3. **考虑使用依赖注入**: 当前的服务实例化方式使测试变得困难，考虑实现依赖注入以提高可测试性。

4. **添加API版本控制**: 随着API的发展，考虑实现版本控制机制以保持向后兼容性。

5. **性能基准测试**: 建议为关键功能添加性能基准测试，以便在未来的更改中监控性能影响。
```

## 10. 多文件审核报告格式

对于涉及多个文件的代码审核，使用以下格式：

```
# 多文件代码审核报告

## 总体项目评估
[项目整体质量评价，包括架构、设计模式、代码组织等]

## 文件概览
1. [文件名1] - [简短描述] - [问题数量]
2. [文件名2] - [简短描述] - [问题数量]
...

## 详细文件审核
### [文件名1]
[该文件的详细审核报告，按上述单文件格式]

### [文件名2]
[该文件的详细审核报告，按上述单文件格式]
...

## 跨文件问题
[涉及多个文件的问题，如架构问题、一致性问题等]

## 总体改进建议
[针对整个项目的改进建议]
```

## 11. 审核报告摘要格式

对于大型代码库，可以提供一个摘要报告：

```
# 代码审核摘要报告

## 统计概览
- 审核的文件数: [数量]
- 发现的问题总数: [数量]
- 按严重程度分布:
  - 阻塞: [数量] ([百分比])
  - 严重: [数量] ([百分比])
  - 一般: [数量] ([百分比])
  - 建议: [数量] ([百分比])
- 按类型分布:
  - 功能: [数量]
  - 安全: [数量]
  - 性能: [数量]
  ...

## 关键发现
[最重要的3-5个问题的简要描述]

## 主要改进领域
[需要重点关注的改进领域]

## 建议的后续步骤
[具体的行动建议，按优先级排序]
```
