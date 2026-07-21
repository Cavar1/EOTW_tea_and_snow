大学期末作业，奈茶的雪点单微信小程序，以及后端。

# 小程序介绍

## 基本介绍：

- 这是一个基于原生微信小程序的点单小程序，使用skyline引擎，配合后端接口及静态资源，实现了首页大图轮播、查看菜单、添加及修改购物车、查看订单、提交订单、模拟支付、查看及更改我的信息等功能。

## 小巧思：

- 修改了官方模板提供的navigation-bar，删除了（存疑）回到首页按钮，调整了细节样式，以适应界面。

- 写了一份tabbar进首页（/page/index），使用swiper标签进行分页，做了切换页面的逻辑。（或许没必要这么复杂？）

- 小程序样式设计整体使用清新绘画风格色调，大量使用直角边方形黑边框，大量加粗字体，增强了手作的风格。

- 使用了一些skyline引擎的特性，如open-container，增强视觉体验。

## 不足：

- skyline引擎目前在windows端支持不完善，在windows的微信实际预览有很多样式问题。

- 网络请求逻辑兜底机制不完善。

- 以及更多没发现的？

# 后端介绍

- 小程序后端一部分由Python语言以及fastapi框架搭建，连接MySQL数据库，利用AI强大的简单项目搭建能力，快速构建了一个能用的后端服务。

- 一部分为静态资源，在static文件夹下存储，由nginx公开；头像数据由fastapi接收并存储进去，同样由nginx公开。

- *~~别管它安不安全合不合理了，就说能不能用吧~~*

# 如何配置

1. **导入小程序**：从微信开发者工具首页导入项目，更改appid。在配置页面检查绕过合法域名以及启用skyline。

2. **配置数据库**：使用mysql数据库，创建tea_and_snow_db库，从server项目的script文件夹下的脚本创建表以及初始数据。

3. **配置后端**：使用uv初始化后端Python项目，在/.env文件夹配置数据库连接，小程序的appid以及appsecret。在启动项中添加--port 22334选项。

4. **配置nginx**：在nginx.conf中添加访问/static时的静态资源路径。

# 

University Final Project: "Snow And Tea" WeChat Mini Program Ordering System and Backend.

# Mini Program Introduction

## Overview

- This is a native WeChat Mini Program ordering app built with the Skyline engine. Combined with backend APIs and static resources, it implements features including a homepage carousel, menu browsing, adding and modifying the shopping cart, order viewing, order submission, simulated payment, and viewing/updating user profile.

## Design Highlights

- Modified the official template's navigation-bar, removed the (questionable) "back to home" button, and adjusted styling details to better fit the interface.

- Implemented a custom tabbar on the homepage (/pages/index), using the swiper tag for pagination with page-switching logic. (Perhaps unnecessarily complicated?)

- The overall visual design adopts a fresh, hand-painted style with extensive use of square black borders and bold fonts, enhancing a handcrafted aesthetic.

- Utilized some Skyline engine features such as open-container to enhance the visual experience.

## Limitations

- Skyline engine support is currently incomplete on Windows; actual preview on WeChat for Windows has various styling issues.

- Network request fallback mechanisms are not robust enough.

- And possibly more undiscovered issues?

# Backend Introduction

- Part of the Mini Program backend is built with Python and the FastAPI framework, connected to a MySQL database. Leveraging the AI's powerful ability to scaffold simple projects, a functional backend service was quickly constructed.

- Another part consists of static resources, stored in the /static folder and served publicly via Nginx; avatar data is received by FastAPI and stored there, also served publicly by Nginx.

- *~~Don't worry about whether it's secure or reasonable—does it work or not?~~*

# How to Configure

1. Import the Mini Program: Import the project from the WeChat DevTools homepage and change the appid. In the settings page, check the options to bypass legal domain validation and enable Skyline.

2. Configure the Database: Use MySQL, create the tea_and_snow_db database, and create tables and initial data using the scripts in the script folder of the server project.

3. Configure the Backend: Initialize the backend Python project using uv, configure the database connection in the /.env file, along with the Mini Program's appid and appsecret. Add the --port 22334 option in the startup configuration.

4. Configure Nginx: Add the static resource path for /static access in nginx.conf.