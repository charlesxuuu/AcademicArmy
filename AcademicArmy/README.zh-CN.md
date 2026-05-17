# AcademicArmy 结构

`AcademicArmy` 按论文生产流程组织为多个岗位和团队。每个文件夹代表一个参与者，负责把论文蓝图转化为完整的研究论文。

顶层角色：

- `ProductManager` 接收初始研究想法，并在正式流程开始前帮助将其收敛为符合规范的论文蓝图。
- `Author` 根据论文蓝图、实验证据、图表和评审反馈撰写并修改论文文本。
- `Coding` 是 Coding Team，负责将论文蓝图转化为代码蓝图、功能实现、测试、代码审查和性能优化。
- `Illustrator` 为方法、流程、系统和概念绘制说明性示意图。
- `Plotter` 根据实验指标、日志和统计结果绘制实验结果图。
- `Reviewer` 评价论文质量，并向 Author 提供可执行的修改反馈。

Coding Team 岗位：

- `Coding/Architect` 生成或修改代码蓝图。
- `Coding/Developer` 实现功能模块和测试脚本。
- `Coding/CodeReviewer` 审查 Developer 的代码，并反馈代码质量、可维护性和可读性问题。
- `Coding/PerformanceEngineer` 运行测试并针对指定指标优化代码。每个测试项由一个单独的 Performance Engineer 负责。
