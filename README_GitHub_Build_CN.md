# ImageMerger Win7 GitHub 自动打包说明

这个包用于通过 GitHub Actions 自动生成 Windows 7 兼容版 EXE。

## 使用方法

1. 登录 GitHub。
2. 新建一个仓库，例如 `image-merger-win7`。
3. 上传本 zip 解压后的所有文件，包括隐藏目录 `.github/workflows/build-win7-exe.yml`。
4. 进入仓库页面，点击上方 `Actions`。
5. 左侧选择 `Build ImageMerger Win7 EXE`。
6. 点击 `Run workflow`。
7. 等待 2-5 分钟。
8. 打包完成后，打开最新的运行记录，在页面底部 `Artifacts` 下载 `ImageMerger_Win7_EXE`。
9. 解压后得到 `ImageMerger_Win7.exe`。

## 说明

- 这个版本为 Windows 7 兼容考虑，去掉了拖拽图片功能。
- 保留中文界面、选择图片、选择文件夹、竖向长图、横向、网格、JPG压缩。
- GitHub 云端打包成功率高，但不是 100%。如果目标电脑是非常旧的 Windows 7，建议安装 SP1 和系统更新。
