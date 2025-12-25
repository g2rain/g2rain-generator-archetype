# 项目说明

本项目由 `g2rain-generator-archetype` 生成，内置多模块结构（`-api`、`-biz`、`-startup`）。建议按以下步骤快速定制并生成 CRUD 代码。

## 1. 前置要求
- Java 21+
- Maven 3.6+
- MySQL 8.0+（或其他 JDBC 数据库）

## 2. 引入代码生成插件

在父 `pom.xml` 中添加（已默认存在可忽略）：

```xml
<build>
  <plugins>
    <plugin>
      <groupId>com.g2rain</groupId>
      <artifactId>g2rain-generator-maven-plugin</artifactId>
      <version>1.0.1</version>
      <!-- 请使用最新的版本 -->
    </plugin>
  </plugins>
</build>
```

> 若希望使用简写命令 `mvn g2rain:generate`，请在 `~/.m2/settings.xml` 中配置 `pluginGroup` 为 `com.g2rain`。

## 3. 准备配置文件

在项目根目录创建 `codegen.properties`（或使用已有文件），示例：

```properties
# 数据库
database.url=jdbc:mysql://localhost:3306/your_db?useSSL=false&serverTimezone=UTC&allowPublicKeyRetrieval=true
database.driver=com.mysql.cj.jdbc.Driver
database.username=root
database.password=your_password

# 基础包名
project.basePackage=com.example.demo

# 需要生成的表（逗号分隔）
database.tables=user,order_info

# 是否覆盖已存在文件
tables.overwrite=false
```

更多可选项、模板与生成内容说明，参考插件文档：<https://github.com/g2rain/g2rain-generator-maven-plugin/blob/main/README.md>

## 4. 执行代码生成

在项目根目录运行（默认读取 `codegen.properties`）：

```bash
mvn com.g2rain:g2rain-generator-maven-plugin:1.0.1:generate
```

指定配置文件路径或表名：

```bash
mvn com.g2rain:g2rain-generator-maven-plugin:1.0.1:generate ^
  -Dconfig.file=./codegen.properties ^
  -Ddatabase.tables=user,order_info
```

> Windows PowerShell 可用反引号换行；Linux/macOS 用 `\`。

## 5. 模块与目录说明
- `${rootArtifactId}-api`：API/DTO/VO 等接口模型
- `${rootArtifactId}-biz`：Controller、Service、DAO、PO、Mapper XML 等
- `${rootArtifactId}-startup`：启动入口、配置文件

生成代码默认放在对应模块的 `src/main/java` 与 `src/main/resources/mybatis` 下。

## 6. 常见问题
- 找不到插件：执行 `mvn -U` 更新仓库，确保可访问 Maven Central。
- 不想覆盖已有文件：设置 `tables.overwrite=false`。
- 仅生成部分表：`-Ddatabase.tables=table1,table2`。

如需自定义模板或更多配置，请查看插件文档。***

