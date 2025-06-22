# 基于Ubuntu 22.04
FROM ubuntu:22.04

# 避免交互式提示
ENV DEBIAN_FRONTEND=noninteractive

# 安装必要的软件包
RUN apt-get update && \
    apt-get install -y \
    curl \
    git \
    jq \
    python3 \
    python3-pip \
    apt-transport-https \
    ca-certificates \
    gnupg \
    lsb-release \
    software-properties-common \
    sudo && \
    rm -rf /var/lib/apt/lists/*

# 添加GitLab Runner仓库
RUN curl -L "https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.deb.sh" | bash

# 安装GitLab Runner
# 如果要安装指定版本的runner，类似于apt install gitlab-runner=17.7.1-1
RUN apt-get update && \
    apt-get install -y gitlab-runner && \
    rm -rf /var/lib/apt/lists/*

# 安装AWS CLI
RUN pip3 install --no-cache-dir awscli requests && pip3 install aiohttp requests asyncio pathlib


# 安装Amazon Q CLI
RUN curl --proto '=https' --tlsv1.2 -sSf https://desktop-release.q.us-east-1.amazonaws.com/latest/amazon-q.deb -o amazon-q.deb && \
    apt-get update && \
    apt-get install -y ./amazon-q.deb && \
    rm amazon-q.deb && \
    rm -rf /var/lib/apt/lists/*

# 创建配置目录
RUN mkdir -p /etc/gitlab-runner
