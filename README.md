# G2Rain Generator Archetype

这是一个基于Spring Boot的多模块Maven Archetype项目模板，使用mvn archetype:create-from-project可以创建g2rain-generator-archetype，用于快速生成标准化的企业级Java应用项目结构。

## 项目结构

```
g2rain-generator-archetype/
├── g2rain-generator-archetype-api/          # API接口模块
├── g2rain-generator-archetype-biz/          # 业务逻辑模块  
├── g2rain-generator-archetype-startup/      # 启动模块
├── codegen.properties           # 代码生成配置文件
└── pom.xml                     # 父POM文件
```

## 模块说明

### g2rain-generator-archetype-api
- **作用**: 定义API接口和数据传输对象(DTO)
- **依赖**: Spring Boot Web Starter
- **说明**: 包含Controller接口定义、请求响应对象等

### g2rain-generator-archetype-biz  
- **作用**: 核心业务逻辑实现
- **依赖**: g2rain-generator-archetype-api模块、Spring Boot Web Starter
- **说明**: 包含Service层、Repository层等业务逻辑

### g2rain-generator-archetype-startup
- **作用**: 应用启动入口
- **依赖**: g2rain-generator-archetype-biz模块、Spring Boot相关依赖
- **说明**: 包含Application启动类、配置文件等

## 技术栈

- **Java**: 21
- **Spring Boot**: 3.5.7
- **Maven**: 3.x
- **数据库**: MySQL 8.0+
- **代码生成**: G2Rain Generator Maven Plugin

## 快速开始

### 1. 编译脚手架g2rain-generator-archetype

#### 1.1 清理已生成的文件
```bash
mvn clean
```

#### 1.2 生成archetype配置文件
```bash
mvn archetype:create-from-project
```

#### 1.3 修改archetype模板配置

**1.3.1 删除maven-archetype-plugin配置**
编辑文件：`target/generated-sources/archetype/src/main/resources/archetype-resources/pom.xml`

删除maven-archetype-plugin的plugin配置标签（通常在`<build><plugins>`部分），避免在生成的项目中包含archetype插件配置。

> **自动化排除**：IDE相关文件已通过`archetype.properties`文件自动排除，无需手动修改配置文件。

**排除规则配置**：
- **archetype.properties文件**：定义了排除模式
- **POM插件配置**：引用属性文件进行过滤

```properties
# archetype.properties
# Maven Archetype
excludePatterns=.idea/*,.vscode/*,*.iml,.settings/*,.project,.classpath,.factorypath,target/*,README.md,.flattened-pom.xml
```

```xml
<!-- pom.xml中的插件配置 -->
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-archetype-plugin</artifactId>
    <configuration>
        <propertyFile>archetype.properties</propertyFile>
    </configuration>
</plugin>
```

#### 1.4 发布脚手架配置
```bash
# 进入archetype目录
cd target/generated-sources/archetype

# 安装archetype到本地Maven仓库
mvn install
```

> **注意**：完成以上步骤后，archetype就安装到了本地Maven仓库中，可以通过`mvn archetype:generate`命令使用。

### 2. 使用Archetype生成新项目

> **重要**：请在**父目录**下执行此命令，Maven会自动创建新的项目目录。

#### 方法1：非交互模式（推荐）
```bash
# 在父目录下执行（例如：D:\java\g2rain\）
mvn archetype:generate \
  -DarchetypeGroupId=com.g2rain \
  -DarchetypeArtifactId=g2rain-generator-archetype \
  -DarchetypeVersion=1.0.0 \
  -DgroupId=com.yourcompany \
  -DartifactId=your-project-name \
  -Dversion=1.0.0 \
  -Dpackage=com.yourcompany.yourproject \
  -DinteractiveMode=false
```

#### 方法2：交互模式
```bash
# 在父目录下执行
mvn archetype:generate \
  -DarchetypeGroupId=com.g2rain \
  -DarchetypeArtifactId=g2rain-generator-archetype \
  -DarchetypeVersion=1.0.0
```
然后按提示输入项目信息。

#### 方法3：在 IDE 中使用（IntelliJ IDEA / Eclipse）

**IntelliJ IDEA：**

1. **更新 Maven 本地缓存**（首次使用前必须执行）：
   ```bash
   mvn archetype:crawl
   ```
   或者在 IDEA 的 Terminal 中执行：
   ```bash
   mvn archetype:generate -DarchetypeCatalog=remote
   ```

2. **刷新 Maven 索引**：
   - 打开 `File` > `Settings` > `Build, Execution, Deployment` > `Maven` > `Repositories`
   - 选择 `central` 仓库，点击 `Update` 按钮
   - 或者在 `File` > `Settings` > `Build, Execution, Deployment` > `Build Tools` > `Maven` > `Importing` 中勾选 `Automatically download: Sources and Documentation`

