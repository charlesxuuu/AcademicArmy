这个skill属于一套基于Codex的autoresearch工具链，任务是根据`paper_blueprint`、`experiment plan`和`coding plan`初始化一个项目脚手架。
本skill处于模板 / 脚手架阶段，核心是先用模板工具、官方初始化方式或高质量template repository生成真实代码库骨架，再叠加论文实验目录和说明文件。
项目初始化skill的核心产物是一个由模板工具、官方初始化命令或高质量template repository生成的真实代码库脚手架，而不是一组README说明文件。
`README.md`、`README.zh-CN.md`、`REFERENCES.md`和`REFERENCES.zh-CN.md`只是脚手架的配套文档，不是主要产物。

本skill接收用户指定的初始代码仓库路径，并只在该路径下创建项目脚手架文件和文件夹。
所有创建的文件和文件夹都必须位于用户输入的代码仓库路径下；仓库内部引用使用相对于仓库根目录的路径。
如果目标仓库路径已经存在文件，skill应在保护用户已有内容的前提下做最小必要检查，根据任务要求在现有内容上生成或补齐脚手架，避免覆盖用户已有文件。
如果用户明确要求基于已有代码仓库初始化或改造，skill才读取目标仓库中与脚手架初始化有关的文件；否则应把指定路径视为新仓库或待初始化目录。

本skill只负责项目脚手架初始化，不实现论文方法、不实现实验流程、不写论文业务逻辑、不跑测试、不跑harness、不执行实验。
skill可以调用选定的模板工具、官方初始化命令或模板仓库来生成starter files、boilerplate structure、依赖声明、入口文件、最小样例和生态相关配置；这些属于项目脚手架的一部分。
skill应区分“模板自带基础代码”和“论文业务代码”：前者可以由模板生成并保留，后者应留给后续代码实现skill。
如果最终仓库只有README、REFERENCES、空目录和说明文件，没有模板生成出的基本代码库结构，应视为skill没有完成项目初始化任务。

skill应只读取生成脚手架所必需的输入，例如`paper_blueprint`、`experiment plan`、`coding plan`和用户指定的仓库路径。
skill应基于这些输入判断项目需要的目标语言、运行时、框架逻辑、实验形态、harness/test需求、输入数据、输出结果和后续实现方向。
这种判断只用于选择初始化方式、生成真实starter repo、叠加固定实验目录、编写README/REFERENCES和创建harness/test说明文件，不用于实现具体method、metric、data loader、result exporter、配置解析或实验runner。
skill不应主动探索当前目录下无关文件；如果需要外部知识，应通过deepresearch调研，而不是从目录噪声中猜上下文。
skill不应把Codex运行环境、沙盒限制、文件读取失败、shell命令受限、MCP调用失败、依赖安装失败等runtime workaround写进skill内容、README或REFERENCES。

skill应使用`academic_army_mcp_tools`中的deepresearch调研当前目标生态通常如何初始化项目。
deepresearch应重点搜索目标生态的官方初始化方式、高质量模板工具、template repository、starter project、boilerplate project、research code template、benchmark template、harness template和目标生态中的高质量公开repo。
skill应调研并比较可实际生成项目结构的工具或来源，例如通用模板生成器、目标生态官方initializer、社区高质量starter template、GitHub template repository或研究代码模板；具体采用哪个由现场调研决定，不写死在skill里。
Cookiecutter、Copier、Yeoman、GitHub template repositories等可以作为deepresearch的候选参考方向，因为它们都支持从模板或generator生成项目结构；但skill不应固定使用其中任何一个。

skill应优先寻找并调用能生成真实starter files或boilerplate structure的工具或来源，而不是只手工创建`README.md`、`REFERENCES.md`、`harness/`和`test/`。
如果目标生态存在官方或事实标准的初始化命令，skill应优先考虑该初始化方式。
如果官方初始化方式不适合论文实验仓库，skill再考虑通用模板生成器、高质量template repository、research code template、benchmark template或harness template。
skill应优先选择能直接生成基本代码库结构的工具或模板，选择标准包括目标生态惯例、维护状态、license清晰度、目录结构清晰度、配置成本、后续代码skill继续实现的便利性，以及与当前论文实验工作流的匹配度。

