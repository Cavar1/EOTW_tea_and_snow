import { baseAPIURL, baseStaticURL, defaultAvatarUrl } from "../../config/config";

// pages/my_page/my_page.js
Page({
  data: {
    baseStaticURL: baseStaticURL,
    token: "",
    myInit: {},
    // 编辑中数据
    tempAvatarUrl: "",
    newUsername: "",
    // 状态
    isSubmitting: false,
    hasChanged: false,
    // 派生展示
    levelName: "",
    joinDays: 0,
  },

  onLoad() {
    this.setData({
      token: wx.getStorageSync("token"),
    });
    this.loadUserInfo();
  },

  // 加载用户信息
  loadUserInfo() {
    wx.showLoading({ title: "加载中", mask: true });
    wx.request({
      url: baseAPIURL + "/api/users/me",
      method: "GET",
      header: { Authorization: this.data.token },
      success: (res) => {
        let myInit = res.data.data || {};
        if (!myInit.avatar_url) {
          myInit.avatar_url = defaultAvatarUrl;
        } else if (!myInit.avatar_url.startsWith("http")) {
          myInit.avatar_url = baseStaticURL + myInit.avatar_url;
        }
        if (myInit.created_at) {
          myInit.created_at = myInit.created_at.slice(0, 10);
        }
        this.setData({
          myInit: myInit,
          tempAvatarUrl: "",
          newUsername: myInit.username || "",
          hasChanged: false,
          levelName: this.getLevelName(myInit.member_level),
          joinDays: this.calcJoinDays(myInit.created_at),
        });
      },
      fail: () => {
        wx.showToast({ title: "加载失败", icon: "none" });
      },
      complete: () => {
        wx.hideLoading();
      },
    });
  },

  // 根据会员等级返回称号
  getLevelName(level) {
    const map = {
      0: "茶芽",
      1: "茶叶",
      2: "茶花",
      3: "茶师",
    };
    return map[level] || "资深茶客";
  },

  // 计算加入天数
  calcJoinDays(dateStr) {
    if (!dateStr) return 0;
    const join = new Date(dateStr);
    const now = new Date();
    const diff = now.getTime() - join.getTime();
    return Math.max(0, Math.floor(diff / (1000 * 60 * 60 * 24)));
  },

  // 选择头像
  onChooseAvatar(e) {
    const { avatarUrl } = e.detail;
    if (!avatarUrl) return;
    this.setData({
      tempAvatarUrl: avatarUrl,
    });
    this.checkChanged();
  },

  // 昵称输入
  onNicknameInput(e) {
    this.setData({
      newUsername: e.detail.value,
    });
    this.checkChanged();
  },

  // 检查是否有变更
  checkChanged() {
    const avatarChanged = !!this.data.tempAvatarUrl;
    const nameChanged = this.data.newUsername !== (this.data.myInit.username || "");
    this.setData({
      hasChanged: avatarChanged || nameChanged,
    });
  },

  // 上传头像
  uploadAvatar() {
    return new Promise((resolve, reject) => {
      const { tempAvatarUrl, token } = this.data;
      if (!tempAvatarUrl) {
        resolve();
        return;
      }
      wx.uploadFile({
        url: baseAPIURL + "/api/users/me/avatar",
        filePath: tempAvatarUrl,
        name: "file",
        header: { Authorization: token },
        success: (res) => {
          if (res.statusCode >= 200 && res.statusCode < 300) {
            resolve();
          } else {
            reject(new Error("头像上传失败"));
          }
        },
        fail: reject,
      });
    });
  },

  // 更新昵称
  updateUsername() {
    return new Promise((resolve, reject) => {
      const { newUsername, myInit, token } = this.data;
      if (newUsername === (myInit.username || "")) {
        resolve();
        return;
      }
      wx.request({
        url: baseAPIURL + "/api/users/me",
        method: "PUT",
        header: {
          Authorization: token,
          "Content-Type": "application/json",
        },
        data: { username: newUsername },
        success: (res) => {
          if (res.statusCode >= 200 && res.statusCode < 300) {
            resolve();
          } else {
            reject(new Error(res.data?.message || "昵称修改失败"));
          }
        },
        fail: reject,
      });
    });
  },

  // 保存资料
  saveProfile() {
    if (!this.data.hasChanged || this.data.isSubmitting) return;
    this.setData({ isSubmitting: true });
    wx.showLoading({ title: "保存中", mask: true });

    this.uploadAvatar()
      .then(() => this.updateUsername())
      .then(() => {
        wx.showToast({ title: "保存成功", icon: "success" });
        this.loadUserInfo();
      })
      .catch((err) => {
        wx.showToast({ title: err.message || "保存失败", icon: "none" });
      })
      .finally(() => {
        this.setData({ isSubmitting: false });
        wx.hideLoading();
      });
  },
});
