import {
  baseAPIURL,
  baseStaticURL,
  defaultAvatarUrl,
} from "../../config/config";

// index.js
Page({
  data: {
    // tab
    tabId: 0,
    indexTabList: [
      {
        id: 0,
        name: "首页",
      },
      {
        id: 1,
        name: "茶单",
      },
      {
        id: 2,
        name: "我的",
      },
    ],
    // 全局
    baseStaticURL: baseStaticURL,
    token: "",
    // 首页
    bannerList: null,
    // 茶单页
    orderList: [],
    // 我的页
    myInit: {},
    levelName: "",
    joinDays: 0,
  },

  // ---------- 载入页面时 ----------
  onLoad() {
    wx.showLoading({
      title: "加载中",
      mask: true,
      fail: (e) => {
        console.log("调用wx.showLoading失败", e);
      },
    });

    // 登录服务，新用户会新建档案，失败重试
    const tryLogin = () => {
      // 向微信获取临时code
      wx.login({
        success: (res) => {
          //发起登录请求
          const serverLogin = () => {
            wx.request({
              url: baseAPIURL + "/api/users/login",
              method: "POST",
              data: {
                code: res.code,
              },
              success: (res2) => {
                // 获得token时
                let token = "Bearer " + res2.data.data.access_token;
                this.setData({
                  token: token,
                });
                wx.setStorageSync("token", token);
                wx.hideLoading();
              },
              fail: () => {
                setTimeout(serverLogin, 250);
              },
            });
          };
          serverLogin();
        },
        fail: () => {
          setTimeout(tryLogin, 250);
        },
      });
    };
    tryLogin();
    // 获取banner数据，包括资源链接
    wx.request({
      url: baseAPIURL + "/api/banners",
      method: "GET",
      success: (res) => {
        this.setData({
          bannerList: res.data.data,
        });
      },
    });
  },

  // ---------- 首页 ----------

  // 跳转到菜单
  goToMenu() {
    wx.navigateTo({ url: "/pages/menu/menu" });
  },

  // ---------- 菜单 ----------

  // 刷新茶单
  refreshOrderList() {
    wx.showLoading({
      title: "刷新中",
      mask: true,
    });
    wx.request({
      url: baseAPIURL + "/api/orders",
      method: "GET",
      header: { Authorization: this.data.token },
      success: (res) => {
        this.setData({
          orderList: res.data.data,
        });
      },
      complete: () => {
        wx.hideLoading();
      },
    });
  },
  // 跳转茶单页
  goToOrder(e) {
    console.log(e);
    console.log(e.currentTarget.dataset.orderno);
    wx.navigateTo({
      url: "/pages/order/order?orderId=" + e.currentTarget.dataset.orderno,
    });
  },

  // ---------- 我的  ----------

  onClickMyCard() {
    wx.navigateTo({
      url: "/pages/my_page/my_page",
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

  // ---------- tabbar -----------

  // 页面滑动时
  onSwiperChange(e) {
    let id = e.detail.current;
    console.log("目前的tab: " + id);
    this.setData({
      tabId: id,
    });
    // 进入首页时
    if (id == 0) {
      // 获取banner数据，包括资源链接
      wx.request({
        url: baseAPIURL + "/api/banners",
        method: "GET",
        success: (res) => {
          this.setData({
            bannerList: res.data.data,
          });
        },
      });
    }
    // 进入茶单页时
    if (id == 1) {
      this.refreshOrderList();
    }
    // 进入我的页时
    if (id == 2) {
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
            levelName: this.getLevelName(myInit.member_level),
            joinDays: this.calcJoinDays(myInit.created_at),
          });
        },
      });
    }
  },
  // 用户点击tabbar时
  // 事件完成后，会触发上面的页面滑动事件
  onClickTab(e) {
    this.setData({
      tabId: e.target.dataset.id,
    });
  },
});