3. **创建新项目**：
   - `File` > `New` > `Project`
   - 选择 `Maven` > `Create from archetype`
   - 点击 `Add Archetype...` 按钮
   - 输入以下信息：
     - **GroupId**: `com.g2rain`
     - **ArtifactId**: `g2rain-generator-archetype`
     - **Version**: `1.0.0`
   - 点击 `OK`，然后选择刚添加的 archetype
   - 点击 `Next`，输入项目信息（GroupId、ArtifactId、Version、Package 等）
   - 点击 `Finish`

4. **如果仍然找不到 archetype**：
   - 在创建项目时，选择 `Maven` > `Create from archetype`，然后点击 `Add Archetype...`
   - 手动输入坐标信息（如上所示）
   - 或者使用命令行方式（方法1或方法2）

**Eclipse：**

1. **更新 Maven 本地缓存**（首次使用前必须执行）：
   ```bash
   mvn archetype:crawl
   ```

2. **创建新项目**：
   - `File` > `New` > `Project...`
   - 选择 `Maven` > `Maven Project`
   - 点击 `Next`
   - 选择 `Create a simple project (skip archetype selection)` 的复选框**不要勾选**
   - 在 archetype 列表中找到 `com.g2rain:g2rain-generator-archetype:1.0.0`
   - 如果找不到，点击 `Add Archetype...` 按钮，手动添加：
     - **GroupId**: `com.g2rain`
     - **ArtifactId**: `g2rain-generator-archetype`
     - **Version**: `1.0.0`
   - 点击 `Next`，输入项目信息
   - 点击 `Finish`

**常见问题：**

- **Q: 在 IDE 中找不到 archetype？**
  - A: 执行 `mvn archetype:crawl` 更新本地缓存，然后重启 IDE 并刷新 Maven 项目。

- **Q: 提示无法下载 archetype？**
  - A: 检查网络连接和 Maven 设置，确保可以访问 Maven Central。可以尝试使用命令行方式（方法1或方法2）。

- **Q: 生成的项目结构不正确？**
  - A: 确保使用最新版本（1.0.0），并检查 Maven 版本是否 >= 3.6.0。

### 3. 配置数据库与代码生成

编辑根目录的 `codegen.properties`（示例与实际文件保持一致）：

```properties
# 数据库连接配置
database.url=jdbc:mysql://localhost:3306/my_database?useSSL=false&serverTimezone=UTC&allowPublicKeyRetrieval=true
database.driver=com.mysql.cj.jdbc.Driver
database.username=root
database.password=root123456

# 生成基础包名
project.basePackage=com.g2rain.example

# 需要生成的表（逗号分隔）
database.tables=test

# 是否允许覆盖已有文件
tables.overwrite=false
```

### 4. 运行项目

```bash
cd your-project-name
mvn clean compile
mvn spring-boot:run -pl your-project-name-startup
```

## 代码生成

项目集成了G2Rain代码生成插件，可以根据数据库表自动生成CRUD代码：

```bash
# 生成代码
mvn g2rain:generate
```

生成的文件包括：
- Entity实体类
- Repository接口
- Service接口和实现
- Controller类
- DTO对象

## 开发指南

### 添加新模块

1. 在父POM中添加新模块：
```xml
<modules>
    <module>your-project-api</module>
    <module>your-project-biz</module>
    <module>your-project-startup</module>
    <module>your-project-new-module</module> <!-- 新增模块 -->
</modules>
```

2. 创建对应的目录结构和POM文件

### 配置管理

- **应用配置**: 在`startup`模块的`src/main/resources`目录下
- **代码生成配置**: 修改根目录的`codegen.properties`文件
- **Maven配置**: 在父POM中统一管理依赖版本

### 最佳实践

1. **模块依赖**: 遵循`startup -> biz -> api`的依赖方向
2. **包命名**: 使用`${package}.模块名`的命名规范
3. **版本管理**: 使用`${revision}`属性进行版本统一管理
4. **代码生成**: 定期使用代码生成插件保持代码同步

## 故障排除

### 常见问题

1. **依赖解析失败**
   - 检查Maven仓库配置
   - 确认`g2rain-common`依赖是否可用

2. **代码生成失败**
   - 检查数据库连接配置
   - 确认表名是否正确
   - 查看Maven日志获取详细错误信息

3. **启动失败**
   - 检查数据库连接
   - 确认端口是否被占用
   - 查看应用日志

### 日志查看

```bash
# 查看应用日志
tail -f logs/application.log

# 查看Maven构建日志
mvn clean compile -X
```

## 版本历史

- **1.0.0**: 初始版本，支持多模块Spring Boot项目生成

## 贡献指南

1. Fork项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 许可证

本项目基于 [Apache 2.0许可证](LICENSE) 开源。

## 联系方式

如有问题或建议，请通过以下方式联系：

- **Issues**: [GitHub Issues](https://github.com/g2rain/g2rain/issues)
- **讨论**: [GitHub Discussions](https://github.com/g2rain/g2rain/discussions)
- **邮箱**: g2rain_developer@163.com

---

**注意**: 使用前请确保已安装Java 21和Maven 3.x环境。