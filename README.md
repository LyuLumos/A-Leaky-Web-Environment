# ![DIagonAlley-Logo](DiagonAlley/img/logo.png) DiagonAlley


## **Guidance**

- [Wiki（点我ヾ(≧▽≦*)o）](https://github.com/LyuLumos/A-Leaky-Web-Environment/wiki/DiagonAlley-(%E2%88%A9%EF%BD%80-%C2%B4)%E2%8A%83%E2%94%81%E2%98%86%EF%BE%9F.*%EF%BD%A5%EF%BD%A1%EF%BE%9F)
- [讨论区](https://github.com/LyuLumos/A-Leaky-Web-Environment/discussions)
- [创新实践能力团队赛评分标准](https://c4pr1c3.github.io/cuc-wiki/cp/assessment.html)

## **Structure**

```bash
.(main)
├── BreakIt
│   ├── EXP/              # exp代码和所需环境
│   ├── Others.md         # 其他部分漏洞环境的总结
│   ├── OurTeam.md        # DiagonAlley环境的官方Writeup (￣y▽,￣)╭ 
│   ├── imgs/             # 文档所用的图片
│   └── teamWDX.md        # 攻击其他组的一个wp
├── DiagonAlley
│   ├── app.py            # flask后端（漏洞环境）
│   ├── database.db       # 数据库
│   ├── img/              # 网站所用的图片
│   ├── requirements.txt  # 运行所需环境
│   ├── static/           # 静态文件
│   └── templates/        # html文件
├── FixIt                 
│   ├── CHECKER/          # checker脚本代码和所需环境
│   ├── README.md         # 修复阶段总结
│   └── diff.patch        # 修复补丁
├── README.md
└── doc_img/              # wiki所用的图片
.(LJY)
└── DiagonAlley/          # 修复好的环境
```

## **Install**

- From Source Code

  ```bash
  $ git clone https://github.com/LyuLumos/A-Leaky-Web-Environment.git
  $ cd DiagonAlley
  $ pip install -r requirements.txt
  $ flask run
  ```

- From Docker

  ```bash
  $ docker pull registry.cn-hangzhou.aliyuncs.com/lyulumos/diagonalley:0.2
  $ docker run -it --rm -p 80:80 registry.cn-hangzhou.aliyuncs.com/lyulumos/diagonalley:0.2
  ```

## **License**

[![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](http://perso.crans.org/besson/LICENSE.html)
