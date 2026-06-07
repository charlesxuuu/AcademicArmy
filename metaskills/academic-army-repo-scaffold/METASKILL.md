这个skill属于一套基于Codex的autoresearch工具链，任务是根据`paper_blueprint`、`experiment plan`和`coding plan`初始化一个项目脚手架。
本skill处于模板 / 脚手架阶段，核心是scaffold the repository，而不是implement the framework。
本skill接收用户指定的初始代码仓库路径，并只在该路径下创建项目脚手架文件和文件夹。
本skill只负责模板化初始化，不写具体业务逻辑代码、不实现论文方法、不实现实验流程、不运行代码、不跑测试、不跑harness、不执行实验。

所有创建的文件和文件夹都必须位于用户输入的代码仓库路径下；仓库内部引用使用相对于仓库根目录的路径。
如果目标仓库路径已经存在文件，skill应在保护用户已有内容的前提下做最小必要检查，根据任务要求创建缺失脚手架、补充说明文件、调整模板化结构或避免覆盖已有内容。
如果用户明确要求基于已有代码仓库初始化或改造，skill才读取目标仓库中与脚手架初始化有关的文件；否则应把指定路径视为新仓库或待初始化目录。

skill应基于`paper_blueprint`、`experiment plan`和`coding plan`理解项目需要支持的实验类型、harness类型、test类型、输入数据、输出结果和后续实现方向。
这种理解只用于决定脚手架目录、模板来源、README说明、REFERENCES记录和harness/test预留结构，不用于实现具体模块、method、metric、result exporter、配置解析或实验流程。
模板阶段可以为后续实现留下清晰位置和说明，但不生成看起来像已经完成的业务逻辑代码。

skill应只读取生成脚手架所必需的输入，例如`paper_blueprint`、`experiment plan`、`coding plan`和用户指定的仓库路径。
skill不应主动探索当前目录下无关文件；如果需要外部知识，应通过deepresearch调研，而不是从目录噪声中猜上下文。
skill不应把Codex运行环境、沙盒限制、文件读取失败、shell命令受限、MCP调用失败、依赖安装失败等runtime workaround写进skill。
skill文档和输出不应混入工具失败、沙盒限制、如何绕过权限、如何读取文件等与脚手架设计无关的内容。

skill应使用`academic_army_mcp_tools`中的deepresearch调研相关开源项目、模板工具、模板仓库和脚手架生成方式。
deepresearch调研对象可以包括项目模板工具、GitHub template repositories、研究代码模板、benchmark仓库模板、harness模板、实验项目模板和目标生态中的高质量公开repo。
Cookiecutter、Copier、GitHub template repositories、Yeoman等只能作为deepresearch的候选参考方向，因为它们分别代表从project templates创建项目、从template生成项目、从已有repo生成相同目录结构和文件以及scaffolding tool等方向。
这些工具适合作为现场调研seed，不应在skill里固定使用其中任何一个。

skill应根据用户输入和deepresearch结果选择合适的语言、运行时、模板工具和模板仓库，但tips本身不应写死任何具体语言、框架、包管理器、测试框架、配置文件名或源码目录布局。
如果用户已经明确指定语言、框架或模板偏好，skill应优先遵守用户指定内容，并围绕该选择调研脚手架最佳实践。
如果用户没有指定语言或框架，skill应根据论文实验需求、可用模板质量、相关开源项目成熟度、harness/test组织便利性和后续实现成本选择。
skill应优先选择维护良好、结构清晰、license明确、社区使用较多、与当前论文实验系统接近的模板或模板工具。
skill应避免从质量较差、过度复杂、长期不维护或与当前任务无关的公开repo中学习脚手架结构。

skill应把模板生成结果裁剪成当前项目需要的脚手架，而不是原样保留模板中的所有无关内容。
模板工具和模板仓库只提供项目起点；最终脚手架应服务当前`paper_blueprint`、`experiment plan`和`coding plan`中描述的实验工作流。
模板阶段可以保留模板自带的基础项目文件、依赖声明、构建配置、测试配置、脚本入口或辅助文件，但只在它们对当前脚手架有必要且license明确时保留。
模板阶段不生成具体功能代码，不把业务逻辑、算法实现、metric实现、data loader实现、result exporter实现或实验runner写进仓库。

项目脚手架采用“固定实验目录 + 动态生态结构”的混合布局。
固定顶层目录和文档包括：`data/`、`output/`、`results/`、`harness/`、`test/`、`README.md`、`README.zh-CN.md`、`REFERENCES.md`、`REFERENCES.zh-CN.md`。
`data/`用于输入数据，`output/`用于程序运行输出，`results/`用于实验结果记录，`harness/`用于所有harness，`test/`用于所有功能测试。
固定目录只规定论文实验工作流的顶层语义，不规定目标语言生态内部的源码布局。
源码目录、依赖声明、构建配置、测试配置、脚本入口和模板自带辅助文件由deepresearch和模板选型现场决定。

