import { baseAPIURL, baseStaticURL } from "../../config/config";

// pages/order/order.js
Page({
  data: {
    // 全局
    baseStaticURL: "",
    token: "",
    // 茶单号
    orderId: "",
    // 茶单信息
    order: {
      created_at:"",
      id:0,
      order_items:[
        {
          tea_item_id:0,
          tea_name:'',
          small_image_url:"",
          quantity:0,
          unit_price:"",
        }
      ],
      order_no:"",
      status:"",
      total_amount:"",
      updated_at:""
    },
  },

  // 首次打开页面
  onLoad(options) {
    this.setData({
      baseStaticURL: baseStaticURL,
      token: wx.getStorageSync("token"),
      orderId: options.orderId,
      order:null
    });
  },

  // 打开页面
  onShow() {
    this.refreshOrder()
  },

  // 点击支付按钮
  goToPay(){
    wx.showModal({
      title: '支付',
      content: '确定支付吗？',
      confirmText:"支付！",
      confirmColor:"#5aa800",
      success :(res)=> {
        if (res.confirm) {
          wx.showLoading({
            title: "支付中",
            mask: true,
          });
          wx.request({
            url:baseAPIURL+"/api/orders/"+this.data.orderId+"/pay",
            method:"POST",
            header:{"Authorization":this.data.token},
            success:()=>{
              wx.hideLoading()
              this.refreshOrder()
            },
            fail:(res)=>{
              wx.hideLoading()
              console.log(res)
              wx.showToast({
                title: '支付失败...',
                icon: 'error',
                mask:true
              })
            }
          })
        }
      }
    })
  },

  // 刷新订单
  refreshOrder(){
    let req = () => {
      wx.showLoading({
        title: "加载中",
        mask: true,
      });
      wx.request({
        url: baseAPIURL + "/api/orders/" + this.data.orderId,
        method: "GET",
        header: { Authorization: this.data.token },
        success: (res) => {
          console.log(res)
          this.setData({
            order: res.data.data,
          });
          wx.hideLoading();
        },
        fail:()=>{
          wx.hideLoading()
          req()
        }
      });
    };
    req()
  }
});