如果存在多个候选模板、initializer或template repository，skill应比较它们的生成结果，而不是只看简介。
比较维度包括目录结构、依赖声明、入口文件、测试结构、配置复杂度、文档质量、license、维护状态和与论文实验工作流的匹配度。
skill应避免从质量较差、过度复杂、长期不维护、license不明确或与当前任务无关的公开repo中学习脚手架结构。
选定模板或初始化方式后，skill应实际调用该模板工具、官方初始化命令或模板仓库，在用户指定repo路径下生成基本代码库结构。

使用模板生成后，skill应在生成出的代码库基础上叠加论文实验固定目录和说明文件，而不是用手写目录完全替代模板生成结果。
模板负责目标生态的标准代码库骨架，固定目录负责论文实验工作流。
模板生成出的源码目录、依赖声明、构建配置、测试配置、入口结构和生态相关文件应由模板工具和deepresearch结果决定，不应在skill里写死。
skill应把生成出的模板结构与固定实验目录合并：模板结构保留目标生态的starter repo语义，固定实验目录保留论文实验工作流语义。
如果模板已经生成了某些与固定目录语义相近的目录，skill应保留固定顶层约定，并在README中简要说明两者关系，避免目录语义混乱。

固定实验目录仍应存在：`data/`、`output/`、`results/`、`harness/`、`test/`。
`data/`用于输入数据，`output/`用于程序运行输出，`results/`用于实验结果记录，`harness/`用于所有harness，`test/`用于所有功能测试。
固定文档仍应存在：`README.md`、`README.zh-CN.md`、`REFERENCES.md`、`REFERENCES.zh-CN.md`。
固定目录只规定论文实验工作流的顶层语义，不规定目标语言生态内部的源码布局。

`harness/`下面应根据`coding plan`中的每种harness创建独立子文件夹，并在每个子文件夹中放置说明文件。
`test/`下面应根据`coding plan`中的每种test创建独立子文件夹，并在每个子文件夹中放置说明文件。
每种harness和test的子文件夹名称应语义化，能表达其服务的任务，不应使用`c1/c2/c3/b1/b2/b3`这类抽象编号。
每个harness说明文件应写清楚该harness的任务、关联实验目标、后续应实现的运行入口、输入、metric、输出artifact和实现占位。
每个test说明文件应写清楚该test类别验证什么功能、后续应覆盖哪些输入输出、pass/fail含义和实现占位。
harness/test说明文件只描述任务和预留结构，不实现具体harness逻辑或测试逻辑。

`README.md`和`README.zh-CN.md`应说明这是一个由模板工具、官方初始化方式或模板仓库初始化出的项目脚手架，并说明固定实验目录、harness/test预留结构和后续实现方向。
`README.md`使用英文，`README.zh-CN.md`使用中文。
README应简要说明项目用途、上游输入、最终采用的初始化方式、模板生成出的基础代码库结构、固定实验目录含义、harness/test预留位置和后续实现方向。
README不应替代模板生成；如果最终仓库只有文档和空目录，没有模板生成出的基本代码库结构，应视为skill没有完成项目初始化任务。
README不应声称具体论文方法、实验流程或功能代码已经实现。

`REFERENCES.md`和`REFERENCES.zh-CN.md`应记录deepresearch调研过的模板工具、模板仓库、开源项目和最终选用的生成方式。
`REFERENCES.md`使用英文，`REFERENCES.zh-CN.md`使用中文。
`REFERENCES.md`应明确记录最终采用的模板来源、生成工具、license、版本或commit、生成方式、保留了哪些模板内容、删除或调整了哪些内容、为什么选择它。
如果调研了但没有采用某个候选模板，`REFERENCES.md`可以简要说明未采用原因，例如结构过重、维护不足、license不合适、与实验工作流不匹配或配置成本过高。
如果模板自带文件被保留或改写，`REFERENCES.md`应说明这些文件来自哪个模板以及做了哪些脚手架层面的调整。
`REFERENCES.zh-CN.md`不需要逐字翻译英文版，但应覆盖同样信息，使用户理解外部模板和开源项目如何影响当前脚手架。

模板阶段不复制具体业务逻辑代码。
如果deepresearch发现有价值的开源实现，应在`REFERENCES.md`和`REFERENCES.zh-CN.md`中记录为后续实现参考，而不是在本阶段移植代码。
如果模板本身自带starter code、boilerplate code或最小入口文件，可以保留这些模板生成内容；这些属于代码库脚手架的一部分，不等同于实现论文业务逻辑。
GitHub关于Codespaces模板的文档也说明template repositories通常包含starter files和boilerplate code，帮助用户快速开始使用某个库、框架或技术；因此模板阶段可以保留模板自带的基础starter files，但不应生成论文方法实现。
对license不明确或不兼容的项目，只能作为阅读参考，不应把其代码或模板文件复制进仓库。