`harness/`下面应为每一种harness单独设置一个子文件夹。
`test/`下面应为每一种test单独设置一个子文件夹。
每种harness和test的子文件夹名称应语义化，能表达其服务的任务，不应使用`c1/c2/c3/b1/b2/b3`这类抽象编号。
每个harness子文件夹中应放置一个说明文件，明确该harness的任务、关联实验目标、后续应实现的运行入口、输入、metric、输出artifact和实现占位。
每个test子文件夹中应放置一个说明文件，明确该test类别验证什么功能、后续应覆盖哪些输入输出、pass/fail含义和实现占位。
harness说明文件只描述任务和预留结构，不实现harness逻辑。
test说明文件只描述测试目标和预留结构，不实现测试逻辑。

仓库应包含`README.md`和`README.zh-CN.md`。
`README.md`使用英文，`README.zh-CN.md`使用中文。
`README.md`应简要说明项目用途、上游输入、固定目录含义、模板选型、当前脚手架结构、harness/test预留位置和后续实现方向。
`README.zh-CN.md`应覆盖同样信息，用自然中文说明项目用法和目录含义，必要时保留英文目录名、harness名、test名、method名、metric和artifact名称。
README应描述当前实际生成出来的脚手架，不应描述通用模板，也不应声称具体论文方法、实验流程或功能代码已经实现。

仓库应包含`REFERENCES.md`和`REFERENCES.zh-CN.md`。
`REFERENCES.md`使用英文，`REFERENCES.zh-CN.md`使用中文。
`REFERENCES.md`应汇总deepresearch参考过的模板工具、模板仓库、开源项目、论文代码、benchmark仓库或harness项目。
`REFERENCES.md`应说明每个参考来源的用途，例如模板来源、结构参考、harness组织参考、test组织参考、依赖候选或后续实现参考。
`REFERENCES.md`应记录每个外部来源的项目名、链接、license、版本或commit、参考内容和选择理由。
如果脚手架由某个模板工具或模板仓库生成，`REFERENCES.md`应明确记录该模板来源和license。
如果模板自带文件被保留或改写，`REFERENCES.md`应说明这些文件来自哪个模板以及做了哪些脚手架层面的调整。
`REFERENCES.zh-CN.md`不需要逐字翻译英文版，但应覆盖同样信息，使用户理解外部模板和开源项目如何影响当前脚手架。

模板阶段不复制具体业务逻辑代码。
如果deepresearch发现有价值的外部实现，应在`REFERENCES.md`和`REFERENCES.zh-CN.md`中记录为后续实现参考，而不是在本阶段移植代码。
对license不明确或不兼容的项目，只能作为阅读参考，不应把其代码或模板文件复制进仓库。
如果模板自带文件的license不明确或不兼容，skill应选择其他模板、只记录为参考，或创建不含受限内容的等价脚手架说明文件。
模板阶段可以记录未来可能直接依赖的库或工具候选，但不需要安装依赖、验证导入或接入具体调用代码。

skill只做脚手架静态检查。
静态检查应确认所有创建路径都位于目标仓库路径内。
静态检查应确认固定顶层目录和文档存在：`data/`、`output/`、`results/`、`harness/`、`test/`、`README.md`、`README.zh-CN.md`、`REFERENCES.md`、`REFERENCES.zh-CN.md`。
静态检查应确认每种harness和test都有独立子文件夹和说明文件。
静态检查应确认README和REFERENCES描述的目录、模板来源、harness/test预留结构与实际仓库一致。
静态检查应确认仓库文档只描述脚手架、模板来源和后续实现方向，没有把placeholder写成已完成实现。
静态检查不包括代码风格检查、lint、format、type check、测试运行、harness运行、依赖安装或实验执行。

skill应使用自然、可读的文档写法，不依赖复杂编号系统。
README、REFERENCES和harness/test说明文件应优先使用目录名、harness名、test名、artifact名或自然简称，不使用抽象编号互相引用。
说明文件应清楚表达“这是预留结构”和“后续实现应在这里补充什么”，避免写成已经完成的功能文档。
最终输出应聚焦创建了哪些脚手架能力、哪些模板来源被采用、哪些harness/test位置已预留，以及后续实现skill应从哪里继续。

**Scaffold-only原则**：本skill只负责创建项目脚手架，生成固定实验目录、模板化项目结构、README、REFERENCES以及harness/test说明文件；具体代码、框架实现、代码风格配置和质量审查留给后续skill。
**Template-informed原则**：项目结构应由deepresearch调研到的高质量模板工具、模板仓库和公开repo共同决定，不在tips里写死具体语言、框架或源码布局。
**Experiment scaffold原则**：固定保留`data/`、`output/`、`results/`、`harness/`和`test/`，让脚手架天然承接论文实验工作流；具体实现文件和源码结构由后续实现阶段继续完善。
**Reference documentation原则**：`REFERENCES.md`和`REFERENCES.zh-CN.md`负责记录模板来源、开源参考、license、采用方式和选择理由；模板阶段发现的外部代码实现只记录为后续参考，不在本阶段移植。
**Repo scaffold总原则**：这个skill负责把论文蓝图、experiment plan和coding plan转化为一个项目脚手架；它通过deepresearch现场选择模板工具、模板仓库、语言生态和公开参考，通过固定实验目录承接论文实验工作流，通过README、REFERENCES和harness/test说明文件完成交接，让后续具体实现skill在清晰脚手架上继续推进。
