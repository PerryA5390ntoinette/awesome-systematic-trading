<div align="center">
  <img src="static/images/awesome-systematic-trading.jpeg" height=200 alt=""/>
  <h1>令人敬畏的系统化交易</h1>
</div>
<div align=center><img src="https://awesome.re/badge.svg" /></div>

我们正在收集一份关于寻找、开发和运行系统性交易（量化交易）策略的资源论文、软件、书籍、文章清单。

<!-- omit in toc -->
### 你在这里会发现什么？

- [97个](#库和包)用于研究和实际交易的[库和包](#库和包)
- 机构和学术界描述的[40+项战略](#战略)
- [55本](#书籍)适合初学者和专业人士的[书籍](#书籍)
- [23个视频](#视频)和采访
- 还有一些[博客](#博客)和[课程](#课程)

> **个人备注：** 本文档为个人学习用途的中文翻译版本，主要关注股票和加密货币策略部分。如有翻译错误欢迎指正。

<details>
<summary>点击这里查看完整的内容表</summary>

- [库和包](#库和包)
  - [回溯测试和真实交易](#回溯测试和真实交易)
    - [一般 - 事件驱动框架](#一般---事件驱动框架)
    - [一般 - 基于矢量的框架](#一般---基于矢量的框架)
    - [加密货币](#加密货币)
  - [交易机器人](#交易机器人)
  - [分析](#分析)
    - [指标](#指标)
    - [度量衡计算](#度量衡计算)
    - [优化](#优化)
    - [定价](#定价)
    - [风险](#风险)
  - [经纪人API](#经纪人api)
  - [数据来源](#数据来源)
    - [一般](#一般)
    - [加密货币](#加密货币-1)
  - [数据科学](#数据科学)
  - [数据库](#数据库)
  - [图形计算](#图形计算)
  - [机器学习](#机器学习)
  - [时间序列分析](#时间序列分析)
  - [视觉化](#视觉化)
- [战略](#战略)
  - [债券、商品、货币、股票](#债券商品货币股票)
  - [债券、商品、股票、REITs](#债券商品股票reits)
  - [债券、股票](#债券股票)
  - [债券、股票、REITs](#债券股票reits)
  - [商品](#商品)
  - [加密货币](#加密货币-2)
  - [货币](#货币)
  - [股票](#股票)
- [书籍](#书籍)
  - [初学者](#初学者)
  - [传记](#传记)
  - [编码](#编码)
  - [隐蔽性](#隐蔽性)
  - [一般](#一般-1)
  - [高频交易](#高频交易)
  - [机器学习](#机器学习-1)
- [视频](#视频)
- [博客](#博客)
- [课程](#课程)
</details>

<!-- omit in toc -->
> ### 我怎样才能提供帮助？
> 你可以通过提交带有建议的问题和在Twitter上分享来帮助。
>
> [![Tweet](https://img.shields.io/twitter/url/http/shields.io.svg?style=social)](https://twitter.com/intent/tweet?text=A%20free%20and%20comprehensive%20list%20of%20papers%2C%20libraries%2C%20books%2C%20blogs%2C%20tutorials%20for%20quantitative%20traders.&url=https://github.com/paperswithbacktest/awesome-systematic-trading)


# 库和包

*97个实现交易机器人、回溯测试器、指标、定价器等的库和包列表。每个库都按其编程语言分类，并按人口降序排列（星星的数量）。*


## 回溯测试和真实交易

### 一般 - 事件驱动框架


| 存储库 | 描述 | 明星 | 使用方法 |
|------------|-------------|-------|-----------|
| [vnpy](https://github.com/vnpy/vnpy) | 基于Python的开源量化交易系统开发框架，于2015年1月正式发布，已经一步步成长为一个全功能的量化交易平台。 | ![GitHub stars](https://badgen.net/github/stars/vnpy/vnpy) | ![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg) |
| [zipline](https://github.com/quantopian/zipline) | Zipline是一个Pythonic算法交易库。它是一个事件驱动的系统，用于回溯测试。 | ![GitHub stars](https://badgen.net/github/stars/quantopian/zipline) | ![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg) |
| [backtrader](https://github.com/mementum/backtrader) | 事件驱动的Python交易策略回测库 | ![GitHub stars](https://badgen.net/github/stars/mementum/backtrader) | ![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg) |
| [QUANTAXIS](https://github.com/QUANTAXIS/QUANTAXIS) | QUANTAXIS 支持任务调度 分布式部署的 股票/期货/期权/港股/虚拟货币 数据/回测/模拟/交易/可视化/多账户 纯本地量化解决方案 | ![GitHub stars](https://badgen.net/github/stars/QUANTAXIS/QUANTAXIS) | ![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg) |
| [QuantConnect](https://github.com/QuantConnect/Lean) | QuantConnect的精益算法交易引擎（Python，C#）。 | ![GitHub stars](https://badgen.net/github/stars/QuantConn