skill只做脚手架静态检查。
静态检查应确认模板生成确实发生过，最终repo中存在目标生态合理的基础代码库结构，而不只是手写README和空文件夹。
静态检查应确认所有创建路径都位于目标仓库路径内。
静态检查应确认模板生成出的源码目录、依赖声明、构建配置、测试配置、入口结构或生态相关文件没有被固定实验目录覆盖或破坏。
静态检查应确认固定实验目录和文档已叠加到模板结构中：`data/`、`output/`、`results/`、`harness/`、`test/`、`README.md`、`README.zh-CN.md`、`REFERENCES.md`、`REFERENCES.zh-CN.md`。
静态检查应确认每种harness和test都有独立子文件夹和说明文件。
静态检查应确认`README.md`、`README.zh-CN.md`、`REFERENCES.md`、`REFERENCES.zh-CN.md`描述的模板来源、生成方式和实际目录结构一致。
静态检查应确认仓库文档只描述脚手架、模板来源和后续实现方向，没有把placeholder写成已完成实现。
静态检查不运行代码、不安装依赖、不执行测试、不运行harness、不执行实验。

推荐的skill流程是：读取`paper_blueprint`、`experiment plan`、`coding plan`和目标repo路径，只提取项目初始化所需的信息；用deepresearch判断目标语言、运行时和框架逻辑；用deepresearch搜索该目标生态的官方初始化方式、高质量模板工具和template repositories；比较候选模板或初始化方式，选择一个最适合当前论文实验仓库的生成方案；在目标repo路径下调用选定方案生成基本代码库结构；在生成出的结构上叠加固定实验目录；根据`coding plan`为每种harness和test创建独立子文件夹及说明文件；创建`README.md`、`README.zh-CN.md`、`REFERENCES.md`、`REFERENCES.zh-CN.md`；做脚手架静态检查，确认“模板生成的基本代码库结构 + 论文实验固定目录 + references文档 + harness/test说明”都存在且一致。

skill应使用自然、可读的文档写法，不依赖复杂编号系统。
README、REFERENCES和harness/test说明文件应优先使用目录名、harness名、test名、artifact名或自然简称，不使用抽象编号互相引用。
说明文件应清楚表达“这是预留结构”和“后续实现应在这里补充什么”，避免写成已经完成的功能文档。
最终输出应聚焦实际采用了什么模板生成方式、生成了哪些starter repo结构、叠加了哪些论文实验目录、哪些harness/test位置已预留，以及后续实现skill应从哪里继续。

**Scaffold generation requirement**：本skill必须通过deepresearch找到适合当前目标生态的项目初始化方式，并实际生成基本代码库脚手架；只创建README、REFERENCES、空目录和说明文件不算完成任务。
**Template-first原则**：项目初始化先通过模板工具、官方initializer或高质量template repository生成真实starter repo，再叠加论文实验目录和说明文件。
**Scaffold-only原则**：本skill只负责创建项目脚手架；具体论文业务代码、实验流程实现、harness逻辑、测试逻辑、代码风格配置和质量审查留给后续skill。
**Template-informed原则**：项目结构应由deepresearch调研到的官方初始化方式、高质量模板工具、template repository和公开repo共同决定，不在tips里写死具体语言、框架或源码布局。
**Experiment scaffold原则**：固定保留`data/`、`output/`、`results/`、`harness/`和`test/`，让脚手架天然承接论文实验工作流；模板生成结构负责目标生态的标准代码库骨架。
**Reference documentation原则**：`REFERENCES.md`和`REFERENCES.zh-CN.md`负责记录模板来源、生成工具、license、版本、采用方式、保留内容、调整内容和选择理由；模板阶段发现的外部代码实现只记录为后续参考，不在本阶段移植。
**Repo scaffold总原则**：这个skill负责把论文蓝图、experiment plan和coding plan转化为一个真实starter repo加论文实验目录的项目脚手架；它通过deepresearch现场选择并调用初始化方式生成基础代码库结构，再叠加固定实验目录、README、REFERENCES和harness/test说明文件，让后续具体实现skill在真实脚手架上继续推进。
